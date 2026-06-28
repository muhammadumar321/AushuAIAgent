# Aushu Web UI

This package provides a lightweight, WhatsApp-inspired local browser UI for Aushu. It is designed to deliver a smooth chat experience for prompts, model selection, and provider health checks.

Aushu's web UI is part of the local-first developer agent direction, supporting fast workflows without cloud lock-in.

## Running the web UI

From the repo root, install dependencies and run:

```bash
python packages/web-ui/server.py
```

Then open `http://127.0.0.1:8000` in your browser.

## Features

- Browser form for prompts and shell-style commands
- Local LLM completion via the `agent.complete` API
- Provider discovery via `/api/providers`
- Response display in the browser
