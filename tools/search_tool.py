# tools/search_tool.py
import requests
from .base_tool import BaseTool

class SearchTool(BaseTool):
    name = "search_tool"
    description = "Tìm kiếm thông tin trên web"

    def run(self, query: str):
        return f"Kết quả giả lập cho truy vấn: {query}"
        # Sau này có thể tích hợp thật bằng API hoặc web scraper
