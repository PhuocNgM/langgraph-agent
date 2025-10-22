# tools/calendar_tool.py
from datetime import datetime
from .base_tool import BaseTool

class CalendarTool(BaseTool):
    name = "calendar_tool"
    description = "Quản lý các sự kiện lịch trong phiên làm việc"

    def __init__(self):
        self.events = []

    def run(self, command: str, **kwargs):
        if command == "add":
            event = {
                "title": kwargs.get("title"),
                "time": kwargs.get("time", datetime.now().isoformat())
            }
            self.events.append(event)
            return f"Đã thêm sự kiện: {event['title']} lúc {event['time']}"
        elif command == "list":
            return "\n".join([f"{e['title']} - {e['time']}" for e in self.events]) or "Không có sự kiện nào"
