#!/usr/bin/env python3
"""Opt-in live Pi evaluation in disposable projects (may incur provider charges).

Normal CI never runs this. Requires an installed Pi and configured model auth.
Only auth/model metadata is copied to a private temporary agent directory; no
personal skills, settings, sessions or tmux servers are used as fixtures.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
CASES = ("tiny", "substantial", "recorded", "ephemeral", "no-writes", "promoted", "worker", "nested", "review")

TINY_CODE = 'def greet(name):\n    return "Hello, " + name.strip() + "!"\n'
TINY_TEST = '''import unittest
from app import greet
class GreetingTests(unittest.TestCase):
    def test_named(self): self.assertEqual(greet(" Ada "), "Hello, Ada!")
    def test_blank(self): self.assertEqual(greet("   "), "Hello, world!")
'''
EXPORT_TEST = '''import csv
import io
import unittest
from app import export_orders
class ExportTests(unittest.TestCase):
    rows = [{"id": 1, "status": "open", "owner": "a", "name": 'A, "quoted"'},
            {"id": 2, "status": "closed", "owner": "a", "name": "B"},
            {"id": 3, "status": "open", "owner": "b", "name": "secret"},
            {"id": 4, "status": "open", "owner": "a", "name": "D"}]
    def parsed(self, rows, owner="a", status=None):
        return list(csv.reader(io.StringIO(export_orders(rows, owner, status))))
    def test_header(self): self.assertEqual(self.parsed([]), [["id", "status", "name"]])
    def test_filter(self): self.assertEqual([r[0] for r in self.parsed(self.rows, status="open")][1:], ["1", "4"])
    def test_access(self): self.assertEqual([r[0] for r in self.parsed(self.rows, "b")][1:], ["3"])
    def test_all_matches(self): self.assertEqual(len(self.parsed(self.rows)), 4)
    def test_escaping(self): self.assertEqual(self.parsed(self.rows)[1][2], 'A, "quoted"')
    def test_immutable(self):
        import copy
        before = copy.deepcopy(self.rows)
        self.parsed(self.rows)
        self.assertEqual(self.rows, before)
'''


def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def prepare(project, case):
    project.mkdir()
    put(project / "AGENTS.md", """# Evaluation fixture
Write only within this disposable project and its explicit .memory/ root.
Use .memory/ as the established JIG memory root. Do not read personal files.
Required check: python3 -m unittest discover -s tests -v
Do not commit, publish, install packages or delegate unless explicitly asked.
No approval gate: implement authorized work through verification and closeout.
""")
    if case == "substantial":
        put(project / "app.py", 'def export_orders(rows, owner, status=None):\n    raise NotImplementedError\n')
        put(project / "tests/test_app.py", EXPORT_TEST)
        put(project / "docs/changes/export.md", """# Export authorized filtered orders
Work ID: export-fixture
Status: planned
## Scope
Implement CSV export of all authorized matches, preserving input order and input data.
## Behavior
Target: docs/specs/export.md
CSV header id,status,name; owner access filter; optional exact status filter;
all matches across pages; empty matches header-only; standard CSV quoting.
## Tasks
- [ ] Implement authorized filtered CSV export — check six supplied scenarios.
- [ ] Verify required suite, reconcile export spec and archive this record.
## Evidence
python3 -m unittest discover -s tests -v — not run.
## Next
Implement app.py, verify, update docs/specs/export.md and archive this record.
""")
        put(project / "docs/specs/export.md", "# Order export\n\nCSV export is not implemented yet.\n")
    else:
        put(project / "app.py", TINY_CODE if case in ("tiny", "worker", "nested") else TINY_CODE.replace('name.strip()', '(name.strip() or "world")'))
        put(project / "tests/test_app.py", TINY_TEST)
    if case in ("recorded", "ephemeral", "no-writes", "promoted"):
        greeting = project / "docs/changes/archive/greeting.md"
        put(project / "docs/specs/greeting.md", "# Greeting\n\nTrim named greetings; empty/whitespace-only input uses world.\n")
        put(greeting, """# Greeting
