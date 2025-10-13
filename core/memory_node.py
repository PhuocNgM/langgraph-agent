# core/memory_node.py

from core.state import AgentState
from langgraph.types import NodeOutput

def memory_node(state: AgentState) -> NodeOutput:
    """
    Node bộ nhớ: lưu lại thông tin hội thoại và kết quả.
    """

    user_input = state.get("input", "")
    plan = state.get("plan", "")
    result = state.get("result", "")
    reflection = state.get("reflection", "")
    history = state.get("history", [])

    # Cập nhật lịch sử hội thoại
    new_entry = {
        "input": user_input,
        "plan": plan,
        "result": result,
        "reflection": reflection,
    }
    updated_history = history + [new_entry]

    # Trả kết quả cuối cùng (END node)
    return {
        "history": updated_history,
        "final_output": result,
        "step": "memory → END",
    }
