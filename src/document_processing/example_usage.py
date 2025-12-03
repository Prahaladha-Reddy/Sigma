from pathlib import Path
from document_processing.document_processing import DocumentProcessor
from document_processing.save_content import ContentSaver
from document_processing.structure_vizualizor import DocumentStructureVisualizer
from document_processing.csv_to_md import convert_table_to_md
from core.process_context import get_documents_dir


async def process_and_save_document(file_path: str, output_dir: str = "data/documents"):

    processor = DocumentProcessor()
    saver = ContentSaver(output_dir=str(get_documents_dir()) if output_dir == "data/documents" else output_dir)

    print(f"Processing document: {file_path}")
    result = processor.process_file(file_path)
    
    document_name = Path(file_path).stem
    
    saved_content = saver.save_all(
        docling_doc=result["docling_doc"],
        document_name=document_name,
        markdown_content=result["markdown"],
    )
    
    print(f"\n Processing complete!")
    print(f" Output directory: {saved_content['output_dir']}")
    print(f"  Saved {len(saved_content['images'])} images")
    print(f" Saved {len(saved_content['tables'])} tables")
    print(f" Text saved: {saved_content['text']}")

    table_md_paths: list[str] = []
    for t in saved_content["tables"]:

        table_path = Path(t) if isinstance(t, str) else Path(t["file_path"])
        md_path = convert_table_to_md(table_path)
        table_md_paths.append(str(md_path))

    saved_content["tables_md"] = table_md_paths

    return saved_content



