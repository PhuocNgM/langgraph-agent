# core/graph.py
from langgraph.graph import StateGraph, END
from core.retrieve_node import retriever_node
from core.state import AgentState
from core.planner_node import planner_node
from core.action_node import action_node
from core.reflect_node import reflect_node
from core.memory_node import memory_node

def AgentGraph  () -> StateGraph:
    """
    Build graph LangGraph for agent.
    """
    graph = StateGraph(AgentState)

    # Add các node vào graph
    graph.add_node("retriever", retriever_node)
    graph.add_node("planner", planner_node)
    graph.add_node("action", action_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("memory", memory_node)

    # Định nghĩa graph
    graph.add_edge("planner", "action")
    graph.add_edge("action", "reflect")
    graph.add_edge("reflect", "memory")
    graph.add_edge("memory", END)

    # Node khởi đầu
    graph.set_entry_point("planner")

    return graph
