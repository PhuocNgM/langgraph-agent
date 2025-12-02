# test_rag.py

from memory.knowledge_base import KnowledgeBase
from memory.vector_store import VectorStore # Cần import để kiểm tra đường dẫn

KB_PATH = "./memory/knowledge_base_store"

def test_query():
    print(f"--- Kiểm tra KnowledgeBase tại: {KB_PATH} ---")
    
    # Kiểm tra xem file đã được tạo ra chưa
    if not os.path.exists(KB_PATH):
        print(f"❌ LỖI: Thư mục Knowledge Base '{KB_PATH}' không tồn tại. Vui lòng chạy lại ingest.py.")
        return
        
    # Khởi tạo KnowledgeBase 
    try:
        kb = KnowledgeBase(path=KB_PATH)
    except Exception as e:
        print(f"❌ LỖI: Không thể khởi tạo/load KnowledgeBase. Lỗi: {e}")
        return
    
    # Kiểm tra số lượng vector đã lưu
    if kb.store.index.ntotal == 0:
        print("❌ LỖI: Knowledge Base RỖNG (0 vector). Quá trình ingest.py đã thất bại.")
        print("   -> Nguyên nhân: File PDF rỗng hoặc lỗi khi tạo embeddings.")
        return

    # Thực hiện truy vấn trực tiếp với từ khóa cụ thể
    query_term = "D5185"
    results = kb.query(query_term)
    
    print(f"\n--- ✅ Đã tìm thấy {len(results)} chunks cho '{query_term}' ---")
    if results:
        print("Nội dung chunk đầu tiên:")
        print("="*40)
        print(results[0][:300]) # In 300 ký tự đầu tiên
        print("="*40)
    else:
        print("❌ KHÔNG tìm thấy tài liệu nào. Có thể do data gốc không khớp hoặc lỗi embedding.")

if __name__ == "__main__":
    import os
    test_query()