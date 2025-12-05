import os
import tempfile
from typing import List, Any, Dict
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions



class DocumentProcessor:
    """Handles document processing using Docling."""

    def __init__(self):
        """Initialize the Docling DocumentConverter."""
        # Configure pipeline options for PDF processing
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.generate_picture_images = True  # Enable image extraction
        pipeline_options.images_scale = 2.0  # Higher resolution for better quality

        # Initialize converter with PDF options
        self.converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a file and return document data.

        Args:
            file_path: Path to the file to process

        Returns:
            Dictionary with:
                - 'filename': Name of the file
                - 'file_path': Full path to the file
                - 'markdown': All text content as markdown string
                - 'docling_doc': The raw Docling document object (contains images, tables, structure)
            
            Example return:
            {
                'filename': 'document.pdf',
                'file_path': '/path/to/document.pdf',
                'markdown': '# Title\n\nSome text...',
                'docling_doc': <DoclingDocument object with images, tables, etc.>
            }
            
            NOTE: This does NOT save anything to disk. Use ContentSaver to save images/tables/text.
        """
        file_path = Path(file_path)
        print(f" Processing {file_path.name}...")

        try:
            # Process the document with Docling
            # This extracts: text, images, tables, structure, OCR, etc.
            result = self.converter.convert(str(file_path))

            # Export to markdown (just the text content)
            markdown_content = result.document.export_to_markdown()

            # Return dictionary with both the markdown text AND the full Docling document
            # The docling_doc contains images, tables, and other structured data
            return {
                'filename': file_path.name,
                'file_path': str(file_path),
                'markdown': markdown_content,  # Text content as markdown
                'docling_doc': result.document  # Full document with images/tables - use with ContentSaver
            }

        except Exception as e:
            print(f" Error processing {file_path.name}: {str(e)}")
            raise

    def process_uploaded_files(self, uploaded_files) -> List[Dict[str, Any]]:
        """
        Process uploaded files (e.g., from Streamlit).

        Args:
            uploaded_files: List of Streamlit UploadedFile objects or file paths

        Returns:
            List of dictionaries (same format as process_file() returns)
            Each dictionary contains: filename, file_path, markdown, docling_doc
            
        NOTE: This handles temporary file creation for Streamlit uploads.
              For regular file paths, use process_file() instead.
        """
        documents = []
        temp_dir = tempfile.mkdtemp()

        try:
            for uploaded_file in uploaded_files:

                if hasattr(uploaded_file, 'getbuffer'):
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_path = temp_file_path
                else:
                    file_path = uploaded_file

                try:
                    result = self.process_file(file_path)
                    documents.append(result)
                    print(f" Successfully processed {result['filename']}")

                except Exception as e:
                    print(f" Error processing file: {str(e)}")
                    continue

        finally:
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f" Warning: Could not clean up temp directory: {str(e)}")

        print(f" Processed {len(documents)} documents successfully")
        return documents