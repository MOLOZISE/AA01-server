# app/tools/tool_manager.py

from typing import Callable, Dict
from app.tools.weather_tool import get_weather_info
from app.tools.summary_tool import summarize_text

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func

    def get_tool(self, name: str) -> Callable:
        if name not in self.tools:
            raise ValueError(f"[ToolManager] 등록되지 않은 Tool: {name}")
        return self.tools[name]

# ✅ 전역 Tool Manager 인스턴스
tool_manager = ToolManager()

# ✅ 툴 등록
tool_manager.register_tool("weather_tool", get_weather_info)
tool_manager.register_tool("summary_tool", summarize_text)
