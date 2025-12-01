import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "jupyter": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:4040/mcp",
            }
        }
    )

    all_tools = await client.get_tools()

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
    tools = [t for t in all_tools if t.name in allowed_names]

    print("Tools the agent can use:", [t.name for t in tools])

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    system_prompt = """
      You are an assistant connected to a Jupyter MCP server. Use the tools properly and don't assume the results always after writing the code and executing the results return to the user
      """

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "there is a csv dataset with name adults.csv , please do a very through data analysis on that data and generate leads and info about the data also at after you understand anything and moving on to the next thing please mention the reason behind the decision in markdown after that cell so that everything will be very transparent also please take a closer look at plots and read them and give description and explain each and every plot in detail like what you have observed after looking at those plots , it should explain each and every plot very accurately and exactly how the numbers and shapes are moving for each plot just below the plot in markdown",
                }
            ]
        }
    )

    print("\nFINAL OUTPUT:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
