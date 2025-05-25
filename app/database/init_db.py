import sqlite3
import os

# 항상 현재 파일 위치 기준으로 고정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 세션 테이블 (summary 컬럼 추가됨)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        summary TEXT
    )
    """)

    # 메시지 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ DB 초기화 완료: sessions(summary 포함), messages 테이블")

if __name__ == "__main__":
    init_db()
