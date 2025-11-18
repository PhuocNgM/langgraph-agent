# core/action_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm # Đảm bảo llm_client đã được sửa

def action_node(state: AgentState) -> Dict[str, Any]:
    """ Thực hiện hành động theo plan """
    plan = state.get("plan") or ""
    steps = [s.strip() for s in plan.splitlines() if s.strip()]
    
    # Lưu trữ các log mới được tạo ra trong node này
    new_logs = []

    for i, step in enumerate(steps, start=1):
        prompt = f"""
        Bước {i}: {step}
        Giả sử bạn đang hướng dẫn thực hành cho học viên.
        Viết hướng dẫn chi tiết hoặc câu hỏi kiểm tra ngắn.
        """
        output = call_llm(prompt)
        print(f"🧠 Output từ LLM (Step {i}): {output[:100]}...")
        
        # Tạo log cho từng bước
        log_entry = ProgressLog(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            step_name="action_node",
            update_key=f"action_step_{i}",
            value=output
        )
        new_logs.append(log_entry)

    # Trả về các cập nhật
    return {
        "progress": state.get("progress", []) + new_logs # Nối tất cả log mới
    }