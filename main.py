from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import chat
from app import memory_db  # ⭐ 추가
from app.workflow import create_workflow  # ⭐ 추가   
from app import vectorstore  # ✅ 추가



from app import chat
from app.database.init_db import init_db  # ⭐ 추가

app = FastAPI()

app.include_router(chat.router)
app.include_router(memory_db.router)  # ⭐ 추가

workflow = create_workflow()  # ⭐ 추가

# ⭐ 앱 시작할 때 DB 초기화
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

app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Hello, Agentic AI!"}


# 신규 워크플로우 기반 /api/ask API 추가
@app.post("/api/ask")
async def ask_tool(question: str):
    inputs = {
        "messages": [{"role": "user", "content": question}],
        "invocations": []
    }
    result = await workflow.ainvoke(inputs)
    return result

from app.workflow import create_workflow

workflow = create_workflow()  # 새 워크플로우 생성!

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


app.include_router(vectorstore.router)
