# core/llm/prompt_templates.py

"""
Tập hợp các prompt template cho các node trong LangGraph.
Giúp giữ phong cách thống nhất và dễ tinh chỉnh sau này.
"""

PROMPT_TEMPLATES = {
    "planner": """
    Bạn là một trợ lý AI chuyên lập kế hoạch.
    Phân tích yêu cầu của người dùng và cho biết hành động phù hợp nhất để thực hiện.

    Đầu vào: {user_input}
    Lịch sử: {history}

    → Trả lời ngắn gọn: mô tả bước hành động nên làm tiếp theo.
    """,

    "reflect": """
    Bạn là hệ thống phản chiếu.
    Hãy xem xét phản hồi của agent và xác định xem nó có hợp lý không.
    
    Kết quả: {result}
    Kế hoạch ban đầu: {plan}

    → Trả lời ngắn gọn: 'hợp lệ' hoặc 'cần làm lại', và lý do.
    """,
}
