# main.py
from core.graph import AgentGraph
from core.state import AgentState # Vẫn dùng TypedDict để kiểm tra kiểu
from typing import Dict, Any

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
        print(f"Lỗi nghiêm trọng khi biên dịch graph: {e}")
        return

    print("--- 🤖 Agent đã sẵn sàng. Gõ 'exit' để thoát. ---")

    # --- 2. Bắt đầu vòng lặp chat ---
    while True:
        try:
            # Lấy input từ người dùng
            user_message = input("Human: ")
            
            if user_message.lower() in ["exit", "quit", "stop", "nghỉ"]:
                print("Agent: Tạm biệt!")
                break
            
            if not user_message.strip():
                continue

            # --- 3. Tạo State MỚI cho tin nhắn này ---
            # Sử dụng tin nhắn của bạn làm 'input'
            # Các giá trị khác có thể giữ làm mặc định
            initial_chat_state: AgentState = {
                'trainee_name': 'Ngọc', # Vẫn giữ ngữ cảnh mặc định
                'goal': 'Trả lời/Thực hiện yêu cầu của người dùng',
                'level': 'beginner',
                'input': user_message, # <--- ĐÂY LÀ ĐIỂM QUAN TRỌNG
                'progress': [],
                'plan': None,
                'reflection': None,
                'memory_saved': None,
                'step_info': None,
            }

            # --- 4. Chạy graph (Dùng .invoke cho nhanh) ---
            # .invoke() sẽ chạy toàn bộ graph và trả về trạng thái CUỐI CÙNG
            print("Agent: ...đang suy nghĩ...")
            final_state: Dict[str, Any] = app.invoke(
                initial_chat_state, 
                config={"recursion_limit": 50}
            )

            # --- 5. In ra câu trả lời ---
            # Chúng ta giả định 'reflection' là câu trả lời cuối cùng
            response = final_state.get('reflection', "Tôi đã xử lý xong, nhưng không có gì để nói.")
            print(f"Agent: {response}")

        except KeyboardInterrupt:
            print("\nAgent: Tạm biệt!")
            break
        except Exception as e:
            print(f"Agent (Lỗi): Đã xảy ra lỗi khi xử lý: {e}")
            # Vòng lặp vẫn tiếp tục

if __name__ == "__main__":
    main_chat() # Gọi hàm chat mới