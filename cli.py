
import click
from config import Config
from providers.factory import ChatClient
from conversation import Conversation

@click.command()
@click.option('--api_key',)
@click.option('--temperature',)
@click.option('--max_tokens',)
@click.option('--provider',)
def chatbot(api_key, temperature, max_tokens, provider):
    config = Config(api_key, temperature, max_tokens, provider)
    client = ChatClient(config).get_client()
    conversation = Conversation(client)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nExiting chatbot. Goodbye!\n")
            break
        
        if (user_input.lower() == "clear"):
            conversation.clear()
            print("\nConversation history cleared.\n")
            continue
                    
        response = conversation.send_message(user_input)
        
        print(f"\nBot: {response}\n")

if __name__ == "__main__":
    chatbot()