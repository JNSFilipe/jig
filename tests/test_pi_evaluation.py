"""Offline checks for the opt-in live evaluator; no Pi/model calls in normal CI."""

from pathlib import Path
import json
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = runpy.run_path(str(ROOT / "scripts/evaluate-pi.py"))


class PiEvaluationTests(unittest.TestCase):
    def test_observation_protects_all_files_additions_and_deletions(self):
        before = {"app.py": b"app", "tests/test_app.py": b"tests", "diff.txt": b"diff",
                  "snapshot/skills/example.md": b"skill"}
        after = {**before, "tests/test_app.py": b"weakened", "new.txt": b"new"}
        del after["snapshot/skills/example.md"]
        changed = EVALUATOR["protected_changes"](before, after, "recorded")
        self.assertEqual(changed, ["new.txt", "snapshot/skills/example.md", "tests/test_app.py"])
        for case in ("ephemeral", "no-writes", "promoted", "review"):
            self.assertEqual(EVALUATOR["protected_changes"](before, after, case), changed)

    def test_only_authorized_receipts_and_runtime_artifacts_are_excluded(self):
        changes = {".memory/sessions/report.md": b"receipt"}
        for case in ("recorded", "promoted", "tiny", "substantial", "nested", "worker"):
            self.assertEqual(EVALUATOR["protected_changes"]({}, changes, case), [])
        for case in ("ephemeral", "no-writes", "review"):
            self.assertEqual(EVALUATOR["protected_changes"]({}, changes, case), list(changes))
        changes = {".pi/artifacts/sessions/task/transcript.jsonl": b"runtime",
                   ".pi/task-registry.json": b"runtime", ".pi/agents/general.md": b"tampered"}
        for case in ("worker", "review"):
            self.assertEqual(EVALUATOR["protected_changes"]({}, changes, case), [".pi/agents/general.md"])
        self.assertEqual(len(EVALUATOR["protected_changes"]({}, changes, "no-writes")), 3)

    def test_snapshot_detects_modes_deletions_and_symlinks_without_following(self):
        with tempfile.TemporaryDirectory(prefix="jig-eval-unit-") as folder:
            project = Path(folder)
            path = project / "sample"
            path.write_text("original")
            path.chmod(0o600)
            before = EVALUATOR["project_snapshot"](project)
            path.chmod(0o644)
            self.assertIn("sample", EVALUATOR["protected_changes"](
                before, EVALUATOR["project_snapshot"](project), "no-writes"))
            path.unlink()
            path.symlink_to("nonexistent-target")
            self.assertEqual(EVALUATOR["project_snapshot"](project)["sample"],
                             ("symlink", "nonexistent-target"))
            path.unlink()
            self.assertEqual(EVALUATOR["protected_changes"](
                before, EVALUATOR["project_snapshot"](project), "review"), ["sample"])

    def test_metrics_require_actual_finalized_readback_and_successful_task_result(self):
        events = [
            {"type": "tool_execution_start", "toolName": "read", "toolCallId": "r",
             "args": {"path": "/fixture/.memory/sessions/receipt.md"}},
            {"type": "tool_execution_end", "toolName": "read", "toolCallId": "r",
             "result": {"content": [{"text": "Session status: active\\nSession next: fix"}]}},
            {"type": "tool_execution_end", "toolName": "task", "isError": True},
        ]
        metrics = EVALUATOR["event_metrics"](events)
        self.assertFalse(metrics["finalized_receipt_readback"])
        self.assertEqual(metrics["successful_task_results"], 0)
        events[1]["result"]["content"][0]["text"] = "Session status: complete\\nSession next: none"
        events[2]["isError"] = False
        metrics = EVALUATOR["event_metrics"](events)
        self.assertTrue(metrics["finalized_receipt_readback"])
        self.assertEqual(metrics["successful_task_results"], 1)

    def test_promoted_observation_rejects_false_feature_completion(self):
        receipt = "Session status: complete\nSession next: none\nWork state: unknown\nChecks: recorded FAILED test_blank; not rerun\n"
        verify = EVALUATOR["promotion_verdict_ok"]
        self.assertFalse(verify("Feature complete; all checks passed.", receipt))
        self.assertFalse(verify("Feature verification: passed", receipt))
        self.assertFalse(verify("Feature verification: not revalidated", receipt))
        self.assertFalse(verify("Feature verification: failed", receipt.replace("unknown", "complete")))
        self.assertFalse(verify("Feature verification: failed", receipt.replace("FAILED", "passed")))
        self.assertFalse(verify("Feature verification: failed\nFeature verification: passed", receipt))
        self.assertTrue(verify("Feature verification: failed\nReporting is complete; fix remains pending.", receipt))

    def test_committed_live_evidence_meets_recorded_rubrics(self):
        for name in ("evaluation-comparison-final.json", "evaluation-workflows-final.json",
                     "evaluation-promotion-final.json"):
            report = json.loads((ROOT / "docs" / name).read_text())
            for run in report["runs"]:
                with self.subTest(report=name, case=run["case"], revision=run["revision"]):
                    self.assertTrue(run["accepted"])
                    self.assertEqual(run["unauthorized_changes"], [])
                    self.assertEqual(run["model_errors"], [])
                    self.assertEqual(run["exit_code"], 0)
                    for key, amount in run["combined_usage"].items():
                        self.assertEqual(amount, run["usage"].get(key, 0) + run["child_usage"].get(key, 0))
                    if run["case"] in ("tiny", "substantial", "nested", "worker"):
                        self.assertTrue(run["independent_checks_passed"])
                        self.assertTrue(run["finalized_receipt_readback"])
                        self.assertEqual(run["receipt_count"], 1)
                    if run["case"] == "worker":
                        self.assertEqual(run["child_models"], [f"{report['provider']}/{report['model']}"])
                    if name == "evaluation-promotion-final.json":
                        self.assertTrue(run["discrepancy_preserved"])
                        self.assertFalse(run["independent_checks_passed"])  # intentionally broken feature

    def test_fixture_agents_and_oracles_do_not_use_personal_skill_installations(self):
        with tempfile.TemporaryDirectory(prefix="jig-eval-unit-") as folder:
            for case in EVALUATOR["CASES"]:
                project = Path(folder) / case
                EVALUATOR["prepare"](project, case)
                self.assertTrue((project / "AGENTS.md").is_file())
                self.assertTrue((project / "tests/test_app.py").is_file())
                prompt = EVALUATOR["prompt_for"](case, Path(folder) / "staged-skills")
                self.assertIn("staged-skills", prompt)
                self.assertNotIn("~/.agents", prompt)
            substantial = Path(folder) / "substantial"
            self.assertTrue((substantial / "docs/changes/export.md").is_file())
            self.assertTrue((substantial / "docs/specs/export.md").is_file())
            self.assertIn("archive closeout", EVALUATOR["prompt_for"]("substantial", Path("/fixture")))


if __name__ == "__main__":
    unittest.main()
