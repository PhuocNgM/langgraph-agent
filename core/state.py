# core/state.py
from typing import TypedDict, List, Any, Optional
from datetime import datetime

# Definition of ProgressLog 
class ProgressLog(TypedDict):
    timestamp: str
    step_name: str 
    update_key: str 
    value: Any      

# Definition of AgentState
class AgentState(TypedDict):
    trainee_name: str
    goal: str
    level: str
    input: str 
    
    progress: List[ProgressLog]

    context: Optional[str]  
    plan: Optional[str]
    reflection: Optional[str]
    memory_saved: Optional[bool]
    step_info: Optional[str] 