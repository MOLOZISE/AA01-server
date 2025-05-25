from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 라우터 import
from app.llm.lmstudio import router as lmstudio_router
from app.llm.gemini import router as gemini_router
from app.chat.session import router as session_router

from app.database.init_db import init_db
from app.workflow import create_workflow
from app import vectorstore
from app.database import memory_db

app = FastAPI()

# 라우터 등록
app.include_router(lmstudio_router, prefix="/api/lm")
app.include_router(gemini_router, prefix="/api/google")
app.include_router(session_router, prefix="/api")  # 공통 세션/메시지 API

# 기타 라우터
app.include_router(memory_db.router)
app.include_router(vectorstore.router)

workflow = create_workflow()

@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, Agentic AI!"}

@app.post("/api/ask")
async def ask_tool(question: str):
    inputs = {
        "messages": [{"role": "user", "content": question}],
        "invocations": []
    }
    result = await workflow.ainvoke(inputs)
    return result

@app.post("/api/run_workflow")
async def run_workflow(input_data: dict):
    input_text = input_data.get("input")
    state = {"input": input_text}

    final = None
    async for output in workflow.astream(state):
        final = output

    return {
        "response": final.get("final_response")
    }
