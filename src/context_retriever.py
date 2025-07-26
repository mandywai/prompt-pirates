from typing import List, Dict, Any
from .pdf_retriever import load_and_prepare_pdf
from .memory import VectorMemory
import os

class ContextRetriever:
    def __init__(self, pdf_folder: str = "src/books"):
        self.pdf_folder = pdf_folder
        self.memory = VectorMemory()
        self.loaded_pdfs = {}
        
    def load_pdf(self, pdf_filename: str) -> bool:
        """Load a PDF file and add its chunks to memory."""
        pdf_path = os.path.join(self.pdf_folder, pdf_filename)
        
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return False
            
        try:
            # Extract and chunk the PDF
            chunks = load_and_prepare_pdf(pdf_path, chunk_size=500)
            
            # Add chunks to memory
            self.memory.add_chunks(chunks)
            self.loaded_pdfs[pdf_filename] = len(chunks)
            
            print(f"Successfully loaded {pdf_filename} with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error loading PDF {pdf_filename}: {e}")
            return False
    
    def search_context(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant context content based on query."""
        results = self.memory.search(query, k=k)
        
        formatted_results = []
        for chunk, distance in results:
            formatted_results.append({
                "content": chunk,
                "relevance_score": 1.0 / (1.0 + distance),  # Convert distance to similarity score
                "source": "context_pdf"
            })
            
        return formatted_results
    
    def get_context_for_query(self, query: str, k: int = 3) -> str:
        """Get formatted context from documents for a query."""
        results = self.search_context(query, k=k)
        
        if not results:
            return "No relevant context content found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"Context {i} (Relevance: {result['relevance_score']:.3f}):\n{result['content']}\n")
        
        return "\n".join(context_parts)
    
    def clear_memory(self):
        """Clear all loaded context from memory."""
        self.memory.clear()
        self.loaded_pdfs.clear()
        print("Context memory cleared.")
    
    def list_loaded_pdfs(self) -> Dict[str, int]:
        """Return a dictionary of loaded PDFs and their chunk counts."""
        return self.loaded_pdfs.copy()

# Example usage functions
def create_context_retriever(pdf_folder: str = "src/books") -> ContextRetriever:
    """Create and return a context retriever instance."""
    return ContextRetriever(pdf_folder)

def load_context_pdf(retriever: ContextRetriever, pdf_filename: str) -> bool:
    """Load a specific PDF into the context retriever."""
    return retriever.load_pdf(pdf_filename)

def query_context(retriever: ContextRetriever, question: str, k: int = 3) -> str:
    """Query the context and return relevant information."""
    return retriever.get_context_for_query(question, k=k) 