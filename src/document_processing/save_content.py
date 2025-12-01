"""
Simple content saver for images, tables, and text from documents.
"""
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


class ContentSaver:
    """Saves images, tables, and text content from processed documents."""

    def __init__(self, output_dir: str = "data/saved_content"):
        """
        Initialize the content saver.

        Args:
            output_dir: Base directory where content will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_images(self, images_info: List[Dict[str, Any]], document_name: str) -> List[str]:
        """
        Save images from document processing.

        Args:
            images_info: List of dictionaries with image information (from structure_vizualizor)
            document_name: Name of the document (used for organizing files)

        Returns:
            List of saved image file paths
        """
        saved_paths = []
        images_dir = self.output_dir / document_name / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for img_info in images_info:
            pil_image = img_info.get('pil_image')
            if pil_image is None:
                continue

            # Generate filename
            img_num = img_info.get('picture_number', len(saved_paths) + 1)
            page = img_info.get('page', 1)
            filename = f"image_{img_num}_page_{page}.png"
            filepath = images_dir / filename

            try:
                # Save PIL image
                pil_image.save(filepath, "PNG")
                saved_paths.append(str(filepath))
                print(f"✅ Saved image: {filename}")
            except Exception as e:
                print(f"❌ Error saving image {img_num}: {str(e)}")

        return saved_paths

    def save_tables(self, tables_info: List[Dict[str, Any]], document_name: str) -> List[str]:
        """
        Save tables from document processing.

        Args:
            tables_info: List of dictionaries with table information (from structure_vizualizor)
            document_name: Name of the document (used for organizing files)

        Returns:
            List of saved table file paths
        """
        saved_paths = []
        tables_dir = self.output_dir / document_name / "tables"
        tables_dir.mkdir(parents=True, exist_ok=True)

        for table_info in tables_info:
            df = table_info.get('dataframe')
            if df is None or df.empty:
                continue

            # Generate filename
            table_num = table_info.get('table_number', len(saved_paths) + 1)
            page = table_info.get('page', 1)
            
            # Make column names unique for JSON export (pandas requires unique columns for orient='records')
            df_for_json = df.copy()
            if df_for_json.columns.duplicated().any():
                # Rename duplicate columns by appending _1, _2, etc.
                new_columns = []
                seen = {}
                for col in df_for_json.columns:
                    if col in seen:
                        seen[col] += 1
                        new_columns.append(f"{col}_{seen[col]}")
                    else:
                        seen[col] = 0
                        new_columns.append(col)
                df_for_json.columns = new_columns
            
            # Save as CSV (original column names preserved)
            csv_filename = f"table_{table_num}_page_{page}.csv"
            csv_path = tables_dir / csv_filename
            df.to_csv(csv_path, index=False)
            saved_paths.append(str(csv_path))
            
            # Also save as JSON for structured data (with unique column names)
            json_filename = f"table_{table_num}_page_{page}.json"
            json_path = tables_dir / json_filename
            try:
                df_for_json.to_json(json_path, orient='records', indent=2)
            except ValueError as e:
                # Fallback to 'index' orient if 'records' still fails
                print(f"⚠️ Warning: Could not save table {table_num} as records JSON, using index format: {e}")
                df_for_json.to_json(json_path, orient='index', indent=2)
            
            print(f"✅ Saved table {table_num}: {csv_filename} and {json_filename}")

        return saved_paths

    def save_text(self, text_content: str, document_name: str, filename: str = "text_content.md") -> str:
        """
        Save text content from document.

        Args:
            text_content: The text content to save
            document_name: Name of the document (used for organizing files)
            filename: Name of the text file to save

        Returns:
            Path to saved text file
        """
        text_dir = self.output_dir / document_name / "text"
        text_dir.mkdir(parents=True, exist_ok=True)

        filepath = text_dir / filename
        filepath.write_text(text_content, encoding="utf-8")
        print(f"✅ Saved text content: {filename}")
        
        return str(filepath)

    def save_markdown(self, markdown_content: str, document_name: str) -> str:
        """
        Save markdown content from document.

        Args:
            markdown_content: The markdown content to save
            document_name: Name of the document (used for organizing files)

        Returns:
            Path to saved markdown file
        """
        return self.save_text(markdown_content, document_name, "document.md")

    def save_all(self, docling_doc, document_name: str, markdown_content: str = None) -> Dict[str, Any]:
        """
        Save all content (images, tables, text) from a processed document.

        Args:
            docling_doc: The Docling document object
            document_name: Name of the document
            markdown_content: Optional markdown content to save

        Returns:
            Dictionary with paths to all saved content
        """
        from document_processing.structure_vizualizor import DocumentStructureVisualizer

        visualizer = DocumentStructureVisualizer(docling_doc)
        
        # Get all content
        images_info = visualizer.get_pictures_info()
        tables_info = visualizer.get_tables_info()
        
        # Save everything
        saved_images = self.save_images(images_info, document_name)
        saved_tables = self.save_tables(tables_info, document_name)
        
        saved_text = None
        if markdown_content:
            saved_text = self.save_markdown(markdown_content, document_name)

        return {
            'document_name': document_name,
            'images': saved_images,
            'tables': saved_tables,
            'text': saved_text,
            'output_dir': str(self.output_dir / document_name)
        }

