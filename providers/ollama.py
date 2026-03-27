from openai import OpenAI
from config import Config


class OllamaClient(OpenAI):

    def __init__(self, config: Config) -> None:
        self.config = config
        super().__init__(api_key=self.config.api_key, base_url="http://localhost:11434/v1/")
