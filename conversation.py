

from openai import OpenAI


class Conversation:
    def __init__(self, provider: OpenAI, config, system_prompt=None):
        self.provider = provider
        self.config = config
        self.history = []
        self.usage = 0
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def send_message(self, message):
        self.history.append({"role": "user", "content": message})
        botMessage = self.provider.chat.completions.create(
            model=self.config.model, messages=self.history, stream=True)
        content = ""
        print("\nBot: ", end="", flush=True)
        for chunk in botMessage:
            if (chunk.choices[0].delta.content is not None):
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
        self.history.append({"role": "assistant", "content": content})

    def chatStream(self, message, history):
        self.history = list(history)
        self.history.append({"role": "user", "content": message})
        botMessage = self.provider.chat.completions.create(
            model=self.config.model, messages=self.history, stream=True, stream_options={"include_usage": True})
        partial = ""
        for chunk in botMessage:

            # if usage chunk
            if chunk.usage is not None:
                self.usage += chunk.usage.total_tokens | 0
                print(f"\n[Usage: {self.usage} tokens]", flush=True)
                continue

            content = chunk.choices[0].delta.content
            if content is not None:
                partial += content
                yield partial

        self.history.append({"role": "assistant", "content": partial})

    def clear(self):
        self.history = []
        self.usage = 0

    def get_history(self):
        return self.history

    def get_usage(self):
        return self.usage
