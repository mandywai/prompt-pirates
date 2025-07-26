import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
from typing import List, Tuple

from .config import get_config

Config = get_config()

class VectorMemory:
    def __init__(self, model_name=None, index_path=None, meta_path=None):
        # Use config values if not provided
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self.index_path = index_path or Config.FAISS_INDEX_PATH
        self.meta_path = meta_path or Config.CHUNK_METADATA_PATH
        self.model = SentenceTransformer(self.model_name)
        self.chunks = []  # List of text chunks
        self.index = None
        self.dimension = None
        self._load()

    def _load(self):
        if os.path.exists(self.meta_path):
            with open(self.meta_path, 'rb') as f:
                self.chunks = pickle.load(f)
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.dimension = self.index.d

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.chunks, f)

    def add_chunks(self, chunks: List[str]):
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        if self.index is None:
            self.dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        self.chunks.extend(chunks)
        self._save()

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        if self.index is None or len(self.chunks) == 0:
            return []
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], dist))
        return results

    def clear(self):
        self.chunks = []
        self.index = None
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.meta_path):
            os.remove(self.meta_path) 