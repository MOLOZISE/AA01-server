# app/agent/retrieval_node.py

from typing import Dict, Any
from app.vector_db.manager import vector_store

async def retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_input = state.get("input", "")
    related_docs = vector_store.similarity_search(user_input, top_k=3)


    return {
        **state,
        "related_docs": related_docs  # 검색된 문서를 상태에 추가
    }
