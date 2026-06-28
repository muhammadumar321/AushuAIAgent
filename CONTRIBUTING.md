# Contributing

This project supports Linux (Debian/Ubuntu, Fedora), macOS, and Windows.

Quick setup

- Linux / macOS: `./install.sh` or `python bootstrap.py`
- Windows PowerShell: `.\bootstrap.ps1`
- Windows CMD: `bootstrap.cmd`

Run tests

```sh
python -m unittest discover -s packages -p 'test_*.py' -v
```

If you'd like CI to run on your PRs, we use GitHub Actions (`.github/workflows/ci.yml`).

## Documentation Rule
- Every change or new feature must include updates to the relevant markdown documentation.
- Update `README.md`, `ONBOARDING_AI_AGENT.md`, or `CONTRIBUTING.md` whenever you add, change, or remove behavior.
- This repository follows the rule: documentation must stay current with code.
- Keep the product direction clear: Aushu should be described as a local-first, open-source competitor to OpenCode, Cursor, and Codex.
- When documenting features, include how they support Aushu's developer-first, self-hosted vision.
- Refer to `VISION.md` for the current product strategy and contributor guidance.

## Product vision for contributors
- Prioritize local model workflows and clear provider discovery.
- Prefer improvements that make the web UI and CLI friendlier for developers.
- Document any changes that affect model selection, provider health, or completion behavior.
- Avoid wording that implies cloud-only usage unless the feature is explicitly cloud provider support.
