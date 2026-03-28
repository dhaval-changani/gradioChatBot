

from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class Conversation:
    def __init__(self, provider: OpenAI, config, system_prompt="You are a helpful assistant"):
        self.provider = provider
        self.config = config
        self.history = [
            {"role": "system", "content": system_prompt}]
        self.usage = 0
        self.system_prompt = system_prompt

    def send_message(self, message):
        self.history.append({"role": "user", "content": message})

        botMessage = self.provider.chat.completions.create(
            model=self.config.model, messages=cast(list[ChatCompletionMessageParam], self.history), stream=True)
        content = ""
        print("\nBot: ", end="", flush=True)
        for chunk in botMessage:
            if (chunk.choices[0].delta.content is not None):
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
        self.history.append({"role": "assistant", "content": content})

    def chatStream(self, message, history):
        self.history = list(history)

        # remove system prompt is already exists
        if self.system_prompt is not None and len(self.history) > 0:

            first_message = self.history[0]
            if first_message["role"] == "system":
                self.history.pop(0)

            self.history.insert(
                0, {"role": "system", "content": self.system_prompt})

        self.history.append({"role": "user", "content": message})

        botMessage = self.provider.chat.completions.create(
            model=self.config.model, messages=cast(list[ChatCompletionMessageParam], self.history), stream=True, stream_options={"include_usage": True})

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
        print(self.history)  # for newline after bot response

    def clear(self):
        self.history = []
        self.usage = 0

    def get_history(self):
        return self.history

    def get_usage(self):
        return self.usage
