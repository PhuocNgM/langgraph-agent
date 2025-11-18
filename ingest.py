# ingest.py (Phiên bản mới, đơn giản)
import os
from memory.knowledge_base import KnowledgeBase # <-- Import lớp mới

# 1. Đường dẫn đến thư mục chứa data
DATA_PATH = "data/" 
# 2. Đường dẫn lưu trữ knowledge base
KB_PATH = "./memory/knowledge_base_store"

def main():
    # 1. Tạo thư mục data nếu chưa có
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Đã tạo thư mục '{DATA_PATH}'. Vui lòng thêm tài liệu (PDF, TXT) vào đó và chạy lại.")
        return

    # 2. Khởi tạo KnowledgeBase
    # Nó sẽ chịu trách nhiệm load/save VectorStore tại KB_PATH
    kb = KnowledgeBase(path=KB_PATH)

    # 3. Ra lệnh cho nó nạp dữ liệu từ thư mục
    kb.ingest_from_directory(DATA_PATH)

if __name__ == "__main__":
    main()