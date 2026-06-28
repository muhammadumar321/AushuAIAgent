from __future__ import annotations

import json
import os
from typing import Protocol, ClassVar, Iterable, Mapping, Optional, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    name: ClassVar[str]
    supported_models: ClassVar[tuple[str, ...]]
    default_model: ClassVar[str]

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        ...


def _parse_provider_model(provider: str) -> tuple[str, Optional[str]]:
    if ":" in provider:
        provider_name, model = provider.split(":", 1)
        return provider_name, model
    return provider, None


class BaseProvider:
    name: ClassVar[str] = "base"
    supported_models: ClassVar[tuple[str, ...]] = ()
    default_model: ClassVar[str] = ""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        self.api_key = api_key
        self.endpoint = endpoint

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        raise NotImplementedError

    @classmethod
    def list_models(cls) -> tuple[str, ...]:
        return cls.supported_models

    @classmethod
    def normalize_model(cls, model: Optional[str]) -> str:
        return model or cls.default_model


class OpenAIProvider(BaseProvider):
    name = "openai"
    supported_models = (
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4o-110k",
        "gpt-4o-realtime-preview",
        "gpt-4o-mini-voice",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    )
    default_model = "gpt-4o"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key or os.environ.get("OPENAI_API_KEY"), endpoint=endpoint or os.environ.get("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.api_key:
            raise NotImplementedError("OpenAI adapter requires OPENAI_API_KEY in environment")
        import requests

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update(kwargs.get("payload", {}))
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("message", {}).get("content", "")
        return json.dumps(data)


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    supported_models = ("claude-2", "claude-3", "claude-instant-v1", "claude-sonnet-4", "claude-haiku-1")
    default_model = "claude-2"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"), endpoint=endpoint or os.environ.get("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/complete"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.api_key:
            raise NotImplementedError("Anthropic adapter requires ANTHROPIC_API_KEY in environment")
        import requests

        payload = {
            "prompt": prompt,
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 512),
        }
        resp = requests.post(self.endpoint, headers={"x-api-key": self.api_key, "Content-Type": "application/json"}, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        return data.get("completion", json.dumps(data))


class GoogleProvider(BaseProvider):
    name = "google"
    supported_models = ("gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-pro", "gemini-2.0-mini")
    default_model = "gemini-1.5-flash"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key or os.environ.get("GOOGLE_API_KEY"), endpoint=endpoint or os.environ.get("GOOGLE_API_URL", "https://generativelanguage.googleapis.com/v1beta2/models:generateText"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.api_key:
            raise NotImplementedError("Google adapter requires GOOGLE_API_KEY in environment")
        import requests

        payload = {"model": model, "prompt": {"text": prompt}}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0].get("output", "")
        return json.dumps(data)


class OpenRouterProvider(BaseProvider):
    name = "openrouter"
    supported_models = ("gpt-4o", "gpt-4o-mini", "qwen", "llama2", "mistral", "vicuna")
    default_model = "gpt-4o"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key or os.environ.get("OPENROUTER_API_KEY"), endpoint=endpoint or os.environ.get("OPENROUTER_API_URL", "https://openrouter.ai/v1/chat/completions"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.api_key:
            raise NotImplementedError("OpenRouter adapter requires OPENROUTER_API_KEY in environment")
        import requests

        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("message", {}).get("content", "")
        return json.dumps(data)


class GroqProvider(BaseProvider):
    name = "groq"
    supported_models = ("groq-1", "groq-2", "groq-3")
    default_model = "groq-1"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key or os.environ.get("GROQ_API_KEY"), endpoint=endpoint or os.environ.get("GROQ_API_URL", "https://api.groq.com/v1/completions"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.api_key:
            raise NotImplementedError("Groq adapter requires GROQ_API_KEY in environment")
        import requests

        payload = {"model": model, "prompt": prompt}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("text", "")
        return json.dumps(data)


class OllamaProvider(BaseProvider):
    name = "ollama"
    supported_models = ("llama2", "mistral", "qwen", "mixtral", "ggml")
    default_model = "llama2"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key, endpoint=endpoint or os.environ.get("OLLAMA_URL", "http://localhost:11434/v1"), **kwargs)

    @classmethod
    def list_models(cls) -> tuple[str, ...]:
        try:
            import requests

            endpoint = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1")
            url = f"{endpoint.rstrip('/')}/models"
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                if "models" in data and isinstance(data["models"], list):
                    installed = [
                        str(m.get("id", m.get("name", m)))
                        if isinstance(m, dict)
                        else str(m)
                        for m in data["models"]
                        if m
                    ]
                    return tuple(dict.fromkeys(installed + list(cls.supported_models)))
                if "data" in data and isinstance(data["data"], list):
                    installed = [
                        str(item.get("id", item.get("name", item)))
                        if isinstance(item, dict)
                        else str(item)
                        for item in data["data"]
                        if item
                    ]
                    return tuple(dict.fromkeys(installed + list(cls.supported_models)))
            if isinstance(data, list):
                installed = [
                    str(item.get("id", item.get("name", item)))
                    if isinstance(item, dict)
                    else str(item)
                    for item in data
                    if item
                ]
                return tuple(dict.fromkeys(installed + list(cls.supported_models)))
        except Exception:
            return cls.supported_models
        return cls.supported_models

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        import requests

        url = f"{self.endpoint.rstrip('/')}/completions"
        payload = {"model": model, "prompt": prompt}
        resp = requests.post(url, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("text", "")
        return json.dumps(data)


class VLLMProvider(BaseProvider):
    name = "vllm"
    supported_models = ("llama2", "mistral", "qwen", "ggml")
    default_model = "llama2"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key, endpoint=endpoint or os.environ.get("VLLM_URL", "http://127.0.0.1:8000"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        import requests

        url = f"{self.endpoint}/api/v1/completions"
        payload = {"model": model, "prompt": prompt}
        resp = requests.post(url, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("text", "")
        return json.dumps(data)


class LMStudioProvider(BaseProvider):
    name = "lmstudio"
    supported_models = ("llama2", "mistral", "qwen", "vicuna")
    default_model = "llama2"

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        super().__init__(api_key=api_key, endpoint=endpoint or os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:8080"), **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        import requests

        url = f"{self.endpoint}/api/generate"
        payload = {"prompt": prompt, "max_new_tokens": kwargs.get("max_tokens", 256)}
        resp = requests.post(url, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        return data.get("text", json.dumps(data))


class CustomProvider(BaseProvider):
    name = "custom"
    supported_models = ()
    default_model = ""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs) -> None:
        endpoint = endpoint or os.environ.get("CUSTOM_OPENAI_URL")
        super().__init__(api_key=api_key or os.environ.get("CUSTOM_API_KEY"), endpoint=endpoint, **kwargs)

    def complete(self, prompt: str, model: str, **kwargs) -> str:
        if not self.endpoint:
            raise NotImplementedError("Custom provider requires CUSTOM_OPENAI_URL or endpoint override")
        import requests

        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0].get("message", {}).get("content", "")
        return json.dumps(data)


PROVIDER_REGISTRY: Mapping[str, type[BaseProvider]] = {
    OpenAIProvider.name: OpenAIProvider,
    AnthropicProvider.name: AnthropicProvider,
    GoogleProvider.name: GoogleProvider,
    OpenRouterProvider.name: OpenRouterProvider,
    GroqProvider.name: GroqProvider,
    OllamaProvider.name: OllamaProvider,
    VLLMProvider.name: VLLMProvider,
    LMStudioProvider.name: LMStudioProvider,
    CustomProvider.name: CustomProvider,
}


def list_providers() -> tuple[str, ...]:
    return tuple(PROVIDER_REGISTRY.keys())


def list_models(provider: str) -> tuple[str, ...]:
    provider_name, _ = _parse_provider_model(provider)
    provider_cls = PROVIDER_REGISTRY.get(provider_name)
    if not provider_cls:
        raise ValueError(f"unknown provider: {provider_name}")
    return provider_cls.list_models()


class LLMClient:
    def __init__(self, provider: str = "openai", model: Optional[str] = None, **kwargs) -> None:
        provider_name, provider_model = _parse_provider_model(provider)
        self.provider_name = provider_name
        self.model = model or provider_model
        provider_cls = PROVIDER_REGISTRY.get(provider_name)
        if not provider_cls:
            raise ValueError(f"unknown provider: {provider_name}")
        self.model = provider_cls.normalize_model(self.model)
        self._provider = provider_cls(**kwargs)

    def complete(self, prompt: str, **opts) -> str:
        return self._provider.complete(prompt, self.model, **opts)
