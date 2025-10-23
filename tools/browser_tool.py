# tools/browser_tool.py
from .base_tool import BaseTool

class BrowserTool(BaseTool):
    name = "browser_tool"
    description = "Giả lập hành vi duyệt web cơ bản"

    def run(self, url: str):
        # Có thể dùng requests hoặc selenium
        return f"Giả lập mở trang: {url}"
