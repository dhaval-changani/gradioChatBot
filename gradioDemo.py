import gradio as gr
from config import Config
from providers.factory import get_client
from conversation import Conversation


def get_model_list(provider, api_key):
    config = Config(api_key, 0.7, 1000, provider, "")
    client = get_client(config)
    models = [model.id for model in client.models.list()]
    return gr.update(choices=models, value=models[0] if models else None)


def setup_conversation(provider, api_key, model, system_prompt, temperature, max_tokens):
    config = Config(api_key, temperature, int(max_tokens), provider, model)
    client = get_client(config)
    return Conversation(client, system_prompt)


def assistant_response(message, history, conversation):
    if conversation is None:
        yield "Please click 'Setup Conversation' before chatting."
        return
    yield from conversation.chatStream(message, history)


with gr.Blocks() as demo:
    gr.Label("Setup your system prompt, select the provider and model, and start chatting!")

    with gr.Row():
        provider_input = gr.Dropdown(
            choices=["openai", "ollama", "claude"],
            label="Select Provider",
            value="openai",
            interactive=True
        )
        api_key_input = gr.Textbox(label="API Key", placeholder="Enter your API key...")
        load_models_btn = gr.Button("Load Models")

    model_input = gr.Dropdown(choices=[], label="Select Model", interactive=True)

    with gr.Row():
        temperature_input = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, value=0.7, step=0.1)
        max_tokens_input = gr.Slider(label="Max Tokens", minimum=1, maximum=2048, value=1000, step=1)

    system_prompt_input = gr.Textbox(label="System Prompt", placeholder="Enter the system prompt...")
    setup_btn = gr.Button("Setup Conversation")

    conversation_state = gr.State()

    load_models_btn.click(
        fn=get_model_list,
        inputs=[provider_input, api_key_input],
        outputs=[model_input]
    )

    setup_btn.click(
        fn=setup_conversation,
        inputs=[provider_input, api_key_input, model_input, system_prompt_input, temperature_input, max_tokens_input],
        outputs=[conversation_state]
    )

    gr.ChatInterface(
        fn=assistant_response,
        additional_inputs=[conversation_state]
    )

demo.launch()
