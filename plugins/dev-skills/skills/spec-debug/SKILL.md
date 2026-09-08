---
name: spec-debug
description: Use automatically when encountering a bug, test or build failure, or unexpected behavior that needs diagnosis, before proposing a fix. Especially useful for uncertain causes, intermittent failures, and unsuccessful fixes. The user need not name this skill. Supports diagnosis-only requests and authorized repair.
---

# Diagnose a failure

Find an explanation supported by evidence, then verify a focused correction within the requested scope.

Apply this procedure when debugging becomes necessary during ordinary work; do not wait for a skill invocation or a separate request to investigate an in-scope failure. Scale the investigation to the problem. Use the active workflow and existing user/project preferences to choose one debugging procedure when several are available.

## Rules

- **Investigate before correcting.** Ground a proposed fix in observed evidence. Distinguish a hypothesis, an experiment, a confirmed cause, and a mitigation.
- **Keep experiments interpretable.** Change one relevant factor at a time where practical. Remove disproven experimental changes you introduced; preserve unrelated work.
- **Respect the request.** Read-only reviews make no edits. Diagnosis-only work stops at findings and the next action. Experiments obey the same permissions as ordinary commands, including on remote devices.
- **Preserve the contract.** Fixing a failure does not justify deleting coverage, weakening assertions, or changing intended behavior to match the defect.

## Process

### 1. Establish the failure

Read project instructions, the request or selected change record, and the relevant code and error output. State expected versus actual behavior and identify the smallest reproduction, inputs, environment, and frequency. Read the relevant stack trace before editing.

Check whether the test's expectation agrees with the user's accepted scenarios and latest decisions. A test may be stale; if the intended contract is unresolved, ask the user before changing either the test or behavior. Correct a demonstrably stale test only within authorized scope, preserving coverage of the agreed behavior.

Attempt the reproduction when permitted. If it is intermittent or unavailable, say what was observed and collect targeted evidence; failure to reproduce is not proof of correctness. Separate application defects from missing dependencies, permissions, and unavailable services.

### 2. Narrow the cause

Trace the failing value or operation toward its origin. Compare a working case and inspect relevant code, configuration, dependency, or environment changes. Read the reference portions needed to understand the difference.

For a reproducible regression with known working and failing cases, narrow the difference by bisection: use commit history when available, or reduce input/configuration differences; isolate checkout changes so the user's working files stay intact. Stabilize an intermittent reproduction before trusting a binary-search verdict.

At an uncertain component boundary, observe what enters and leaves it. Prefer existing logs or a read-only probe; add minimal temporary instrumentation only when authorized. Record presence, types, or redacted values instead of dumping credentials or whole environments.

### 3. Test an explanation

State: “I suspect X because Y; checking Z should distinguish it from the alternative.” For example, if filtered export fails but unfiltered export works, compare the filter passed to the exporter before changing CSV escaping.

Run the smallest discriminating experiment and record its actual result. A negative result should narrow the search, not trigger another speculative patch. When repeated fixes fail or introduce new symptoms, revisit assumptions and gather different evidence. Escalate consequential design decisions or missing access; a fixed attempt count does not establish an architectural defect. Honor any enclosing worker retry limit.

### 4. Correct, verify, and preserve findings

When fixing is authorized, make the smallest correction supported by the evidence. Add a regression test when useful, establishing that it fails for the original reason before the fix. For cases unsuitable for automation, record a reproducible manual check. Recheck the original scenario and relevant neighboring behavior; run required project checks.

If urgent containment is authorized before the cause is established, label it a mitigation and retain the unresolved investigation. An unavailable check remains unverified.

Keep hypotheses, ruled-out causes, experiments, and results in the existing record's Approach/Evidence; put the next experiment and ownership in Next before pausing or handing off. Tiny fixes need no record. If durable notes are needed and none exists, use one ordinary change record under the project's convention, normally docs/changes/. No separate debugging dossier is required.

Return findings to the enclosing workflow or assigned parent. An authorized implementation can continue through spec-apply when installed; otherwise report the correction, evidence, and remaining work. Diagnosis alone does not authorize closeout or publication.
