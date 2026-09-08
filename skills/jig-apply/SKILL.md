---
name: jig-apply
description: Implement or resume a change from a spec or local plan. Use when the user asks to build a planned feature, continue pending tasks, or run the lean spec workflow through completion.
---

# Apply a change

Deliver the requested behavior in verified slices, with a durable record of progress.

## Rules

- **Evidence determines completion.** Mark tasks complete only after their outcomes and checks pass. Missing dependencies and unavailable services mean unverified.
- **Preserve intent.** Never weaken a requirement to make a failing test pass. Reconcile behavior changes with the user's direction.
- **Respect ownership.** An implementation worker handles its assigned scope, returns evidence, and neither redelegates nor archives. The primary agent owns final verification and closeout.
- **Honor boundaries.** Respect requested models, stopping points, and review-only constraints. Local completion does not authorize publication, merging, or deployment.
- **Report real transitions.** A checkpoint or model switch does not clear history; claim a context reset only when the host performed it.

## Process

### 1. Select and inspect the work

Read project instructions and inspect relevant files and local edits; use version-control status when available. Select the record named by the user or established in context. Otherwise inspect active records, normally `docs/changes/*.md`, and ask if more than one plausibly matches. Resume an archived change only on an explicit request.

Read the selected record, linked constraints/specs, and affected code/tests. Reconcile the user's latest instructions and check completed tasks against actual files.

With no record, handle a trivial fix directly and run an appropriate check, keeping any affected existing spec accurate. For substantive work, use `jig-plan` if available; otherwise write one local record with scope, scenarios, approach, verifiable tasks, evidence, and next action. Follow existing project conventions, including OpenSpec's native schema and artifacts.

### 2. Choose context and executor

Reassess at the start, after a meaningful slice or long detour, and when context pressure or confusion appears:

| Situation | Action |
| --- | --- |
| Small or tightly coupled task; current context remains useful | Continue locally. Session length alone does not require a reset. |
| Substantial exploration finished; a bounded task is ready | Checkpoint; prefer one economical worker with fresh history when native tools permit it and the benefit exceeds transfer/review costs. |
| Host reports context pressure, or obsolete decisions repeatedly confuse work | Checkpoint; compact for continuity, or start fresh when the record is sufficient to resume. |
| Meaningful slice complete, pause, or upcoming long detour | Update tasks, evidence, decisions, ownership, and Next in the record; reset only if otherwise warranted. |
| Same failure persists after a correction | Revisit the diagnosis or escalate under the worker retry policy; clearing context alone does not fix the cause. |

Read [context and execution guidance](references/context-and-execution.md) before carrying out a handoff/reset or responding to a requested transition. Reuse it once loaded. The table above guides routine decisions without loading the reference.

Checkpoint before handing off or resetting. Prefer fresh task history over copying the planning conversation. Use host pressure signals and actual confusion to judge resets, rather than invented token thresholds. If controls are unavailable, preserve state, give a useful manual recommendation once, and continue feasible work. An explicit fresh-context requirement remains binding.

An assigned worker follows the work order and skips further delegation. A primary agent waits for delegated results and inspects the actual changes before closeout; it can perform independent read-only work while the worker writes.

### 3. Implement and check a slice

Choose the smallest pending outcome that exercises the real path through the affected layers. Implement it, then check its observable behavior before extending the solution.

For an unexplained failure, intermittent bug, or unsuccessful fix, read an installed `jig-debug/SKILL.md` directly and reuse it once loaded. Otherwise reproduce the failure, trace the cause, and test one explanation before correcting it. Keep diagnostic evidence in the same record; a known, localized cause needs no separate debugging step.

Derive checks from scenarios, including meaningful failures. Reuse project test frameworks. Reproduce bugs and add regression coverage when useful. For requested TDD, observe one intended test failure, implement until it passes, then refactor while green. Mechanical or documentation edits may need inspection rather than new tests.

Record the command or procedure, actual result, and behavior established. Run focused checks while iterating and required broader checks appropriate to the change. Update routine design decisions in place; reopen affected tasks and invalidate evidence after relevant changes.

### 4. Close or leave resumable progress

Checkpoint after meaningful verified slices and when pausing. Preserve partial results, failed/unrun checks, active ownership, and the exact next action.

An implementation worker returns its results to the parent. The primary agent reads and follows `jig-close` when available. Otherwise verify every in-scope scenario, reconcile only verified changes into the named baseline specs, and archive the record under `docs/changes/archive/YYYY-MM-DD-<name>.md`. Re-read specs before editing, preserve unrelated requirements, resolve conflicts, and choose a distinct archive name on collision. Incomplete scope or required checks keep the record active.

For updates and handoffs, read an installed `jig-feedback/SKILL.md` directly when useful; reuse it if already loaded. Otherwise report working behavior, evidence, remaining limitations, and the record's current path.