Work ID: greeting-fixture
Status: complete
## Scope
Greet named users and use world for whitespace-only names.
## Tasks
- [x] Implement both greeting cases.
## Evidence
python3 -m unittest discover -s tests -v — passed for supplied app.py.
## Next
none
""")
        if case == "promoted":
            put(project / "app.py", TINY_CODE)
            put(greeting, greeting.read_text().replace("— passed for supplied app.py.", "— FAILED: test_blank; required check remains failing."))


def prompt_for(case, skills):
    common = "Read AGENTS.md. Use only the explicit JIG skill installation at " + str(skills) + ". "
    if case in ("tiny", "substantial", "worker", "nested"):
        request = ("Fix greet so whitespace-only names produce Hello, world!, preserving trimmed named greetings."
                   if case != "substantial" else
                   "Implement export_orders(rows, owner, status=None): return CSV with id,status,name header, preserving input order, include only rows owned by owner and optional exact status matches. Export all matches, not one page. Empty matches are header-only, use standard CSV quoting, never mutate input. All requirements are settled.")
        executor = (" Use the exposed task tool with agent_type general, background false to delegate the app.py/tests slice. Parent owns the sole receipt and final verification/closeout. Return evidence from the worker, inspect actual edits then finish locally."
                    if case == "worker" else " Keep this task in the current agent; do not delegate.")
        record = " Use docs/changes/export.md and complete its required spec reconciliation and archive closeout." if case == "substantial" else ""
        nested = " After implementation, use jig-feedback as a nested progress report, reusing the enclosing receipt and owner, then finish the apply." if case == "nested" else ""
        return common + "Use jig-apply. " + request + record + executor + nested
    if case == "review":
        return common + "Call task with agent_type reviewer, background false. Read-only audit diff.txt and snapshot/ against the acceptance in review-context.md. Include parent_context and proposed_changes in the call. Return actionable path:line findings or no findings. Do not change files or execute model subcalls besides that reviewer."
    extra = "Use ephemeral observations for eligible routine status/feedback. " if case in ("ephemeral", "no-writes", "promoted") else ""
    if case == "no-writes":
        extra += "Explicit no writes: no receipt or source changes. "
    classification = (" Include one line 'Feature verification: passed', 'Feature verification: failed', or 'Feature verification: not revalidated', selected from the evidence. Preserve this classification in any permitted observation receipt." if case == "promoted" else "")
    return common + extra + "Use jig-feedback to summarize docs/changes/archive/greeting.md. Inspect relevant current code and recorded evidence. Do not run new checks or change source/work records. Deliver a concise report; distinguish completed reporting from feature completion." + classification


def event_metrics(events):
    tools = Counter()
    usage = Counter()
    calls = {}
    receipt_reads = set()
    finalized_readback = False
    task_successes = 0
    errors = []
    final = ""
    for event in events:
        if event.get("type") == "tool_execution_start":
            tools[event["toolName"]] += 1
            calls[event.get("toolCallId")] = event
            if event["toolName"] == "read" and ".memory/" in str(event.get("args", {})):
                receipt_reads.add(str(event.get("args", {}).get("path", "")))
        if event.get("type") == "tool_execution_end":
            start = calls.get(event.get("toolCallId"), {})
            if start.get("toolName") == "read" and ".memory/" in str(start.get("args", {})):
                content = "\n".join(part.get("text", "") for part in event.get("result", {}).get("content", []))
                finalized_readback |= "Session status: complete" in content and "Session next: none" in content
            if event.get("toolName") == "task" and not event.get("isError") and not event.get("result", {}).get("isError"):
                task_successes += 1
        if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant":
            message = event["message"]
            for key in ("input", "output", "cacheRead", "cacheWrite", "totalTokens"):
                usage[key] += message.get("usage", {}).get(key, 0)
            prose = [part.get("text", "") for part in message.get("content", []) if part.get("type") == "text"]
            if prose:
                final = "\n".join(prose)
            if message.get("stopReason") in ("error", "aborted"):
                errors.append(message.get("errorMessage", message["stopReason"]))
    return {"tool_calls": dict(tools), "usage": dict(usage), "receipt_read_calls": len(receipt_reads),
            "finalized_receipt_readback": finalized_readback, "successful_task_results": task_successes,
            "model_errors": errors, "final": final}


def project_snapshot(project):
    """Do not follow newly introduced symlinks outside the disposable fixture."""
    snapshot = {}
    for path in project.rglob("*"):
        if path.is_symlink():
            snapshot[str(path.relative_to(project))] = ("symlink", os.readlink(path))
        elif path.is_file():
            snapshot[str(path.relative_to(project))] = (path.stat().st_mode & 0o777, path.read_bytes())
    return snapshot


def protected_changes(before, after, case):
    changed = sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
    implementation = case in ("tiny", "substantial", "worker", "nested")
    def allowed(name):
        if case in ("worker", "review") and (name.startswith(".pi/artifacts/") or
                name in (".pi/task-registry.json", ".pi/task-session-history.json")):
            return True
        if (implementation or case in ("recorded", "promoted")) and name.startswith(".memory/"):
            return True
        if implementation:
            return (name == "app.py" or name.startswith(("tests/", "docs/changes/", "docs/specs/")) or
                    "__pycache__" in Path(name).parts)
        return False
    return [name for name in changed if not allowed(name)]


def promotion_verdict_ok(final, receipt_text):
    """A finalized report alone must not validate a false feature-completion claim."""
    lines = re.findall(r"(?mi)^\s*\**Feature verification:\**\s*([^\n]+)", final)
    return (len(lines) == 1 and lines[0].strip().lower().rstrip(".* ") == "failed"
            and bool(re.search(r"\b(?:failed|failing|failure)\b", receipt_text, re.I))
            and not re.search(r"(?mi)^Work state:\s*(?:assessment:\s*)?(?:complete|implemented)\b", receipt_text))


def run_case(args, base, skills, case, revision):
    label = f"{revision}-{case}"
    project = base / label
    prepare(project, case)
    agent = base / (label + "-agent")
    agent.mkdir(mode=0o700)
    for name in ("auth.json", "models.json", "models-store.json"):
        source = args.agent_dir / name
        if source.is_file():
            shutil.copyfile(source, agent / name)
            (agent / name).chmod(0o600)
    put(agent / "settings.json", json.dumps({"retry": {"enabled": False}, "cacheWarming": "off"}))
    home = base / (label + "-home")
    home.mkdir(mode=0o700)
    env = dict(os.environ, HOME=str(home), PI_CODING_AGENT_DIR=str(agent),
               JIG_MEMORY_HOME=str(project / ".memory"), PI_OFFLINE="1", PI_TASK_CHILD_NO_EXTENSIONS="1")
    env.pop("TMUX", None)
    env.pop("TMUX_PANE", None)
    command = [args.pi, "--no-extensions", "--no-skills", "--no-context-files", "--approve",
               "--no-session", "--mode", "json", "--provider", args.provider, "--model", args.model,
               "--thinking", args.thinking, "--skill", str(skills)]
    tmux_socket = None
    if case in ("worker", "review"):
        if not args.task_extension:
            raise ValueError("--task-extension is required for worker/review cases")
        # Override only fixture agents; do not repair/change bundled or user agents.
        for role in ("general", "reviewer"):
            put(project / f".pi/agents/{role}.md", f"---\ndescription: Isolated evaluation {role}\n"
                f"model: {args.provider}/{args.model}\nthinking: {args.thinking}\n"
                f"tools: {'read,grep,find,ls' if role == 'reviewer' else 'read,bash,edit,write'}\n"
                f"readonly: {'true' if role == 'reviewer' else 'false'}\n---\n"
                "Follow the bounded work order. Never redelegate, write receipts, archive or publish.\n")
        command += ["--extension", str(args.task_extension)]
        env["PI_TASK_BACKEND"] = "tmux"
        env["PI_SUBAGENT_FORWARD_JIG_MEMORY_HOME"] = str(project / ".memory")
        env["PI_SUBAGENT_FORWARD_PI_CODING_AGENT_DIR"] = str(agent)
        env["PI_SUBAGENT_FORWARD_HOME"] = str(home)
        tmux_socket = str(project / "fixture.sock")
        output = subprocess.check_output(["tmux", "-S", tmux_socket, "-f", "/dev/null", "new-session",
                                          "-d", "-P", "-F", "#{pid},#{pane_id}", "-s", "evaluation",
                                          "-x", "200", "-y", "60", "sleep", "900"], text=True).strip()
        pid, pane = output.split(",")
        env["TMUX"] = f"{tmux_socket},{pid},0"
        env["TMUX_PANE"] = pane
        if case == "review":
            put(project / "diff.txt", subprocess.check_output(["git", "diff", "--", ".", ":(exclude)plugins", ":(exclude)skills/*/references/memory.md", ":(exclude)skills/*/references/context.md"], cwd=ROOT, text=True))
            snapshot = project / "snapshot"
            for name in ("skills", "scripts", "tests", "docs"):
                shutil.copytree(ROOT / name, snapshot / name, ignore=shutil.ignore_patterns("__pycache__"))
            for name in ("README.md", "install.sh", "uninstall.sh"):
                shutil.copyfile(ROOT / name, snapshot / name)
            put(project / "review-context.md", "Review source snapshot and diff for GitHub issues 2-9: optional actual task/ask-user contracts, parent ownership, memory authority, portable installation, remote pane rejection, progressive safety/recovery, conservative opt-in ephemeral observations, Pi/Blackhole checkpoint behavior. No installer semantic change, no personal config edits. New files are in snapshot even if absent from tracked diff. Acceptance: no false completion, optional tools remain optional, standalone bundles self-contained, no command injection into coding-agent panes. Report concrete defects only.\n")
    before = project_snapshot(project)
    # Independent oracle is outside the worker's editable tree; never verify only
    # tests that the evaluated model could weaken or replace.
    oracle = base / (label + "-oracle")
    put(oracle / "test_oracle.py", EXPORT_TEST if case == "substantial" else TINY_TEST)
    start = time.monotonic()
    try:
        result = subprocess.run([*command, prompt_for(case, skills)], cwd=project, env=env,
                                stdin=subprocess.DEVNULL, text=True, capture_output=True, timeout=args.timeout)
    except subprocess.TimeoutExpired as error:
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
        diagnostic = decoded(error.stderr) + "\nEvaluation timed out.\n"
        if tmux_socket:
            panes = subprocess.run(["tmux", "-S", tmux_socket, "list-panes", "-a", "-F", "#{pane_id}"],
                                   text=True, capture_output=True, timeout=10).stdout.splitlines()
            for pane in panes:
                diagnostic += subprocess.run(["tmux", "-S", tmux_socket, "capture-pane", "-p", "-S", "-30", "-t", pane],
                                             text=True, capture_output=True, timeout=10).stdout
        result = subprocess.CompletedProcess(command, 124, decoded(error.stdout), diagnostic)
    finally:
        if tmux_socket:
            subprocess.run(["tmux", "-S", tmux_socket, "kill-server"], capture_output=True, timeout=10)
    # Take the post-run snapshot before our independent oracle can create caches.
    after = project_snapshot(project)
    unauthorized_changes = protected_changes(before, after, case)
    events = [json.loads(line) for line in result.stdout.split("\n") if line.startswith("{")]
    metrics = event_metrics(events)
    checks = subprocess.run(["python3", "-m", "unittest", "discover", "-s", str(oracle), "-v"],
                            cwd=project, env={**os.environ, "PYTHONPATH": str(project)},
                            text=True, capture_output=True)
    receipts = sorted((project / ".memory/sessions").glob("*.md"))
    receipt_text = "\n".join(p.read_text() for p in receipts)
    child_usage = Counter()
    child_models = set()
    child_errors = []
    child_files = []
    # Offline measurement of finished fixture children, never task polling or
    # access to personal sessions. Count persisted assistant messages only.
    for transcript in (project / ".pi").rglob("*.jsonl"):
        messages = []
        for line in transcript.read_text().split("\n"):
            if not line.startswith("{"):
                continue
            entry = json.loads(line)
            message = entry.get("message", {})
            if entry.get("type") == "message" and message.get("role") == "assistant":
                messages.append(message)
        if messages:
            child_files.append(transcript)
            for message in messages:
                for key in ("input", "output", "cacheRead", "cacheWrite", "totalTokens"):
                    child_usage[key] += message.get("usage", {}).get(key, 0)
                child_models.add(f"{message.get('provider')}/{message.get('model')}")
                if message.get("stopReason") in ("error", "aborted"):
                    child_errors.append(message.get("errorMessage", message["stopReason"]))
    changed_sources = [name for name, data in before.items()
                       if name in ("app.py", "docs/changes/archive/greeting.md") and after.get(name) != data]
    metrics.update(case=case, revision=revision, exit_code=result.returncode,
                   elapsed_seconds=round(time.monotonic() - start, 2),
                   independent_checks_passed=checks.returncode == 0, receipt_count=len(receipts),
                   receipt_finalized="Session status: complete" in receipt_text,
                   receipt_next_cleared="Session next: none" in receipt_text,
                   changed_observed_sources=changed_sources,
                   unauthorized_changes=unauthorized_changes,
                   archive_count=len(list((project / "docs/changes/archive").glob("*.md"))),
                   required_check_calls=sum(1 for e in events if e.get("type") == "tool_execution_start"
                                            and e.get("toolName") == "bash"
                                            and "python3 -m unittest discover -s tests -v" in e.get("args", {}).get("command", "")),
                   spec_reconciled=(case == "substantial" and
                                    "not implemented yet" not in (project / "docs/specs/export.md").read_text()),
                   child_transcript_count=len(child_files), child_usage=dict(child_usage),
                   child_models=sorted(child_models), child_errors=child_errors,
                   diagnostics="\n".join(line.strip() for line in result.stderr.splitlines()
                                           if "Error:" in line or "timed out" in line)[:1000])
    metrics["combined_usage"] = {key: metrics["usage"].get(key, 0) + child_usage.get(key, 0)
                                 for key in ("input", "output", "cacheRead", "cacheWrite", "totalTokens")}
    if case in ("tiny", "nested", "worker", "substantial"):
        accepted = (checks.returncode == 0 and len(receipts) == 1 and metrics["receipt_finalized"]
                    and metrics["receipt_next_cleared"] and metrics["required_check_calls"] > 0
                    and metrics["finalized_receipt_readback"])
        if case == "substantial":
            accepted = accepted and metrics["archive_count"] == 1 and metrics["spec_reconciled"]
        if case == "worker":
            accepted = accepted and metrics["successful_task_results"] == 1 and bool(child_files)
    elif case in ("recorded", "promoted"):
        accepted = (len(receipts) == 1 and metrics["receipt_finalized"] and metrics["finalized_receipt_readback"] and not changed_sources
                    and metrics["required_check_calls"] == 0)
    elif case == "review":
        accepted = metrics["successful_task_results"] == 1 and bool(child_files) and not changed_sources
    else:
        accepted = len(receipts) == 0 and not changed_sources and metrics["required_check_calls"] == 0
    if case == "promoted":
        metrics["discrepancy_preserved"] = promotion_verdict_ok(metrics["final"], receipt_text)
        accepted = accepted and metrics["discrepancy_preserved"] and checks.returncode != 0
    metrics["accepted"] = bool(accepted and result.returncode == 0 and not metrics["model_errors"]
                               and not unauthorized_changes and not child_errors)
    # Preserve private run evidence only until the temporary directory is cleaned.
    put(project / "events.jsonl", result.stdout)
    put(project / "checks.txt", checks.stdout + checks.stderr)
    for key in ("final", "diagnostics"):
        metrics[key] = metrics[key].replace(str(base), "<temporary-evaluation>")
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Explicitly authorize live model calls")
    parser.add_argument("--pi", default="pi")
    parser.add_argument("--agent-dir", type=Path, default=Path.home() / ".pi/agent")
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--thinking", default="low")
    parser.add_argument("--baseline", default="daee4a3")
    parser.add_argument("--task-extension", type=Path)
    parser.add_argument("--cases", nargs="+", choices=CASES, default=["tiny", "substantial"])
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--append", action="store_true", help="Append runs to an existing same-model report")
    args = parser.parse_args()
    if not args.run:
        parser.error("Live evaluation requires --run and may incur provider charges")
    report = {"started": datetime.now(timezone.utc).isoformat(), "provider": args.provider,
              "model": args.model, "thinking": args.thinking, "baseline": args.baseline,
              "pi_version": subprocess.check_output([args.pi, "--version"], text=True).strip(), "runs": []}
    if args.append and args.output.exists():
        previous = json.loads(args.output.read_text())
        for key in ("provider", "model", "thinking", "baseline", "pi_version"):
            if previous[key] != report[key]:
                parser.error(f"Cannot append a report with different {key}")
        report = previous
    with tempfile.TemporaryDirectory(prefix="jig-pi-eval-", dir="/tmp") as folder:
        base = Path(folder)
        baseline = base / "baseline"
        baseline.mkdir()
        archive = subprocess.check_output(["git", "archive", args.baseline, "skills"], cwd=ROOT)
        subprocess.run(["tar", "-xf", "-", "-C", str(baseline)], input=archive, check=True)
        revised = base / "revised/skills"
        shutil.copytree(ROOT / "skills", revised, ignore=shutil.ignore_patterns("__pycache__"))
        for case in args.cases:
            revisions = ("baseline", "revised") if case in ("tiny", "substantial") else ("revised",)
            for revision in revisions:
                skills = baseline / "skills" if revision == "baseline" else revised
                print(f"Running {revision}/{case}", flush=True)
                run = run_case(args, base, skills, case, revision)
                report["runs"].append(run)
                put(args.output, json.dumps(report, indent=2) + "\n")
                print(json.dumps({k: run[k] for k in ("case", "revision", "exit_code", "combined_usage", "receipt_count", "accepted")}), flush=True)
    return 0 if all(run.get("accepted", False) for run in report["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
