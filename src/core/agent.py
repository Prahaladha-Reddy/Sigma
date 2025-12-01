from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
import asyncio
from core.prompt import CORE_PROMPT, Agent_layer2_prompt, The_STORY_TELLER, Theme_Picker
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from core.tools import data_analyst_tool, file_system_tools, ls
from deep_researcher.research.tools import tavily_search, save_to_local_file
from deep_researcher.research.check_tool import tavily_quick_search
load_dotenv()

# Configuration
NUMBER_SLIDES = 15
current_date = datetime.now().strftime("%Y-%m-%d")

# Initialize LLMs
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
story_teller_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)
final_slide_llm = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")

tools_agent_1 = file_system_tools + [data_analyst_tool, save_to_local_file, ls]
tools_agent_2 = file_system_tools + [tavily_quick_search, ls, save_to_local_file]
final_slide_agent_tools = file_system_tools + [save_to_local_file, ls]

system_prompt_agent_1 = CORE_PROMPT.replace("DATE", current_date)
system_prompt_agent_2 = Agent_layer2_prompt.replace("DATE", current_date)
system_prompt_story_teller = The_STORY_TELLER.replace("NUM_SLIDES", str(NUMBER_SLIDES))

agent_1 = create_deep_agent(
    model=llm,
    tools=tools_agent_1,
    system_prompt=system_prompt_agent_1,
)



agent_2 = create_deep_agent(
    model=llm,
    tools=tools_agent_2,
    system_prompt=system_prompt_agent_2,
)

story_telling_agent = create_deep_agent(
    model=story_teller_llm,
    system_prompt=system_prompt_story_teller,
)

final_slide_generator = create_deep_agent(
    model=final_slide_llm,
    tools=final_slide_agent_tools,
    system_prompt=Theme_Picker
)


class AgentState(TypedDict):
    user_request: str
    agent_1_output: str
    agent_2_output: str
    story_output: str
    final_slides: str
    messages: Annotated[list, operator.add]


async def run_agent_1(state: AgentState) -> AgentState:
    """First agent - initial processing"""
    print(f"\n🤖 Agent 1: Processing request...")
    print(f"User Request: {state['user_request']}")
    
    try:
        result = await agent_1.ainvoke(
            {"messages": [{"role": "user", "content": state["user_request"]}]}
        )
        output = result["messages"][-1].content
        print("✅ Agent 1: Complete")
        
        return {
            **state,
            "agent_1_output": output,
            "messages": [f"Agent 1 completed: {output[:100]}..."]
        }
    except Exception as e:
        print(f"❌ Agent 1 Error: {str(e)}")
        return {**state, "agent_1_output": f"Error: {str(e)}"}


async def run_agent_2(state: AgentState) -> AgentState:
    """Second agent - research and expansion"""
    print(f"\n🤖 Agent 2: Expanding content...")
    
    try:
        result = await agent_2.ainvoke(
            {"messages": [{"role": "user", "content": state["agent_1_output"]}]}
        )
        output = result["messages"][-1].content
        
        
        print("✅ Agent 2: Complete")
        return {
            **state,
            "agent_2_output": output,
            "messages": [f"Agent 2 completed: Saved to expanded_comprehensive_presentation.md"]
        }
    except Exception as e:
        print(f"❌ Agent 2 Error: {str(e)}")
        return {**state, "agent_2_output": f"Error: {str(e)}"}


async def run_story_teller(state: AgentState) -> AgentState:
    """Story teller agent - narrative creation"""
    print(f"\n📖 Story Teller: Creating narrative...")
    
    try:
        with open("data/expanded_comprehensive_presentation.md") as f:
            story = f.read()
        
        result = await story_telling_agent.ainvoke(
            {"messages": [{"role": "user", "content": story}]}
        )
        story_content = result["messages"][-1].content
        
        output_path = "data/final_story.md"
        with open(output_path, "w") as f:
            f.write(story_content)
        
        print(f"✅ Story Teller: Complete - saved to {output_path}")
        return {
            **state,
            "story_output": story_content,
            "messages": [f"Story Teller completed: Saved to {output_path}"]
        }
    except Exception as e:
        print(f"❌ Story Teller Error: {str(e)}")
        return {**state, "story_output": f"Error: {str(e)}"}


async def run_final_slides(state: AgentState) -> AgentState:
    """Final slides generator - HTML presentation"""
    print(f"\n🎨 Slides Generator: Creating presentation...")
    
    try:
        with open("data/final_story.md") as f:
            story = f.read()
        
        result = await final_slide_llm.ainvoke([
            SystemMessage(content=Theme_Picker),
            HumanMessage(content=story),
        ])
        
        slides_html = result.content
        
        output_path = "data/final_slides.html"
        with open(output_path, "w") as f:
            f.write(slides_html)
        
        print(f"✅ Slides Generator: Complete - saved to {output_path}")
        return {
            **state,
            "final_slides": slides_html,
            "messages": [f"Slides Generator completed: Saved to {output_path}"]
        }
    except Exception as e:
        print(f"❌ Slides Generator Error: {str(e)}")
        return {**state, "final_slides": f"Error: {str(e)}"}


def create_presentation_pipeline():
    """Creates the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent_1", run_agent_1)
    workflow.add_node("agent_2", run_agent_2)
    workflow.add_node("story_teller", run_story_teller)
    workflow.add_node("final_slides", run_final_slides)
    
    workflow.set_entry_point("agent_1")
    workflow.add_edge("agent_1", "agent_2")
    workflow.add_edge("agent_2", "story_teller")
    workflow.add_edge("story_teller", "final_slides")
    workflow.add_edge("final_slides", END)
    
    return workflow.compile()


async def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 Starting Presentation Generation Pipeline")
    print("=" * 60)
    
    pipeline = create_presentation_pipeline()
    
    initial_state = {
        "user_request": "Please help me to make best slides for autonumous ride hailing, use the mini presentation avaliable",
        "agent_1_output": "",
        "agent_2_output": "",
        "story_output": "",
        "final_slides": "",
        "messages": []
    }
    
    final_state = await pipeline.ainvoke(initial_state)
    
    print("\n" + "=" * 60)
    print("✨ Pipeline Complete!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("📄 data/expanded_comprehensive_presentation.md")
    print("📖 data/final_story.md")
    print("🎨 data/final_slides.html")
    print("\n" + "=" * 60)
    
    return final_state


if __name__ == "__main__":
    asyncio.run(main())