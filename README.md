# Agentic AI App Hackathon -- Team Prompt Pirates!!

# Classroom Assistant Agent with PDF Summarization RAG

A Classroom Assistant built using Google’s **Agent Development Kit (ADK)** + Gemini for reading PDFs, summarizing content, and generating study aids.

---

## 🚀 Features

- Upload PDF files via ADK Web interface  
- Automatic extraction + summarization using a RAG model
- Flashcard and mind‑map generation via separate tool agent  
- Cleanup and chaining with ADK agents (Sequential)

---

## 📁 Project Structure

'''
├── .github/
│   └── workflows/
│       └── ci.yml       # CI smoke-test workflow
├── src/                 # Your agent code
│ └── tools/
│ │ ├─ xxx
│ ├── init.py
│ ├── agent.py
│ └── .env               # hidden
├── README.md
├── environment.yml      # Conda environment specification
├── Dockerfile           # Docker build file (alternative to Conda)
├── TEST.sh              # Smoke‑test script to verify core functionality
├── ARCHITECTURE.md     # High‑level diagram and component breakdown
├── EXPLANATION.md      # Technical write‑up of your design choices
└── DEMO.md             # Link to demo video with timestamps
'''
