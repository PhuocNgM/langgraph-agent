# memory/knowledge_base.py
import os
from typing import List
from dotenv import load_dotenv 

# --- CÁC IMPORT QUAN TRỌNG (Đừng xóa) ---
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from .vector_store import VectorStore
# ----------------------------------------

try:
    load_dotenv()
except Exception:
    pass

class KnowledgeBase:
    def __init__(self, path="./memory/knowledge_base_store"):
        # vector store definition     
        self.store = VectorStore(path)
        print(f"INFO: Initialized KnowledgeBase at: {path}")

    def ingest_from_directory(self, directory_path: str = "./data"):
        """
        adding one by one files.
        """
        # 1. Kiểm tra thư mục tồn tại
        if not os.path.exists(directory_path):
            print(f"ERROR: Directory '{directory_path}' does not exist.")
            return
        
        print(f"--- Starting Ingestion from: {directory_path} ---")

        # 2. Quét toàn bộ file trong thư mục
        pdf_files = []
        txt_files = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
                elif file.lower().endswith(".txt"):
                    txt_files.append(os.path.join(root, file))

        documents = []

        # 3. Load từng file PDF (An toàn)
        print(f"Found {len(pdf_files)} PDF files. Processing one by one...")
        for pdf_path in pdf_files:
            try:
                # Dùng PyPDFLoader cho từng file
                loader = PyPDFLoader(pdf_path) 
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✅ Loaded: {os.path.basename(pdf_path)}")
            except Exception as e:
                # Nếu file lỗi, in ra warning và bỏ qua, không crash chương trình
                print(f"  ❌ SKIPPING corrupted file: {os.path.basename(pdf_path)} - Error: {e}")

        # 4. Load từng file TXT (An toàn)
        print(f"Found {len(txt_files)} TXT files...")
        for txt_path in txt_files:
            try:
                loader = TextLoader(txt_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✅ Loaded: {os.path.basename(txt_path)}")
            except Exception as e:
                print(f"  ❌ SKIPPING file: {os.path.basename(txt_path)}")

        if not documents:
            print("WARNING: No valid documents loaded. Stopping.")
            return

        # 5. Chia nhỏ văn bản (Splitting)
        print(f"Splitting {len(documents)} documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"  > Generated {len(texts)} raw text chunks.")

        # 6. Lọc và làm sạch dữ liệu
        string_texts = []
        for doc in texts:
            content = doc.page_content.strip()
            # Chỉ lấy các đoạn có nội dung dài hơn 5 ký tự
            if len(content) > 5: 
                string_texts.append(content)

        if not string_texts:
            print("WARNING: No valid chunks generated.")
            return

        # 7. Nạp vào VectorStore theo lô (Batching)
        total_chunks = len(string_texts)
        BATCH_SIZE = 2000 
        
        print(f"💾 Ingesting {total_chunks} chunks into VectorStore (Batch Size: {BATCH_SIZE})...")
        
        for i in range(0, total_chunks, BATCH_SIZE):
            batch = string_texts[i : i + BATCH_SIZE]
            batch_num = (i // BATCH_SIZE) + 1
            
            try:
                print(f"  > Processing Batch {batch_num} ({len(batch)} chunks)...")
                self.store.add(batch)
            except Exception as e:
                print(f"  ❌ Error adding Batch {batch_num}: {e}")
                
        print("✅ Ingestion process completed successfully.")

    def query(self, question: str) -> List[str]:
        """
        Truy vấn dữ liệu.
        """
        try:
            results = self.store.search(question, top_k=5)
            # Trả về list text
            return [text for text in results] 
        except Exception as e:
            print(f"Query Error: {e}")
            return []