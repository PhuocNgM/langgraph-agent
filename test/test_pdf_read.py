# check_pdf_text.py
import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader

DATA_PATH = "document/" 

def check_extraction():
    """
    Loads all PDF files and prints the raw, extracted content to the console.
    """
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Data directory '{DATA_PATH}' not found.")
        return

    print("--- STARTING RAW PDF TEXT EXTRACTION CHECK ---")

    # Sử dụng cùng cấu hình loader như trong knowledge_base.py (chỉ cho PDF)
    pdf_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.pdf",  
        loader_cls=UnstructuredFileLoader, 
        recursive=True
    )
    
    try:
        documents = pdf_loader.load()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load PDF documents. Reason: {e}")
        return

    if not documents:
        print("WARNING: No PDF documents found to check.")
        return

    print(f"SUCCESS: Loaded {len(documents)} document(s).")
    
    # In ra nội dung thô (raw content)
    for i, doc in enumerate(documents):
        content = doc.page_content.strip()
        print("\n" + "="*50)
        print(f"FILE: {doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page_number', 'N/A')})")
        print("="*50)
        
        if len(content) < 50:
            print(f"ALERT: Content is suspiciously short or empty (Length: {len(content)}).")
        
        # In ra 1000 ký tự đầu tiên
        print(content[:1000])
        print("\n[END OF PREVIEW]")

if __name__ == "__main__":
    check_extraction()