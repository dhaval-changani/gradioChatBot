import json
import tempfile
import os
from datetime import datetime

import gradio as gr
from config import Config
from providers.factory import get_client
from conversation import Conversation

DEFAULT_PROVIDER = "ollama"


def export_conversation(conversation, fmt):
    """Export chat history as JSON or Markdown. Returns a temp file path for download."""
    if conversation is None:
        gr.Warning("Set up a conversation first.")
        return None
    history = conversation.get_history()
    if not history:
        gr.Warning("No messages to export yet.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if fmt == "JSON":
        content = json.dumps(history, indent=2, ensure_ascii=False)
        suffix = ".json"
    else:
        lines = [
            f"# Chat Export — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
        for msg in history:
            lines.append(f"### {msg['role'].capitalize()}\n{msg['content']}\n")
        content = "\n".join(lines)
        suffix = ".md"

    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, prefix=f"chat_{timestamp}_", mode="w", encoding="utf-8"
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


def get_model_list(provider, api_key):
    config = Config(api_key, 0.7, 1000, provider, "")
    client = get_client(config)
    models = [model.id for model in client.models.list()]
    return gr.update(choices=models, value=models[0] if models else None)


def setup_conversation(provider, api_key, model, system_prompt, temperature, max_tokens):
    config = Config(api_key, temperature, int(max_tokens), provider, model)
    client = get_client(config)
    return Conversation(client, config, system_prompt)


def assistant_response(message, history, conversation):
    if conversation is None:
        yield "Please click 'Setup Conversation' before chatting."
        return
    yield from conversation.chatStream(message, history)


def token_usage(conversation):
    print(conversation.get_history())
    return conversation.get_usage()


with gr.Blocks() as demo:
    gr.Label(
        "Setup your system prompt, select the provider and model, and start chatting!")

    with gr.Row():
        provider_input = gr.Dropdown(
            choices=["openai", "ollama", "claude"],
            label="Select Provider",
            value=DEFAULT_PROVIDER,
            interactive=True
        )
        api_key_input = gr.Textbox(
            label="API Key", placeholder="Enter your API key...")
        load_models_btn = gr.Button("Load Models")

    model_input = gr.Dropdown(
        choices=[], label="Select Model", interactive=True)

    with gr.Row():
        temperature_input = gr.Slider(
            label="Temperature", minimum=0.0, maximum=1.0, value=0.7, step=0.1)
        max_tokens_input = gr.Slider(
            label="Max Tokens", minimum=1, maximum=2048, value=1000, step=10)

    system_prompt_input = gr.Textbox(
        label="System Prompt", placeholder="Enter the system prompt...")
    setup_btn = gr.Button("Setup Conversation")

    conversation_state = gr.State()

    load_models_btn.click(
        fn=get_model_list,
        inputs=[provider_input, api_key_input],
        outputs=[model_input]
    )

    setup_btn.click(
        fn=setup_conversation,
        inputs=[provider_input, api_key_input, model_input,
                system_prompt_input, temperature_input, max_tokens_input],
        outputs=[conversation_state]
    )

    gr.ChatInterface(
        fn=assistant_response,
        additional_inputs=[conversation_state]
    )

    # show token usage
    token_usage_btn = gr.Button("Show Token Usage")
    token_usage_output = gr.Textbox(label="Token Usage", interactive=False)
    token_usage_btn.click(
        fn=token_usage,
        inputs=[conversation_state],
        outputs=[token_usage_output]
    )

    gr.Markdown("---")
    with gr.Row():
        export_format = gr.Radio(
            choices=["Markdown", "JSON"],
            value="Markdown",
            label="Export Format",
            interactive=True
        )
        export_btn = gr.Button("Export Chat", variant="secondary")

    export_file = gr.File(label="Download", visible=False)

    def handle_export(conversation, fmt):
        path = export_conversation(conversation, fmt)
        if path:
            return gr.update(value=path, visible=True)
        return gr.update(visible=False)

    export_btn.click(
        fn=handle_export,
        inputs=[conversation_state, export_format],
        outputs=[export_file]
    )

demo.launch()
