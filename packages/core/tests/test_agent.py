from pathlib import Path
import sys
import os
import tempfile
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent.parent.parent / "packages" / "ai"))

from aushu_core.agent import Agent
from aushu_core.cli import main


class TestAgentCLI(unittest.TestCase):
    def test_agent_read_write(self):
        env = os.environ.copy()
        cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            os.chdir(tmpdir)
            config_dir = Path(".aushu")
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "settings.local.yaml"
            config_file.write_text(textwrap.dedent(
                f"""\
tools:
  shell:
    allow:
      - 'git *'
      - 'python *'
    deny:
      - 'rm -rf *'
paths:
  allow:
    - '{str(Path(tmpdir).resolve())}/**'
"""
            ))
            f = Path("hello.txt")
            a = Agent()
            res = a.run(f"write {f} hello-world")
            self.assertEqual(res["action"], "write")
            res = a.run(f"read {f}")
            self.assertIn("hello-world", res["content"])
            os.chdir(cwd)
        os.environ.clear()
        os.environ.update(env)

    def test_cli_providers_list(self):
        exit_code = main(["providers"])
        self.assertEqual(exit_code, 0)

    def test_cli_models_list(self):
        exit_code = main(["models", "openai"])
        self.assertEqual(exit_code, 0)

    def test_cli_model_set_get(self):
        env = os.environ.copy()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            exit_code = main(["model", "set", "openai:gpt-4o-mini"])
            self.assertEqual(exit_code, 0)
            exit_code = main(["model", "get"])
            self.assertEqual(exit_code, 0)
        os.environ.clear()
        os.environ.update(env)

    def test_cli_setup_wizard(self):
        env = os.environ.copy()
        cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            os.chdir(tmpdir)
            with patch("builtins.input", side_effect=["n", "openai", "openai:gpt-4o-mini", "always-ask", "y"]):
                exit_code = main(["setup"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(".aushu") / "settings.local.yaml").exists())
            config_text = (Path(".aushu") / "settings.local.yaml").read_text()
            self.assertIn("always-ask", config_text)
            exit_code = main(["model", "get"])
            self.assertEqual(exit_code, 0)
            os.chdir(cwd)
        os.environ.clear()
        os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
