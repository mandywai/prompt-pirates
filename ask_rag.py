from langchain_google_genai import GoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import pdf_reader

def ask_rag(question):
  google_api_key = 'AIzaSyAGZHRXgoSgdSdC-R5_BDK0C75w_5YY1Q0'
  llm = GoogleGenerativeAI(model = 'gemini-2.5-flash', google_api_key = google_api_key)
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

def ask_rag(question):
  google_api_key = 'AIzaSyAGZHRXgoSgdSdC-R5_BDK0C75w_5YY1Q0'
  llm = GoogleGenerativeAI(model = 'gemini-2.5-flash', google_api_key = google_api_key)
  documents = pdf_reader(r'/content/Nelson-Physics-11.pdf')
  docs = [Document(page_content=doc) for doc in documents]
  embeddings = HuggingFaceEmbeddings()
  vectorstore = FAISS.from_documents(docs, embeddings)
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