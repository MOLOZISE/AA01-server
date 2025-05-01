# # app/agent/router_node.py

# import requests
# import json
# from langgraph.prebuilt import ToolInvocation

# LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# async def router_node(state: dict) -> dict:
#     messages = state.get("messages", [])
#     if not messages:
#         return {}

#     user_message = messages[-1]

#     prompt = [
#         {
#             "role": "system",
#             "content": """사용자의 요청을 분석하여 호출해야 할 도구를 선택하세요.

# - 날씨 관련 질문: search_weather
# - 텍스트 요약 요청: summarize_text
# - 파일 기반 검색 요청: vectorstore_search
# - 아무것도 해당되지 않으면: none

# 다음 JSON 형태로만 답변하세요:
# {"tool": "도구명", "args": {키:값}}"""
#         },
#         {"role": "user", "content": user_message["content"]}
#     ]

#     payload = {
#         "model": "deepseek-r1-distill-qwen-7b",  # LM Studio 모델명
#         "messages": prompt
#     }

#     response = requests.post(LM_STUDIO_API_URL, json=payload)
#     response.raise_for_status()
#     result = response.json()
#     llm_reply = result['choices'][0]['message']['content']

#     try:
#         parsed = json.loads(llm_reply)
#         tool = parsed.get("tool")
#         args = parsed.get("args", {})

#         if tool and tool != "none":
#             return {
#                 "invocations": [
#                     ToolInvocation(
#                         tool_name=tool,
#                         input=args
#                     )
#                 ],
#                 "messages": []
#             }
#         else:
#             return {
#                 "messages": [{"role": "assistant", "content": "별도의 도구 호출은 필요하지 않습니다."}]
#             }
#     except Exception as e:
#         print("Router parsing error:", e)
#         return {
#             "messages": [{"role": "assistant", "content": "요청을 이해했지만 처리가 어렵습니다."}]
#         }
