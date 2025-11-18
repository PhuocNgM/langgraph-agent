# core/memory_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog

def memory_node(state: AgentState) -> Dict[str, Any]:
    """ Cập nhật thông tin vào bộ nhớ dài hạn """
    reflection = state.get("reflection", "")
    progress = state.get("progress", [])

    # print(f"🧠 Lưu vào memory {len(progress)} bước và reflection.")
    
    # Tạo log
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="memory_node",
        update_key="memory_saved",
        value=True
    )

    # Trả về các cập nhật
    return {
        "memory_saved": True,
        "progress": state.get("progress", []) + [log_entry]
    }