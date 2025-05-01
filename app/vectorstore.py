# app/api/vectorstore.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.vector_db.manager import vector_store

router = APIRouter()

class AddDocumentRequest(BaseModel):
    doc_id: str
    content: str

@router.post("/api/vectorstore/add")
async def add_document(req: AddDocumentRequest):
    vector_store.add_document(req.doc_id, req.content)
    vector_store.persist()
    return {"message": "Document added to vector store."}
