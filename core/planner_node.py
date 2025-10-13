# core/planner_node.py

from core.state import AgentState
from langgraph.types import NodeOutput
from typing import Dict

def planner_node(state: AgentState) -> NodeOutput:
    """
    Node phân tích yêu cầu và lên kế hoạch hành động cho agent.
    """

    user_input = state.get("input", "")
    history = state.get("history", [])

    # (Tạm thời logic giả — sau này bạn có thể thay bằng LLM call)
    if "tìm" in user_input.lower():
        plan = "Sử dụng công cụ tìm kiếm để lấy thông tin."
    elif "tính toán" in user_input.lower():
        plan = "Dùng tool tính toán để trả kết quả."
    else:
        plan = "Trả lời trực tiếp bằng mô hình ngôn ngữ."

    # Cập nhật state
    return {
        "plan": plan,
        "step": "planner → action",
    }
