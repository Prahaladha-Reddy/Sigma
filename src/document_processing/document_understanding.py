from document_processing.document_summary import understand_document
from document_processing.example_usage import process_and_save_document
from document_processing.extract_multimodel import build_document_asset_graph
from document_processing.content_hyderator import hydrate_markdown_content
import os
import asyncio
from pathlib import Path
import json
from dotenv import load_dotenv
from core.process_context import get_data_dir, get_documents_dir

load_dotenv()

async def process_pdf_pipeline(file_path: str):
    file_path = str(file_path)
    document_name = Path(file_path).stem
    documents_dir = get_documents_dir()
    directory_path = documents_dir / document_name
    result_json_path = directory_path / "result.json"

    summary_text = ""
    saved_content = {}
    try:
        summary_task = asyncio.create_task(understand_document(file_path))
        save_task = asyncio.create_task(process_and_save_document(file_path))
        summary_text, saved_content = await asyncio.gather(summary_task, save_task)
    except Exception as e:
        print(f"Error during summary/extraction: {e}")
        raise

    doc_output_dir = saved_content.get("output_dir", "")
    resolved = {}
    raw_presentation = None

    try:
        graph = build_document_asset_graph()
        final_state = await graph.ainvoke(
            {"summary_text": summary_text, "saved_content": saved_content}
        )
        resolved = final_state.get("resolved_assets", {})
        raw_presentation = final_state.get("presentation_markdown")
        print("Hydrating presentation with table data...")
        final_presentation = hydrate_markdown_content(
            raw_presentation, search_roots=[doc_output_dir, "data"]
        )
    except Exception as e:
        print(f"Error building/hydrating mini presentation: {e}")
        final_presentation = raw_presentation or summary_text

    presentation_filename = f"mini_presentation_{document_name}.md"
    data_dir = get_data_dir().expanduser().resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    mini_path = data_dir / presentation_filename
    mini_path.write_text(final_presentation, encoding="utf-8")

    json_to_return = {
        "document_name": document_name,
        "summary_text": summary_text,
        "output_dir": saved_content.get("output_dir", ""),
        "images": resolved.get("figures", []),
        "tables": resolved.get("tables", []),
        "mini_presentation_path": str(mini_path),
    }

    directory_path.mkdir(parents=True, exist_ok=True)
    with open(result_json_path, "w", encoding="utf-8") as f:
        json.dump(json_to_return, f, indent=4)

    return json_to_return


            

if __name__=="__main__":
    asyncio.run(process_pdf_pipeline("data/uploaded/ch1.pdf"))
