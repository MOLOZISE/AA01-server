from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from google import genai
import os
from dotenv import load_dotenv
import traceback
from app.database.chat_db import ensure_session, save_message, load_messages

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
router = APIRouter()

@router.post("/chat")
async def chat_with_gemini(request: Request):
    try:
        body = await request.json()
        session_id = body["session_id"]
        user_input = body["user_input"]

        ensure_session(session_id)
        messages = load_messages(session_id)
        messages.append({"role": "user", "content": user_input})

        contents = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in messages]

        response = client.models.generate_content(
            model="gemini-2.0-flash",  # ✅ 최신 안정 모델
            contents=contents,
        )

        reply = response.candidates[0].content.parts[0].text

        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", reply)

        return {"reply": reply}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import StreamingResponse

@router.post("/chat-stream")
async def chat_with_gemini_stream(request: Request):
    try:
        body = await request.json()
        session_id = body["session_id"]
        user_input = body["user_input"]

        ensure_session(session_id)
        messages = load_messages(session_id)
        messages.append({"role": "user", "content": user_input})

        contents = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in messages]

        def stream():
            try:
                response = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    contents=contents
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                traceback.print_exc()
                yield "[ERROR] Gemini stream failed.\n"

        save_message(session_id, "user", user_input)
        return StreamingResponse(stream(), media_type="text/plain")

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))