---
name: jig-consistency
description: Audit durable memory for broken links, contradictory work/session states, stale evidence, and unclear ownership. Use primarily when the user asks to check memory consistency; an existing workflow may use a bounded audit when conflicting records prevent reliable reporting or safe resumption. Ordinary progress updates need only the normal freshness check.
---

# Memory consistency

Check whether stored work history is internally coherent, reachable, and supported by current evidence. Default to an audit of the current project's memory, not repair or implementation. Accept a project path, receipt path, Session ID, or Work ID to narrow the audit. This is a point-in-time check; it cannot guarantee that later external changes leave memory current.

Read and follow [the shared memory contract](references/memory.md) before starting. A standalone audit gets its own receipt with `Mode: observation`; repository-wide audits use `Work ID: none`. When called inside a workflow, reuse its receipt without changing the caller's mode, Work ID, or owner; record the audit findings as observations. Do not treat a standalone audit receipt as feature work or a new authoritative implementation state.

For progress, findings, decision questions, completion, and handoffs, read `jig-feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep the audit scope and memory owner. If unavailable, apply the shared memory pre-report freshness check and report findings, evidence, uncertainty, next action, and record path directly.

## Select and inspect

Resolve the shared root and legacy locations through the memory contract. Read project instructions and enumerate project work records/archives, matching shared receipts, and relevant legacy crunch/polish records. Filter by project identity before reading unrelated records. Follow Source, Previous, Work ID, and Work record links only within the selected scope; clarify a genuinely ambiguous requested ID. Do not search unrelated personal files or require a memory migration.

Inspect receipts' actual field meanings rather than imposing the new schema on old records. Missing optional metadata or an older status vocabulary is not itself corruption. Resolve repository-relative paths using the record's project convention and absolute paths directly; `self` and `none` are special values, not missing files. Use stable identity and linked archive moves to resolve historical paths before calling them broken.

Compare the selected records with relevant current files, available check evidence, and exposed live ownership/process state. Do not run a full test suite, start services, contact remote devices, or resume jobs just to certify memory. If an external fact cannot be checked within the audit's scope, mark it unknown. Treat concurrent writes as a changing snapshot; re-read an affected record before concluding it contradicts another.

## Checks

| Area | Check |
| --- | --- |
| Reachability | Source/Previous/work-record links resolve directly or through a documented move; referenced archives, specs, and evidence are accessible. Distinguish absent from inaccessible. |
| Identity and history | Session IDs are unique; one Work ID follows one coherent change. Detect unintended cycles in Source/Previous chains, orphaned follow-ups, cross-project links, conflicting concurrent continuations, and duplicate active/archive records. A Work record of `self` is valid, and multiple sessions sharing one Work ID are expected. |
| Session lifecycle | Completed sessions have no pending Session next or retained execution owner. Paused/blocked sessions explain the next step. An active label has supporting liveness evidence or is reported as liveness unknown; age alone proves neither interruption nor success. |
| Work lifecycle | Scope, tasks, outcomes, and required closeout agree. A completed plan/report/diagnosis can leave work unfinished; a completed polish pass covers only its selected improvements. Accepted debt does not imply an active session. Missing requirements or failing/unrun required checks do not support verified work completion. |
| Freshness | Check dates and evidence basis match what was actually observed. Later relevant edits invalidate affected checks. A refreshed receipt timestamp is not refreshed verification. Distinguish stale evidence from proof that the implementation is wrong. |
| Ownership and next actions | No conflicting writers or unsafe takeover. Resolved blockers/debt are not projected as current pending work; preserve their historical entries and use supported continuations for current state. Live remote jobs and idle retained panes are distinguished. |
| Observation isolation | Status, feedback, audits, and reviews are not counted as feature changes or used to supersede implementation state. Audit findings do not silently rewrite the records being audited. |

Do not equate lack of recorded history with lack of work. Separate **confirmed inconsistency**, **unverified state**, and **coverage gap**. Examples: a completed session retaining a pending Session next is a contradiction; an old active session with no available liveness signal is unverified; an inaccessible registry is a coverage gap. A missing new-schema field in a legacy record may simply limit confidence.

## Report and finish

Use feedback to report the scope and observation time, inspected sources/counts, and a compact findings list or table with record links, the conflict, supporting evidence, consequence, and recommended correction. Lead with issues that could cause duplicate execution or false completion. Report `no inconsistencies found in inspected scope` only when that is what the evidence establishes; disclose unchecked areas and uncertainties. An empty registry means no records were available to audit, not a clean bill of health for all past work.

Save findings and coverage in the owned receipt, read it back, and finish the audit session when the requested inspection/report is delivered, even if it found defects. Use paused/blocked only when the requested audit itself cannot be completed. Do not complete an enclosing implementation session merely because its nested audit finished. Explicit read-only/no-writes instructions suppress even receipt writes.

## Optional reconciliation

An audit does not authorize repairs. If the user also asks to reconcile memory, apply only corrections supported by inspected evidence in the selected records. Preserve original outcomes and verification timestamps; record dated corrections with their before/after meaning, reason, and audit receipt link. Examples include fixing a confirmed moved-record pointer, clearing an obsolete blocker in the current owned work record, or marking a confirmed abandoned session interrupted. Do not delete history, invent missing sessions, merge ambiguous IDs, mark unknown work complete, or modify feature code under memory repair authority.

Before each correction, re-read the target and confirm ownership has not changed. Skip ambiguous/conflicting targets with a precise explanation while completing independent justified corrections. Re-read corrected records and rerun the affected consistency checks; record what changed and what remains unresolved. Reconciliation receipts stay observation records for feature counting, with explicit correction evidence; they do not become a new implementation session.

## Use inside other skills

Primarily run this on the user's request. Status may use it when linked records conflict and a bounded check would clarify the report; apply may use it when contradictory state or ownership blocks safe resumption. Ordinary reporting uses feedback's freshness check and needs no extra audit. Inspect only the affected chain, reuse the caller's receipt/ownership, and return findings to the caller. Do not call status/apply back, invoke this audit recursively through feedback, or add an automatic repair/approval stage. If this skill is unavailable, the caller can inspect the conflicting evidence directly and disclose uncertainty.
