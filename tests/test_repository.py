"""Check distribution drift in this checkout and sync behavior in disposable copies."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_distribution_is_synchronized(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/sync-plugin.py"), "--check"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-sync-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("scripts", "skills", "plugins", ".claude-plugin"):
            shutil.copytree(ROOT / folder, self.root / folder,
                            ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))

    def sync(self, *args, success=True):
        result = subprocess.run([sys.executable, str(self.root / "scripts/sync-plugin.py"), *args],
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result.stdout + result.stderr

    def test_check_detects_content_drift_without_writing(self):
        destination = self.root / "plugins/jig/skills/apply/SKILL.md"
        destination.write_text("stale distribution")
        output = self.sync("--check", success=False)
        self.assertIn("apply/SKILL.md", output)
        self.assertEqual(destination.read_text(), "stale distribution")
        self.sync()
        self.assertNotEqual(destination.read_bytes(), (self.root / "skills/jig-apply/SKILL.md").read_bytes())
        self.sync("--check")

    def test_distribution_drops_the_prefix_and_rewrites_references(self):
        canonical = (self.root / "skills/jig-apply/SKILL.md").read_text()
        self.assertIn("name: jig-apply", canonical)
        self.assertIn("`jig-feedback/SKILL.md`", canonical)
        distributed = (self.root / "plugins/jig/skills/apply/SKILL.md").read_text()
        self.assertIn("name: apply", distributed)
        self.assertIn("`feedback/SKILL.md`", distributed)
        self.assertNotIn("jig-", distributed)
        self.assertFalse((self.root / "plugins/jig/skills/jig-apply").exists())

    def test_manifest_version_drives_marketplace_without_changing_other_fields(self):
        manifest_path = self.root / "plugins/jig/.claude-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["version"] = "9.8.7"
        manifest_path.write_text(json.dumps(manifest))
        market_path = self.root / ".claude-plugin/marketplace.json"
        before = market_path.read_bytes()
        self.assertIn("version", self.sync("--check", success=False))
        self.assertEqual(market_path.read_bytes(), before)
        self.sync()
        expected = json.loads(before)
        expected["version"] = "9.8.7"
        next(entry for entry in expected["plugins"] if entry["name"] == manifest["name"])["version"] = "9.8.7"
        self.assertEqual(json.loads(market_path.read_text()), expected)
        self.sync("--check")

    def test_plugin_only_work_is_preserved(self):
        extra = self.root / "plugins/jig/skills/plan/private-note.md"
        extra.write_text("preserve this")
        self.assertIn("Plugin-only", self.sync("--check", success=False))
        self.sync(success=False)
        self.assertEqual(extra.read_text(), "preserve this")
