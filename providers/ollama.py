
from openai import OpenAI
from config import Config

def ollama_provider(config: Config):
    return OpenAI(api_key=config.api_key, base_url="http://localhost:11434/v1/",)