# tools/file_tool.py
import os
from .base_tool import BaseTool

class FileTool(BaseTool):
    name = "file_tool"
    description = "Đọc và ghi file cục bộ"

    def run(self, command: str, path: str, content: str = None):
        if command == "read":
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read()
            return "File không tồn tại"
        elif command == "write":
            with open(path, "w") as f:
                f.write(content or "")
            return f"Đã ghi nội dung vào {path}"
