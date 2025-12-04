# core/reflect_node.py
from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog
from llm.llm_client import call_llm


def reflect_node(state: AgentState) -> Dict[str, Any]:
    query = state.get("input", "No user query.") 
    context = state.get("context", "")
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
        1.  Analyze ALL retrieved context chunks and synthesize a comprehensive, detailed response that fully answers the query.
        2.  Your response MUST be structured into **at least three (3) distinct paragraphs** and MUST have a **minimum length of 200 words**.
        3.  Structure the paragraphs to cover: (1) Purpose/Introduction, (2) Methodology, and (3) Key Considerations/Summary.
        4.  Strictly use only the information available in the RETRIEVED KNOWLEDGE section.
        5.  If the context does not contain sufficient information, reply with the most relevant information found, BUT also add the disclaimer: "Note: The provided context was limited."
        6.  Provide the final response directly.
    
    """
    # Debugging print
    # print("\n--- FINAL LLM PROMPT SENT (DEBUG) ---")
    # print(prompt) 
    # print("-------------------------------------\n")
    
    reflection = call_llm(prompt)
    print(f"Reflection: {reflection[:150]}...") # Print EN

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