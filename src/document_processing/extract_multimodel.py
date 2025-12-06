import asyncio
from pathlib import Path
from typing import List, Dict, Any, TypedDict
import json
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field

from google import genai
from google.genai import types

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from document_processing.document_summary import understand_document
from document_processing.example_usage import process_and_save_document


class FigureInfo(BaseModel):
    id: str = Field(..., description="Figure ID, e.g. 'Figure 1'")
    page: int = Field(..., description="Page number in the original PDF")
    title: str = Field(..., description="Title/caption of the figure")
    description: str = Field(
        ...,
        description="Full explanation of what the figure shows and why it matters",
    )


class TableInfo(BaseModel):
    id: str = Field(..., description="Table ID, e.g. 'Table 2' or 'Appendix B'")
    page: int = Field(..., description="Page number in the original PDF")
    title: str = Field(..., description="Title/caption of the table")
    description: str = Field(
        ...,
        description="Full explanation of what the table contains and why it is important",
    )


class DocumentAssets(BaseModel):
    figures: List[FigureInfo] = Field(
        default_factory=list,
        description="List of important figures mentioned in the summary",
    )
    tables: List[TableInfo] = Field(
        default_factory=list,
        description="List of important tables mentioned in the summary",
    )



class DocState(TypedDict, total=False):
    summary_text: str
    saved_content: Dict[str, Any]
    figures: List[Dict[str, Any]]     
    tables: List[Dict[str, Any]]     
    resolved_assets: Dict[str, Any]
    presentation_markdown: str



EXTRACT_SYSTEM_PROMPT = """
You are given a LONG markdown summary of a research PDF.

Inside that summary, you have already written sections like:
- "Important Images / Figures (with page numbers)"
- "Important Tables (with page numbers)"

Your job now:

1. Re-read the ENTIRE summary carefully.
2. For EVERY figure (image) you described in the summary, extract:
   - An ID (e.g., 'Figure 1')
   - A page number
   - A title/caption
   - A description of what the figure shows and why it matters
3. For EVERY table you described in the summary, extract:
   - An ID (e.g., 'Table 2', 'Appendix B')
   - A page number
   - A title/caption
   - A description of what the table contains and why it is important.

You MUST output data that fits exactly the following schema:

- DocumentAssets
  - figures: List[FigureInfo]
      - id: string
      - page: integer
      - title: string
      - description: string
  - tables: List[TableInfo]
      - id: string
      - page: integer
      - title: string
      - description: string

Important rules (CRITICAL):
- Do NOT skip or drop any figure/table that you mentioned in the summary.
- If you described 7 figures in the summary, your JSON MUST contain 7 figures.
- If you described 4 tables in the summary, your JSON MUST contain 4 tables.
- Use the page numbers you already wrote in the summary.
- If a page number is missing in the summary for a figure/table, you may infer it ONLY if you clearly specified it elsewhere. If you truly cannot infer it, then skip that item.
- Do NOT invent new figures or tables that were not in the summary.
"""






async def extract_assets_node(state: DocState) -> DocState:
    structured_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    ).with_structured_output(DocumentAssets)

    summary = state["summary_text"]
    messages = [
        SystemMessage(content=EXTRACT_SYSTEM_PROMPT),
        HumanMessage(content=f"Here is the full summary markdown:\n\n{summary}"),
    ]
    assets: DocumentAssets = await structured_llm.ainvoke(messages)
    state["figures"] = [f.model_dump() for f in assets.figures]
    state["tables"] = [t.model_dump() for t in assets.tables]
    return state




def group_images_by_page(image_paths: List[str]) -> Dict[int, List[str]]:
    """
    Input: list of paths like '.../image_1_page_8.png'
    Output: {8: [path1, path2...], 9: [...], ...}
    """
    by_page: Dict[int, List[str]] = {}
    for p in image_paths:
        name = Path(p).name  # 'image_1_page_8.png'
        try:
            prefix, page_part = name.split("_page_")
            page_str = page_part.split(".")[0]
            page = int(page_str)
        except ValueError:
            continue

        by_page.setdefault(page, []).append(p)

    return by_page


def group_tables_by_page(table_paths: List[str]) -> Dict[int, List[str]]:
    """
    Input: list of paths like '.../table_1_page_15.csv'
    Output: {15: [path1, path2...], ...}
    """
    by_page: Dict[int, List[str]] = {}
    for p in table_paths:
        name = Path(p).name  
        try:
            prefix, page_part = name.split("_page_")
            page_str = page_part.split(".")[0]
            page = int(page_str)
        except ValueError:
            continue

        by_page.setdefault(page, []).append(p)

    return by_page




client = genai.Client()


