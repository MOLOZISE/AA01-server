# app/agent/planner_node.py

import requests
import json
from typing import Dict, List, Any

LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_input = state.get("input", "")
    tasks = []

    prompt = [
        {
            "role": "system",
            "content": """당신은 Task Planner입니다.
사용자의 요청을 분석하고 필요한 작업만 JSON 배열로 출력하세요.
지원하는 작업:
- 요약: summary_tool
- 날씨 조회: weather_tool
- 파일 검색: vectorstore_search

오직 아래 포맷만 출력하세요:

[
  {"tool_name": "summary_tool", "input": "요약할 텍스트"},
  {"tool_name": "weather_tool", "input": "도시 이름"}
]

단순 대화면 빈 리스트([])만 반환하세요.
"""
        },
        {"role": "user", "content": user_input}
    ]

    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": prompt
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload)
        response.raise_for_status()
        if response.text.strip() == "":
            print("[Planner Error] Empty LLM response")
            tasks = []
        else:
            result = response.json()
            llm_reply = result['choices'][0]['message']['content'].strip()
            parsed_tasks = json.loads(llm_reply)
            if isinstance(parsed_tasks, list):
                tasks = parsed_tasks

    except Exception as e:
        print(f"[Planner Error] {e}")
        tasks = []

    if not tasks:
        tasks.append({
            "tool_name": "summary_tool",
            "input": user_input
        })

    return {
        **state,
        "tasks": tasks
    }
