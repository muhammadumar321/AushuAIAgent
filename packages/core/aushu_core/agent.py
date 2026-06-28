from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

from . import tools
from .config import get_default_provider_model

try:
    from aushu_ai import LLMClient
except ImportError:  # pragma: no cover
    LLMClient = None


@dataclass
class Agent:
    """Minimal agent loop for Phase 1.

    The Agent routes simple commands to built-in tools and aggregates results.
    """

    name: str = "aushu"

    def run(self, prompt: str) -> Dict[str, Any]:
        """Interpret a very small set of prompt patterns for the scaffold.

        Supported patterns:
        - "read <path>"
        - "write <path> <content>"
        - "run <cmd>"
        """
        parts = prompt.strip().split(maxsplit=2)
        if not parts:
            return {"error": "empty prompt"}

        cmd = parts[0].lower()
        if cmd == "read" and len(parts) >= 2:
            path = parts[1]
            content = tools.read_file(path)
            return {"action": "read", "path": path, "content": content}
        if cmd == "write" and len(parts) >= 3:
            path = parts[1]
            body = parts[2]
            tools.write_file(path, body)
            return {"action": "write", "path": path}
        if cmd == "run" and len(parts) >= 2:
            run_cmd = parts[1]
            out = tools.run_command(run_cmd)
            return {"action": "run", "cmd": run_cmd, "output": out}

        return {"error": "unrecognized command"}

    def complete(self, prompt: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        if LLMClient is None:
            raise RuntimeError("The aushu-ai package is required for LLM completion")
        default_provider, default_model = get_default_provider_model()
        if provider is None:
            provider = default_provider
        if model is None:
            model = default_model
        client = LLMClient(provider=provider, model=model)
        output = client.complete(prompt, **kwargs)
        return {"action": "complete", "provider": provider, "model": client.model, "output": output}
