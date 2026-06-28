#!/usr/bin/env bash
set -euo pipefail

# If running on macOS, check Homebrew and suggest/install Python if missing
if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "macOS detected — checking Homebrew..."
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew not found. Consider installing Homebrew: https://brew.sh"
  else
    echo "Homebrew found. Ensuring Python is installed via Homebrew..."
    if ! brew list python >/dev/null 2>&1; then
      echo "Installing python via Homebrew..."
      brew install python
    fi
  fi
fi

echo "Aushu local installer (scaffold)"
PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Error: $PYTHON not found. Install Python 3 first." >&2
  exit 1
fi

echo "Creating virtual environment in .venv..."
$PYTHON -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
  echo "Installing Python requirements..."
  python -m pip install -r requirements.txt
fi

echo "Installing editable local packages..."
python -m pip install -e packages/ai -e packages/core -e packages/permissions

echo ""
echo "Setup complete. Activate the environment with:"
echo "  source .venv/bin/activate"
echo "Then run the CLI with:"
echo "  agent providers"

# Interactive post-install: optional default model + permissions
if [ -t 0 ]; then
  echo
  read -p "Set default LLM provider (openai/ollama/anthropic) [openai]: " PROVIDER
  PROVIDER=${PROVIDER:-openai}
  read -p "Set default model (format provider:model) [${PROVIDER}:gpt-4o]: " MODEL
  MODEL=${MODEL:-"${PROVIDER}:gpt-4o"}

  mkdir -p .aushu
  cat > .aushu/settings.local.yaml <<EOF
model: ${MODEL}
tools:
  shell:
    allow:
      - 'git *'
      - 'python *'
    deny:
      - 'rm -rf *'
paths:
  allow:
    - '$(pwd)/**'
EOF
  echo "Saved default model to .aushu/settings.local.yaml"

  read -p "Initialize a local permissions config? [Y/n]: " INIT_PERMS
  INIT_PERMS=${INIT_PERMS:-y}
  if echo "$INIT_PERMS" | grep -i -q "^y"; then
    # settings.local.yaml already contains a basic permissions block above
    echo "Local permissions initialized in .aushu/settings.local.yaml"
  else
    echo "Skipping local permissions initialization."
  fi
fi
