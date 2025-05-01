# app/tools/weather_tool.py
from langchain.tools import tool
import requests

@tool
def get_weather_info(city: str) -> str:
    """특정 도시의 현재 날씨를 검색합니다."""
    response = requests.get(f"http://localhost:8000/api/weather?city={city}")
    if response.status_code == 200:
        data = response.json()
        return f"{data['city']}의 현재 날씨는 {data['weather']}이고, 온도는 {data['temperature']}도 입니다."
    else:
        return "날씨 정보를 가져오는 데 실패했습니다."
