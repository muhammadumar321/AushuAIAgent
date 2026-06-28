from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG = {
    "mode": "always-ask",
    "tools": {
        "shell": {"allow": [], "deny": []}
    },
    "paths": {"allow": [], "deny": []},
}


def _config_global() -> Path:
    return Path(os.environ.get("HOME", "~")).expanduser() / ".aushu" / "settings.yaml"


def _config_project() -> Path:
    return Path(".aushu") / "settings.yaml"


def _config_local() -> Path:
    return Path(".aushu") / "settings.local.yaml"


@dataclass
class PermissionMode:
    name: str
    description: str


@dataclass
class PermissionsConfig:
    mode: str = "always-ask"
    tools: dict[str, Any] = field(default_factory=lambda: {"shell": {"allow": [], "deny": []}})
    paths: dict[str, Any] = field(default_factory=lambda: {"allow": [], "deny": []})


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
        return data if isinstance(data, dict) else {}


def save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle)


def load_permissions_config() -> PermissionsConfig:
    config: dict[str, Any] = {}
    config.update(load_yaml(_config_global()))
    project_path = _config_project()
    if project_path.exists():
        config.update(load_yaml(project_path))
    local_path = _config_local()
    if local_path.exists():
        config.update(load_yaml(local_path))
    merged = {**DEFAULT_CONFIG, **config}
    return PermissionsConfig(mode=merged["mode"], tools=merged.get("tools", DEFAULT_CONFIG["tools"]), paths=merged.get("paths", DEFAULT_CONFIG["paths"]))


def save_permissions_config(config: PermissionsConfig, location: Path | None = None) -> None:
    if location is None:
        location = _config_local()
    save_yaml(location, {"mode": config.mode, "tools": config.tools, "paths": config.paths})
