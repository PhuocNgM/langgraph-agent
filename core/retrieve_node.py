# core/retriever_node.py

from typing import Dict, Any
from datetime import datetime
from core.state import AgentState, ProgressLog  
from memory.knowledge_base import KnowledgeBase 
# IMPORTANT: Removed import for call_llm (no translation needed)

# --- Knowledge Base Configuration ---
KB_PATH = "./memory/knowledge_base_store" 
# ------------------------------------

# 1. Initialize Knowledge Base ONCE upon module load
try:
    kb = KnowledgeBase(path=KB_PATH)
    print(f"✅ [RETRIEVER] Connected to Knowledge Base at: {KB_PATH}")
except Exception as e:
    print(f"❌ [RETRIEVER] ERROR: Failed to load Knowledge Base. Error: {e}")
    kb = None

def retriever_node(state: AgentState) -> Dict[str, Any]:
    
    print("--- STATUS: RETRIEVER NODE EXECUTING ---")
    
    if kb is None:
        print("Error: Knowledge base unavailable.")
        return {"context": "Error: Knowledge base unavailable."}

    print("--- 🔎 Retrieving Base Knowledge (RAG)... ---")
    
    # 1. ASSUME INPUT IS ENGLISH AND USE DIRECTLY FOR QUERY
    query_en = state.get("input", "")
    
    # 2. Execute search
    try:
        docs = kb.query(query_en) 
    except Exception as e:
        print(f"Retrieval Error: {e}")
        docs = []

    # --- Debugging Prints (Keep for now to confirm retrieval) ---
    print(f"DEBUG: Retrieved {len(docs)} documents.")
    if len(docs) > 0:
        print(f"DEBUG: First 50 chars of document 1: {docs[0][:50]}")
    # -----------------------------------------------------------

    # 3. Format context
    formatted_context = "\n\n--- Retrieved Knowledge ---\n"
    if not docs:
        formatted_context += "No relevant documents found."
    else:
        for i, doc_content in enumerate(docs):
            formatted_context += f"\n[Source {i+1}]: {doc_content}\n"
    
    print("\n--- 🔎 RETRIEVED CONTEXT (DEBUG) ---")
    if not docs:
        print("❌ ERROR: Context is empty. VectorStore returned 0 results.")
    else:
        print(formatted_context[:500].replace('\n', ' '))
    print("-----------------------------------------\n")


    # 4. Create log and Return
    log_entry = ProgressLog(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        step_name="retriever_node",
        update_key="context",
        value=f"Retrieved {len(docs)} documents for query: '{query_en}'"
    )

    return {
        "context": formatted_context, 
        "progress": state.get("progress", []) + [log_entry],
        "input": query_en # Ensure the English query is saved
    }