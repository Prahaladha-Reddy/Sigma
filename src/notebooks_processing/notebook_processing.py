import base64
from pathlib import Path
import os
import nbformat
import numpy as np
import plotly.graph_objects as go
from nbformat.notebooknode import NotebookNode
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from notebooks_processing.prompt import NOTEBOOK_PRESENTATION_PROMPT
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)
def load_notebook(nb_path):
    return nbformat.read(nb_path, as_version=4)


def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def decode_binary_array(node: NotebookNode):
    """Decode {'bdata': base64, 'dtype': 'f8'/'i2'/...} -> numpy array"""
    b = base64.b64decode(node["bdata"])
    dt = node["dtype"]

    dtype_map = {
        "f8": np.float64,
        "f4": np.float32,
        "i2": np.int16,
        "i4": np.int32,
    }

    dtype = dtype_map.get(dt, np.dtype(dt))
    return np.frombuffer(b, dtype=dtype)


def normalize_plotly_spec(obj):
    """
    Recursively convert NotebookNode + binary-array objects
    into plain dict/list/number structures that go.Figure understands.
    """
    if isinstance(obj, NotebookNode):
        obj = dict(obj)

    if isinstance(obj, dict):
        # detect binary array
        if set(obj.keys()) == {"bdata", "dtype"}:
            return decode_binary_array(obj).tolist()

        return {k: normalize_plotly_spec(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [normalize_plotly_spec(v) for v in obj]

    return obj


def fig_from_plotly_json(plot_spec):
    """
    Take the raw 'application/vnd.plotly.v1+json' value
    and return a usable go.Figure.
    """
    spec_clean = normalize_plotly_spec(plot_spec)

    if isinstance(spec_clean, dict):
        layout = spec_clean.get("layout")
        if isinstance(layout, dict) and "template" in layout:
            layout.pop("template", None)

    try:
        return go.Figure(spec_clean)
    except Exception:
        return go.Figure(spec_clean, skip_invalid=True)



def extract_notebook_content(nb_path, image_output_dir="notebook_images"):
    nb_path = Path(nb_path)
    print("loading notebook")
    nb = load_notebook(nb_path)
    print("notebook loaded")

    image_dir = ensure_dir(image_output_dir)
    nb_name = nb_path.stem

    md_chunks = []
    assets = []  
    for cell_idx, cell in enumerate(nb.cells):
        print(f"processing cell {cell_idx}")
        md_chunks.append(f"\n\n---\n### Cell {cell_idx} ({cell.cell_type})")

        if cell.cell_type == "markdown":
            md_chunks.append(cell.source)
            continue

        md_chunks.append("```python")
        md_chunks.append(cell.source)
        md_chunks.append("```")

        for out_idx, out in enumerate(cell.get("outputs", [])):
            data = out.get("data", {})

            txt = data.get("text/plain")
            if txt:
                md_chunks.append("\n**Output (text):**")
                md_chunks.append("```text")
                md_chunks.append(txt if isinstance(txt, str) else "\n".join(txt))
                md_chunks.append("```")

            plotly_image_handled = False
            for mime, value in list(data.items()):
                if mime.startswith("image/"):
                    ext = mime.split("/")[-1]
                    img_path = image_dir / f"{nb_name}_cell{cell_idx}_out{out_idx}.{ext}"

                    b64 = value
                    if isinstance(b64, list):
                        b64 = "".join(b64)
                    img_path.write_bytes(base64.b64decode(b64))

                    md_chunks.append(f"\n![Image]({img_path.as_posix()})")
                    assets.append(img_path.as_posix())

                    if mime == "image/png":
                        plotly_image_handled = True

            plotly_spec = data.get("application/vnd.plotly.v1+json")
            if plotly_spec is not None and not plotly_image_handled:
                print(f"  Exporting Plotly figure (HTML) from cell {cell_idx} output {out_idx}...")
                try:
                    fig = fig_from_plotly_json(plotly_spec)
                    html_path = image_dir / f"{nb_name}_cell{cell_idx}_out{out_idx}_plotly.html"

                    html_str = fig.to_html(full_html=False, include_plotlyjs="cdn")
                    html_path.write_text(html_str, encoding="utf-8")

                    md_chunks.append(f"\n[Interactive Plotly Figure]({html_path.as_posix()})")
                    assets.append(html_path.as_posix())

                except Exception as e:
                    error_msg = f"Plotly HTML export failed in cell {cell_idx} output {out_idx}: {e}"
                    print("", error_msg)
                    md_chunks.append(f"\n[{error_msg}]")

    full_markdown = "\n".join(md_chunks)
    return full_markdown, assets


def convert_notebook(nb_file: str, base_output_dir: str = "data/notebook"):
    """
    Notebook → Markdown + Assets + Mini-Presentation

    Notebook layout:
        data/notebook/<notebook_name>/
            <notebook_name>_extracted.md
            images/
            result.json

    Mini-presentation:
        data/<notebook_name>_mini_presentation.md

    Returns:
        (markdown_path: Path, assets: list[str], mini_presentation_path: Path)
    """

    nb_file = Path(nb_file)
    base_output_dir = Path(base_output_dir)

    notebook_name = nb_file.stem

    notebook_dir = base_output_dir / notebook_name
    assets_dir = notebook_dir / "images"
    markdown_path = notebook_dir / f"{notebook_name}_extracted.md"
    result_json_path = notebook_dir / "result.json"

    mini_presentation_path = Path("data") / f"{notebook_name}_mini_presentation.md"

    if result_json_path.exists():
        print(f"Using cached notebook: {notebook_name}")
        with open(result_json_path, "r", encoding="utf-8") as f:
            cached = json.load(f)

        md_path = Path(cached["markdown_path"])
        assets = cached.get("assets", [])


        return str(mini_presentation_path)

    print(f"Converting notebook: {notebook_name}")

    notebook_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    md, assets = extract_notebook_content(nb_file, image_output_dir=assets_dir)
    markdown_path.write_text(md, encoding="utf-8")

    md_text = markdown_path.read_text(encoding="utf-8")

    messages = [
        SystemMessage(content=NOTEBOOK_PRESENTATION_PROMPT),
        HumanMessage(
            content=(
                f"Notebook name: {notebook_name}\n\n"
                "Here is the full extracted markdown of the notebook:\n\n"
                "```markdown\n"
                f"{md_text}\n"
                "```"
            )
        ),
    ]

    resp = llm.invoke(messages)
    presentation_md = getattr(resp, "content", str(resp))

    mini_presentation_path.write_text(presentation_md, encoding="utf-8")

    result = {
        "markdown_path": str(markdown_path),
        "assets": assets,
    }
    with open(result_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return str(mini_presentation_path)
