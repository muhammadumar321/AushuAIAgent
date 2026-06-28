# Aushu AI Agent

Aushu is a local-first developer AI agent designed to compete with OpenCode, Cursor, and Codex. It combines a lightweight CLI, provider extensibility, and a polished browser chat interface for fast, open-source developer workflows.

## Quick start

From the repo root, run either:

```bash
make setup
```

or, if `make` is unavailable:

```bash
python bootstrap.py
```

Then activate the created virtual environment:

```bash
source .venv/bin/activate
```
Platform-specific quickstart

Linux / macOS

Run the shell installer (works on Ubuntu, Fedora, macOS):

```sh
./install.sh
# or
python bootstrap.py
```

Windows (PowerShell)

Open PowerShell and run:

```powershell
.\bootstrap.ps1
# or (if ExecutionPolicy blocks scripts):
#powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1
```

Windows (CMD)

Open Command Prompt and run:

```cmd
bootstrap.cmd
```

The Windows bootstraps will create `.venv`, install dependencies from `requirements.txt`, and install editable packages from `packages/ai`, `packages/core`, and `packages/permissions`. They will also print the command to activate the venv.

Use the CLI directly through the environment:

```bash
agent providers
```

Run the full test suite:

```bash
python -m unittest discover -s packages -p 'test_*.py' -v
```

Run a model completion with local Ollama:

```bash
python bootstrap.py
source .venv/bin/activate
agent run "Hello from Ollama" --llm --provider ollama --model qwen2.5-coder:7b
```

## Docs

- `VISION.md` — product vision, mission, and open-source positioning.
- `ONBOARDING_AI_AGENT.md` — contributor onboarding and local setup guidance.
- `CONTRIBUTING.md` — contribution rules, documentation expectations, and product vision for contributors.
- `packages/web-ui/README.md` — local browser UI usage and features.

## Product direction

Aushu is designed as a local-first developer AI agent, aimed at open-source competition with OpenCode, Cursor, and Codex. The focus is on extensible provider adapters, strong local model support, and a polished browser chat workflow that developers can run without cloud lock-in.

Read the full product vision in `VISION.md`.

### Vision

Aushu aims to be the open-source developer AI platform for daily coding flows. It should:

- support local and self-hosted models first,
- offer fast prompt-driven workflows for developers,
- expose clean provider and model selection,
- keep sensitive code and prompts off locked cloud platforms.

### Differentiators

- Local-first model discovery and completion via Ollama and other adaptable providers.
- Developer-centric CLI and browser UX with a chat-style prompt experience.
- Clear provider health, model availability, and error feedback.
- Open, extensible architecture that avoids cloud provider lock-in.

## Local browser UI

Aushu includes a lightweight WhatsApp-style local browser UI for prompt chat, model selection, and provider health checks. It is built to feel smooth and responsive while remaining easy to run locally.

Start the local web interface from the repo root after installing dependencies:

```bash
python packages/web-ui/server.py
```

Then open:

```text
http://127.0.0.1:8000
```

If you installed via `make`, you can also run:

```bash
make web
```

## Packages

- `packages/ai` — Python LLM provider adapters, local/remote model discovery, and a unified completion client.
- `packages/core` — Agent runtime, CLI, config management, and developer command workflows.
- `packages/permissions` — Permission configuration and enforcement utilities for safer agent actions.
- `packages/tui` — Terminal UI scaffold package for console-first workflows.
- `packages/web-ui` — Lightweight browser UI package with chat-style prompt handling and provider controls.

## Running tests

From the repo root:

```bash
python -m unittest discover -s packages -p 'test_*.py' -v
```

Or run package-specific suites:

```bash
python -m unittest discover -s packages/ai/tests -p 'test_*.py'
python -m unittest discover -s packages/core/tests -p 'test_*.py'
python -m unittest discover -s packages/permissions/tests -p 'test_*.py'
```
