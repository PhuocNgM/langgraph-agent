# core/action_node.py

from core.state import AgentState
from langgraph.types import NodeOutput
from typing import Dict

def action_node(state: AgentState) -> NodeOutput:
    """
    Node thực thi hành động theo kế hoạch của planner.
    """

    plan = state.get("plan", "")
    user_input = state.get("input", "")

    # Mô phỏng hành vi thực thi — sau này có thể thay bằng tool hoặc LLM call
    if "tìm kiếm" in plan.lower():
        result = f"[Tool] Kết quả giả lập cho yêu cầu: '{user_input}'"
    elif "tính toán" in plan.lower():
        result = f"[Tool] Kết quả phép tính cho yêu cầu: '{user_input}'"
    else:
        result = f"[LLM] Trả lời trực tiếp cho: '{user_input}'"

    # Cập nhật state
    return {
        "result": result,
        "step": "action → reflect",
    }
