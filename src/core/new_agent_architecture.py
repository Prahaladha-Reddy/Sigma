import os
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.new_architecture_prompt import Agent_1,Agent_3_prompt,Agent_4_prompt,Agent_2_with_Dataset ,Agent_2_with_search
from core.convert_html_pdf import html_to_pdf
from core.tools import process_notebook_tool,process_pdf_document_tool,data_analyst_tool
from typing import Optional
import asyncio
from typing import List
from dotenv import load_dotenv
load_dotenv()



def mini_presentations_reader(data_dir: str = "./data") -> str:
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Directory '{data_dir}' does not exist.")
    
    md_files = [f.name for f in data_path.glob("*.md") if f.name!="presentation.md"]
    if not md_files:
        return ""  
    
    parts: List[str] = []
    separator_template = """#===========================================================
# {filename}
#===========================================================

"""
    
    for filename in sorted(md_files):  
        try:
            file_path = data_path / filename
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            separator = separator_template.format(filename=filename)
            parts.append(separator + content)
        except IOError as e:
            print(f"Warning: Could not read '{filename}': {e}")
            continue  
    
    return "\n\n\n\n".join(parts) 



def agent_1(content: str, model: str = "gemini-2.5-pro", output_dir: str = "./data") -> Optional[str]:
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 1 is in action")
    try:
        result = llm.invoke([
            SystemMessage(content=Agent_1),
            HumanMessage(content=content),
        ])


        if isinstance(result.content, str):
            presentation = result.content
        elif isinstance(result.content, list):

            presentation = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in result.content
            )
        else:
            presentation = str(result.content)

        output_path = Path(output_dir) / "presentation.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)

        print(f"Presentation saved to {output_path}")
        return presentation

    except Exception as e:
        print(f"Error in agent_1: {e}")
        return None

async def agent_2_with_dataset(content: str,data_set_path:str, model: str = "gemini-2.5-pro", output_dir: str = "./data"):
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 1 is in action")
    try:
        result = llm.invoke([
            SystemMessage(content=Agent_2_with_Dataset),
            HumanMessage(content=content),
        ])
        if isinstance(result.content, str):
            query = result.content
        elif isinstance(result.content, list):

            query = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in result.content
            )
        else:
            query = str(result.content)
        await data_analyst_tool.ainvoke({"file_path":data_set_path,"query":query})
    except Exception as e:
        print(f"Error in agent_2_with_data: {e}")
        return None
    


def agent_2_with_search(content: str, model: str = "gemini-2.5-pro", output_dir: str = "./data"):
    llm = ChatGoogleGenerativeAI(model=model)
    print("agent 2 with search in action")
    try:
      model_with_search = llm.bind_tools([{"google_search": {}}])
      response = model_with_search.invoke([
            SystemMessage(content=Agent_2_with_search),
            HumanMessage(content=content),
        ]
      )
      print(response)
      if isinstance(response.content, str):
        presentation = response.content
      elif isinstance(response.content, list):

        presentation = "\n".join(
                part if isinstance(part, str) else str(part)
                for part in response.content
            )
      else:
        presentation = str(response.content)
      with open("./data/presentation.md","w") as f:
          f.write(presentation)
    except Exception as e:
        print(f"Error in agent_2_with_search: {e}")
        return None



def agent_3(content: str,Agent_3_prompt=Agent_3_prompt, model: str = "gemini-2.5-pro", output_dir: str = "./data") -> Optional[str]:

    llm = ChatGoogleGenerativeAI(model=model)
    
    try:
        response = llm.invoke([
            SystemMessage(content=Agent_3_prompt),
            HumanMessage(content=content),
        ])
        
        output_path = Path(output_dir) / "Final_story.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(response.content, str):
            presentation = response.content
        elif isinstance(response.content, list):

            presentation = "\n".join(
                    part if isinstance(part, str) else str(part)
                    for part in response.content
                )
        else:
            presentation = str(response.content)        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)
        
        print(f"Final story saved to {output_path}")
        return presentation
        
    except Exception as e:
        print(f"Error in agent_3 {e}")
        return None


def agent_4(
    content: str,
    model: str = "gemini-3-pro-preview",
    output_dir: str = "./data",
) -> Optional[str]:

    llm = ChatGoogleGenerativeAI(model=model)

    try:
        response = llm.invoke([
            SystemMessage(content=Agent_4_prompt),
            HumanMessage(content=content),
        ])

        if hasattr(response, "text") and response.text:
            presentation = response.text
        else:

            if isinstance(response.content, str):
                presentation = response.content
            elif isinstance(response.content, list):
                parts = []
                for block in response.content:
                    if isinstance(block, dict) and "text" in block:
                        parts.append(block["text"])
                    elif isinstance(block, str):
                        parts.append(block)
                    else:
                        parts.append(str(block))
                presentation = "\n".join(parts)
            else:
                presentation = str(response.content)

        output_path = Path(output_dir) / "Final_slides.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(presentation)

        print(f"Final html saved to {output_path}")
        return presentation

    except Exception as e:
        print(f"Error in agent_4: {e}")
        return None
    


def has_documents():
    Files_in_Uploaded=os.listdir("./data/uploaded")
    pdf_files=[file for file in Files_in_Uploaded if file.endswith(".pdf")]
    jupyter_notebooks=[file for file in Files_in_Uploaded if file.endswith(".ipynb")]
    total_files=pdf_files+jupyter_notebooks
    if len(total_files)>=1:
        return total_files
    else :
        return []

def has_datasets():
    Files_in_Uploaded=os.listdir("./data/uploaded")
    data_sets=[file for file in Files_in_Uploaded if file.endswith(".csv") or file.endswith(".xlsx") or file.endswith(".xls")]
    if len(data_sets)>=1:
        return data_sets
    else:
        return []



async def run_tool(file_name: str):
    file_path = f"./data/uploaded/{file_name}"
    if file_name.endswith(".pdf"):
        return await process_pdf_document_tool.ainvoke(file_path)
    else:
        return await process_notebook_tool.ainvoke(file_path)



async def the_runner(user_query:str,num_slides:int=12):
   docs= has_documents()
   print(len(docs))
   datasets=has_datasets()
   markdown=""
   final_slides=""
   final_presentation=""
   if len(docs)>=1:
    tasks = [asyncio.create_task(run_tool(file)) for file in docs]
    await asyncio.gather(*tasks, return_exceptions=True)
   markdown=mini_presentations_reader()

   agent_1(content=f"{user_query} \n\n\n"+markdown)
   if len(datasets)>=1:
       with open("./data/presentation.md") as f:
           markdown=f.read()
       await agent_2_with_dataset(content=f"{user_query} \n\n\n"+markdown,data_set_path=datasets[0])
       markdown=mini_presentations_reader()
       agent_1(content=f"{user_query} \n\n\n"+markdown)
   agent_2_with_search(content=f"{user_query} \n\n\n"+markdown)
   markdown=mini_presentations_reader()
   with open("./data/presentation.md") as f:
       final_presentation=f.read()
   agent_3(content=f"{user_query} \n\n\n"+final_presentation,Agent_3_prompt=Agent_3_prompt.replace("NUM_SLIDES",str(num_slides)))
   with open("./data/Final_story.md") as f:
       final_slides=f.read()
   agent_4(f"{user_query} \n\n\n"+final_slides)




if __name__=="__main__":
    asyncio.run(the_runner(user_query="Pease help me make best presentation on inflation , interest and unemployment",num_slides=15))



       