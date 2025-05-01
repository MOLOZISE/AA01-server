# # app/agent/llm_node.py

# import requests
# from langgraph.prebuilt import ToolInvocation

# LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# async def llm_node(state: dict) -> dict:
#     messages = state.get("messages", [])

#     if not messages:
#         return {}

#     user_message = messages[-1]

#     chat_history = [
#         {"role": "system", "content": "너는 사용자의 요청에 따라 여러 도구를 호출할 수 있는 AI야. '날씨'라는 단어가 들어있으면 search_weather를 호출하고, '요약'이라는 단어가 들어있으면 summarize_text를 호출해."},
#         {"role": "user", "content": user_message["content"]}
#     ]

#     payload = {
#         "model": "deepseek-r1-distill-qwen-7b",  # LM Studio에서 사용하는 모델명
#         "messages": chat_history
#     }

#     response = requests.post(LM_STUDIO_API_URL, json=payload)
#     response.raise_for_status()
#     result = response.json()
#     llm_reply = result['choices'][0]['message']['content']

#     invocations = []

#     if "날씨" in user_message["content"]:
#         city_name = user_message["content"].replace("날씨 알려줘", "").strip()
#         invocations.append(
#             ToolInvocation(
#                 tool_name="search_weather",
#                 input={"city": city_name}
#             )
#         )

#     if "요약" in user_message["content"]:
#         text_to_summarize = user_message["content"]
#         invocations.append(
#             ToolInvocation(
#                 tool_name="summarize_text",
#                 input={"text": text_to_summarize}
#             )
#         )

#     if invocations:
#         return {
#             "invocations": invocations,
#             "messages": []
#         }
#     else:
#         return {
#             "messages": [{"role": "assistant", "content": llm_reply}]
#         }
