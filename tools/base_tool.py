# tools/base_tool.py
from abc import ABC, abstractmethod

class BaseTool(ABC):
    name: str = "base_tool"
    description: str = "Abstract base class for all tools"

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
