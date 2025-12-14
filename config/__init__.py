# config/__init__.py

from .settings import settings
from .loader import load_prompt_config

# Load YAML prompt config on import
prompt_config = load_prompt_config()

__all__ = ["settings", "prompt_config"]
