
from config import Config


def get_client(config: Config):
    provider = config.provider.lower()
    if provider == "ollama":
        from providers.ollama import OllamaClient
        return OllamaClient(config)
    elif provider == "claude":
        from providers.claude import AnthropicClient
        return AnthropicClient(config)
    else:
        from providers.openai import OpenAIClient
        return OpenAIClient(config)