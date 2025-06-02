from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.llm.gemini import call_gemini  # ✅ 기존 Gemini 호출 함수 import

router = APIRouter()

# 간단한 메모리 저장소 (프로토타입용)
file_store: Dict[str, Dict[str, str]] = {}  # {filename: {"summary": ..., "content": ...}}

# 업로드된 파일 정보 형식
class FileInfo(BaseModel):
    filename: str
    summary: str  # 파일 요약 (300자 내외)
    content: str  # 전체 텍스트 (이건 optional로도 가능)

# 검색 요청 형식
class SearchRequest(BaseModel):
    query: str

@router.post("/api/files")
def upload_file_info(file: FileInfo):
    file_store[file.filename] = {
        "summary": file.summary,
        "content": file.content
    }
    return {"status": "ok", "filename": file.filename}

@router.post("/api/search-by-llm")
def search_by_llm(req: SearchRequest):
    if not file_store:
        return {"results": []}

    # 🔧 문제 표현식을 바깥으로 분리
    file_list_text = "\n".join([
        f"{i+1}. 파일명: {fname}\n요약: {info['summary']}"
        for i, (fname, info) in enumerate(file_store.items())
    ])

    prompt = f"""
당신은 문서를 매우 잘 이해하는 AI 비서입니다.
사용자가 여러 파일을 업로드했으며, 각 파일은 이름과 간단한 요약으로 설명되어 있습니다.

사용자 질문:
"{req.query}"

다음은 업로드된 파일 목록입니다:

{file_list_text}

이 중 사용자 질문과 가장 관련 있는 파일 3개를 고르고, 그 이유도 함께 설명해 주세요.

결과는 JSON 형식으로 반환해 주세요. 예:
[
  {{ "filename": "파일명", "reason": "선택 이유" }},
  ...
]
"""

    answer = call_gemini(prompt)
    return {"results": answer}


@router.post("/api/summarize")
def summarize_file(req: dict):
    content = req["content"]
    prompt = f"""
다음은 사용자가 업로드한 파일의 내용입니다.

{content[:2000]}

이 파일의 내용을 300자 이내로 간략히 요약해 주세요.
"""
    return { "summary": call_gemini(prompt) }
