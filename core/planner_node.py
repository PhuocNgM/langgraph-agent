# core/planner_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog # Import state và cấu trúc log

def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Node phân tích yêu cầu và lên kế hoạch hành động.
    Nhận vào DICT, trả về DICT chứa các cập nhật.
    """
    user_input = state.get("input", "")
    
    # ... (Logic lập kế hoạch của bạn) ...
    if "tìm" in user_input.lower():
        plan = "Sử dụng công cụ tìm kiếm để lấy thông tin."
    elif "tính toán" in user_input.lower():
        plan = "Dùng tool tính toán để trả kết quả."
    else:
        plan = "Trả lời trực tiếp bằng mô hình ngôn ngữ."

    step_info = "planner → action"

    # Tạo log thủ công
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="planner_node",
        update_key="plan",
        value=plan
    )

    # Trả về DICT chứa các khóa cần CẬP NHẬT
    # LangGraph sẽ tự động hợp nhất (merge) chúng
    return {
        "plan": plan,
        "step_info": step_info,
        "progress": state.get("progress", []) + [log_entry] # Nối log mới
    }