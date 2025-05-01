import json
import os
from typing import List, Dict

MEMORY_DIR = "memory_storage"

# memory_storage 폴더 없으면 만들기
os.makedirs(MEMORY_DIR, exist_ok=True)

def _get_memory_path(session_id: str) -> str:
    return os.path.join(MEMORY_DIR, f"{session_id}.json")

def load_memory(session_id: str) -> List[Dict]:
    path = _get_memory_path(session_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(session_id: str, memory: List[Dict]):
    path = _get_memory_path(session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def append_memory(session_id: str, role: str, content: str):
    memory = load_memory(session_id)
    memory.append({"role": role, "content": content})
    save_memory(session_id, memory)