def check_image_matches_description(image_path: str, description: str) -> bool:
    """
    Returns True if Gemini thinks this image matches the description,
    False otherwise. Strict: any doubt -> NO_MATCH.
    """
    path = Path(image_path)
    ext = path.suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "image/png"  

    with open(path, "rb") as f:
        image_bytes = f.read()

    prompt = f"""
You are a STRICT verifier.

You are given:
1. An image from a research paper.
2. A textual description of a specific figure from that paper.

The description is:

\"\"\"{description}\"\"\"

Your task:
- Decide if THIS image matches THAT description.

Rules:
- If the image clearly matches the description (same kind of chart/diagram, roughly same axes or legend, same main message), answer exactly:

MATCH

- If it does NOT match, or you are uncertain, answer exactly:

NO_MATCH

Do NOT write anything else.
"""



    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime),
            prompt,
        ],
    )

    text = (resp.text or "").strip().upper()
    return text.startswith("MATCH")



def resolve_assets_node(state: DocState) -> DocState:
    figures = state.get("figures", [])
    tables = state.get("tables", [])
    saved = state["saved_content"]

    image_paths = saved.get("images", [])
    table_paths = saved.get("tables", [])

    images_by_page = group_images_by_page(image_paths)
    tables_by_page = group_tables_by_page(table_paths)

    resolved_figs: List[Dict[str, Any]] = []

    for fig in figures:
        page = fig["page"]
        description = fig.get("description", "")
        candidates = images_by_page.get(page, [])

        chosen = None

        if not candidates:
            chosen = None
        elif len(candidates) == 1:

            chosen = candidates[0]
        else:

            for img_path in candidates:
                if check_image_matches_description(img_path, description):
                    chosen = img_path
                    break

            if chosen is None:

                chosen = candidates[0]

        fig_resolved = dict(fig)
        fig_resolved["file_path"] = chosen
        resolved_figs.append(fig_resolved)

    resolved_tabs: List[Dict[str, Any]] = []
    table_index_by_page: Dict[int, int] = {}

    all_table_files = list(table_paths)
    used_table_files = set()

    for tbl in tables:
        page = tbl["page"]
        idx = table_index_by_page.get(page, 0)
        page_tables = tables_by_page.get(page, [])

        chosen = None

        if page_tables:
            if idx < len(page_tables):
                chosen = page_tables[idx]
            else:

                chosen = page_tables[-1]

            table_index_by_page[page] = idx + 1

        else:

            remaining = [p for p in all_table_files if p not in used_table_files]
            if remaining:
                chosen = remaining[0]
            else:
                chosen = None 
        if chosen is not None:
            used_table_files.add(chosen)

        tbl_resolved = dict(tbl)
        tbl_resolved["file_path"] = chosen
        resolved_tabs.append(tbl_resolved)

    state["figures"] = resolved_figs
    state["tables"] = resolved_tabs
    state["resolved_assets"] = {
        "figures": resolved_figs,
        "tables": resolved_tabs,
    }
    return state


