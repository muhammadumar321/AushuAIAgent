from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aushu_ai.llm import LLMClient


class TestLLMClient(unittest.TestCase):
    def test_llm_client_init(self):
        c = LLMClient(provider="openai")
        self.assertEqual(c.provider_name, "openai")


if __name__ == "__main__":
    unittest.main()
