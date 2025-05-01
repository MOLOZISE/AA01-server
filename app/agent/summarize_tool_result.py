# app/agent/summarize_tool_result.py
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# LLM 연결 (LM Studio 사용시 base_url 수정)
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="gpt-3.5-turbo"
)

async def summarize_tool_result(state: dict) -> dict:
    tool_messages = state.get("messages", [])

    if not tool_messages:
        return {"messages": []}

    last_tool_result = tool_messages[-1]["content"]

    prompt = [
        SystemMessage(content="너는 사용자의 이해를 돕기 위해, 결과를 한 문장으로 간결하게 요약하는 AI야."),
        HumanMessage(content=f"다음 내용을 요약해줘:\n\n{last_tool_result}")
    ]

    summary = await llm.ainvoke(prompt)

    return {
        "messages": [
            {"role": "assistant", "content": summary.content}
        ]
    }
