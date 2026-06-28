# Aushu AI Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Discord](https://img.shields.io/badge/chat-discord-7289da.svg)](https://discord.gg/aushu)
[![GitHub stars](https://img.shields.io/github/stars/muhammadumar321/AushuAIAgent?style=social)](https://github.com/muhammadumar321/AushuAIAgent)

**Aushu** is a local-first, open-source developer AI agent built to compete with OpenCode, Cursor, and Codex. It combines a lightweight CLI, extensible LLM provider adapters, and a polished browser chat interface — all running on your machine, under your control.

---

## Why Aushu?

Most AI coding tools lock you into their cloud, their models, and their pricing. Aushu is different:

- **Local-first** — Run models via Ollama, self-hosted LLMs, or your preferred provider. Your code never leaves your machine.
- **Open source** — MIT licensed. Fork it, extend it, trust it.
- **Provider agnostic** — Swap between Ollama, OpenAI, and future providers with a single flag.
- **Developer UX** — CLI-first with a beautiful WhatsApp-style browser UI for chat workflows.
- **Cross-platform** — Linux, macOS, and Windows.

## Quick start

```bash
make setup
```

Or without `make`:

```bash
python bootstrap.py
source .venv/bin/activate
```

Then run:

```bash
agent providers          # list available LLM providers
agent run "Hello world" --llm --provider ollama --model qwen2.5-coder:7b
```

**Platform-specific installers:**

| Platform | Command |
|----------|---------|
| Linux / macOS | `./install.sh` or `python bootstrap.py` |
| Windows (PowerShell) | `.\bootstrap.ps1` |
| Windows (CMD) | `bootstrap.cmd` |

## Features

- **LLM Provider Adapters** — Pluggable architecture supporting Ollama, OpenAI, and custom providers
- **CLI Agent** — Fast command-line interface for prompt execution and model management
- **Browser UI** — WhatsApp-style chat interface running locally on `http://127.0.0.1:8000`
- **Model Discovery** — Auto-detect available models from connected providers
- **Provider Health** — Real-time provider status and model availability checks
- **Permission System** — Configurable safety layer for agent actions
- **Extensible** — Add new providers, tools, and workflows without changing core

## Packages

```
packages/
├── ai/           — LLM provider adapters, model discovery, unified completion client
├── core/         — Agent runtime, CLI, config management, developer workflows
├── permissions/  — Permission configuration and enforcement for safer agent actions
├── tui/          — Terminal UI scaffold for console-first workflows
└── web-ui/       — Lightweight browser chat UI with provider controls
```

## Running tests

```bash
python -m unittest discover -s packages -p 'test_*.py' -v
```

## Local browser UI

```bash
python packages/web-ui/server.py
# then open http://127.0.0.1:8000
```

Or via `make`:

```bash
make web
```

## Roadmap

- [x] CLI agent with provider discovery
- [x] Ollama and OpenAI provider support
- [x] Browser chat UI
- [x] Permission system
- [ ] Codebase indexing and context-aware completions
- [ ] File editing and code generation tools
- [ ] Multi-agent orchestration
- [ ] VS Code extension
- [ ] Plugin system for community providers

## Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

- 🐛 Found a bug? [Open an issue](https://github.com/muhammadumar321/AushuAIAgent/issues)
- 💡 Have an idea? Start a [discussion](https://github.com/muhammadumar321/AushuAIAgent/discussions)
- 🚀 Want to contribute? Check our [good first issues](https://github.com/muhammadumar321/AushuAIAgent/labels/good%20first%20issue)

## Community

- [Discord](https://discord.gg/aushu) — Chat with the team and other contributors
- [Twitter / X](https://x.com/aushu_ai) — Follow for updates
- [Blog](https://aushu.ai/blog) — Deep dives and release notes

## License

[MIT](LICENSE) — free to use, modify, and distribute.
