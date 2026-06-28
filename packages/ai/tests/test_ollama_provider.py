from pathlib import Path
import sys
import unittest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aushu_ai.llm import OllamaProvider


class TestOllamaProvider(unittest.TestCase):
    @patch("requests.post")
    def test_ollama_complete_posts_to_v1_completions(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"choices": [{"text": "hello from ollama"}]}
        mock_post.return_value = mock_resp

        provider = OllamaProvider(endpoint="http://localhost:11434/v1")
        out = provider.complete("hi there", "qwen2.5-coder:7b")
        self.assertEqual(out, "hello from ollama")

        # Ensure we posted to a completions URL
        self.assertTrue(mock_post.called)
        called_url = mock_post.call_args[0][0]
        self.assertTrue(called_url.endswith("/v1/completions") or called_url.endswith("/completions"))


if __name__ == "__main__":
    unittest.main()
