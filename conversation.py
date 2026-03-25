


from openai import OpenAI

class Conversation:
    def __init__(self, provider: OpenAI, system_prompt=None):
        self.provider = provider
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def send_message(self, message):
        self.history.append({"role":"user", "content":message})
        botMessage =  self.provider.chat.completions.create(model="gpt-4.1-nano", messages=self.history, stream=True)
        content = ""
        print("\nBot: ", end="", flush=True)
        for chunk in botMessage:
            if (chunk.choices[0].delta.content is not None):
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
        self.history.append({"role": "assistant", "content": content})
        return content
    
    def chatStream(self, message, history):
        self.history = history
        self.history.append({"role":"user", "content":message})
        botMessage =  self.provider.chat.completions.create(model="gpt-4.1-nano", messages=self.history, stream=True)
        partial = ""
        for chunk in botMessage:
            content = chunk.choices[0].delta.content
            if content is not None:
                partial += content
                yield partial
    
    def clear(self):
        self.history = []
        
    def get_history(self):
        return self.history