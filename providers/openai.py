
from openai import OpenAI
from config import Config

def openai_provider(config: Config):
    return OpenAI(api_key=config.api_key)