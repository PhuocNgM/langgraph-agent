# memory/vector_store.py (SỬ DỤNG CHROMA DB - Phiên bản Tinh chỉnh)

import os
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Load environment variables (Essential for OpenAI Key)
load_dotenv() 

class VectorStore:
    def __init__(self, path: str = "./memory/knowledge_base_store"):
        self.path = path
        self.collection_name = "rag_agent_collection" # <-- Khai báo tên Collection
        
        openai_api_key = os.getenv("OPENAI_API_KEY") 
        self.model_name = "text-embedding-3-small"
        
        # 1. Khởi tạo Embedding Model
        self.embedding_model = OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=openai_api_key 
        )
        
        # 2. Khởi tạo ChromaDB client (tự động load từ path nếu có)
        self.db = Chroma(
            persist_directory=self.path,
            embedding_function=self.embedding_model,
            collection_name=self.collection_name # <-- Gán Collection Name
        )
        
        self.texts = [] 

    def add(self, texts: List[str]):
        """Thêm văn bản mới. Chroma tự động tạo vector và lưu (persist)."""
        if not texts:
            print("WARNING: No text provided to add to Chroma.")
            return

        # Chroma's add_texts returns a list of IDs.
        self.db.add_texts(
            texts=texts,
        )
        
        # Đảm bảo dữ liệu được ghi xuống đĩa ngay lập tức
        print(f"INFO: Successfully added {len(texts)} chunks to ChromaDB.")
        
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Performs a similarity search using Chroma's built-in vector search."""
        
        # Chroma's similarity_search_with_score trả về (document, score)
        results = self.db.similarity_search_with_score(
            query=query,
            k=top_k
        )
        
        # Định dạng lại output để khớp với định dạng (text, score) cũ của bạn
        return [(doc.page_content, score) for doc, score in results]