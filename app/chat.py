
import requests
from pydantic import BaseModel
from fastapi import APIRouter
from app.database.chat_db import ensure_session, save_message, load_messages

router = APIRouter()

LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

class ChatRequest(BaseModel):
    session_id: str
    user_input: str

@router.post("/api/chat")
def chat_with_llm(chat_request: ChatRequest):
    session_id = chat_request.session_id
    user_input = chat_request.user_input

    # 1. 세션 보장
    ensure_session(session_id)

    # 2. 이전 메시지 불러오기
    messages = load_messages(session_id)

    # 3. 현재 사용자 메시지 추가
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": messages
    }

    # 4. LM Studio 호출
    response = requests.post(LM_STUDIO_API_URL, json=payload)
    response.raise_for_status()

    result = response.json()
    reply = result['choices'][0]['message']['content']

    # 5. DB에 메시지 저장
    save_message(session_id, "user", user_input)
    save_message(session_id, "assistant", reply)

    return {"reply": reply}

#### ChatGPT 답변

from app.database.chat_db import (
    ensure_session,
    save_message,
    load_messages,
    list_sessions,
    delete_session,
)

# (기존 /api/chat 아래 추가)

@router.get("/api/sessions")
def get_sessions():
    return list_sessions()


import asyncio
from concurrent.futures import ThreadPoolExecutor

# 이미 있는 코드

executor = ThreadPoolExecutor()
@router.delete("/api/sessions/{session_id}")
async def remove_session(session_id: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, delete_session, session_id)
    return {"message": f"Session {session_id} deleted."}
################# 백엔드 - 세션별 메시지 불러오는 API 추가

@router.get("/api/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    messages = load_messages(session_id)
    return messages

@router.get("/api/messages/{session_id}")
async def get_session_messages(session_id: str):
    """
    특정 세션의 모든 메시지를 가져오는 API
    """
    messages = load_messages(session_id)
    return messages

from app.memory_db import delete_session

@router.delete("/api/messages/{session_id}")
async def delete_session_messages_api(session_id: str):
    """
    특정 세션의 모든 메시지를 삭제하는 API
    """
    delete_session(session_id)
    return {"message": f"Messages for session {session_id} deleted."}


class MessageRequest(BaseModel):
    session_id: str
    role: str
    content: str

@router.post("/api/messages")
async def save_session_message(message_request: MessageRequest):
    """
    특정 세션에 메시지를 저장하는 API
    """
    save_message(
        message_request.session_id,
        message_request.role,
        message_request.content
    )
    return {"message": "Message saved successfully."}

@router.get("/api/weather")
async def get_weather(city: str):
    weather = random.choice(["맑음", "흐림", "비", "눈", "번개"])
    temperature = random.randint(-5, 35)
    return {
        "city": city,
        "weather": weather,
        "temperature": temperature
    }

# 요약용 API
@router.post("/api/summarize")
async def summarize(text: str):
    # 그냥 텍스트 길이를 줄여주는 Mock
    if len(text) > 30:
        return {"summary": text[:30] + "..."}
    else:
        return {"summary": text}
