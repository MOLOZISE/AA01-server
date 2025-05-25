# app/database/memory_db.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
from typing import List
from app.database.chat_db import delete_session as delete_session_from_db  # ✅ DB 삭제 연결

router = APIRouter()

MEMORY_DIR = os.path.join(os.path.dirname(__file__), "..", "memory_storage")
os.makedirs(MEMORY_DIR, exist_ok=True)

class Message(BaseModel):
    sessionId: str
    role: str
    content: str

class MessageResponse(BaseModel):
    role: str
    content: str

# 세션 삭제 (DB + JSON)
@router.delete("/messages/{session_id}")
async def delete_session_api(session_id: str):
    try:
        # ✅ 1. DB 메시지 삭제
        delete_session_from_db(session_id)

        # ✅ 2. JSON 파일 삭제 (백업 파일)
        json_path = os.path.join(MEMORY_DIR, f"{session_id}.json")
        print(f"🔍 삭제 시도: {json_path}")
        if os.path.exists(json_path):
            os.remove(json_path)
            print(f"✅ 파일 삭제됨: {json_path}")
        else:
            print(f"⚠️ 파일 없음: {json_path}")

    except Exception as e:
        print(f"❌ 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "session deleted (db + json)"}

# 메시지 저장
@router.post("/messages")
async def save_message(message: Message):
    from app.database.chat_db import save_message as save_message_to_db
    try:
        save_message_to_db(message.sessionId, message.role, message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "saved"}

# 세션별 메시지 조회
@router.get("/messages/{session_id}", response_model=List[MessageResponse])
async def get_messages(session_id: str):
    from app.database.chat_db import load_messages
    try:
        messages = load_messages(session_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))