from langchain_community.agent_toolkits import FileManagementToolkit
from deep_researcher.research.tools import save_to_local_file
from pathlib import Path
import os
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
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

@tool("ls")
def ls(path: str = ".") -> str:
    """
    Disabled. Use `list_directory` instead.
    """
    raise RuntimeError("The `ls` tool is disabled. Use `list_directory`.")

file_system_tools = toolkit.get_tools()

tools=file_system_tools+[save_to_local_file,ls]