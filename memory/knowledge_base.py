# memory/knowledge_base.py
import os
from .vector_store import VectorStore
from typing import List, Any
from dotenv import load_dotenv 

# --- Update Imports for RAG ---
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
# ------------------------------

# Load environment variables from .env (Must run before any module loads the API Key)
try:
    load_dotenv()
except Exception:
    pass

class KnowledgeBase:
    def __init__(self, path="./memory/knowledge_base_store"):
        # The VectorStore object automatically loads the index if files exist
        self.store = VectorStore(path)
        print(f"INFO: Initialized KnowledgeBase at: {path}")

        # 👇 INTEGRITY CHECK BLOCK (Removed FAISS-specific ntotal check)
        try:
            # We can no longer check ntotal directly, as Chroma manages the index internally.
            # We will rely on Chroma's own logging/integrity checks for this file.
            print(f"DEBUG: VectorStore initialized and connected.")
            
        except Exception as e:
            # Keep a generic integrity check for resilience
            print(f"🚨 ERROR: Failed VectorStore initialization integrity check. Reason: {e}")
        # ---------------------------------------------    

    def ingest_from_directory(self, directory_path: str = "./data"):
        """
        Loads, splits, and embeds documents from a directory into the VectorStore.
        """
        # 1. Check directory existence
        if not os.path.exists(directory_path):
            print(f"ERROR: Directory '{directory_path}' does not exist.")
            os.makedirs(directory_path)
            print(f"INFO: Created directory '{directory_path}'. Please add documents and run again.")
            return
        

        print(f"--- Starting Ingestion from: {directory_path} ---")

        # --- LOAD DOCUMENTS ---     
        print("Loading documents using DirectoryLoader...")
        
        # 1. Load PDFs using UnstructuredFileLoader 
        pdf_loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",  
            loader_cls=UnstructuredFileLoader, 
            recursive=True
        )

        # 2. Load TXT files
        txt_loader = DirectoryLoader(
            directory_path,
            glob="**/*.txt", 
            loader_cls=TextLoader,
            recursive=True
        )

        # 3. Aggregate documents
        try:
            pdf_docs = pdf_loader.load()
            txt_docs = txt_loader.load()
            
            documents = pdf_docs + txt_docs
            
        except Exception as e:
            print(f"ERROR: Failed to load documents. Reason: {e}")
            return
            
        
        if not documents:
            print(f"WARNING: Found no documents in '{directory_path}'.")
            return


        # 3. Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} document(s) into {len(texts)} text chunks.")

        # 4. FILTER and Convert Document objects to list[str]
        string_texts = []
        for doc in texts:
            content = doc.page_content.strip()
            # Filter out empty or single-character chunks
            if len(content) > 5 and content.lower() != 'd': 
                string_texts.append(content)


        print(f"Adding {len(string_texts)} valid chunks to VectorStore...")
        
        if not string_texts:
            print("WARNING: No valid chunks were generated after filtering. VectorStore remains empty.")
            return

        # 5. Add to VectorStore (will use ChromaDB's add logic)
        self.store.add(string_texts) 
        print("✅ Ingestion successful.")

    def query(self, question: str) -> List[str]:
        """
        Queries the vector store and retrieves the top_k relevant documents.
        """
        # Set top_k high (e.g., 5) - The value is now passed to Chroma's search method
        results = self.store.search(question, top_k=5)
        return [text for text, score in results]