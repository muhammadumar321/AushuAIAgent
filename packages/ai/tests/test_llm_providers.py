from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aushu_ai.llm import LLMClient, list_models, list_providers


class TestLLMProviders(unittest.TestCase):
    def test_llm_supported_providers(self):
        providers = list_providers()
        self.assertIn("openai", providers)
        self.assertIn("anthropic", providers)
        self.assertIn("ollama", providers)
        self.assertIn("lmstudio", providers)
        self.assertIn("google", providers)
        self.assertIn("openrouter", providers)
        self.assertIn("groq", providers)
        self.assertIn("vllm", providers)
        self.assertIn("custom", providers)

    def test_llm_supported_model_lists(self):
        openai_models = list_models("openai")
        self.assertIn("gpt-4o", openai_models)
        self.assertIn("gpt-3.5-turbo", openai_models)
        self.assertIn("claude-2", list_models("anthropic"))
        self.assertIn("llama2", list_models("ollama"))

    def test_llm_runtime_provider_model_parsing(self):
        client = LLMClient(provider="openai:gpt-4o-mini")
        self.assertEqual(client.provider_name, "openai")
        self.assertEqual(client.model, "gpt-4o-mini")

    def test_llm_complete_raises_without_creds(self):
        c = LLMClient(provider="openai")
        with self.assertRaises(NotImplementedError):
            c.complete("hello")
        c2 = LLMClient(provider="anthropic")
        with self.assertRaises(NotImplementedError):
            c2.complete("hello")


if __name__ == "__main__":
    unittest.main()
