# llm/llm_client.py

import openai
from config.settings import settings

class LLMClient:
    """
    Lớp bao (wrapper) để giao tiếp với các mô hình ngôn ngữ.
    Có thể mở rộng cho local model (Ollama, v.v.)
    """

    def __init__(self, model: str = None):
        self.provider = settings.LLM_PROVIDER
        self.model = model or "gpt-4o-mini"

        if self.provider == "openai" and settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            raise ValueError(f"Unsupported or unconfigured LLM provider: {self.provider}")

    def generate(self, prompt: str) -> str:
        """Sinh phản hồi từ mô hình LLM."""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[LLM Error] {e}"
