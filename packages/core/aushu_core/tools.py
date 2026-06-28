from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

try:
    from aushu_permissions.config import load_permissions_config
    from aushu_permissions.checker import PermissionChecker
except ImportError:
    from pathlib import Path as _Path
    import sys as _sys
    repo_root = _Path(__file__).resolve().parents[3]
    local_perm_path = repo_root / "packages" / "permissions"
    if local_perm_path.exists():
        _sys.path.insert(0, str(local_perm_path))
    try:
        from aushu_permissions.config import load_permissions_config
        from aushu_permissions.checker import PermissionChecker
    except ImportError:  # pragma: no cover
        load_permissions_config = None
        PermissionChecker = None


class PermissionDenied(RuntimeError):
    pass


def _get_permission_checker() -> PermissionChecker | None:
    if load_permissions_config is None or PermissionChecker is None:
        return None
    config = load_permissions_config()
    return PermissionChecker(config)


def read_file(path: str) -> str:
    p = Path(path).expanduser()
    checker = _get_permission_checker()
    if checker and not checker.is_path_allowed(str(p), write=False):
        raise PermissionDenied(f"Read access denied for path: {path}")
    if not p.exists():
        raise FileNotFoundError(path)
    return p.read_text()


def write_file(path: str, contents: str) -> None:
    p = Path(path).expanduser()
    checker = _get_permission_checker()
    if checker and not checker.is_path_allowed(str(p), write=True):
        raise PermissionDenied(f"Write access denied for path: {path}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contents)


def run_command(cmd: str) -> str:
    checker = _get_permission_checker()
    if checker and not checker.is_tool_allowed("shell", cmd):
        raise PermissionDenied(f"Shell command denied: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        return res.stderr
    return res.stdout
