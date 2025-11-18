# memory/vector_store.py
import os
import faiss
import pickle  # <-- Thêm thư viện pickle
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, path: str = "./memory/vector_db"):
        self.path = path
        self.index_path = os.path.join(self.path, "index.faiss")
        self.text_path = os.path.join(self.path, "texts.pkl") # <-- Đường dẫn cho file texts
        
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.d = 384  # 384 là dimension của model embedding
        
        # Khởi tạo index và texts
        self.index = faiss.IndexFlatL2(self.d)
        self.texts = []
        
        # Tự động load nếu tồn tại
        self.load() 

    def add(self, texts: List[str]):
        """Thêm văn bản mới và tự động lưu."""
        vectors = self.model.encode(texts)
        self.index.add(np.array(vectors).astype('float32')) # Đảm bảo kiểu float32
        self.texts.extend(texts)
        self.save() # Tự động lưu mỗi khi thêm

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Tìm kiếm và trả về văn bản cùng độ tương đồng (distance)."""
        if self.index.ntotal == 0:
            return [] # Trả về rỗng nếu index chưa có gì
            
        q_vec = self.model.encode([query])
        D, I = self.index.search(np.array(q_vec).astype('float32'), top_k)
        
        results = []
        for k, i in enumerate(I[0]):
            if i != -1: # FAISS có thể trả về -1 nếu không tìm thấy
                results.append((self.texts[i], float(D[0][k])))
        return results

    def save(self):
        """Lưu cả index và danh sách texts."""
        os.makedirs(self.path, exist_ok=True)
        
        # 1. Lưu FAISS index
        faiss.write_index(self.index, self.index_path)
        
        # 2. SỬA LỖI: Lưu self.texts bằng pickle
        with open(self.text_path, "wb") as f:
            pickle.dump(self.texts, f)
        
        # print(f"Đã lưu VectorStore vào {self.path}")

    def load(self):
        """Tải cả index và danh sách texts."""
        
        # 1. Tải FAISS index
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                
                # 2. SỬA LỖI: Tải self.texts từ pickle
                if os.path.exists(self.text_path):
                    with open(self.text_path, "rb") as f:
                        self.texts = pickle.load(f)
                else:
                    print(f"Cảnh báo: Không tìm thấy file {self.text_path}. 'texts' sẽ bị rỗng.")
                    self.texts = [] # Đảm bảo texts rỗng nếu file không có

            except Exception as e:
                print(f"Lỗi khi tải VectorStore: {e}")
                # Reset nếu tải lỗi
                self.index = faiss.IndexFlatL2(self.d)
                self.texts = []
        # else:
            # print("Chưa có VectorStore. Sẽ tạo mới khi 'add' được gọi.")