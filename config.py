import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, api_key: str, temperature: float, max_tokens: int, provider: str, model: str):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature or 0.7
        self.max_tokens = max_tokens or 1000
        self.provider = provider or 'openai'
        self.model = model or 'gpt-3.5-turbo'
