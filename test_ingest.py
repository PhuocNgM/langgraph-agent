# Ví dụ kiểm tra trong ingest.py (hoặc script mới)

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Thay thế bằng tên file PDF cụ thể trong thư mục 'data/' của bạn
TEST_FILE_PATH = "document/D5185.pdf" 

if not os.path.exists(TEST_FILE_PATH):
    print(f"Lỗi: Không tìm thấy file kiểm tra {TEST_FILE_PATH}")
    exit()

print(f"\n--- Bắt đầu kiểm tra file {TEST_FILE_PATH} ---")

# 1. Kiểm tra Loader
try:
    loader = PyPDFLoader(TEST_FILE_PATH)
    documents = loader.load()
except Exception as e:
    print(f"❌ LỖI LỚN: Không thể tải file PDF. Nguyên nhân: {e}")
    exit()

print(f"✅ Số lượng trang/document tải được: {len(documents)}")

if not documents or not documents[0].page_content.strip():
    print("❌ LỖI: File PDF KHÔNG chứa văn bản có thể trích xuất.")
    print("   -> Nguyên nhân: File có thể là ảnh quét (scanned image) hoặc bị mã hóa.")
    exit()

# 2. Kiểm tra nội dung
print(f"Nội dung trang 1 (150 ký tự đầu):")
print("-" * 20)
print(documents[0].page_content.strip()[:150])
print("-" * 20)

# 3. Kiểm tra Splitter (Cắt)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = splitter.split_documents(documents)
print(f"✅ Số lượng chunks sau khi cắt: {len(texts)}")