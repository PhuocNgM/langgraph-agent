# ingest.py
import os
from dotenv import load_dotenv 
from memory.knowledge_base import KnowledgeBase 

# --- Path Configuration ---
DATA_PATH = "document/" 
KB_PATH = "./memory/knowledge_base_store" 

def main():
    # Load environment variables (Essential for OpenAI Key)
    # This ensures the key is available even when running ingest.py standalone.
    load_dotenv() 

    print("--- Starting Knowledge Base Ingestion ---")
    
    # 1. Check for data directory
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"INFO: Created '{DATA_PATH}' folder. Please add your documents and run again.")
        return

    # 2. Initialize KnowledgeBase (This also attempts to load the VectorStore)
    kb = KnowledgeBase(path=KB_PATH)

    # 3. Check if we need to clean old data before ingesting
    # (Optional: Add logic here to delete the KB_PATH folder if you want to force a clean start every time)

    # 4. Start ingestion process (This handles loading/splitting/saving)
    kb.ingest_from_directory(DATA_PATH)
    
    print("--- Ingestion process finished. ---")

if __name__ == "__main__":
    main()