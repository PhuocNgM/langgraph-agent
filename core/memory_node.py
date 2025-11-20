# core/memory_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog

def memory_node(state: AgentState) -> Dict[str, Any]:
    """ Simulates updating the long-term memory with the final reflection/progress. """
    print("--- STATUS: MEMORY NODE EXECUTING ---")
    
    reflection = state.get("reflection", "")
    progress = state.get("progress", [])

    # In a real system, you would call a database client here
    print(f"🧠 Saving to Memory: {len(progress)} steps and final reflection.")
    
    # Create log
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="memory_node",
        update_key="memory_saved",
        value=True
    )

    # Return updates
    return {
        "memory_saved": True,
        "progress": state.get("progress", []) + [log_entry]
    }