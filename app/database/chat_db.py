import sqlite3
import os
from typing import List, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), "chat.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def ensure_session(session_id: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO sessions (id) VALUES (?)", (session_id,))
    conn.commit()
    conn.close()

def save_message(session_id: str, role: str, content: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def load_messages(session_id: str) -> List[Dict]:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"role": role, "content": content} for role, content in rows]


# (기존 코드 위에 추가)

def list_sessions() -> List[Dict]:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, created_at FROM sessions ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"session_id": session_id, "created_at": created_at} for session_id, created_at in rows]

def delete_session(session_id: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
