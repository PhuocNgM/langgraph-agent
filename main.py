# main.py
from core.graph import AgentGraph
from core.state import AgentState # Vẫn dùng TypedDict để kiểm tra kiểu
    
from typing import Dict, Any

from dotenv import load_dotenv # <-- Import gói dotenv
import os

load_dotenv()

def main_chat():
    """
    Chạy agent trong chế độ vòng lặp chat tương tác.
    """
    
    # --- 1. Biên dịch đồ thị MỘT LẦN ---
    # Việc này chỉ cần làm một lần khi khởi động
    try:
        graph_builder = AgentGraph() 
        app = graph_builder.compile()
    except Exception as e:
        print(f"ERROR: Failed to compile graph: {e}")
        return

    print("--- 🤖 Agent is Ready. Type 'exit' to quit. ---")

    while True:
        try:
            user_message = input("Human (English Query): ")
            
            if user_message.lower() in ["exit", "quit", "stop"]:
                print("Agent: Goodbye!")
                break
            
            # ... (Tạo initial_chat_state với input = user_message) ...
            initial_chat_state: AgentState = {
                'trainee_name': 'Ngoc', 
                'goal': 'Answer/Execute user requests',
                'level': 'beginner',
                'input': user_message, 
                'progress': [],
                'plan': None,
                'reflection': None,
                'memory_saved': None,
                'step_info': None,
            }

            print("Agent: ...thinking...")
            final_state: Dict[str, Any] = app.invoke(
                initial_chat_state, 
                config={"recursion_limit": 50}
            )

            response = final_state.get('reflection', "I have finished processing, but found nothing relevant.")
            print(f"Agent: {response}")

        except Exception as e:
            print(f"Agent (Error): An error occurred during processing: {e}")

if __name__ == "__main__":
    main_chat()