# core/planner_node.py
from typing import Dict, Any
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm # Assuming this is used for planning
from datetime import datetime

def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyzes the current request, retrieved context, and history to form a plan.
    """
    print("--- STATUS: PLANNER NODE EXECUTING ---")
    
    user_input = state.get("input", "No user query.")
    context = state.get("context", "No context retrieved.")
    # history = state.get("history", []) 

    planner_prompt = f"""
    You are an expert planner. Based on the user query and the RAG context:
    [CONTEXT]: {context}
    [QUERY]: {user_input}
    
    Determine the optimal next step to generate the final response. 
    Respond only with the plan, phrased as a single action step.
    """

    try:
        # Calling LLM to generate plan
        plan = call_llm(planner_prompt) 
        # print(f"Plan generated: {plan[:50]}...")
    except Exception:
        # Fallback to a default plan if LLM call fails
        plan = "Analyze the provided RAG context and summarize the key findings."

    step_info = "Planner finished execution."
    
    # Create log
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="planner_node",
        update_key="plan",
        value=plan
    )

    return {
        "context": state.get("context", ""), # <-- BẮT BUỘC trả lại context
        "plan": plan,
        "step_info": step_info,
        "progress": state.get("progress", []) + [log_entry],
    }