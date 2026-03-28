# gradioChatBot — Task Tracker

## Completed

- [x] **CLI chatbot** — Click-based CLI (`cli.py`) with options for provider, API key, temperature, max tokens, and system prompt
- [x] **Conversation management** — `Conversation` class with history tracking, `clear()`, and streaming support
- [x] **Multi-provider support** — Factory pattern (`providers/factory.py`) supporting OpenAI, Ollama, and Claude
- [x] **Streaming responses** — Both CLI (prints token-by-token) and Gradio UI (yields partial text)
- [x] **Config via env vars** — `.env` support via `python-dotenv`; CLI options override env vars
- [x] **Gradio web UI** — `gradioDemo.py` with `gr.ChatInterface`, streaming, and custom title/description
- [x] **Ollama provider** — Local inference at `http://localhost:11434`, no API key required
- [x] **Claude provider** — Anthropic via OpenAI-compatible endpoint

---

## Next Tasks

### Core improvements
- [x] **Make model configurable** — Model name (`gpt-4.1-nano`) is hardcoded in `conversation.py`; expose it via `Config` and CLI `--model` option
- [x] **Fix Gradio system prompt** — `gradioDemo.py` has a hardcoded system prompt; make it configurable (env var or UI input)
- [x] **Provider support in Gradio UI** — Gradio always uses OpenAI; add provider selection to the UI or read from env
- [x] **Persist conversation across Gradio sessions** — Currently `conversation` is a global; use Gradio `State` to give each browser session its own history

### Features
- [x] **Conversation export** — Save chat history to a file (JSON or Markdown) from CLI (`save` command) or Gradio download button
- [x] **Token usage display** — Show token count / cost estimate after each response
- [x] **System prompt editor in UI** — Allow users to change the system prompt mid-session via a Gradio `Textbox`
- [ ] **Multi-turn context limit** — Trim history when it exceeds a token limit to avoid API errors on long conversations
- [ ] **Retry / error handling** — Graceful error messages when the API call fails (rate limits, network issues)

### Code quality
- [ ] **Add `.env.example`** — Template file documenting all supported env vars
- [ ] **Add `requirements.txt` or lock deps in `pyproject.toml`** — Dependencies are currently undeclared in `pyproject.toml`
- [ ] **Type hints throughout** — `conversation.py` and providers lack type annotations
- [ ] **Unit tests** — Basic tests for `Config`, `Conversation`, and the provider factory

### Stretch / advanced
- [ ] **RAG support** — Allow uploading a document and chatting with it (Gradio file upload + embedding lookup)
- [ ] **Voice input/output** — Gradio microphone input + TTS playback
- [ ] **Deployable Docker image** — `Dockerfile` + `docker-compose.yml` for one-command local setup
