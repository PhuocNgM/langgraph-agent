# core/reflect_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm

def reflect_node(state: AgentState) -> Dict[str, Any]:
    """ Đánh giá lại hiệu quả training """
    progress = state.get("progress", [])
    prompt = f"""
    Dưới đây là tiến trình đào tạo:
    {progress}

    Hãy đánh giá mức độ đạt mục tiêu và gợi ý cải thiện cho lần sau.
    """
    reflection = call_llm(prompt)
    print(f"💭 Phản tư: {reflection[:150]}...")

    # Tạo log
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="reflect_node",
        update_key="reflection",
        value=reflection
    )

    # Trả về các cập nhật
    return {
        "reflection": reflection,
        "progress": state.get("progress", []) + [log_entry]
    }
