from typing import List, Dict, Any, Optional
from .context_retriever import ContextRetriever
import google.generativeai as genai
import os
from .config import get_config

Config = get_config()

class TaskExecutor:
    """Executor that handles calling LLMs and tools to fulfill sub-tasks."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        self.model_name = model or Config.GEMINI_MODEL
        self.context_retriever = None
        self.llm = None
        
        # Initialize Gemini API
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from config
            api_key = Config.GEMINI_API_KEY
            if api_key:
                genai.configure(api_key=api_key)
            else:
                print("Warning: No API key provided. Set GEMINI_API_KEY in .env file or environment.")
        
        try:
            self.llm = genai.GenerativeModel(model)
        except Exception as e:
            print(f"Error initializing LLM: {e}")
    
    def set_context_retriever(self, retriever: ContextRetriever):
        """Set the context retriever for this executor."""
        self.context_retriever = retriever
    
    def execute_context_retrieval(self, query: str, k: int = 3) -> str:
        """Execute context retrieval from loaded documents."""
        if not self.context_retriever:
            return "No context retriever available."
        
        try:
            context = self.context_retriever.get_context_for_query(query, k=k)
            return context
        except Exception as e:
            return f"Error retrieving context: {e}"
    
    def execute_llm_generation(self, prompt: str, context: str = "") -> str:
        """Execute LLM generation with optional context."""
        if not self.llm:
            print("test")
            return "LLM not available. Please check API configuration."
        
        try:
            # Combine context and prompt
            full_prompt = f"""
            Context Information:
            {context}
            
            Task:
            {prompt}
            
            Please provide a clear, accurate, and helpful response based on the context provided.
            """
            
            response = self.llm.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"
    
    def execute_explanation_task(self, query: str) -> str:
        """Execute explanation sub-tasks."""
        # Step 1: Retrieve relevant context
        context = self.execute_context_retrieval(query)
        
        # Step 2: Generate explanation
        explanation_prompt = f"""
        Based on the provided context, please explain: {query}
        
        Your explanation should:
        1. Be clear and easy to understand
        2. Use the context information provided
        3. Include key concepts and definitions
        4. Provide examples if helpful
        5. Summarize the main points
        """
        
        return self.execute_llm_generation(explanation_prompt, context)
    
    def execute_comparison_task(self, query: str) -> str:
        """Execute comparison sub-tasks."""
        # Step 1: Retrieve context for comparison
        context = self.execute_context_retrieval(query)
        
        # Step 2: Generate comparison
        comparison_prompt = f"""
        Based on the provided context, please compare the items mentioned in: {query}
        
        Your comparison should:
        1. Identify the items being compared
        2. List key characteristics of each
        3. Highlight similarities and differences
        4. Present the comparison in a structured format
        5. Provide a balanced analysis
        """
        
        return self.execute_llm_generation(comparison_prompt, context)
    
    def execute_analysis_task(self, query: str) -> str:
        """Execute analysis sub-tasks."""
        # Step 1: Retrieve comprehensive context
        context = self.execute_context_retrieval(query, k=5)  # More context for analysis
        
        # Step 2: Generate analysis
        analysis_prompt = f"""
        Based on the provided context, please analyze: {query}
        
        Your analysis should:
        1. Break down the subject into components
        2. Evaluate each component systematically
        3. Identify patterns, trends, or relationships
        4. Provide evidence from the context
        5. Synthesize findings into coherent conclusions
        """
        
        return self.execute_llm_generation(analysis_prompt, context)
    
    def execute_solution_task(self, query: str) -> str:
        """Execute problem-solving sub-tasks."""
        # Step 1: Retrieve relevant methods/formulas
        context = self.execute_context_retrieval(query)
        
        # Step 2: Generate solution
        solution_prompt = f"""
        Based on the provided context, please solve: {query}
        
        Your solution should:
        1. Clearly state the problem
        2. Identify the appropriate method or approach
        3. Show step-by-step solution process
        4. Verify the result
        5. Explain the reasoning behind each step
        """
        
        return self.execute_llm_generation(solution_prompt, context)
    
    def execute_general_task(self, query: str) -> str:
        """Execute general query tasks."""
        # Step 1: Retrieve context
        context = self.execute_context_retrieval(query)
        
        # Step 2: Generate response
        general_prompt = f"""
        Please answer the following question: {query}
        
        Your response should:
        1. Be accurate and based on the provided context
        2. Be comprehensive and well-structured
        3. Address all aspects of the question
        4. Be clear and easy to understand
        """
        
        return self.execute_llm_generation(general_prompt, context)
    
    def execute_task(self, task_type: str, query: str) -> str:
        """Execute a specific task type."""
        if task_type == 'explain':
            return self.execute_explanation_task(query)
        elif task_type == 'compare':
            return self.execute_comparison_task(query)
        elif task_type == 'analyze':
            return self.execute_analysis_task(query)
        elif task_type == 'solve':
            return self.execute_solution_task(query)
        else:
            return self.execute_general_task(query)

# Convenience functions
def create_executor(api_key: Optional[str] = None, model: str = None) -> TaskExecutor:
    """Create and return a task executor instance."""
    return TaskExecutor(api_key, model)

def execute_user_query(executor: TaskExecutor, task_type: str, query: str) -> str:
    """Execute a user query based on task type."""
    return executor.execute_task(task_type, query)
