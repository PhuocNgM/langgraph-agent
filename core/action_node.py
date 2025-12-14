# core/action_node.py

from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm 


def action_node(state: AgentState) -> Dict[str, Any]:
    plan = state.get("plan") or ""
    context = state.get("context", "No base knowledge provided.") 
    
    steps = [s.strip() for s in plan.splitlines() if s.strip()]
    new_logs = []

    for i, step in enumerate(steps, start=1):
        prompt = f"""
        YOU ARE A TRAINING ASSISTANT. YOUR RESPONSE MUST BE STRICTLY BASED ON THE PROVIDED CONTEXT.

        [RETRIEVED KNOWLEDGE]:
        {context}
        ---

        Step to execute: {step}
        Generate detailed instructions OR a short quiz question based only on the RETRIEVED KNOWLEDGE for this step.
        If the context is insufficient, state that the information is limited, BUT still attempt to provide a brief answer based on what you have.        
        """

        output = call_llm(prompt)
        print(f"LLM Output (Step {i}): {output[:100]}...") # Print EN
        
        log_entry = ProgressLog(
            # ... (log creation) ...
            step_name="action_node",
            value=output
        )
        new_logs.append(log_entry)

    return {
        "context": state.get("context", ""), # <-- BẮT BUỘC trả lại context
        "progress": state.get("progress", []) + new_logs
    }
