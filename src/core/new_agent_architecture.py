import asyncio
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from core.convert_html_pdf import pass_html_get_pdf
from core.convert_image_base64 import embed_images_as_base64
from core.new_architecture_prompt import (
    Agent_1,
    Agent_2_with_Dataset,
    Agent_2_with_search,
    Agent_3_prompt,
    Agent_4_prompt,
)
from core.process_context import (
    ProcessContext,
    get_data_dir,
    get_uploaded_dir,
    reset_current,
)
from core.tools import data_analyst_tool, process_notebook_tool, process_pdf_document_tool

load_dotenv()


def mini_presentations_reader(data_dir: Optional[str | Path] = None) -> str:
    data_path = Path(data_dir) if data_dir else get_data_dir()
    if not data_path.exists():
        return ""

    md_files = [f.name for f in data_path.glob("*.md") if f.name != "presentation.md"]
    if not md_files:
        return ""

    parts: List[str] = []
    separator_template = """#===========================================================
# {filename}
#===========================================================

"""

    for filename in sorted(md_files):
        try:
            file_path = data_path / filename
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            separator = separator_template.format(filename=filename)
            parts.append(separator + content)
        except IOError as e:
            print(f"Warning: Could not read '{filename}': {e}")
            continue

    return "\n\n\n\n".join(parts)


async def _invoke_llm(llm, messages):
    """Run blocking llm.invoke in a worker thread so concurrent runs don't block the event loop."""
    return await asyncio.to_thread(llm.invoke, messages)


async def agent_1(
    content: str,
    model: str = "gemini-2.5-pro",
    output_dir: Optional[str | Path] = None,
    process_context: Optional[ProcessContext] = None,
) -> Optional[str]:
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 1 is in action")
    try:
        result = await _invoke_llm(
            llm,
            [
                SystemMessage(content=Agent_1),
                HumanMessage(content=content),
            ],
        )

        if isinstance(result.content, str):
            presentation = result.content
        elif isinstance(result.content, list):
            presentation = "\n".join(
                part if isinstance(part, str) else str(part) for part in result.content
            )
        else:
            presentation = str(result.content)

        data_dir = Path(output_dir) if output_dir else get_data_dir()
        output_path = data_dir / "presentation.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)

        print(f"Presentation saved to {output_path}")
        return presentation

    except Exception as e:
        print(f"Error in agent_1: {e}")
        return None


async def agent_2_with_dataset(
    content: str,
    data_set_path: str,
    model: str = "gemini-2.5-pro",
    output_dir: Optional[str | Path] = None,
    process_context: Optional[ProcessContext] = None,
):
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 2 with dataset is in action")
    try:
        result = await _invoke_llm(
            llm,
            [
                SystemMessage(content=Agent_2_with_Dataset),
                HumanMessage(content=content),
            ],
        )
        if isinstance(result.content, str):
            query = result.content
        elif isinstance(result.content, list):
            query = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in result.content
            )
        else:
            query = str(result.content)
        await data_analyst_tool.ainvoke({"file_path": data_set_path, "query": query})
    except Exception as e:
        print(f"Error in agent_2_with_data: {e}")
        return None


async def agent_2_with_search(
    content: str,
    model: str = "gemini-2.5-pro",
    output_dir: Optional[str | Path] = None,
    process_context: Optional[ProcessContext] = None,
):
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 2 with search in action")
    try:
        model_with_search = llm.bind_tools([{"google_search": {}}])
        response = await _invoke_llm(
            model_with_search,
            [
                SystemMessage(content=Agent_2_with_search),
                HumanMessage(content=content),
            ],
        )
        print(response)
        if isinstance(response.content, str):
            presentation = response.content
        elif isinstance(response.content, list):
            presentation = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in response.content
            )
        else:
            presentation = str(response.content)
        data_dir = Path(output_dir) if output_dir else get_data_dir()
        with open(data_dir / "presentation.md", "w", encoding="utf-8") as f:
            f.write(presentation)
    except Exception as e:
        print(f"Error in agent_2_with_search: {e}")
        return None


async def agent_3(
    content: str,
    Agent_3_prompt=Agent_3_prompt,
    model: str = "gemini-2.5-pro",
    output_dir: Optional[str | Path] = None,
    process_context: Optional[ProcessContext] = None,
) -> Optional[str]:
    print("agent 3 is in action")
    llm = ChatGoogleGenerativeAI(model=model)

    try:
        response = await _invoke_llm(
            llm,
            [
                SystemMessage(content=Agent_3_prompt),
                HumanMessage(content=content),
            ],
        )

        data_dir = Path(output_dir) if output_dir else get_data_dir()
        output_path = data_dir / "Final_story.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(response.content, str):
            presentation = response.content
        elif isinstance(response.content, list):
            presentation = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in response.content
            )
        else:
            presentation = str(response.content)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)

        print(f"Final story saved to {output_path}")
        return presentation

    except Exception as e:
        print(f"Error in agent_3 {e}")
        return None


