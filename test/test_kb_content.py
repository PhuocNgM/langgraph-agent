# check_kb_content.py
import os
from memory.knowledge_base import KnowledgeBase 
from dotenv import load_dotenv
from typing import List, Any

# --- Configuration (Must match ingest.py) ---
KB_PATH = "./memory/knowledge_base_store"

def check_store_content():
    # Load environment variables (needed for OpenAI embeddings)
    load_dotenv()
    
    print("--- STARTING KNOWLEDGE BASE CONTENT CHECK ---")
    
    # 1. Initialize KnowledgeBase (automatically loads data via VectorStore.__init__)
    try:
        kb = KnowledgeBase(path=KB_PATH)
    except Exception as e:
        print(f"ERROR: Failed to load KnowledgeBase. Ensure API key is set. Error: {e}")
        return

    # 2. Access the VectorStore's internal data attributes
    vector_count = kb.store.index.ntotal
    text_list = kb.store.texts
    
    print(f"SUCCESS: Loaded {vector_count} vectors and {len(text_list)} text chunks.")
    
    if vector_count == 0:
        print("WARNING: Store is empty. Please run 'python ingest.py' first.")
        return

    # 3. Print the first 5 chunks for inspection
    print("\n--- PREVIEW OF FIRST 5 STORED CHUNKS (FOR INSPECTION) ---")
    for i in range(min(5, vector_count)):
        text = text_list[i]
        print("\n" + "="*50)
        print(f"[CHUNK {i+1} / Length: {len(text)}]")
        print("="*50)
        print(text[:500] + "...") # Print first 500 characters
        
    print("\n--- CHECK COMPLETE ---")

if __name__ == "__main__":
    check_store_content()