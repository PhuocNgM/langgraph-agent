# memory/vector_store.py

import os
import faiss
import pickle
import numpy as np
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables (to ensure API key is available)
load_dotenv()

class VectorStore:
    def __init__(self, path: str = "./memory/vector_db"):
        self.path = path
        self.index_path = os.path.join(self.path, "index.faiss")
        self.text_path = os.path.join(self.path, "texts.pkl")
        
        openai_api_key = os.getenv("OPENAI_API_KEY") 

        # Initialize the embedding model
        self.model_name = "text-embedding-3-small"
        self.embedding_model = OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=openai_api_key 
        )
        # Dimension for text-embedding-3-small
        self.d = 1536 
        
        # Initialize attributes and load data
        self.index = None 
        self.texts = []
        
        # CRITICAL FIX: Use IndexFlatIP for Cosine Similarity
        self.index = faiss.IndexFlatIP(self.d) 

        self.load() 

    def add(self, texts: List[str]):
        """Adds new text chunks to the store, embeds them, and saves."""
        vectors = self.embedding_model.embed_documents(texts) 
        vector_array = np.array(vectors).astype('float32')
        
        # CRITICAL FIX: Normalize vectors before adding to the IP index
        faiss.normalize_L2(vector_array)
        
        if vector_array.ndim == 1:
            vector_array = vector_array.reshape(1, -1)
            
        self.index.add(vector_array)
        self.texts.extend(texts)
        self.save()

    def save(self):
        """Saves the FAISS index and the corresponding texts."""
        os.makedirs(self.path, exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.text_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self):
        """Loads the FAISS index and texts from disk."""
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                if os.path.exists(self.text_path):
                    with open(self.text_path, "rb") as f:
                        self.texts = pickle.load(f)
                else:
                    self.texts = [] 
            except Exception as e:
                print(f"ERROR: Failed to load VectorStore: {e}")
                # Fallback to a new IP index on failure
                self.index = faiss.IndexFlatIP(self.d) 
                self.texts = []
        else:
            print("INFO: No VectorStore found. Creating new IndexFlatIP index.")
            self.index = faiss.IndexFlatIP(self.d)
            self.texts = []

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Performs a similarity search using the normalized query vector."""
        if self.index.ntotal == 0:
            print("WARNING: Index is empty, cannot search.")
            return []
            
        # 1. Embed the query
        q_vec = self.embedding_model.embed_query(query) 
        q_vec_faiss = np.array([q_vec]).astype('float32')
        
        # CRITICAL FIX: Normalize the query vector before searching
        faiss.normalize_L2(q_vec_faiss)
        
        # 2. Perform FAISS search
        D, I = self.index.search(q_vec_faiss, top_k)
        
        # 3. Compile results
        results = []
        for k, i in enumerate(I[0]):
            if i != -1:
                # D is the score (higher is better for IP/Cosine)
                results.append((self.texts[i], float(D[0][k]))) 
        return results