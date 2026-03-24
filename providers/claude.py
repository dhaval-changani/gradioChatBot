
from openai import OpenAI
from config import Config

def claude_provider(config: Config):
    return OpenAI(api_key=config.api_key, base_url="https://api.anthropic.com/v1/",)