# core/state.py
from typing import Dict, Any

class AgentState:
    """
    Lightweight state manager for LangGraph flow.
    It wraps a dict but allows attribute-style access.
    """
    def __init__(self, initial_state: Dict[str, Any] = None):
        self._state = initial_state or {}

    def get(self, key: str, default=None):
        return self._state.get(key, default)

    def set(self, key: str, value: Any):
        self._state[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return self._state

    def __getitem__(self, key: str):
        return self._state[key]

    def __setitem__(self, key: str, value: Any):
        self._state[key] = value

    def __contains__(self, key: str):
        return key in self._state

    def __repr__(self):
        return f"AgentState({self._state})"
