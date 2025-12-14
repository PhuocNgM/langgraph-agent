import yaml
import os

def load_prompt_config():
    """Load prompt style configuration from YAML file."""
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.join(base_dir, "prompt_style.yaml")

    if not os.path.exists(yaml_path):
        return {}

    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)
