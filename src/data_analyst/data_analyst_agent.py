import asyncio
import os
import sys
from pathlib import Path
from typing import List, Set
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from typing import Dict ,Any
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from data_analyst.prompt import DAta_Analyst_promt
from notebooks_processing.notebook_processing import convert_notebook  

load_dotenv()


async def data_analyst_agent(Query: str):
    client = MultiServerMCPClient(
        {
            "jupyter": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:4040/mcp",
            }
        }
    )

    all_tools = await client.get_tools()
    os.makedirs("data/analysis", exist_ok=True)

    allowed_names = {
        "insert_cell",
        "execute_cell",
        "read_cell",
        "use_notebook",
        "execute_code",
        "list_notebooks",
        "list_kernels",
        "list_files",
        "read_notebook",
        "unuse_notebook",
    }

    mcp_tools = [t for t in all_tools if t.name in allowed_names]



    print("Tools the agent can use:", [t.name for t in mcp_tools])

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)

    agent = create_agent(
        model=llm,
        tools=mcp_tools,
        system_prompt=DAta_Analyst_promt,
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": Query,
                }
            ]
        }
    )

    last_msg = result["messages"][-1]
    content = last_msg.content

    if isinstance(content, str):
        answer = content
    elif isinstance(content, list):
        parts = []
        for chunk in content:
            if isinstance(chunk, dict) and chunk.get("type") == "text":
                parts.append(chunk.get("text", ""))
        answer = "\n\n".join(parts)
    else:
        answer = str(content)

    print(answer)
    return answer




def convert_new_notebooks(before: Set[Path], after: Set[Path]):
    """
    Convert only notebooks created during the agent run.
    Returns the string path of the generated markdown presentation (or None).
    """
    new_nbs = after - before

    if not new_nbs:
        print("[POST] No new notebooks detected in data/analysis")
        return None 

    print(f"[POST] Found {len(new_nbs)} new notebook(s) to convert:")
    
    last_presentation = None
    
    for nb in sorted(new_nbs):
        print(f"  - Converting {nb}")
        presentation_path = convert_notebook(str(nb))
        last_presentation = str(presentation_path)

    return last_presentation

async def data_analyst(query: str) -> Dict[str, Any]:
    analysis_dir = Path("data/analysis")
    analysis_dir.mkdir(parents=True, exist_ok=True)

    before_notebooks = set(analysis_dir.glob("*.ipynb"))

    answer_text = await data_analyst_agent(query)

    after_notebooks = set(analysis_dir.glob("*.ipynb"))

    markdown_presentation_path = convert_new_notebooks(before_notebooks, after_notebooks)

    return {
        "answer": answer_text,
        "markdown_presentation_path": markdown_presentation_path,
    }



if __name__ == "__main__":
    result = asyncio.run(
        data_analyst(
            "take a look at the adults.csv file, just clean and describe the data, very basic stats, no need of thorough analysis also just plot one hist plot"
        )
    )
    print("Answer:\n", result["answer"])
    print("Notebooks info:\n", result["notebooks"])
    print(type(result["answer"]), type(result["notebooks"]))
