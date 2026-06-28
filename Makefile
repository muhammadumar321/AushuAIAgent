.PHONY: setup activate test providers run clean help

setup:
	./install.sh

activate:
	@echo "To activate the virtual environment, run:"
	@echo "  source .venv/bin/activate"

help:
	@echo "Available targets:"
	@echo "  make setup       - bootstrap the repo and install dependencies"
	@echo "  make activate    - print the activate command for .venv"
	@echo "  make test        - run Python tests"
	@echo "  make providers   - list available LLM providers"
	@echo "  make run         - run a prompt with the CLI (set prompt/provider/model)"
	@echo "  make clean       - remove the virtual environment"
	@echo "If make is not installed, use python bootstrap.py instead."

test:
	python -m unittest discover -s packages -p 'test_*.py' -v

providers:
	.venv/bin/agent providers

run:
	@echo "Usage: make run prompt=\"Hello\" provider=ollama model=qwen2.5-coder:7b"
	@.venv/bin/agent run "$(prompt)" --llm --provider $(provider) --model $(model)

web:
	@echo "Starting the local web UI on http://127.0.0.1:8000"
	@.venv/bin/python packages/web-ui/server.py

clean:
	rm -rf .venv