async def agent_4(
    content: str,
    model: str = "gemini-3-pro-preview",
    output_dir: Optional[str | Path] = None,
    process_context: Optional[ProcessContext] = None,
) -> Optional[str]:
    print("agent 4 is in action")
    llm = ChatGoogleGenerativeAI(model=model)

    try:
        response = await _invoke_llm(
            llm,
            [
                SystemMessage(content=Agent_4_prompt),
                HumanMessage(content=content),
            ],
        )

        if hasattr(response, "text") and response.text:
            presentation = response.text
        else:
            if isinstance(response.content, str):
                presentation = response.content
            elif isinstance(response.content, list):
                parts = []
                for block in response.content:
                    if isinstance(block, dict) and "text" in block:
                        parts.append(block["text"])
                    elif isinstance(block, str):
                        parts.append(block)
                    else:
                        parts.append(str(block))
                presentation = "\n".join(parts)
            else:
                presentation = str(response.content)

        data_dir = Path(output_dir) if output_dir else get_data_dir()
        output_path = data_dir / "Final_slides.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        presentation = embed_images_as_base64(presentation, image_dir=data_dir)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)

        print(f"Final html saved to {output_path}")
        return presentation

    except Exception as e:
        print(f"Error in agent_4: {e}")
        return None


def has_documents(uploaded_dir: Optional[Path] = None):
    upload_dir = uploaded_dir or get_uploaded_dir()
    if not upload_dir.exists():
        return []
    pdf_files = list(upload_dir.glob("*.pdf"))
    jupyter_notebooks = list(upload_dir.glob("*.ipynb"))
    total_files = pdf_files + jupyter_notebooks
    return total_files


def has_datasets(uploaded_dir: Optional[Path] = None):
    upload_dir = uploaded_dir or get_uploaded_dir()
    if not upload_dir.exists():
        return []
    data_sets = [
        p
        for p in upload_dir.glob("*")
        if p.suffix.lower() in {".csv", ".xlsx", ".xls"}
    ]
    return data_sets


async def run_tool(file_path: Path):
    if file_path.suffix.lower() == ".pdf":
        return await process_pdf_document_tool.ainvoke(str(file_path))
    else:
        return await process_notebook_tool.ainvoke(str(file_path))


async def the_runner(
    user_query: str,
    num_slides: int = 12,
    process_context: Optional[ProcessContext] = None,
):
    ctx = process_context or ProcessContext.get_current()
    token = None
    if process_context is not None and ProcessContext.get_current() is None:
        token = process_context.activate()

    try:
        data_dir = get_data_dir()
        uploaded_dir = get_uploaded_dir()

        docs = has_documents(uploaded_dir)
        datasets = has_datasets(uploaded_dir)
        markdown = ""

        if docs:
            tasks = [asyncio.create_task(run_tool(file)) for file in docs]
            await asyncio.gather(*tasks, return_exceptions=True)

        markdown = mini_presentations_reader(data_dir)

        await agent_1(content=f"{user_query} \n\n\n" + markdown, output_dir=data_dir)

        if datasets:
            presentation_path = data_dir / "presentation.md"
            if presentation_path.exists():
                with open(presentation_path, encoding="utf-8") as f:
                    markdown = f.read()
            await agent_2_with_dataset(
                content=f"{user_query} \n\n\n" + markdown,
                data_set_path=str(datasets[0]),
                output_dir=data_dir,
            )
            markdown = mini_presentations_reader(data_dir)
            await agent_1(content=f"{user_query} \n\n\n" + markdown, output_dir=data_dir)

        await agent_2_with_search(
            content=f"{user_query} \n\n\n" + markdown, output_dir=data_dir
        )

        markdown = mini_presentations_reader(data_dir)
        presentation_path = data_dir / "presentation.md"
        if presentation_path.exists():
            with open(presentation_path, encoding="utf-8") as f:
                final_presentation = f.read()
        else:
            final_presentation = markdown

        await agent_3(
            content=f"{user_query} \n\n\n" + final_presentation,
            Agent_3_prompt=Agent_3_prompt.replace("NUM_SLIDES", str(num_slides)),
            output_dir=data_dir,
        )
        final_story_path = data_dir / "Final_story.md"
        if final_story_path.exists():
            with open(final_story_path, encoding="utf-8") as f:
                final_slides = f.read()
        else:
            final_slides = ""
        await agent_4(f"{user_query} \n\n\n" + final_slides, output_dir=data_dir)

        final_html_path = data_dir / "Final_slides.html"
        final_pdf_path = data_dir / "final_presentation.pdf"
        await pass_html_get_pdf(str(final_html_path), str(final_pdf_path))

        return {
            "process_id": ctx.process_id if ctx else None,
            "process_dir": str(ctx.base_dir) if ctx else None,
            "data_dir": str(data_dir),
            "presentation_md": str(presentation_path),
            "final_story_md": str(final_story_path),
            "final_slides_html": str(final_html_path),
            "final_pdf": str(final_pdf_path),
        }
    finally:
        if token is not None:
            reset_current(token)



if __name__ == "__main__":
    asyncio.run(
        the_runner(
            user_query="Pease help me make best presentation on inflation , interest and unemployment",
            num_slides=15,
        )
    )
