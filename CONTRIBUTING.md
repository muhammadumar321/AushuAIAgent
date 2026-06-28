# Contributing to Aushu

We're excited you want to contribute! Aushu is a community-driven open-source project, and every contribution — whether code, documentation, bug reports, or ideas — is valued.

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold it. Report unacceptable behavior to the maintainers.

## Getting started

### Prerequisites

- **Python 3.10+**
- **Git**
- **Make** (optional but recommended)

### Setup

```bash
# Fork and clone the repo
git clone https://github.com/your-username/AushuAIAgent.git
cd AushuAIAgent

# Run setup
make setup

# Activate virtual environment
source .venv/bin/activate

# Verify it works
agent providers
```

**Platform-specific setup:**

| Platform | Command |
|----------|---------|
| Linux / macOS | `./install.sh` or `python bootstrap.py` |
| Windows (PowerShell) | `.\bootstrap.ps1` |
| Windows (CMD) | `bootstrap.cmd` |

### Running tests

```bash
# All tests
python -m unittest discover -s packages -p 'test_*.py' -v

# Per package
python -m unittest discover -s packages/ai/tests -p 'test_*.py'
python -m unittest discover -s packages/core/tests -p 'test_*.py'
python -m unittest discover -s packages/permissions/tests -p 'test_*.py'
```

## How to contribute

### 1. Find something to work on

- Check [open issues](https://github.com/muhammadumar321/AushuAIAgent/issues), especially [good first issues](https://github.com/muhammadumar321/AushuAIAgent/labels/good%20first%20issue)
- Look for issues labeled `help wanted` or `bug`
- Propose a new feature by opening a [discussion](https://github.com/muhammadumar321/AushuAIAgent/discussions)

### 2. Branch and code

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Commit guidelines

- Use clear, descriptive commit messages
- Reference issues in commits when applicable (`Closes #123`)
- Keep commits focused on a single change

### 4. Open a Pull Request

- Push your branch and open a PR against `main`
- Fill out the PR template with details about your change
- Ensure CI passes (we use GitHub Actions)
- Request review from maintainers

## Development guidelines

### Code style

- Follow PEP 8 conventions
- Use type hints for function signatures
- Write docstrings for public APIs
- Keep functions focused and small

### Documentation rule

Every change or new feature **must** include updates to the relevant documentation:

- `README.md` - if the change affects user-facing behavior
- `ONBOARDING_AI_AGENT.md` - if the change affects setup or onboarding
- `CONTRIBUTING.md` - if the change affects the contribution workflow
- Package `README.md` files - if the change affects package-specific behavior

### Architecture

Aushu is organized as a monorepo with these packages:

```
packages/
├── ai/           — LLM provider adapters (Ollama, OpenAI, etc.)
├── core/         — Agent runtime, CLI entrypoint, config
├── permissions/  — Safety layer for agent actions
├── tui/          — Terminal UI components
└── web-ui/       — Browser-based chat interface
```

When adding a feature:
1. Place it in the appropriate package
2. If it spans multiple packages, add interfaces in the relevant packages
3. Add tests alongside your changes
4. Update documentation

### Adding a new LLM provider

1. Create a new adapter in `packages/ai/aushu_ai/`
2. Implement the provider interface
3. Register it in the provider registry
4. Add tests in `packages/ai/tests/`
5. Document the provider in `packages/ai/README.md`

## Project vision

Aushu aims to be the leading open-source developer AI platform. Read our full vision in [VISION.md](VISION.md).

- **Local-first** — Self-hosted models and data sovereignty
- **Developer UX** — Fast CLI + polished browser UI
- **Extensible** — Pluggable providers, tools, and workflows
- **Community-driven** — Built by developers, for developers

## Getting help

- [Discord](https://discord.gg/aushu) — Real-time chat with the community
- [GitHub Issues](https://github.com/muhammadumar321/AushuAIAgent/issues) — Bug reports and feature requests
- [Discussions](https://github.com/muhammadumar321/AushuAIAgent/discussions) — Ideas and questions

Thank you for contributing to Aushu! 🚀
