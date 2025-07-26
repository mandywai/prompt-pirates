import os
from typing import List
import PyPDF2


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Splits text into chunks of approximately chunk_size words."""
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


def search_chunks(chunks: List[str], query: str) -> List[str]:
    """Returns all chunks containing the query string (case-insensitive)."""
    return [chunk for chunk in chunks if query.lower() in chunk.lower()]


def load_and_prepare_pdf(pdf_path: str, chunk_size: int = 500) -> List[str]:
    """Extracts and chunks text from a PDF file."""
    text = extract_text_from_pdf(pdf_path)
    return chunk_text(text, chunk_size=chunk_size)
