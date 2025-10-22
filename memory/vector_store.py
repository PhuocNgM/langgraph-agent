# memory/vector_store.py
import os
import faiss
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, path: str = "./memory/vector_db"):
        self.path = path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # 384 là dimension của model embedding
        self.texts = []

    def add(self, texts: List[str]):
        vectors = self.model.encode(texts)
        self.index.add(np.array(vectors))
        self.texts.extend(texts)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        q_vec = self.model.encode([query])
        D, I = self.index.search(np.array(q_vec), top_k)
        return [(self.texts[i], float(D[0][k])) for k, i in enumerate(I[0])]

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(self.path, "index.faiss"))

    def load(self):
        index_path = os.path.join(self.path, "index.faiss")
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
