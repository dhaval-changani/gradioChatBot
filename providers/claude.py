from openai import OpenAI
from config import Config
class AnthropicClient(OpenAI):

    def __init__(self, config: Config) -> None:
        self.config = config
        super().__init__(api_key=self.config.api_key, base_url="https://api.anthropic.com/v1/",)