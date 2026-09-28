"""Check distribution drift in this checkout and sync behavior in disposable copies."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_reporting_dependency_resolves_in_standalone_and_plugin_skills(self):
        for base, prefix in ((ROOT / "skills", "jig-"), (ROOT / "plugins/jig/skills", "")):
            feedback = f"{prefix}feedback/SKILL.md"
            for entrypoint in base.glob("*/SKILL.md"):
                if entrypoint.parent.name == f"{prefix}feedback":
                    continue
                with self.subTest(skill=str(entrypoint)):
                    references = re.findall(r"`([^`]+/SKILL\.md)`", entrypoint.read_text())
                    self.assertIn(feedback, references)
                    self.assertTrue((base / feedback).is_file())

    def test_every_skill_can_reach_its_bundled_memory_contract(self):
        shared = (ROOT / "skills/_shared/memory.md").read_bytes()
        context = (ROOT / "skills/_shared/context.md").read_bytes()
        memory_links = re.findall(r"\]\(([^)]+)\)", shared.decode())
        self.assertIn("context.md", memory_links)
        for entrypoint in (ROOT / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=entrypoint.parent.name):
                links = re.findall(r"\]\(([^)]+)\)", entrypoint.read_text())
                self.assertIn("references/memory.md", links)
                self.assertEqual((entrypoint.parent / "references/memory.md").read_bytes(), shared)
                self.assertEqual((entrypoint.parent / "references/context.md").read_bytes(), context)
                plugin = ROOT / "plugins/jig/skills" / entrypoint.parent.name.removeprefix("jig-")
                self.assertEqual((plugin / "references/memory.md").read_bytes(), shared)
                self.assertEqual((plugin / "references/context.md").read_bytes(), context)

    def test_guardrails_routes_resolve_after_plugin_rewrite(self):
        for base, name, prefix in ((ROOT / "skills", "jig-guardrails", "jig-"),
                                   (ROOT / "plugins/jig/skills", "guardrails", "")):
            text = (base / name / "SKILL.md").read_text()
            routes = re.findall(r"`([a-z-]+/SKILL\.md)`", text)
            for target in ("apply", "plan", "close", "debug", "crunch", "polish",
                           "remote", "status", "feedback", "consistency"):
                relative = f"{prefix}{target}/SKILL.md"
                with self.subTest(distribution=str(base), target=target):
                    self.assertIn(relative, routes)
                    self.assertTrue((base / relative).is_file())

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

    def test_shared_source_updates_every_standalone_and_plugin_copy(self):
        source = self.root / "skills/_shared/memory.md"
        updated = source.read_bytes() + b"\nShared contract revision for this fixture.\n"
        source.write_bytes(updated)
        before = {path: path.read_bytes() for path in self.root.rglob("memory.md")}
        self.assertIn("shared reference", self.sync("--check", success=False))
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)
        self.sync()
        for entrypoint in (self.root / "skills").glob("*/SKILL.md"):
            self.assertEqual((entrypoint.parent / "references/memory.md").read_bytes(), updated)
            plugin = self.root / "plugins/jig/skills" / entrypoint.parent.name.removeprefix("jig-")
            self.assertEqual((plugin / "references/memory.md").read_bytes(), updated)
        self.sync("--check")

    def test_shared_bundle_drift_is_detected_without_writes_and_repaired(self):
        bundled = self.root / "skills/jig-status/references/memory.md"
        bundled.write_text("stale bundle")
        self.assertIn("shared reference", self.sync("--check", success=False))
        self.assertEqual(bundled.read_text(), "stale bundle")
        self.sync()
        self.assertEqual(bundled.read_bytes(), (self.root / "skills/_shared/memory.md").read_bytes())
        bundled.unlink()
        self.sync("--check", success=False)
        self.assertFalse(bundled.exists())
        self.sync()
        self.assertTrue(bundled.is_file())
        self.sync("--check")

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
        bundled = self.root / "skills/jig-status/references/memory.md"
        bundled.write_text("preserve until preflight succeeds")
        self.assertIn("Plugin-only", self.sync("--check", success=False))
        self.sync(success=False)
        self.assertEqual(extra.read_text(), "preserve this")
        self.assertEqual(bundled.read_text(), "preserve until preflight succeeds")
