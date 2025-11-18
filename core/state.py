# core/state.py
from typing import TypedDict, List, Any, Optional
from datetime import datetime

# Định nghĩa cấu trúc cho một mục log (thay thế logic auto_log)
class ProgressLog(TypedDict):
    timestamp: str
    step_name: str  # Tên của node (ví dụ: 'planner', 'reflect')
    update_key: str # Khóa nào trong state đã bị thay đổi
    value: Any      # Giá trị mới được thêm vào

# Định nghĩa State chính bằng TypedDict (chuẩn LangGraph)
class AgentState(TypedDict):
    # Các trường bắt buộc khi khởi tạo
    trainee_name: str
    goal: str
    level: str
    input: str # Cần một input ban đầu cho planner

    # Danh sách các log tiến trình
    progress: List[ProgressLog]

    # Các trường này sẽ được thêm vào bởi các node
    plan: Optional[str]
    reflection: Optional[str]
    memory_saved: Optional[bool]
    step_info: Optional[str] # Ghi lại bước đi (ví dụ: 'planner -> action')