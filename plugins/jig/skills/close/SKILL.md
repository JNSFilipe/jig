---
name: close
description: Verify a change against its requirements, reconcile durable specs, and archive completed work. Use for closeout or a verification-only review of an implemented change.
---

# Verify and close a change

Reconcile intended behavior, implementation, and the written contract.

Read and follow [the shared memory contract](references/memory.md) before starting. Reuse the enclosing receipt or open a new linked closeout receipt; explicit no-writes requests suppress receipt writes too.

## Rules

For progress, findings, decision questions, completion, and handoffs, read `feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep this skill's scope and memory owner. If unavailable, apply the shared memory pre-report freshness check and report the outcome, evidence, uncertainty, next action, and record path directly.

- **Review-only means no work edits.** Report findings without changing code, specs, task state, or archive files. Only the review's observation receipt may be written, unless the user requires no writes at all.
- **Completion requires evidence.** Incomplete scope, failing/unavailable required checks, and unresolved spec conflicts keep the change active.
- **Preserve the contract.** Never rewrite intended behavior to conceal a defect or discard unrelated requirements and scenarios.
- **Preserve history.** Never overwrite an archive entry.
- **Keep ownership clear.** Implementation workers return to the parent. Local closeout does not imply a commit, publication, or deployment.

## Process

### 1. Establish the current state

Read project instructions and inspect relevant files and local edits; Git is optional. Select the named active record or the one established in context, normally under `docs/changes/`. Ask when selection is ambiguous. An archived record needs no second archive; inspect it when explicitly asked to reverify or investigate.

Follow the project's existing conventions, including OpenSpec's native artifacts/schema. Read the record, affected code/tests, and linked baseline specs. After a handoff or compaction, reconstruct state from these files. For delegated implementation, wait for the worker to stop and resolve ownership or integration gaps.

### 2. Verify behavior against evidence

Assess:

- **Coverage:** each in-scope requirement and task has implementation and evidence; check behavior rather than checkboxes.
- **Correctness:** concrete scenarios, relevant error paths, and compatibility hold. A passing suite does not establish an untested scenario.
- **Consistency:** implementation and important design choices agree with the intended behavior.

Reuse check results still valid for current code, dependencies, and configuration. Run missing or invalidated checks and the project's required checks. Manual verification is appropriate when its steps and observations establish the behavior; distinguish passed, failed, and not run.

For an unexplained failing check, read an installed `debug/SKILL.md` directly, reusing it once loaded. Otherwise reproduce the failure and test a focused explanation. Keep the current scope: review-only diagnosis stays read-only; normal closeout may fix authorized defects. Return to verification afterward, keeping unresolved failures active.

During normal closeout, fix authorized scoped defects and reverify. During review-only work, report findings and stop here. Defer scope only when consistent with user direction, recording what was excluded. On a blocker, record the evidence and next action and leave the change active.

### 3. Reconcile baseline specs

Re-read the affected specs, normally `docs/specs/<capability>.md`, before writing: another change may have updated them. Resolve overlapping edits while preserving unrelated work.

Add new requirements, replace modified requirements with their complete resulting contract, and remove only explicitly retired behavior. Reconcile an existing addition instead of duplicating it. Write current behavior and scenarios in the project's style; retain motivation and test logs in the change record. A behavior-preserving refactor may need no baseline edit.

Check the resulting specs against verified implementation. Create specs only for touched capabilities.

### 4. Archive and report

After verification and reconciliation succeed, save the evidence with work `implemented`, then move the record to `docs/changes/archive/YYYY-MM-DD-<name>.md` or the existing convention. Only after the move succeeds, mark the archived work complete and update the receipt. Use a distinct suffix on collision and preserve contents and working links.

Keep the Work ID stable and set the receipt's Work record to the actual archive path. Complete both work and session only after reconciliation and archiving succeed; clear resolved blockers and obsolete Next entries. Read back the receipt and archived record before reporting. If interrupted between operations, inspect both locations on recovery; record the remaining step as blocked or paused without duplicating the archive. Receipt-only work needs no new project archive. A finished review finalizes its observation receipt, not the reviewed work's lifecycle.

Keep reconciliation and archiving together as one local operation. If interrupted, inspect current state and perform only the remaining edits.

Use the feedback reporting procedure for the final report, including delivered behavior, meaningful check results, limitations, and the final spec/archive paths.
