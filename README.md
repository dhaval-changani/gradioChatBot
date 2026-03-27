# gradioChatBot

A Python chatbot with two interfaces: a CLI and a Gradio web UI. Supports multiple LLM providers (OpenAI, Ollama, Claude) via the OpenAI-compatible API.

## Project Structure

```
gradioChatBot/
├── cli.py              # Click-based CLI entrypoint
├── config.py           # Configuration (API key, temperature, max_tokens, provider)
├── conversation.py     # Conversation history and message management
├── gradioDemo.py       # Gradio web UI chatbot
├── providers/
│   ├── factory.py      # Provider factory (selects client based on config)
│   ├── openai.py       # OpenAI provider
│   ├── ollama.py       # Ollama provider (local, OpenAI-compatible)
│   └── claude.py       # Claude provider (Anthropic, OpenAI-compatible endpoint)
└── pyproject.toml
```

## Setup

1. Install dependencies:
   ```bash
   pip install openai click gradio python-dotenv
   ```

2. Create a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### CLI

```bash
python cli.py [OPTIONS]
```

Options:
| Option | Description |
|---|---|
| `--api_key` | API key (overrides `OPENAI_API_KEY` env var) |
| `--provider` | Provider: `openai`, `ollama`, or `claude` |
| `--temperature` | Sampling temperature |
| `--max_tokens` | Max tokens in response |
| `--model` | Update the model which should be used to chat with Ai |

Example:
```bash
python cli.py --provider openai
```

**CLI commands during chat:**
- Type a message and press Enter to chat
- `clear` — clear conversation history
- `exit` or `quit` — exit the chatbot

### Gradio Web UI

```bash
python gradioDemo.py
```

Opens a browser-based chat interface ("Private Concierge") powered by OpenAI.

## Providers

| Provider | Notes |
|---|---|
| `openai` | Requires `OPENAI_API_KEY` |
| `ollama` | Local inference at `http://localhost:11434`; no API key needed |
| `claude` | Uses Anthropic's OpenAI-compatible endpoint; requires Anthropic API key |
