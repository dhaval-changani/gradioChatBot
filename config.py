import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, api_key: str, temperature: float, max_tokens: int, provider: str, model: str):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature or float(os.getenv("TEMPERATURE", 0.7))
        self.max_tokens = max_tokens or int(os.getenv("MAX_TOKENS", 150))
        self.provider = provider or os.getenv("PROVIDER", "openai")
        self.model = model or os.getenv("MODEL", "gpt-3.5-turbo")