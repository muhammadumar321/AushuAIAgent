from pathlib import Path
import sys
import tempfile
import os
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aushu_permissions.config import PermissionsConfig, load_permissions_config, save_permissions_config
from aushu_permissions.checker import PermissionChecker


class TestPermissions(unittest.TestCase):
    def test_permission_config_save_and_load(self):
        env = os.environ.copy()
        cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            os.chdir(tmpdir)
            config = PermissionsConfig(mode="accept-edits", tools={"shell": {"allow": ["git *"], "deny": ["rm -rf *"]}}, paths={"allow": [{"path": f"{tmpdir}/projects/**", "write": True}], "deny": ["~/.ssh/**"]})
            save_permissions_config(config)
            loaded = load_permissions_config()
            self.assertEqual(loaded.mode, "accept-edits")
            self.assertIn("git *", loaded.tools["shell"]["allow"])
            os.chdir(cwd)
        os.environ.clear()
        os.environ.update(env)

    def test_permission_checker(self):
        config = PermissionsConfig(mode="allow-all", tools={"shell": {"allow": ["git *"], "deny": ["rm -rf *"]}}, paths={"allow": ["/tmp/**"], "deny": ["/tmp/secret/**"]})
        checker = PermissionChecker(config)
        self.assertTrue(checker.is_tool_allowed("shell", "git status"))
        self.assertFalse(checker.is_tool_allowed("shell", "rm -rf /tmp/test"))
        self.assertTrue(checker.is_path_allowed("/tmp/log.txt"))
        self.assertFalse(checker.is_path_allowed("/tmp/secret/data"))


if __name__ == "__main__":
    unittest.main()
