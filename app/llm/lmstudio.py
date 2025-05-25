import httpx
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.database.chat_db import ensure_session, save_message, load_messages

router = APIRouter()

@router.post("/chat-stream")
async def chat_with_lmstudio_stream(request: Request):
    body = await request.json()
    session_id = body["session_id"]
    user_input = body["user_input"]

    ensure_session(session_id)
    messages = load_messages(session_id)
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": messages,
        "stream": True
    }

    async def stream_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", "http://localhost:1234/v1/chat/completions", json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line.removeprefix("data: ").strip()
                        if chunk == "[DONE]":
                            break
                        try:
                            content = eval(chunk)["choices"][0]["delta"].get("content")
                            if content:
                                yield content
                        except Exception:
                            continue

    save_message(session_id, "user", user_input)
    return StreamingResponse(stream_generator(), media_type="text/plain")

@router.post("/chat")
async def chat_with_lmstudio(request: Request):
    body = await request.json()
    session_id = body["session_id"]
    user_input = body["user_input"]

    ensure_session(session_id)
    messages = load_messages(session_id)
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": messages,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post("http://localhost:1234/v1/chat/completions", json=payload)
            reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    save_message(session_id, "user", user_input)
    save_message(session_id, "assistant", reply)
    return {"reply": reply}