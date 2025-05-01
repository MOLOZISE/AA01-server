# app/vector_db/vector_store.py

import chromadb

class VectorStoreManager:
    def __init__(self):
        # ✅ New client 방식
        self.client = chromadb.Client()

        # collection 가져오기 (없으면 생성)
        self.collection = self.client.get_or_create_collection(name="agentic-memory")

    def add_document(self, doc_id: str, content: str):
        self.collection.add(documents=[content], ids=[doc_id])

    def similarity_search(self, query: str, top_k: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results
