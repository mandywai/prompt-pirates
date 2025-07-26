from typing import List, Dict, Any
import re

class TaskPlanner:
    """Planner that breaks down user goals into sub-tasks for the teaching assistant."""
    
    def __init__(self):
        self.task_patterns = {
            'explain': ['define', 'describe', 'explain', 'what is', 'how does'],
            'compare': ['compare', 'difference', 'similar', 'versus', 'vs'],
            'analyze': ['analyze', 'examine', 'evaluate', 'assess'],
            'solve': ['solve', 'calculate', 'compute', 'find', 'determine'],
            'create': ['create', 'design', 'develop', 'build', 'make']
        }
    
    def identify_task_type(self, user_query: str) -> str:
        """Identify the type of task from the user query."""
        query_lower = user_query.lower()
        
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if pattern in query_lower:
                    return task_type
        
        return 'general'  # Default task type
    
    def plan_explanation_task(self, query: str) -> List[str]:
        """Plan sub-tasks for explanation requests."""
        return [
            "1. Retrieve relevant context from curriculum",
            "2. Identify key concepts and definitions",
            "3. Structure explanation in logical order",
            "4. Provide examples or analogies if needed",
            "5. Summarize main points"
        ]
    
    def plan_comparison_task(self, query: str) -> List[str]:
        """Plan sub-tasks for comparison requests."""
        return [
            "1. Identify items to compare from query",
            "2. Retrieve context for each item",
            "3. Extract key characteristics of each",
            "4. Identify similarities and differences",
            "5. Present comparison in structured format"
        ]
    
    def plan_analysis_task(self, query: str) -> List[str]:
        """Plan sub-tasks for analysis requests."""
        return [
            "1. Identify the subject to analyze",
            "2. Retrieve comprehensive context",
            "3. Break down into components or aspects",
            "4. Evaluate each component",
            "5. Synthesize findings into coherent analysis"
        ]
    
    def plan_solution_task(self, query: str) -> List[str]:
        """Plan sub-tasks for problem-solving requests."""
        return [
            "1. Understand the problem statement",
            "2. Retrieve relevant formulas, methods, or concepts",
            "3. Identify solution approach",
            "4. Apply solution step-by-step",
            "5. Verify and explain the result"
        ]
    
    def plan_general_task(self, query: str) -> List[str]:
        """Plan sub-tasks for general queries."""
        return [
            "1. Retrieve relevant context from curriculum",
            "2. Analyze the query requirements",
            "3. Generate comprehensive response",
            "4. Ensure accuracy and clarity"
        ]
    
    def plan(self, user_query: str) -> Dict[str, Any]:
        """Main planning function that breaks down user goals into sub-tasks."""
        task_type = self.identify_task_type(user_query)
        
        # Get sub-tasks based on task type
        if task_type == 'explain':
            sub_tasks = self.plan_explanation_task(user_query)
        elif task_type == 'compare':
            sub_tasks = self.plan_comparison_task(user_query)
        elif task_type == 'analyze':
            sub_tasks = self.plan_analysis_task(user_query)
        elif task_type == 'solve':
            sub_tasks = self.plan_solution_task(user_query)
        else:
            sub_tasks = self.plan_general_task(user_query)
        
        return {
            'original_query': user_query,
            'task_type': task_type,
            'sub_tasks': sub_tasks,
            'estimated_steps': len(sub_tasks)
        }

# Convenience function for easy usage
def create_planner() -> TaskPlanner:
    """Create and return a task planner instance."""
    return TaskPlanner()

def plan_user_query(query: str) -> Dict[str, Any]:
    """Plan a user query and return the breakdown."""
    planner = create_planner()
    return planner.plan(query)
