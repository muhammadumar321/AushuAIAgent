# packages/core

Core agent runtime and CLI scaffolding for Aushu.

## Purpose

This package provides the agent runtime, command-line interface, configuration management, and workflow tools used by Aushu.

## Contents

- `aushu_core/agent.py` — core `Agent` runtime and completion wrapper.
- `aushu_core/cli.py` — CLI entrypoint `agent` with commands such as `run`, `providers`, `models`, and `setup`.
- `aushu_core/config.py` — configuration loading and defaults.
- `aushu_core/tools.py` — small helper tools used by the agent runtime.

## Usage

Install in editable mode and run the CLI from the repo root:

```bash
python -m pip install -e packages/core
agent providers
agent run "Hello" --provider ollama --model qwen2.5-coder:7b
```
