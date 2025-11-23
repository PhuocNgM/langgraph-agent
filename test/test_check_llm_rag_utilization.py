# check_llm_rag_utilization.py

import os
from dotenv import load_dotenv 
from memory.knowledge_base import KnowledgeBase
from llm.llm_client import call_llm
from typing import List, Any

# Cấu hình phải khớp với main.py và ingest.py
KB_PATH = "./memory/knowledge_base_store"

def check_llm_utilization(query: str):
    load_dotenv()
    
    print("--- STARTING LLM CONTEXT UTILIZATION TEST ---")
    
    # 1. Load Knowledge Base
    try:
        kb = KnowledgeBase(path=KB_PATH)
    except Exception as e:
        print(f"ERROR: Failed to load KnowledgeBase. Error: {e}")
        return

    # 2. Query the Vector Store (uses top_k=10/20 as defined in knowledge_base.py)
    context_list = kb.query(query)
    
    if not context_list:
        print("FAIL: Retrieval returned 0 documents. Fix the vector search first.")
        return

    # 3. Format Context for Prompt (using the same format as reflect_node)
    context_text = "\n\n--- Retrieved Knowledge ---\n" + "\n".join(
        [f"[Source {i+1}]: {doc}" for i, doc in enumerate(context_list)]
    )
    
    # 4. Construct the Forcing Prompt
    # Prompt buộc LLM phải chứng minh nó đã đọc context
    test_prompt = f"""
    You are a QA testing agent. Your task is to prove that you are reading the source material.

    [CONTEXT FOR TEST]:
    {context_text}
    ---
    
    QUESTION: {query}

    INSTRUCTIONS:
    1.  STRICTLY ANSWER the question ONLY using the provided [CONTEXT FOR TEST].
    2.  If you cannot find the answer, reply: "Context is insufficient."
    3.  Begin your response by confirming the source, like: "Based on Source 1, D5185 is used for..."
    """
    
    # 5. Call LLM and Print Result
    print("\n--- FINAL LLM PROMPT (SENT FOR SYNTHESIS) ---")
    print(test_prompt[:500] + "...")
    print("\n--- LLM RESPONSE ---")
    
    test_response = call_llm(test_prompt)
    
    print(test_response)
    
    print("\n--- TEST COMPLETE ---")


if __name__ == "__main__":
    # ⚠️ THAY THẾ bằng một câu hỏi cụ thể từ tài liệu của bạn
    test_query = "What is the primary use of the D5185 component?" 
    
    check_llm_utilization(test_query)