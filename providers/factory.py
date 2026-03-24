
from config import Config


class ChatClient:
    
    def __init__(self, config: Config) -> None:
        self.config = config
    
    def get_client(self):
        config = self.config
        provider = config.provider.lower()
        if provider == "openai":
            from providers.openai import openai_provider
            return openai_provider(config)
        elif provider == "ollama":
            from providers.ollama import ollama_provider
            return ollama_provider(config)
        elif provider == "claude":
            from providers.claude import claude_provider
            return claude_provider(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
        
