"""Exercise real installation behavior in temporary projects; never change user config."""

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {"spec-plan", "spec-apply", "spec-close", "spec-feedback", "cmd-remote"}


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "project with spaces"

    def run_script(self, script, *args, success=True):
        result = subprocess.run(
            ["bash", str(ROOT / script), *map(str, args)],
            cwd=self.temp.name, text=True, capture_output=True, stdin=subprocess.DEVNULL,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def skill_parents(self):
        return [self.project / host / "skills" for host in (".claude", ".agents")]

    def test_copy_update_and_uninstall_preserve_unrelated_files(self):
        self.run_script("install.sh", "--local", self.project)
        self.assertFalse((self.project / ".git").exists())
        for parent in self.skill_parents():
            self.assertEqual({p.name for p in parent.iterdir()}, SKILLS)
            for name in SKILLS:
                self.assertEqual((parent / name / "SKILL.md").read_bytes(),
                                 (ROOT / "skills" / name / "SKILL.md").read_bytes())
            self.assertTrue((parent / "spec-plan/references/change-template.md").is_file())
            self.assertEqual(
                (parent / "spec-apply/references/context-and-execution.md").read_bytes(),
                (ROOT / "skills/spec-apply/references/context-and-execution.md").read_bytes(),
            )
            self.assertEqual(
                (parent / "cmd-remote/references/session-protocol.md").read_bytes(),
                (ROOT / "skills/cmd-remote/references/session-protocol.md").read_bytes(),
            )
            (parent / "unrelated").mkdir()
            (parent / "unrelated/keep.txt").write_text("keep")
            (parent / "spec-plan/SKILL.md").write_text("old version")
        self.run_script("install.sh", "--local", self.project)
        for parent in self.skill_parents():
            self.assertEqual((parent / "spec-plan/SKILL.md").read_bytes(),
                             (ROOT / "skills/spec-plan/SKILL.md").read_bytes())
        self.run_script("uninstall.sh", "--local", self.project)
        self.run_script("uninstall.sh", "--local", self.project)
        for parent in self.skill_parents():
            self.assertEqual({p.name for p in parent.iterdir()}, {"unrelated"})
            self.assertEqual((parent / "unrelated/keep.txt").read_text(), "keep")

    def test_symlinks_and_copy_conversion_leave_sources_intact(self):
        before = {p: p.read_bytes() for p in (ROOT / "skills").rglob("*.md")}
        self.run_script("install.sh", "--local", self.project, "--mode", "symlink")
        self.run_script("install.sh", "--local", self.project, "--mode", "symlink")
        for parent in self.skill_parents():
            self.assertEqual({p.name for p in parent.iterdir()}, SKILLS)
            for name in SKILLS:
                self.assertTrue((parent / name).is_symlink())
                self.assertEqual((parent / name).resolve(), ROOT / "skills" / name)
        self.run_script("install.sh", "--local", self.project)
        for parent in self.skill_parents():
            for name in SKILLS:
                self.assertFalse((parent / name).is_symlink())
        self.run_script("install.sh", "--local", self.project, "--mode", "symlink")
        self.run_script("uninstall.sh", "--local", self.project)
        for parent in self.skill_parents():
            self.assertFalse(parent.exists())
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)

    def test_dry_run_has_no_side_effects_and_global_paths_are_correct(self):
        self.run_script("install.sh", "--local", self.project, "--dry-run")
        self.assertFalse(self.project.exists())
        output = self.run_script("install.sh", "--global", "--dry-run")
        self.assertIn(str(Path.home() / ".agents/skills/spec-plan"), output)
        self.assertIn(str(Path.home() / ".claude/skills/spec-plan"), output)
        self.assertNotIn(".gemini", output)
        output = self.run_script("uninstall.sh", "--global", "--dry-run")
        self.assertIn("~/.agents/skills/", output)
        self.assertNotIn(".gemini", output)
        self.run_script("install.sh", "--local", self.project)
        self.run_script("uninstall.sh", "--local", self.project, "--dry-run")
        for parent in self.skill_parents():
            self.assertEqual({p.name for p in parent.iterdir()}, SKILLS)

    def test_bad_arguments_fail_before_writing(self):
        for script in ("install.sh", "uninstall.sh"):
            for args in (("--unknown",),):
                self.run_script(script, "--local", self.project, *args, success=False)
        self.run_script("install.sh", "--local", self.project, "--mode", success=False)
        self.assertFalse(self.project.exists())

    def test_parent_symlink_cannot_delete_canonical_skills(self):
        host = self.project / ".claude"
        host.mkdir(parents=True)
        (host / "skills").symlink_to(ROOT / "skills", target_is_directory=True)
        for script in ("install.sh", "uninstall.sh"):
            output = self.run_script(script, "--local", self.project, success=False)
            self.assertIn("Destination is the source skill", output)
        self.assertTrue((ROOT / "skills/spec-plan/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
