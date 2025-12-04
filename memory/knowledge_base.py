# memory/knowledge_base.py
import os
from .vector_store import VectorStore
from typing import List

# --- Thêm các thư viện LangChain để xử lý file ---
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# --------------------------------------------------

class KnowledgeBase:
    def __init__(self, path="./memory/knowledge_base"):
        """
        Khởi tạo KnowledgeBase. 
        Nó sẽ tự động tải VectorStore nếu đã tồn tại.
        """
        self.store = VectorStore(path)
        print(f"Khởi tạo KnowledgeBase tại: {path}")

    def ingest_from_directory(self, directory_path: str = "./data"):
        """
        Tự động tìm, tải, cắt và nạp tài liệu từ một thư mục (ví dụ: './data').
        Đây là cách "chuẩn" để nạp data cho agent.
        """
        # 1. Kiểm tra thư mục
        if not os.path.exists(directory_path):
            print(f"Lỗi: Thư mục '{directory_path}' không tồn tại.")
            os.makedirs(directory_path)
            print(f"Đã tạo thư mục '{directory_path}'. Vui lòng thêm tài liệu vào đó.")
            return

        print(f"--- Bắt đầu nạp kiến thức nền từ: {directory_path} ---")

        print("Đang khởi tạo Loaders...")
        
        # 1. Khởi tạo Loader cho PDF (Globbing cho file .pdf)
        pdf_loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",  
            loader_cls=PyPDFLoader, # Sử dụng PyPDFLoader (hoặc UnstructuredFileLoader nếu có)
            recursive=True
        )

        # 2. Khởi tạo Loader cho TXT (Globbing cho file .txt)
        txt_loader = DirectoryLoader(
            directory_path,
            glob="**/*.txt", 
            loader_cls=TextLoader, 
            recursive=True
        )

        # 3. Hợp nhất kết quả tải (Load)
        try:
            print("Đang tải file PDF...")
            pdf_docs = pdf_loader.load()
            print("Đang tải file TXT...")
            txt_docs = txt_loader.load()
            
            documents = pdf_docs + txt_docs
            
        except Exception as e:
            print(f"Lỗi khi tải tài liệu: {e}")
            return

        if not documents:
            print(f"Không tìm thấy tài liệu nào trong '{directory_path}'.")
            return

        # 3. Cắt tài liệu
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"Đã chia {len(documents)} tài liệu thành {len(texts)} chunks văn bản.")

        # 4. Chuyển đổi Document (LangChain) thành list[str]
        # (Vì VectorStore tùy chỉnh của chúng ta chỉ nhận list[str])
        string_texts = [doc.page_content for doc in texts]

        # 5. Thêm logic batch để tránh lỗi quá tải bộ nhớ
        print(f"Adding {len(string_texts)} valid chunks to VectorStore in batches...")
        
        if not string_texts:
            print("WARNING: No valid chunks were generated after filtering. VectorStore remains empty.")
            return

        # 5. THÊM LOGIC CHIA BATCH TẠI ĐÂY
        BATCH_SIZE = 2000 # Chọn một batch size an toàn (dưới 5461)
        
        for i in range(0, len(string_texts), BATCH_SIZE):
            batch = string_texts[i:i + BATCH_SIZE]
            
            # 5.1. Thêm Batch hiện tại vào VectorStore
            self.store.add(batch) # Gọi add cho từng lô nhỏ
            
            print(f"INFO: Added batch {i//BATCH_SIZE + 1} / {len(batch)} chunks.")

        # self.store.add() đã tự gọi persist(), không cần gọi thêm
        # LOẠI BỎ CÁC DÒNG CODE CŨ XỬ LÝ ADD/PERSIST Ở DƯỚI ĐÂY
        
        print(f"✅ Ingestion successful. Total chunks added: {len(string_texts)}")

    def query(self, question: str) -> List[str]:
        """
        Truy vấn kiến thức nền và chỉ trả về nội dung văn bản.
        """
        results = self.store.search(question)
        # Chỉ trả về văn bản, bỏ qua điểm số (score)
        return [text for text, score in results]