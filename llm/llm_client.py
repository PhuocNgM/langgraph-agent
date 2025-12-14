# llm/llm_client.py

import openai
# Explicitly import the client object from the modern SDK
from openai import OpenAI 
from config.settings import settings

class LLMClient:
    """
    Wrapper class for communicating with Large Language Models.
    Uses the modern OpenAI client object for thread-safety and robustness.
    """

    def __init__(self, model: str = None):
        self.provider = settings.LLM_PROVIDER
        self.model = model or "gpt-4o-mini"
        self.client = None # Initialize client object

        if self.provider == "openai":
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing or empty in configuration.")
            
            # Instantiate the modern OpenAI client object, passing the API key directly
            self.client = OpenAI(api_key=api_key)
            
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(self, prompt: str) -> str:
        """Generates a response from the LLM model."""
        
        if not self.client:
             return "[LLM Error] Client is not initialized."
             
        try:
            # Use the instantiated client object to call the API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Ensure proper error handling, as this is a wrapper
            return f"[LLM Error] {e}"


# Utility function outside the class
def call_llm(prompt: str) -> str:
    """Convenience function to quickly call the LLM (maintaining compatibility)."""
    client = LLMClient()
    return client.generate(prompt)