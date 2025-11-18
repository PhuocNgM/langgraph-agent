from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog  # Import cấu trúc state và log
from memory.knowledge_base import KnowledgeBase # Import lớp KnowledgeBase đã tạo

# --- Cấu hình Knowledge Base ---
# Đường dẫn này PHẢI KHỚP với đường dẫn bạn dùng trong ingest.py
KB_PATH = "./memory/knowledge_base_store" 
# --------------------------------

# 1. Khởi tạo Knowledge Base MỘT LẦN khi nạp module
# Nó sẽ tự động gọi .load() bên trong __init__
try:
    kb = KnowledgeBase(path=KB_PATH)
    print(f"✅ [retriever_node] Đã kết nối với Knowledge Base tại: {KB_PATH}")
except Exception as e:
    print(f"❌ [retriever_node] LỖI: Không thể tải Knowledge Base tại '{KB_PATH}'. Lỗi: {e}")
    kb = None

def retriever_node(state: AgentState) -> Dict[str, Any]:
    """
    Node đầu tiên: Lấy input và truy xuất kiến thức nền (RAG).
    """
    if kb is None:
        print("Lỗi: Knowledge Base (retriever) không khả dụng.")
        return {"context": "Lỗi: Không thể truy cập kiến thức nền."}

    print("--- 🔎 Đang truy xuất kiến thức nền (RAG)... ---")
    query = state.get("input", "")
    
    # 2. Thực hiện tìm kiếm
    try:
        # kb.query() chỉ trả về list[str]
        docs = kb.query(query)
    except Exception as e:
        print(f"Lỗi khi tìm kiếm RAG: {e}")
        docs = []

    # 3. Định dạng lại kết quả tìm kiếm thành một chuỗi văn bản
    formatted_context = "\n\n--- Kiến thức được truy xuất ---\n"
    if not docs:
        formatted_context += "Không tìm thấy tài liệu nào liên quan."
    else:
        for i, doc_content in enumerate(docs):
            formatted_context += f"\n[Nguồn {i+1}]: {doc_content}\n"
    
    print(f"   Đã tìm thấy {len(docs)} tài liệu liên quan.")

    # 4. Tạo log
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="retriever_node",
        update_key="context",
        value=f"Đã truy xuất {len(docs)} tài liệu cho câu hỏi: '{query}'"
    )

    # 5. Trả về DICT cập nhật
    return {
        "context": formatted_context, # Đây là kiến thức nền
        "progress": state.get("progress", []) + [log_entry]
    }