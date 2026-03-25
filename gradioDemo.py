import gradio as gr
from config import Config
from providers.factory import ChatClient
from conversation import Conversation

config = Config("",0.7,500,"openai")
client = ChatClient(config).get_client()
conversation = Conversation(client, "You are a helpful Data Scientist assistant")

def assistant_response(message, history):
    yield from conversation.chatStream(message,history)

chatBot = gr.ChatInterface(fn=assistant_response, 
                           title="Data Scientist Assistant", 
                           description="Ask me anything about data science! I can help with concepts, code, and more.")

chatBot.launch()