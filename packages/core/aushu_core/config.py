from __future__ import annotations

import os
from pathlib import Path

import yaml

DEFAULT_CONFIG = {"model": "openai:gpt-4o"}


def _config_dir() -> Path:
    return Path(os.environ.get("HOME", "~")).expanduser() / ".aushu"


def _config_file() -> Path:
    return _config_dir() / "settings.yaml"


def _ensure_config_dir() -> None:
    _config_dir().mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    config_file = _config_file()
    _ensure_config_dir()
    if not config_file.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with config_file.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            if not isinstance(data, dict):
                return DEFAULT_CONFIG.copy()
            return {**DEFAULT_CONFIG, **data}
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    config_file = _config_file()
    _ensure_config_dir()
    with config_file.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(config, fh)


def get_default_provider_model() -> tuple[str, str]:
    config = load_config()
    provider_model = str(config.get("model", DEFAULT_CONFIG["model"]))
    if ":" in provider_model:
        provider, model = provider_model.split(":", 1)
    else:
        provider, model = provider_model, ""
    return provider, model


def set_default_provider_model(provider_model: str) -> None:
    if ":" not in provider_model:
        raise ValueError("provider_model must be formatted as provider:model")
    config = load_config()
    config["model"] = provider_model
    save_config(config)
