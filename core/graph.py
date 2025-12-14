# core/graph.py
from langgraph.graph import StateGraph, END
# Note: Assuming 'retriever_node' is the function name from the import below
from core.retrieve_node import retriever_node 
from core.state import AgentState
from core.planner_node import planner_node
from core.action_node import action_node
from core.reflect_node import reflect_node
from core.memory_node import memory_node

def AgentGraph  () -> StateGraph:
    """
    Builds the LangGraph for the Agent, ensuring the RAG pipeline runs first.
    """
    graph = StateGraph(AgentState)

    # 1. Add all nodes
    graph.add_node("retriever", retriever_node)
    graph.add_node("planner", planner_node)
    graph.add_node("action", action_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("memory", memory_node)

    # 2. Define Edges (The Flow)
    # RAG must run before planning
    graph.add_edge("retriever", "action") 
    graph.add_edge("planner", "retriever")
    graph.add_edge("action", "reflect")
    graph.add_edge("reflect", "memory")
    graph.add_edge("memory", END)

    # 3. Set the Entry Point 
    graph.set_entry_point("planner") 

    return graph