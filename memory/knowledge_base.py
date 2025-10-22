# memory/knowledge_base.py
from .vector_store import VectorStore

class KnowledgeBase:
    def __init__(self, path="./memory/knowledge_base"):
        self.store = VectorStore(path)

    def ingest_documents(self, docs):
        # docs là list[str]
        self.store.add(docs)
        self.store.save()

    def query(self, question: str):
        results = self.store.search(question)
        return [text for text, score in results]
