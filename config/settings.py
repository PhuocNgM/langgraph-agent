# config/settings.py

import os
from dotenv import load_dotenv

# Nếu muốn hỗ trợ .env thì bật dòng này
load_dotenv()

class Settings:
    # LLM Config
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai / local / ollama
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    # Environment Mode
    ENV = os.getenv("APP_ENV", "development")  # development / production

    # Tool Flags - giúp bật/tắt nhanh các module
    ENABLE_CALENDAR_TOOL = True
    ENABLE_BROWSER_TOOL = False  # để bật sau khi cài selenium hoặc playwright

    # Memory Settings
    MEMORY_MODE = "in_memory"  # in_memory / vector
    VECTOR_STORE_PATH = "./memory/vector_db"

    # Debug mode
    DEBUG = True

settings = Settings()
