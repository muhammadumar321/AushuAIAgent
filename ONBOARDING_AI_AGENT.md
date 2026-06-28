# Aushu AI Agent — Project Onboarding (for AI agents and new contributors)

Purpose: this document contains everything an AI agent or a new developer needs to start working on the Aushu monorepo locally and contribute safely.

## Overview
- Repository: AushuAIAgent (monorepo)
- Main languages: Python (CLI, core, providers), a small web UI (FastAPI + simple frontend)
- Positioning: an open-source, local-first competitor to OpenCode, Cursor, and Codex designed for developer workflows and privacy-aware local model usage.
- Vision document: `VISION.md` explains the product strategy and developer-centered goals.
- Packages:
  - `packages/ai` — `aushu_ai`: LLM provider adapters and `LLMClient`
  - `packages/core` — `aushu_core`: Agent runtime, CLI, config, tools
  - `packages/permissions` — `aushu_permissions`: permission checks and configs
  - `packages/tui` — terminal UI scaffold
  - `packages/web-ui` — lightweight browser UI server (FastAPI)

## Goals for the AI agent reading this file
- Be able to set up the repo locally across platforms (Linux, macOS, Windows).
- Run and pass Python unit tests.
- Start and use the local browser UI.
- Discover and invoke LLM providers, including local Ollama models.
- Add or modify providers, tests, and features following repo conventions.
- Understand Aushu's product direction as a local-first rival to OpenCode, Cursor, and Codex.

## Quick Prerequisites
- Python 3.10+ (3.11/3.12/3.14 tested in CI matrix)
- Git
- On macOS: Homebrew (optional) for installing Python
- For local Ollama provider testing: local Ollama service running (default: `http://localhost:11434/v1`)

## Bootstrap (all platforms)

1. Clone the repo and change into it:

```bash
git clone <repo-url> AushuAIAgent
cd AushuAIAgent
```

2. Quick automated install

- Linux / macOS (bash):

```bash
./install.sh
# or
python bootstrap.py
```

- Windows PowerShell:

```powershell
.\bootstrap.ps1
```

- Windows CMD:

```cmd
bootstrap.cmd
```

Notes:
- The bootstraps create `.venv`, install dependencies from `requirements.txt`, and install editable packages `packages/ai`, `packages/core`, `packages/permissions`.
- macOS script includes Homebrew checks and suggestions.

## Manual setup (if preferred)

```bash
python3 -m venv .venv
source .venv/bin/activate    # PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e packages/ai -e packages/core -e packages/permissions
```

## Run test suite

```bash
python -m unittest discover -s packages -p 'test_*.py' -v
```

## Development notes

- Makefile targets:
  - `make setup` — run `install.sh`
  - `make test` — run the Python tests
  - `make web` — start the local web UI server (`python packages/web-ui/server.py` inside the virtualenv)

### Product direction
- Keep Aushu focused on open-source developer AI workflows, not closed cloud-first lock-in.
- Prioritize local provider support first, with Ollama and other self-hosted models as primary paths.
- Make the UI fast, chat-first, and developer-friendly, with a polished web experience and clear provider health/status.
- Continue to grow the platform around extensible provider adapters, solid docs, and a stable CLI + web stack.
- Build for developers who want a self-hosted alternative to closed systems like OpenCode, Cursor, and Codex.

### Vision
- Aushu should feel like a developer's local AI companion: responsive, extensible, and privacy-aware.
- New features should add value for everyday coding tasks, not just benchmark-style completions.
- Documentation must make it easy for contributors to expand provider support and improve the local-first experience.

## Local Web UI (browser)
- The lightweight web UI is provided at `packages/web-ui/server.py` using FastAPI and serves a single-page UI.
- Start it with (after dependencies):

```bash
python packages/web-ui/server.py
# or (from Makefile after setup):
make web
```

- Open `http://127.0.0.1:8000` in your browser.
- The UI lists available providers and loads models for the selected provider. For `ollama` it queries the local Ollama `/models` endpoint to discover installed models.

## Providers and LLM integration

- `packages/ai/aushu_ai/llm.py` contains provider adapters (`OpenAIProvider`, `OllamaProvider`, etc.) and a `PROVIDER_REGISTRY`.
- `LLMClient` picks a provider and normalizes model names.
- New providers should:
  - Add a provider class inheriting `BaseProvider`.
  - Set `name`, `supported_models`, `default_model`.
  - Implement `complete(self, prompt, model, **kwargs)` and (optionally) `list_models()` for dynamic discovery.

## Ollama specifics (local)
- Default Ollama URL: `http://localhost:11434/v1` (environment override: `OLLAMA_URL`).
- `OllamaProvider.list_models()` queries `GET /models` and returns model IDs. If the Ollama service is unreachable, it falls back to built-in static `supported_models`.
- Completion endpoint used: `POST {OLLAMA_URL.rstrip('/')}/completions` with payload `{"model": "<model>", "prompt": "<prompt>"}`.

## Debugging provider failures (500s)
- Common causes:
  - Missing API key for a cloud provider: set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc., in environment.
  - Local Ollama not running or different API path — verify with:

```bash
curl -sS http://localhost:11434/v1/models | jq .
curl -sS -X POST http://localhost:11434/v1/completions -H 'Content-Type: application/json' -d '{"model":"<model>","prompt":"hi"}' | jq .
```

## Web UI 500 handling
- The web UI forwards exceptions from agent methods. If completions return a 500, the UI shows the error detail. Consider:
  - Using the UI to switch to a local provider (ollama) and a known installed model.
  - Or set the required environment variables before starting the UI server.

## Testing and CI
- CI workflow is `.github/workflows/ci.yml` — runs tests on Ubuntu, macOS, and Windows across Python versions.
- Keep tests fast and focused; mocking network calls is preferred for provider tests.

## Documentation Rule
- Every technical change, new feature, or provider update must include a markdown documentation update.
- Keep `README.md`, `ONBOARDING_AI_AGENT.md`, `CONTRIBUTING.md`, and provider notes in sync with code changes.
- This rule helps AI agents and humans onboard quickly and prevents stale instructions.

## Repo structure (important files)
- `README.md` — quick start and high-level info
- `ONBOARDING_AI_AGENT.md` — this file (read first)
- `install.sh`, `bootstrap.py` — bootstrapping scripts
- `Makefile` — convenience commands
- `requirements.txt` — key Python dependencies
- `packages/ai/aushu_ai/llm.py` — LLM providers and `LLMClient`
- `packages/core/aushu_core/agent.py` — `Agent` runtime and `complete()` wrapper
- `packages/core/aushu_core/cli.py` — CLI entrypoint `agent` (commands: run, providers, models, model set/get, setup)
- `packages/web-ui/server.py` — local browser UI server (FastAPI)

## Development guidelines
- Run unit tests often. Add tests for new providers under `packages/ai/tests`.
- For networked providers, write tests that mock `requests` calls.
- Follow existing code style and naming: classes for providers, uppercase `PROVIDER_REGISTRY` mapping.

## First tasks an AI agent could do
1. Run full tests locally and report any failures.
2. Verify Ollama model discovery by starting a local Ollama instance and checking `/models` via the UI.
3. Add an API health-check endpoint in `packages/web-ui/server.py` that verifies provider reachability (optional enhancement).
4. Improve UI error messaging for unreachable providers (e.g., show "provider unreachable" instead of raw stack trace).

## Contact points and context
- This repo is a scaffold; reach out to the human maintainer for credentials or to run long-lived services locally.
- Use the `Makefile` and `bootstrap` scripts when preparing environments for CI runs.

## License
- See `LICENSE` at the repo root.

---

_End of onboarding_
