
import click
from config import Config
from providers.factory import ChatClient
from conversation import Conversation

@click.command()
@click.option('--api_key',)
@click.option('--temperature',)
@click.option('--max_tokens',)
@click.option('--provider',)
@click.option('--system_prompt', default="You are a snarky assistant.", help='System prompt for the chatbot.')
def chatbot(api_key, temperature, max_tokens, provider, system_prompt):
    config = Config(api_key, temperature, max_tokens, provider)
    client = ChatClient(config).get_client()
    conversation = Conversation(client, system_prompt)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nExiting chatbot. Goodbye!\n")
            break
        
        if (user_input.lower() == "clear"):
            conversation.clear()
            print("\nConversation history cleared.\n")
            continue
                    
        conversation.send_message(user_input)

if __name__ == "__main__":
    chatbot()