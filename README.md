# gradioChatBot

A Python chatbot with two interfaces: a CLI and a Gradio web UI. Supports multiple LLM providers (OpenAI, Ollama, Claude) via the OpenAI-compatible API.

## Project Structure

```
gradioChatBot/
├── cli.py              # Click-based CLI entrypoint
├── config.py           # Configuration (API key, temperature, max_tokens, provider, model)
├── conversation.py     # Conversation history, streaming, and token usage tracking
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
   pip install -e .
   ```
   Or manually:
   ```bash
   pip install gradio openai python-dotenv
   ```

2. Create a `.env` file with your API key(s):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   For Claude, use your Anthropic API key in the same variable or pass it via `--api_key`.

## Usage

### CLI

```bash
python cli.py [OPTIONS]
```

Options:
| Option | Default | Description |
|---|---|---|
| `--provider` | `openai` | Provider: `openai`, `ollama`, or `claude` |
| `--model` | `gpt-3.5-turbo` | Model name to use |
| `--api_key` | `$OPENAI_API_KEY` | API key (overrides env var) |
| `--temperature` | `0.7` | Sampling temperature (0.0–1.0) |
| `--max_tokens` | `1000` | Max tokens in response |
| `--system_prompt` | `"You are a snarky assistant."` | System prompt for the chatbot |

Example:
```bash
python cli.py --provider openai --model gpt-4o
python cli.py --provider ollama --model llama3
python cli.py --provider claude --api_key YOUR_ANTHROPIC_KEY --model claude-sonnet-4-6
```

**CLI commands during chat:**
- Type a message and press Enter to chat
- `clear` — clear conversation history
- `exit` or `quit` — exit the chatbot

### Gradio Web UI

```bash
python gradioDemo.py
```

Opens a browser-based chat interface. Features:
- Select provider (`openai`, `ollama`, `claude`) and load available models dynamically
- Enter API key, configure temperature and max tokens
- Set a custom system prompt before starting the conversation
- Streaming responses
- Token usage tracking (click "Show Token Usage")
- Export chat history as **Markdown** or **JSON**

## Providers

| Provider | Default Model | Notes |
|---|---|---|
| `openai` | `gpt-3.5-turbo` | Requires `OPENAI_API_KEY` |
| `ollama` | *(any local model)* | Local inference at `http://localhost:11434`; no API key needed |
| `claude` | *(any Anthropic model)* | Uses Anthropic's OpenAI-compatible endpoint; requires Anthropic API key |

## Features

- **Streaming responses** — both CLI and web UI stream tokens in real time
- **Token usage tracking** — cumulative token count displayed in the Gradio UI
- **Editable system prompt** — set before starting a conversation in the web UI or via `--system_prompt` in CLI
- **Chat export** — download conversation history as Markdown or JSON from the web UI
- **Dynamic model loading** — load available models from your chosen provider with one click
