from typing import List, Dict, Any
from docling_core.types.doc import DoclingDocument


class DocumentStructureVisualizer:

    def __init__(self, docling_document: DoclingDocument):

        self.doc = docling_document

    def get_document_hierarchy(self) -> List[Dict[str, Any]]:

        hierarchy = []

        if not hasattr(self.doc, 'texts') or not self.doc.texts:
            return hierarchy

        for item in self.doc.texts:
            label = getattr(item, 'label', None)

            if label and 'header' in label.lower():
                text = getattr(item, 'text', '')
                prov = getattr(item, 'prov', [])
                page_no = prov[0].page_no if prov else None

                hierarchy.append({
                    'type': label,
                    'text': text,
                    'page': page_no,
                    'level': self._infer_heading_level(label)
                })

        return hierarchy

    def _infer_heading_level(self, label: str) -> int:
        if 'title' in label.lower():
            return 1
        elif 'section' in label.lower():
            return 2
        elif 'subsection' in label.lower():
            return 3
        else:
            return 4

    def get_tables_info(self) -> List[Dict[str, Any]]:

        tables_info = []

        if not hasattr(self.doc, 'tables') or not self.doc.tables:
            return tables_info

        for i, table in enumerate(self.doc.tables, 1):
            try:
                df = table.export_to_dataframe(doc=self.doc)

                prov = getattr(table, 'prov', [])
                page_no = prov[0].page_no if prov else None

                caption_text = getattr(table, 'caption_text', None)
                caption = caption_text if caption_text and not callable(caption_text) else None

                tables_info.append({
                    'table_number': i,
                    'page': page_no,
                    'caption': caption,
                    'dataframe': df,
                    'shape': df.shape,
                    'is_empty': df.empty
                })

            except Exception as e:
                print(f"Warning: Could not process table {i}: {e}")
                continue

        return tables_info

    def get_pictures_info(self) -> List[Dict[str, Any]]:

        pictures_info = []

        if not hasattr(self.doc, 'pictures') or not self.doc.pictures:
            return pictures_info

        for i, pic in enumerate(self.doc.pictures, 1):
            prov = getattr(pic, 'prov', [])

            if prov:
                page_no = prov[0].page_no
                bbox = prov[0].bbox

                caption_text = getattr(pic, 'caption_text', None)
                caption = caption_text if caption_text and not callable(caption_text) else None

                pil_image = None
                try:
                    if hasattr(pic, 'image') and pic.image is not None:
                        if hasattr(pic.image, 'pil_image'):
                            pil_image = pic.image.pil_image
                except Exception as e:
                    print(f"Warning: Could not extract image {i}: {e}")

                pictures_info.append({
                    'picture_number': i,
                    'page': page_no,
                    'caption': caption,
                    'pil_image': pil_image,  
                    'bounding_box': {
                        'left': bbox.l,
                        'top': bbox.t,
                        'right': bbox.r,
                        'bottom': bbox.b
                    } if bbox else None
                })

        return pictures_info

    def get_document_summary(self) -> Dict[str, Any]:

        pages = getattr(self.doc, 'pages', {})
        texts = getattr(self.doc, 'texts', [])
        tables = getattr(self.doc, 'tables', [])
        pictures = getattr(self.doc, 'pictures', [])

        text_types = {}
        for item in texts:
            label = getattr(item, 'label', 'unknown')
            text_types[label] = text_types.get(label, 0) + 1

        return {
            'name': self.doc.name,
            'num_pages': len(pages) if pages else 0,
            'num_texts': len(texts),
            'num_tables': len(tables),
            'num_pictures': len(pictures),
            'text_types': text_types
        }

    def export_full_structure(self) -> Dict[str, Any]:

        return {
            'summary': self.get_document_summary(),
            'hierarchy': self.get_document_hierarchy(),
            'tables': self.get_tables_info(),
            'pictures': self.get_pictures_info()
        }