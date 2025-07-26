from google.adk.agents import Agent
from typing import Dict, Any
from .planner import create_planner
from .executor import create_executor
from .context_retriever import create_context_retriever, load_context_pdf
import os

# Initialize the RAG assistant
rag_assistant = None

def initialize_rag_assistant():
    """Initialize the RAG assistant if not already done."""
    global rag_assistant
    if rag_assistant is None:
        # Create components
        planner = create_planner()
        executor = create_executor()
        context_retriever = create_context_retriever()
        
        # Connect executor to context retriever
        executor.set_context_retriever(context_retriever)
        
        # Create assistant object
        rag_assistant = {
            'planner': planner,
            'executor': executor,
            'context_retriever': context_retriever,
            'loaded_documents': {}
        }
        
        # Load the default curriculum
        pdf_filename = "book1.pdf"
        if os.path.exists(f"src/books/{pdf_filename}"):
            load_curriculum_document(pdf_filename)
        else:
            print(f"⚠️  Warning: {pdf_filename} not found in src/books/")
    return rag_assistant

def ask_curriculum_question(question: str) -> Dict[str, Any]:
    """Ask a question about the curriculum using RAG.
    
    Args:
        question: The question to ask about the curriculum
        
    Returns:
        dict: A dictionary containing the response and metadata
    """
    assistant = initialize_rag_assistant()
    
    # Plan the query
    plan = assistant['planner'].plan(question)
    
    # Execute the query
    response = assistant['executor'].execute_task(plan['task_type'], question)
    
    return {
        "status": "success",
        "response": response,
        "task_type": plan['task_type'],
        "steps_taken": len(plan['sub_tasks'])
    }

def load_curriculum_document(filename: str) -> Dict[str, Any]:
    """Load a curriculum document into the RAG assistant.
    
    Args:
        filename: The PDF filename to load (should be in src/books/)
        
    Returns:
        dict: A dictionary containing the load status
    """
    assistant = initialize_rag_assistant()
    success = load_context_pdf(assistant['context_retriever'], filename)
    
    if success:
        assistant['loaded_documents'][filename] = True
        return {
            "status": "success",
            "message": f"Successfully loaded curriculum: {filename}",
            "loaded_documents": list(assistant['loaded_documents'].keys())
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to load curriculum: {filename}",
            "error": "File not found or could not be processed"
        }

def get_loaded_documents() -> Dict[str, Any]:
    """Get list of currently loaded curriculum documents.
    
    Returns:
        dict: A dictionary containing the list of loaded documents
    """
    assistant = initialize_rag_assistant()
    documents = assistant['loaded_documents']
    
    return {
        "status": "success",
        "loaded_documents": list(documents.keys()),
        "count": len(documents)
    }

def clear_memory() -> Dict[str, Any]:
    """Clear all loaded documents and memory.
    
    Returns:
        dict: A dictionary containing the clear status
    """
    assistant = initialize_rag_assistant()
    assistant['context_retriever'].clear_memory()
    assistant['loaded_documents'].clear()
    
    return {
        "status": "success",
        "message": "Memory cleared successfully"
    }

# Create the ADK agent
root_agent = Agent(
    name="rag_teaching_assistant",
    model="gemini-2.0-flash",
    description="A RAG-powered teaching assistant that can answer questions about curriculum documents loaded from PDFs.",
    instruction="""You are a RAG-powered teaching assistant. You can:

1. Answer questions about curriculum documents loaded from PDFs
2. Load new curriculum documents
3. Show which documents are currently loaded
4. Clear memory when needed

When a user asks a question about curriculum content, use the ask_curriculum_question tool to get relevant information from the loaded documents.

Be helpful, accurate, and educational in your responses.""",
    tools=[ask_curriculum_question, load_curriculum_document, get_loaded_documents, clear_memory]
) 