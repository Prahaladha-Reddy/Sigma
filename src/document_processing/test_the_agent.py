from pathlib import Path
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
from document_processing.tools import tools
from document_processing.new_prompt import PDF_Agent_Prompt
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

mini_agent = create_deep_agent(
    model=llm,
    system_prompt=PDF_Agent_Prompt,
    tools=tools,
)

async def process_pdf_pipeline(file_path: str):
    """
    TEST VERSION

    - Assumes data/documents/<document_name>/result.json already exists.
    - Loads that JSON.
    - Calls mini_agent to generate a presentation.
    - Writes back presentation_path into the same JSON.
    """
    file_path = str(file_path)
    document_name = Path(file_path).stem
    directory_path = Path("data/documents") / document_name
    result_json_path = directory_path / "result.json"

    # 1) Load existing JSON (the one you already generated earlier)
    if not result_json_path.exists():
        raise FileNotFoundError(f"{result_json_path} does not exist. Run the full pipeline first.")

    with open(result_json_path, "r", encoding="utf-8") as f:
        json_to_return = json.load(f)

    # 2) Dump it to a JSON string for the agent
    json_str = json.dumps(json_to_return, indent=2)

    # 3) Call mini_agent (DeepAgent) with messages format
    mini_input = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Here is the processed PDF JSON. Use it and help me generate a well narrated "
                    "presentation:\n\n```json\n"
                    + json_str +
                    "\n```"
                ),
            }
        ]
    }

    mini_result= await mini_agent.ainvoke(            {"messages": [{"role": "user","content":"the json is in this path  documents/The effect of Inflation and Unemployment on Economic Growth_Article (1) (1)/result.json please make a presentation with it"}]}
        )
    
    print(mini_result)
    directory_path.mkdir(parents=True, exist_ok=True)
    with open(result_json_path, "w", encoding="utf-8") as f:
        json.dump(json_to_return, f, indent=4)

    return json_to_return
