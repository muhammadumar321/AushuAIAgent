from __future__ import annotations

import fnmatch
import os
from pathlib import Path
from typing import Any

from .config import PermissionsConfig


def _normalize_path(path: str) -> str:
    return str(Path(path).expanduser().resolve())


def _match_rule(value: str, pattern: str) -> bool:
    return fnmatch.fnmatch(value, pattern)


class PermissionChecker:
    def __init__(self, config: PermissionsConfig) -> None:
        self.config = config

    def is_tool_allowed(self, tool_name: str, command: str) -> bool:
        tool_rules = self.config.tools.get(tool_name, {})
        deny_rules = tool_rules.get("deny", [])
        allow_rules = tool_rules.get("allow", [])

        if self._matches_any(command, deny_rules):
            return False
        if self._matches_any(command, allow_rules):
            return True
        return self.config.mode == "allow-all"

    def is_path_allowed(self, path: str, write: bool = False) -> bool:
        normalized = _normalize_path(path)
        deny_rules = self.config.paths.get("deny", [])
        allow_rules = self.config.paths.get("allow", [])

        if self._matches_any(normalized, deny_rules, path_match=True):
            return False
        if self._matches_any(normalized, allow_rules, path_match=True):
            if write:
                return True
            return True
        return False

    def _matches_any(self, value: str, patterns: list[str], path_match: bool = False) -> bool:
        for pattern in patterns:
            normalized_pattern = self._normalize_pattern(pattern) if path_match else pattern
            if fnmatch.fnmatch(value, normalized_pattern):
                return True
        return False

    def _normalize_pattern(self, pattern: str) -> str:
        pattern = pattern.replace("~", os.path.expanduser("~"))
        if not os.path.isabs(pattern):
            pattern = str(Path.cwd() / pattern)
        return os.path.normpath(pattern)
