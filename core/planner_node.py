# core/planner_node.py

from core.state import AgentState
from langgraph.types import NodeOutput
from typing import Dict
from llm.llm_client import LLMClient
from llm.prompt_templates import PROMPT_TEMPLATES

def planner_node(state: AgentState):
    """
    Sinh kế hoạch hành động (plan) dựa trên input từ người dùng.
    """
    user_input = state.get("input")
    if not user_input:
        return {"error": "Không có input để lập kế hoạch."}

    llm = LLMClient()

    # Gọi LLM với prompt
    prompt = PROMPT_TEMPLATES.format(user_input=user_input)
    plan = llm.generate(prompt)

    # Cập nhật state
    state.set("plan", plan)
    return {"plan": plan}


# [planner_node] → [action_node] → [reflect_node] → [memory_node] → END
