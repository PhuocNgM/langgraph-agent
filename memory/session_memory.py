# memory/session_memory.py
from collections import deque

class SessionMemory:
    def __init__(self, max_messages: int = 10):
        self.history = deque(maxlen=max_messages)

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_context(self) -> str:
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history])

    def clear(self):
        self.history.clear()
