


from openai import OpenAI

class Conversation:
    def __init__(self, provider: OpenAI, system_prompt=None):
        self.provider = provider
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def send_message(self, message):
        self.history.append({"role":"user", "content":message})
        botMessage =  self.provider.chat.completions.create(model="gpt-4.1-nano", messages=self.history)
        content = botMessage.choices[0].message.content
        self.history.append({"role": "assistant", "content": content})
        return content
    
    def clear(self):
        self.history = []
        
    def get_history(self):
        return self.history