"""Instruction-contract regression tests, not a simulator of model/tool behavior.

Installation and terminal tests exercise real code separately. These checks keep
optional routing, authority, recovery and observation boundaries discoverable.
"""

import json
from pathlib import Path
import re
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text()


class PiWorkflowContractTests(unittest.TestCase):
    def test_pi_worker_example_uses_supported_contract_and_complete_handoff(self):
        execution = text("skills/jig-apply/references/context-and-execution.md")
        example = json.loads(re.search(r"```json\n(.*?)\n```", execution, re.S)[1])
        self.assertEqual(set(example), {"agent_type", "description", "cwd", "prompt"})
        self.assertTrue(Path(example["cwd"]).is_absolute())
        self.assertEqual(example["agent_type"], "general")
        for field in ("Goal:", "Read AGENTS.md", "Parent Work ID:", "Scope:",
                      "Write policy:", "Acceptance:", "Verification:", "Stop", "Return"):
            self.assertIn(field, example["prompt"])
        for boundary in ("no competing receipt", "redelegation", "archiving", "parent tasks"):
            self.assertIn(boundary, example["prompt"])
        for preserved in ("**Codex:**", "**Claude Code:**", "**Pi / pi-task:**",
                          "current-agent-only", "budget", "task_id", "do not poll",
                          "separate worktrees", "continue locally", "missing declared skills"):
            self.assertIn(preserved.lower(), execution.lower())

    def test_decision_presentation_is_optional_and_not_an_approval_gate(self):
        feedback = text("skills/jig-feedback/SKILL.md")
        plan = text("skills/jig-plan/SKILL.md")
        for rule in ("ask_user_question", "2–4 options", "description per option",
                     "(Recommended)", "Visible page only", "ask plainly",
                     "cancellation", "no-approval", "existing work record/receipt"):
            self.assertIn(rule.lower(), feedback.lower())
        for rule in ("ask_user_question", "otherwise ask conversationally",
                     "settled decisions", "planning-only", "no-writes"):
            self.assertIn(rule, plan)

    def test_authority_and_compaction_do_not_promote_remembered_success(self):
        memory = text("skills/_shared/memory.md")
        for rule in ("contextual evidence", "not instructions", "current project files",
                     "cannot silently complete", "do not mirror", "directly access their stores",
                     "before final response", "read back", "Work next / debt"):
            self.assertIn(rule.lower(), memory.lower())
        transition = text("skills/_shared/context-transitions.md")
        for rule in ("/compact", "/new", "pi-blackhole", "pi-claude-bridge",
                     "state changed or is missing", "without rewriting",
                     "not proof of fresh context", "worker", "ownership", "cache"):
            self.assertIn(rule, transition)

    def test_progressive_core_routes_safety_and_recovery(self):
        memory = text("skills/_shared/memory.md")
        for reference in ("context.md", "receipt-format.md", "memory-recovery.md",
                          "context-transitions.md", "observation-policy.md"):
            self.assertIn(f"]({reference})", memory)
        recovery = text("skills/_shared/memory-recovery.md")
        for scenario in ("crunch/sessions/", "polish/", "interrupted", "liveness unknown",
                         "cross-host", "active and archive", "Age", "jig-consistency/SKILL.md"):
            self.assertIn(scenario.lower(), recovery.lower())
        for skill in ("apply", "crunch", "plan", "status"):
            entry = text(f"skills/jig-{skill}/SKILL.md")
            self.assertNotIn("before the first report", entry)
            self.assertIn("freshness check", entry)
            self.assertIn("jig-feedback/SKILL.md", entry)

    def test_instruction_load_measurements_match_current_documented_paths(self):
        measurement = runpy.run_path(str(ROOT / "scripts/measure-instructions.py"))
        paths = measurement["load_paths"]()
        report = text("docs/instruction-loading.md")
        self.assertNotIn(measurement["FEEDBACK"], paths["tiny fix"][1])
        self.assertIn(measurement["TRANSITION"], paths["substantial change + handoff"][1])
        for name, (_, revised) in paths.items():
            self.assertEqual(len(revised), len(set(revised)), name)
            size, tokens = measurement["measure"](revised)
            rows = [line for line in report.splitlines() if line.startswith(f"| {name} |")]
            self.assertEqual(len(rows), 1, name)
            self.assertIn(f"{size:,} / {tokens:,}", rows[0])

    def test_recorded_ephemeral_promoted_and_nested_observation_contracts(self):
        policy = text("skills/_shared/observation-policy.md")
        # Each documented scenario has an explicit result; these are policy
        # assertions, not claims that a model executed the scenario correctly.
        for scenario, result in (
            ("Routine status, default policy", "One observation receipt"),
            ("explicit opt-in, all criteria met", "Zero receipts"),
            ("failed required check", "Promote to one observation receipt"),
            ("explicit no writes", "Zero writes"),
            ("Feedback nested in apply", "Reuse apply receipt"),
            ("requested history", "Normal receipt"),
        ):
            rows = [line for line in policy.splitlines() if scenario in line]
            self.assertTrue(any(result in line for line in rows), scenario)
        for exclusion in ("diagnosis", "handoff", "ownership", "verification evidence",
                          "Default: **recorded**", "no-writes/read-only wins"):
            self.assertIn(exclusion, policy)
        for skill in ("status", "consistency"):
            entry = text(f"skills/jig-{skill}/SKILL.md")
            self.assertIn("unrecorded", entry)
            self.assertIn("observation", entry)


if __name__ == "__main__":
    unittest.main()