PRESENTATION_PROMPT = """
You are given:
1) A long markdown summary of a research paper.
2) A JSON list of resolved figures (each with id, title, description, file_path).
3) A JSON list of resolved tables (each with id, title, description, file_path).

Your job: write a **mini-presentation** in Markdown.

This is NOT the final polished deck. It is a rich, well-structured draft that later agents will refine.
Do **not** aggressively compress or oversimplify. Preserve important nuance and context.

Inputs you may use:
- The summary markdown (all sections: overview, detailed summary, key ideas, concepts, limitations, notes).
- The figure descriptions and their file paths.
- The table descriptions and their file paths.

You MUST NOT:
- Invent new numbers, equations, or results.
- Add external knowledge.
- Hallucinate new figures or tables.

====================================================
GLOBAL FORMAT
====================================================
- Output **pure Markdown**.
- Separate major sections/slides with `---` on a line by itself.
- Each section must have a clear heading using `#`, `##`, or `###`.
- Within a section, you can use short paragraphs and bullet points.
- It should read like a human presenter walking through the story, not like a paper abstract.

====================================================
STRUCTURE (GUIDELINE, FLEXIBLE BUT COMPLETE)
====================================================

1. **Title slide**
   - Use the paper title or document_name from the summary.
   - 2–4 lines describing what the study is about and why it matters.
   - This can refer to the country/context, variables, and general aim.

2. **Context & Motivation**
   - Explain the real-world problem or economic/scientific issue being addressed.
   - Use multiple short paragraphs or bullets.
   - Include any key background insights from the summary (e.g., country history, macro instability, sectoral context).
   - Do **not** reduce this to one or two sentences; keep enough detail so later agents can choose what to cut.

3. **Methodology / Approach**
   - Describe the approach in plain language:
     - What data (period, frequency, main variables).
     - What main methods/models (e.g., ARDL, unit root tests, causality tests).
   - No derivations, no formulas, but you may mention names of tests and what they are used for.
   - A few short paragraphs or bullets are fine.

4. **Key Findings**
   - Summarize the main results in 5–10 bullet points.
   - Each bullet can be 1–3 sentences long (not ultra-short).
   - Cover:
     - Long-run relationships
     - Short-run dynamics
     - Any causality findings
     - Stability / diagnostics
     - Major policy-relevant conclusions
   - All content must come from the summary.

5. **Figures (integrated but explicit)**

   For EACH figure in the JSON list, in order:
   - Embed the image exactly using:
       ![](PATH_FROM_file_path)
   - Immediately below, write:
       **<ID> — <Title>**
   - Then add 2–4 sentences, based ONLY on the description, explaining:
       - What the figure shows,
       - How it connects to the story (e.g., context, trends, diagnostics),
       - Why it matters for understanding the results.

   Do **not** change paths. Use file_path exactly as given.

6. **Tables (integrated but explicit)**

   For EACH table in the JSON list, in order:
   - Write:
       **<ID> — <Title>**
   - Add 2–4 sentences, based ONLY on the description, explaining:
       - What the table contains (e.g., unit root tests, long-run estimates, diagnostics),
       - Why it is important for the analysis or conclusions.
   - Then include a source line:
       *(Table source: PATH_WITH_MD_EXTENSION)*
   
   **CRITICAL EXTENSION RULE:**
   - If the `file_path` in JSON ends in `.csv`, you **MUST change the extension to `.md`** in the source line above.
   - Example: if JSON has `data/table1.csv`, you write `(Table source: data/table1.md)`.
   - This ensures the formatted table is displayed correctly.

7. **Embedding**
   - Naturally embed the figures and tables in the right place in the right context in the narration

8. **Conclusions & Policy / Practical Implications**
   - Summarize what the reader should remember if they only recall one slide:
     - Core message of the paper.
     - Main risks, constraints, or limitations.
     - Main recommendations or implications (policy, practice, or future work).
   - 3–7 bullets or a few concise paragraphs are fine.
   - Stay strictly within what the summary and table/figure descriptions say.

====================================================
TONE AND NARRATION
====================================================
- Professional, clear, and slightly narrative.
- You may connect sections with light transitions (e.g., “Building on these results…”), but do not add new facts.
- Do **not** be ultra-telegraphic. A bit of richness in wording is fine because later agents will compress if needed.
- No meta-commentary (do not mention that you are an AI, or that you were given JSON, etc.).

====================================================
STRICT CONSTRAINTS
====================================================
- Use ONLY information from:
  - The markdown summary,
  - The figure descriptions,
  - The table descriptions.
- Do NOT invent or guess:
  - New variables,
  - New interpretations,
  - New statistics or thresholds.
- Do NOT alter any `file_path` string **EXCEPT** for the specific `.csv` to `.md` swap required for tables and you write `(Table source: data/table1.md)` like this
- Do NOT output JSON. Only pure Markdown with sections separated by `---`.
"""



async def write_presentation_node(state: DocState) -> DocState:
    summary = state["summary_text"]
    resolved = state["resolved_assets"]
    figures = resolved.get("figures", [])
    tables = resolved.get("tables", [])

    figures_json = json.dumps(figures, indent=2)
    tables_json = json.dumps(tables, indent=2)

    messages = [
        SystemMessage(content=PRESENTATION_PROMPT),
        HumanMessage(
            content=(
                "Here is the full summary markdown:\n\n"
                f"{summary}\n\n"
                "Here is the resolved figures JSON:\n\n"
                f"{figures_json}\n\n"
                "Here is the resolved tables JSON:\n\n"
                f"{tables_json}\n\n"
                "Now write the mini-presentation in Markdown."
            )
        ),
    ]
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    )
    resp = await llm.ainvoke(messages)
    state["presentation_markdown"] = resp.content
    return state

def build_document_asset_graph():
    builder = StateGraph(DocState)

    builder.add_node("extract_assets", extract_assets_node)
    builder.add_node("resolve_assets", resolve_assets_node)
    builder.add_node("write_presentation", write_presentation_node)  

    builder.set_entry_point("extract_assets")
    builder.add_edge("extract_assets", "resolve_assets")
    builder.add_edge("resolve_assets", "write_presentation")        
    builder.add_edge("write_presentation", END)                     

    return builder.compile()



async def main():
    pdf_file = "WP-514-Fakih-Amrin-Kamaluddin-Final.pdf"

    summary_text = await understand_document(pdf_file)
    saved_content = await process_and_save_document(pdf_file)

    graph = build_document_asset_graph()

    final_state = await graph.ainvoke({
        "summary_text": summary_text,
        "saved_content": saved_content,
    })

    resolved = final_state["resolved_assets"]

    print("Resolved figures:")
    for f in resolved["figures"]:
        print(f["id"], "→", f.get("file_path"))

    print("\nResolved tables:")
    for t in resolved["tables"]:
        print(t["id"], "→", t.get("file_path"))


if __name__ == "__main__":
    asyncio.run(main())
