from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import Agent
from .config import get_default_provider_model, set_default_provider_model

try:
    from aushu_ai import list_models, list_providers
except ImportError:
    repo_root = Path(__file__).resolve().parents[3]
    local_ai_path = repo_root / "packages" / "ai"
    if local_ai_path.exists():
        sys.path.insert(0, str(local_ai_path))
    try:
        from aushu_ai import list_models, list_providers
    except ImportError:  # pragma: no cover
        list_models = None
        list_providers = None

try:
    from aushu_permissions import save_permissions_config
    from aushu_permissions.config import PermissionsConfig
except ImportError:
    repo_root = Path(__file__).resolve().parents[3]
    local_perm_path = repo_root / "packages" / "permissions"
    if local_perm_path.exists():
        sys.path.insert(0, str(local_perm_path))
    try:
        from aushu_permissions import save_permissions_config
        from aushu_permissions.config import PermissionsConfig
    except ImportError:  # pragma: no cover
        PermissionsConfig = None
        save_permissions_config = None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a shell command or complete with an LLM")
    run_parser.add_argument("prompt", nargs="+", help="Prompt or shell command text")
    run_parser.add_argument("--provider", default=None, help="LLM provider to use")
    run_parser.add_argument("--model", default=None, help="Model to use for the provider")
    run_parser.add_argument("--llm", action="store_true", help="Use the LLM provider instead of shell tools")

    subparsers.add_parser("providers", help="List available LLM providers")

    models_parser = subparsers.add_parser("models", help="List available models for a provider")
    models_parser.add_argument("provider", help="Provider name")

    model_parser = subparsers.add_parser("model", help="Manage default model settings")
    model_subparsers = model_parser.add_subparsers(dest="subcommand", required=True)
    set_parser = model_subparsers.add_parser("set", help="Set default provider:model")
    set_parser.add_argument("provider_model", help="Provider:model string, e.g. openai:gpt-4o-mini")
    get_parser = model_subparsers.add_parser("get", help="Show current default provider:model")

    subparsers.add_parser("setup", help="Run initial agent setup wizard")

    args = parser.parse_args(argv)
    agent = Agent()

    if args.command == "providers":
        if list_providers is None:
            print("LLM provider registry not available. Install aushu-ai.")
            return 1
        print("Available providers:")
        for provider in list_providers():
            print(f"- {provider}")
        return 0

    if args.command == "models":
        if list_models is None:
            print("LLM model registry not available. Install aushu-ai.")
            return 1
        try:
            models = list_models(args.provider)
        except ValueError as exc:
            print(str(exc))
            return 1
        print(f"Models for provider {args.provider}:")
        for model in models:
            print(f"- {model}")
        return 0

    if args.command == "model":
        if args.subcommand == "set":
            set_default_provider_model(args.provider_model)
            print(f"Default provider:model set to {args.provider_model}")
            return 0
        if args.subcommand == "get":
            provider, model = get_default_provider_model()
            print(f"Default provider:model = {provider}:{model}")
            return 0

    if args.command == "setup":
        print("Aushu Agent setup")
        use_local = input("Use local models only? [y/N]: ").strip().lower().startswith("y")
        default_provider = "ollama" if use_local else "openai"
        provider = input(f"Default provider [{default_provider}]: ").strip() or default_provider

        model_defaults = {
            "openai": "openai:gpt-4o",
            "anthropic": "anthropic:claude-3", 
            "google": "google:gemini",
            "openrouter": "openrouter:gpt-4o-mini",
            "groq": "groq:groq-1",
            "ollama": "ollama:llama2",
            "vllm": "vllm:meta-llama",
            "lmstudio": "lmstudio:llama2",
        }
        default_model = model_defaults.get(provider, f"{provider}:latest")
        model = input(f"Default model (provider:model) [{default_model}]: ").strip() or default_model
        if ":" not in model:
            model = f"{provider}:{model}"
        set_default_provider_model(model)
        print(f"Default provider:model set to {model}")

        permission_mode = input("Permission mode [always-ask|allow-all|accept-edits|deny-all] [always-ask]: ").strip() or "always-ask"
        if permission_mode not in {"always-ask", "allow-all", "accept-edits", "deny-all"}:
            print("Unknown permission mode, falling back to always-ask.")
            permission_mode = "always-ask"

        if save_permissions_config is not None:
            init_permissions = input("Initialize local permissions config? [Y/n]: ").strip().lower()
            if init_permissions == "" or init_permissions.startswith("y"):
                config = PermissionsConfig(
                    mode=permission_mode,
                    tools={
                        "shell": {
                            "allow": ["git *", "python *"],
                            "deny": ["rm -rf *"],
                        }
                    },
                    paths={
                        "allow": ["./**"],
                        "deny": [],
                    },
                )
                save_permissions_config(config)
                print("Local permissions config saved to .aushu/settings.local.yaml")
            else:
                print("Skipping local permissions config setup.")
        else:
            print("Permissions package not available, skipping permission config creation.")

        print(f"Permission mode set to {permission_mode}.")
        return 0

    if args.command == "run":
        prompt = " ".join(args.prompt)
        if args.llm:
            result = agent.complete(prompt, provider=args.provider, model=args.model)
        else:
            result = agent.run(prompt)
        print(result)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
