# app/tools/summary_tool.py
from langchain.tools import tool
import requests

@tool
def summarize_text(text: str) -> str:
    """주어진 텍스트를 요약합니다."""
    try:
        response = requests.post("http://localhost:8000/api/summarize", params={"text": text})
        response.raise_for_status()
        data = response.json()
        return data["summary"]
    except Exception as e:
        return f"요약 요청 실패: {e}"
