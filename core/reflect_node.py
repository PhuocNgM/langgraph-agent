# core/reflect_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm


def reflect_node(state: AgentState) -> Dict[str, Any]:
    query = state.get("input", "No user query.") 
    context = state.get("context", "No base knowledge provided.")
    progress_list = state.get("progress", []) 
    
    progress_text = "\n".join([
        f"- {log.get('step_name')}: {log.get('update_key')} | {log.get('value')}"
        for log in progress_list
    ])
    
    prompt = f"""
    You are a professional training assistant. Your final response must be based strictly on the provided context.

    [RETRIEVED KNOWLEDGE]:
    {context}
    ---
    
    [EXECUTION PROGRESS]:
    {progress_text}

    INSTRUCTIONS:
    1.  Strictly use only the information available in the RETRIEVED KNOWLEDGE section.
    2.  If the context does not contain sufficient information to answer the user's query ({query}), you MUST reply: "I apologize, but I could not find specific information related to your query in the reference documents."
    3.  Provide the final response directly.
    """
    # 👇 THÊM KHỐI LỆNH CHẨN ĐOÁN NÀY TRƯỚC KHI GỌI LLM
    print("\n--- FINAL LLM PROMPT SENT (DEBUG) ---")
    print(prompt) 
    print("-------------------------------------\n")
    
    reflection = call_llm(prompt)
    print(f"💭 Reflection: {reflection[:150]}...") # Print EN

    log_entry = ProgressLog(
        # ... (log creation) ...
        step_name="reflect_node",
        update_key="reflection",
        value=reflection
    )
    
    return {
        "reflection": reflection,
        "progress": state.get("progress", []) + [log_entry]
    }