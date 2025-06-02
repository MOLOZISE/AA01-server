@router.post("/api/summarize")
def summarize_file(req: dict):
    content = req["content"]
    prompt = f"""
다음은 사용자가 업로드한 파일의 내용입니다.

{text[:2000]}

이 파일의 내용을 300자 이내로 간략히 요약해 주세요.
"""
    return { "summary": call_gemini(prompt) }