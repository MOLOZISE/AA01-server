# app/memory_db.py (SQLite 기반 FastAPI Router)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

router = APIRouter()

DB_PATH = "memory.sqlite"

class Message(BaseModel):
    sessionId: str
    role: str
    content: str

class MessageResponse(BaseModel):
    role: str
    content: str

# 메시지 저장
@router.post("/messages")
async def save_message(message: Message):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (message.sessionId, message.role, message.content)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"status": "saved"}

# 세션별 메시지 조회
@router.get("/messages/{session_id}", response_model=List[MessageResponse])
async def get_messages(session_id: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return [{"role": row[0], "content": row[1]} for row in rows]

# 세션 전체 삭제 (옵션)
@router.delete("/messages/{session_id}")
async def delete_session(session_id: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {"status": "session deleted"}
