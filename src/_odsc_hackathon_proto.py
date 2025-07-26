# import os
# import re
# import asyncio
# from IPython.display import display, Markdown
# import google.generativeai as genai
# from google.adk import Agent
# from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
# from google.adk.planners import BuiltInPlanner
# from google.genai import types
# from google.adk.tools import google_search
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService, Session
# from google.genai.types import Content, Part
# from getpass import getpass

# # Defining Agents

# GEMINI_MODEL = 'gemini-2.0-flash'

# # Defining instructor agent
# initial_instructor_agent = LlmAgent(
#     name="instructor_agent",
#     model=GEMINI_MODEL,
#     include_contents='none',
#     description="Generate lesson plan to instruct student on a topic.",
#     instruction=f"""You are an instructor tasked with teaching (previous instruction text). Write the first draft of the lecture material. Base the content *only* on the topic provided below. Try to tailor the material towards the student's learning preferences and behaviors. Focus on accuracy of the information.
#     Topic: {{initial_topic}}""",
#     tools=[google_search] # Provide the function directly
# )

# # Defining Critic instructor Agent
# critic_agent = LlmAgent(
#     name="critic_agent",
#     model=GEMINI_MODEL,
#     include_contents='none',
#     # MODIFIED Instruction: More nuanced completion criteria, look for clear improvement paths.
#     instruction=f"""You are a Constructive Critic AI reviewing instructor materials for a lecture. Your goal is focusing on accuracy of the information provided in a concise and easy to understand manner.

#     **Document to Review:**
#     ```
#     {{current_document}}
#     ```

#     **Task:**
#     Review the document for clarity, accuracy, and basic coherence according to the initial topic (if known).

#     IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader understanding (e.g., "Needs a clarifying sentence", "Clarify the sentence for easier understanding"):
#     Provide these specific suggestions concisely. Output *only* the critique text.

#     ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
#     Respond *exactly* with the phrase "{COMPLETION_PHRASE}" and nothing else. It doesn't need to be perfect, just functionally complete for this stage. Avoid suggesting purely subjective stylistic preferences if the core is sound.
# """,
#     description="Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
#     output_key=STATE_CRITICISM
# )

# # We update the router's instructions to know about the new 'combo' task.
# router_agent = Agent(
#     name="router_agent",
#     model=GEMINI_MODEL,
#     instruction="""
#     You are a request router. Your job is to analyze a user's query and decide which of the following agents or workflows is best suited to handle it.
#     Do not answer the query yourself, only return the name of the most appropriate choice.

#     Available Options:
#     - 'initial_instructor_agent': For queries *only* about food, restaurants, or eating.
#     - 'critic_agent': For queries about events, concerts, or activities happening on a specific timeframe like a weekend.
#     - 'find_and_navigate_combo': Use this for complex queries that ask to *first find a place* and *then get directions* to it.

#     Only return the single, most appropriate option's name and nothing else.
#     """
# )

# # Defining Planner Agent
# planner_agent = Agent(
#     model="gemini-2.5-flash",
#     name="planner_agent", # Add the name argument here
#     planner=BuiltInPlanner(
#         thinking_config=types.ThinkingConfig(
#             include_thoughts=True,
#             thinking_budget=1024,
#         )
#     ),
#     tools=[]
# )

# # We'll create a dictionary of all our individual worker agents
# worker_agents = {
#     "initial_instructor_agent": initial_instructor_agent,
#     "critic_agent": critic_agent,
#     "router_agent": router_agent,
#     "planner_agent": planner_agent, # Add the new agent!
# }

# from google.colab import drive
# drive.mount('/content/drive')

# from langchain_community.tools import Tool
# from transformers import pipeline

# # Creating Vision Tool
# clip = pipeline("image-classification", model="openai/clip-vit-base-patch32")
# def clip_image_analysis(image_path: str) -> dict:
#     """Classifies an image using CLIP.
#     Args:
#         image_path: Path to the image file.
#     Returns:
#         dict: Classification results.
#     """
#     results = clip(image_path)
#     return {"status": "success", "predictions": results}

# clip_tool = Tool(
#     name="clip_image_analysis",
#     func=clip_image_analysis,
#     description="Classifies images using CLIP model."
# )

# from google.adk.tools import LangchainTool
# adk_clip_tool = LangchainTool(clip_tool)

# # List of tools
# from google.adk import tools
# print(dir(tools))

# # A Helper Function to Run Our Agents

# async def run_agent_query(agent: Agent, query: str, session: Session, user_id: str, is_router: bool = False):
#     """Initializes a runner and executes a query for a given agent and session."""
#     print(f"\n🚀 Running query for agent: '{agent.name}' in session: '{session.id}'...")

#     runner = Runner(
#         agent=agent,
#         session_service=session_service,
#         app_name=agent.name
#     )

#     final_response = ""
#     try:
#         async for event in runner.run_async(
#             user_id=user_id,
#             session_id=session.id,
#             new_message=Content(parts=[Part(text=query)], role="user")
#         ):
#             if not is_router:
#                 # Let's see what the agent is thinking!
#                 print(f"EVENT: {event}")
#             if event.is_final_response():
#                 final_response = event.content.parts[0].text
#     except Exception as e:
#         final_response = f"An error occurred: {e}"

#     if not is_router:
#      print("\n" + "-"*50)
#      print("✅ Final Response:")
#      display(Markdown(final_response))
#      print("-"*50 + "\n")

#     return final_response

# # Initialize our Session Service (This one service will manage all the different sessions in our notebook).
# session_service = InMemorySessionService()
# my_user_id = "adk_adventurer_001"

# # !pip install langchain-google-genai langchain-community faiss-cpu sentence-transformers
# # !pip install pypdf

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from pypdf import PdfReader
from langchain_google_genai import GoogleGenerativeAI

def reader(pdf_file_path=r'/content/Nelson-Physics-11.pdf'):
  # Create a PdfReader object
  reader = PdfReader(pdf_file_path)

  # You can now access PDF properties and content
  num_pages = len(reader.pages)
  print(f"Number of pages: {num_pages}")

  # To extract text from a specific page (e.g., the first page):
  # first_page = reader.pages[0]
  # page_text = first_page.extract_text()
  num_pages = 2
  documents = []
  for ind in range(num_pages):
    page = reader.pages[ind]
    text = page.extract_text()
    if text:
      documents.append(text)

test_query = 'When did Julie Payette become a crew member of the space shuttle Discovery?'
docs = [Document(page_content=doc) for doc in documents]
embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
relevant_document = vectorstore.similarity_search(test_query, k=1)
print(relevant_document)

# google_api_key = 'AIzaSyAGZHRXgoSgdSdC-R5_BDK0C75w_5YY1Q0'
llm = GoogleGenerativeAI(model = 'gemini-2.5-flash', google_api_key = google_api_key)

def raw_ai():
  question = input('Ask Gemini anything: ')
  response = llm.invoke(question)
  print(f'\n Gemini: \n {response}')

def ask_rag(question):
  relevant_document = vectorstore.similarity_search(question, k=1)
  context = '\n'.join([doc.page_content for doc in relevant_document])
  rag_prompt = f"""
  Based on this textbook information:
  {context}
  Question: {question}

  Please
  - provide a helpful answer based on the textbook information provided.

  Answer:
  """
  response = llm.invoke(rag_prompt)
  return response

question = 'When did Julie Payette become a crew member of the space shuttle Discovery?'
answer = ask_rag(question)
print(answer)

# Commented out IPython magic to ensure Python compatibility.
# %%python --version

