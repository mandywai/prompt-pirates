import os
from google.adk.agents import Agent, SequentialAgent
import pdf_reader
import ask_rag  # assuming it returns {flashcards, mindmap_structure}

MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# Summarizer: uses reader_tool to create `pdf_summary`
summarizer_agent = Agent(
    name="summarizer_agent",
    model=MODEL,
    instruction="Use reader_tool to extract and summarize the uploaded PDF.",
    tools=[pdf_reader, ask_rag],
    output_key="pdf_summary"
)

# Mindmap + Flashcard generator
mindmap_agent = Agent(
    name="mindmap_agent",
    model=MODEL,
    instruction="""
You are a study assistant. Given this summary:
{pdf_summary}

Generate flashcards (Q&A) and a mind map structure.
Return JSON with keys `flashcards` and `mindmap_structure`.
""",
    tools=[pdf_reader, ask_rag],
    output_key="study_artifacts"
)

# Final Synthesis
synthesis_agent = Agent(
    name="synthesis_agent",
    model=MODEL,
    instruction="""
Here's your study packet:

**Summary:**
{{state.pdf_summary}}

**Flashcards:**
{{state.study_artifacts.flashcards}}

**Mind Map:**
{{state.study_artifacts.mindmap_structure}}
""",
    tools=[pdf_reader, ask_rag]
)

# Root agent runs them in sequence
root_agent = SequentialAgent(
    name="study_pipeline",
    description="Reads uploaded PDF, summarizes it, and generates flashcards/mindmap.",
    sub_agents=[summarizer_agent, mindmap_agent, synthesis_agent]
)