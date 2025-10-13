# core/reflect_node.py

from core.state import AgentState
from langgraph.types import NodeOutput

def reflect_node(state: AgentState) -> NodeOutput:
    """
    Node phản chiếu: đánh giá kết quả hành động trước đó và quyết định bước tiếp theo.
    """

    result = state.get("result", "")
    plan = state.get("plan", "")

    # Giả lập logic phản chiếu — sau này có thể dùng LLM để kiểm định chất lượng
    if not result or "lỗi" in result.lower():
        reflection = "Kết quả không hợp lệ, cần thử lại hành động."
        next_step = "planner → action"
    else:
        reflection = "Kết quả hợp lệ, chuyển sang cập nhật bộ nhớ."
        next_step = "reflect → memory"

    # Ghi lại suy nghĩ vào state
    return {
        "reflection": reflection,
        "step": next_step,
    }
