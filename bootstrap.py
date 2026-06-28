#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"
PACKAGES = ["packages/ai", "packages/core", "packages/permissions"]


def run_command(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def create_virtualenv() -> None:
    if VENV_DIR.exists():
        print(f"Virtual environment already exists at {VENV_DIR}")
        return

    python_exe = os.environ.get("PYTHON", sys.executable)
    print(f"Creating virtual environment with {python_exe}...")
    run_command([python_exe, "-m", "venv", str(VENV_DIR)])


def install_dependencies() -> None:
    pip_exe = VENV_DIR / "bin" / "pip"
    if not pip_exe.exists():
        raise SystemExit("Virtual environment missing. Run bootstrap.py again after creation.")

    print("Upgrading pip...")
    run_command([str(pip_exe), "install", "--upgrade", "pip"])

    if REQUIREMENTS.exists():
        print("Installing requirements...")
        run_command([str(pip_exe), "install", "-r", str(REQUIREMENTS)])

    editable_packages = [str(ROOT / p) for p in PACKAGES if (ROOT / p).exists()]
    if editable_packages:
        print("Installing local packages in editable mode...")
        run_command([str(pip_exe), "install", "-e", *editable_packages])


def print_success() -> None:
    print("\nSetup complete.")
    print("Activate the environment with:")
    print("  source .venv/bin/activate")
    print("Then run the CLI using:")
    print("  agent providers")


def main() -> None:
    create_virtualenv()
    install_dependencies()
    print_success()


if __name__ == "__main__":
    main()
