from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import asyncio
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.tools import tool
from typing import Any, Dict
from pydantic import BaseModel, Field
from data_analyst.data_analyst_agent import data_analyst
from notebooks_processing.notebook_processing import convert_notebook
from deep_researcher.agents import deep_researcher_run
from document_processing.document_understanding import process_pdf_pipeline
import os
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parents[2]
target_directory = project_root / "data"
DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploaded"
NOTEBOOK_CWD = DATA_DIR / "analysis" 

if not target_directory.exists():
    target_directory.mkdir(parents=True, exist_ok=True)

toolkit = FileManagementToolkit(
    root_dir=str(target_directory),
    selected_tools=["read_file", "list_directory", "file_search"]
)
file_system_tools = toolkit.get_tools()


class DataAnalystInput(BaseModel):
    file_path:str=Field(
        ...,
        description=(
            "Give the path of the dataset"
        ),
    )
    query: str = Field(
        ...,
        description=(
            "Describe what analysis you want on the available dataset(s). "
            "Example: 'Clean and describe adults.csv, provide basic stats only.'"
        ),
    )

@tool(args_schema=DataAnalystInput)
async def data_analyst_tool(file_path: str, query: str) -> Dict[str, Any]:
    """
    Run the Jupyter-based data analyst agent.

    It will:
    - Load the relevant dataset(s) (e.g. adults.csv).
    - Perform ONLY focused, question-driven analysis (no unnecessary full EDA).
    - Save any notebooks it creates to data/analysis.
    - Convert new notebooks to markdown + extract assets via convert_notebook.
    It Won't:
    - It won't load a jupyter notebook given the path created by someone else

    - Return a JSON object with:
        {
          "markdown_presentation_path": Eg data/inflation_mini_presentation.md
        }

    """

    filename = Path(file_path).name

    repo_rel = UPLOAD_DIR / filename            

    if not repo_rel.exists():
        raise FileNotFoundError(
            f"Dataset '{filename}' not found under data/uploaded/. "
            f"Expected at '{repo_rel.as_posix()}'."
        )

 
    nb_rel = os.path.relpath(repo_rel, start=NOTEBOOK_CWD)
    nb_rel = nb_rel.replace("\\", "/")  

    query_with_path = (
        query
        + "\n\nUse the dataset file with name "
        f"`{filename}`.\n"
        "From your current working directory (`data/analysis`), "
        "load it with:\n"
        f"    pd.read_csv('{nb_rel}')\n"
        "Do NOT try to guess any other path."
    )

    answer = await data_analyst(query_with_path)

    return answer


@tool("deep_researcher")
async def deep_researcher_tool(query: str) -> dict:
    """
    Run the deep research workflow on the given query.

    Returns:
      {
        "report_path": "data/reports/final_report.md",
        "report_text": "<short preview text>"
      }
    """
    return await deep_researcher_run(query)



@tool()
async def process_pdf_document_tool(file_path: str) -> dict:
    """
    End-to-end PDF processing tool.

    Given the path to a PDF file, it:
      - It will summarize and pin points the highlights and things that would help in making presentation 
      - It will extract the tables and images from the pdf and and points key images and tables that would help in making presentation better
      - Ingests the markdown text of the into Qdrant with so that you can use it to query for furter information if needed by using the collection_name

    Returns a dict with:
      {
        "document_name": ...,
        "summary_text": ...,
        "output_dir": ...,
        "images": [...],
        "tables": [...]
      }
    """
    filename = Path(file_path).name
    repo_rel = UPLOAD_DIR / filename
    if not repo_rel.exists():
      raise FileNotFoundError(
          f"File '{filename}' not found under data/uploaded/. "
          f"Expected at '{repo_rel.as_posix()}'."
        )

    return await process_pdf_pipeline(str(repo_rel))

@tool()
async def process_notebook_tool(file_path: str) -> dict:
    """
    Convert a Jupyter Notebook (.ipynb) into Markdown + extracted assets.
    """
    filename = Path(file_path).name
    repo_rel = UPLOAD_DIR / filename
    if not repo_rel.exists():
      raise FileNotFoundError(
          f"Dataset '{filename}' not found under data/uploaded/. "
          f"Expected at '{repo_rel.as_posix()}'."
        )
    
    presentation_path = convert_notebook(str(repo_rel))
    
    return {
        "markdown_presentation_path": str(presentation_path)
    }


@tool("ls")
def ls(path: str = ".") -> str:
    """
    Disabled. Use `list_directory` instead.
    """
    raise RuntimeError("The `ls` tool is disabled. Use `list_directory`.")

async def main():
    corona=asyncio.create_task(process_pdf_document_tool.ainvoke("data/uploaded/Direct_and_indirect_effects.pdf"))
    cloths=asyncio.create_task(process_pdf_document_tool.ainvoke("data/uploaded/WRAP-changing-our-clothes-why-the-clothing-sector-should-adopt-new-business-models.pdf"))
    avip=asyncio.create_task( process_pdf_document_tool.ainvoke("data/uploaded/avip.pdf"))
    await asyncio.gather(cloths,corona,avip)

if __name__=="__main__":
    asyncio.run(process_pdf_document_tool.ainvoke("data/uploaded/avip.pdf"))


