from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database.chat_db import (
    ensure_session,
    save_message,
    load_messages,
    list_sessions,
    delete_session,
    save_session_summary  # ✅ 누락된 import 추가
)
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
executor = ThreadPoolExecutor()

class MessageRequest(BaseModel):
    session_id: str
    role: str
    content: str

class SummaryRequest(BaseModel):  # ✅ 요약 요청용 BaseModel 추가
    summary: str

@router.get("/sessions")
def get_sessions():
    return list_sessions()

@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, delete_session, session_id)
    return {"message": f"Session {session_id} deleted."}

@router.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    return load_messages(session_id)

@router.delete("/messages/{session_id}")
async def delete_session_messages_api(session_id: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, delete_session, session_id)
    return {"message": f"Messages for session {session_id} deleted."}

@router.post("/messages")
async def save_session_message(message_request: MessageRequest):
    save_message(
        message_request.session_id,
        message_request.role,
        message_request.content
    )
    return {"message": "Message saved successfully."}

@router.post("/sessions/{session_id}/summary")
def update_session_summary(session_id: str, request: SummaryRequest):  # ✅ BaseModel로 변경
    summary = request.summary
    if not summary:
        raise HTTPException(status_code=400, detail="Missing summary")
    save_session_summary(session_id, summary)
    return {"message": "Summary updated"}
