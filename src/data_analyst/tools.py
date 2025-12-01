from typing import Dict, List
from langchain_core.tools import tool
from notebooks_processing.notebook_processing import convert_notebook  
@tool
def convert_notebook_tool(notebook_path: str) -> Dict[str, List[str]]:
    """
    Convert a Jupyter notebook to markdown and extract assets.

    Args:
        notebook_path: Path to the .ipynb file on disk.

    Returns:
        A dict with:
          - markdown_path: path to the generated markdown file
          - assets: list of asset file paths (plots, images, etc.)
    """
    md_path, assets = convert_notebook(notebook_path)
    return {
        "markdown_path": str(md_path),
        "assets": [str(p) for p in assets],
    }
