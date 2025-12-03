from datetime import datetime
from dotenv import load_dotenv
import asyncio
load_dotenv()
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
from langchain_core.messages import AIMessage
from unused_deep_researcher.utils import format_messages
from core.process_context import get_reports_dir
from unused_deep_researcher.research.prompts import (
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)
from unused_deep_researcher.research.tools import tavily_search, think_tool,save_to_local_file

max_concurrent_research_units = 3
max_researcher_iterations = 3
REPORT_PATH = Path("data/reports/final_report.md")
current_date = datetime.now().strftime("%Y-%m-%d")

INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_researcher_iterations,
    )
)

research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools": [tavily_search, think_tool,save_to_local_file],
}

model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview", temperature=0.0)

agent = create_deep_agent(
    model=model,
    tools=[tavily_search, think_tool,save_to_local_file],
    system_prompt=INSTRUCTIONS,
    subagents=[research_sub_agent],
)

def extract_text(ai_msg: AIMessage) -> str:
    """Turn AIMessage.content into a plain text string."""
    content = ai_msg.content
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)

    return str(content)

async def deep_researcher_run(request:str):
    result =await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request,
                }
            ],
        }, 
    )
    final_msg = result["messages"][-1]

    report_text = extract_text(final_msg)

    report_dir = get_reports_dir()
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / REPORT_PATH.name

    return {
        "report_path": str(report_path),
        "report_text": report_text,
    }

if __name__ == "__main__":
    asyncio.run(deep_researcher_run("write a very short and simple report on english language"))
