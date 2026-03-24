import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

OPENAI_API_KEY =  os.environ.get("OPENAI_API_KEY")
GPT_MODEL = "gpt-4.1-nano-2025-04-14"

client = OpenAI()

assistant = {"role": "assistant", "content": "You are a personal assistant, named Nikita, help user solve any problem they face"}

def assistant_response(message, history):
    messages=[assistant, *history, {"role": "user", "content": message}]
    print(messages)
    response = client.chat.completions.create(model=GPT_MODEL, messages=messages, stream=true)
    responseContent = response.choices[0].message.content
    return responseContent

chatBot = gr.ChatInterface(fn=assistant_response, 
                           title="Private Concierge",
                           description="Helps with anything you want!",
)

chatBot.launch()