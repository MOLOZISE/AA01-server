# app/workflow.py

import requests
from langgraph.graph import StateGraph, END
from app.tools.tool_manager import tool_manager
from app.agent.planner_node import planner_node
from app.agent.retrieval_node import retrieval_node

from typing import TypedDict, List, Dict, Any

# LM Studio API 설정
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "deepseek-r1-distill-qwen-7b"  # 네가 사용 중인 모델 이름

# 대화 State 정의
class ChatState(TypedDict, total=False):
    input: str
    tasks: List[Dict[str, Any]]
    results: List[str]
    related_docs: List[str]
    final_response: str

# Executor: Tool 실행
def executor(state: ChatState) -> ChatState:
    tasks = state.get("tasks", [])
    results = []

    for task in tasks:
        tool_name = task.get("tool_name")
        input_data = task.get("input")

        try:
            tool_func = tool_manager.get_tool(tool_name)
            result = tool_func.invoke(input_data)  # ✅ 최신 방식
            results.append(result)
        except Exception as e:
            results.append(f"[Tool Error] {str(e)}")

    return {
        **state,
        "results": results,
    }

# FinalResponse: LM Studio로 최종 답변 생성
async def final_response_node(state: ChatState) -> ChatState:
    combined_text = "\n".join(state.get("results", []))
    related_context = "\n".join(state.get("related_docs", [])) if state.get("related_docs") else ""

    prompt = "다음 문맥을 참고해서 사용자의 질문에 대답해줘.\n\n"
    if related_context:
        prompt += f"[참고 문서]\n{related_context}\n\n"
    prompt += f"[Task 결과]\n{combined_text}"

    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "당신은 작업 결과와 참고 문서를 바탕으로 사용자의 질문에 친절하게 답변하는 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(LM_STUDIO_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        reply = result['choices'][0]['message']['content']

    except Exception as e:
        print(f"[FinalResponse Error] {e}")
        reply = "최종 답변 생성에 실패했습니다."

    return {
        **state,
        "final_response": reply
    }

# Workflow 정의
def create_workflow():
    workflow = StateGraph(ChatState)

    workflow.add_node("Planner", planner_node)
    workflow.add_node("Executor", executor)
    workflow.add_node("Retriever", retrieval_node)
    workflow.add_node("FinalResponse", final_response_node)

    workflow.set_entry_point("Planner")
    workflow.add_edge("Planner", "Executor")
    workflow.add_edge("Executor", "Retriever")
    workflow.add_edge("Retriever", "FinalResponse")
    workflow.add_edge("FinalResponse", END)

    return workflow.compile()
