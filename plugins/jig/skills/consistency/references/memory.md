# Shared memory contract

This contract is bundled with every skill so each standalone installation can discover and maintain the same memory. Read it once per task and reuse it across skill transitions.

Also read [context and workflow reminders](context.md) once per task. Apply its plan/close reminders and keep/compact/fresh-context decisions at meaningful boundaries; report recommendations through the calling skill's feedback procedure and preserve a checkpoint before transitions.

## Storage and discovery

Resolve the memory root from an explicitly established shared root, otherwise `JIG_MEMORY_HOME` when set, otherwise `~/.local/share/jig/`. Expand it to an absolute path. An older custom crunch directory is a legacy lookup location, not automatically a new shared root. Never store runtime memory inside a skill installation. Do not require repository initialization or a memory service.

New session receipts live at `<memory-root>/sessions/YYYYMMDDTHHMMSSZ-<random-id>.md`. All skills use this directory. Match records to the absolute project path; include repository/worktree identity when available, but do not equate checkouts solely by basename or remote URL. Remote-only work may use `Project: none` with an explicit target. Search metadata first and read only relevant records.

Durable memory has two complementary parts:

- **Work record:** the authoritative scope, task list, evidence, and next action. Reuse the selected project record, normally `docs/changes/<name>.md`, its archive, or the project's native equivalent. Small work can keep this information in session receipts instead of creating a project document: the first captures scope and later linked continuations carry current progress.
- **Session receipt:** which request/skills ran, the work record or source session they concern, their actual outcome, and whether execution stopped. It links to the authoritative task list; do not duplicate that list in every receipt.

Lookup explicit paths first, then the shared registry by session ID, work ID, and project. Also inspect relevant project records, the legacy `~/.local/share/jig/crunch/sessions/` (or established custom crunch directory), and legacy `polish/<crunch-record-stem>/` follow-ups beside their source. Preserve old records in place; new receipts link to them. If the shared root differs from the default, still check the default legacy location when resolving old references. No bulk migration or invented history is needed.

Use one stable `Work ID` across a change and its continuations, including polish. Reuse an existing native ID or recorded Work ID; otherwise assign the first session ID. Add the ID to a writable work record when practical; with native schemas that cannot accept it, keep the mapping in the receipt. An older record can be mapped by its exact path. Record its current archive path after a move so other skills can resolve earlier links through the Work ID and receipt chain.

## Who writes

Create a receipt for each top-level skill request, including small plans, independent applies, diagnosis, remote work, status, and feedback. Reuse it across nested skills, tool calls, and continuations of that request; list the skills used. A subsequent request gets a new receipt with `Previous` pointing to the relevant prior session. One primary agent owns receipt writes. Workers return evidence or update explicitly assigned work-record sections; they do not create competing receipts or finalize the parent's state.

Observation requests (status, feedback, reviews, diagnosis-only) write only their own receipt unless project-record updates were separately authorized. They do not change the records they inspect. Set `Mode: observation`; use `Work ID: none` for repository-wide reports and reference the inspected work for a focused review. Reporting completion means the report was delivered, never that the underlying feature was implemented. An explicit read-only/no-writes instruction overrides receipt creation too: report in chat and disclose that no memory was written. Do not backfill those sessions later without authorization.

Implementation and planning requests maintain both their receipt and the project work record they own, when one exists. For receipt-only work, preserve previous receipts as history and put current progress in the new receipt with `Work record: self`, the same Work ID, and source/predecessor links. Carry unresolved scope forward without reopening or rewriting a completed planning/crunch session; the supported continuation chain is one logical work record. A small plan/apply/debug task needs at least a compact receipt even when no project document is justified. Do not add a second task list for an enclosing crunch or polish session. Loading a skill to author or review its instructions is not an invocation of its runtime workflow.

## Lifecycle and finalization

Create the receipt with `Session status: active` before starting the requested work. Record the request, mode, project, origin, owner, and known source/work links. Origin records how the change began (`plan-led`, `independent apply`, `crunch`, `debug`, `remote`, or `unknown`); append skills without rewriting that origin.

Checkpoint after a meaningful outcome, failure, scope change, or ownership transfer, and before context compaction. Record actual checks, invalidate evidence affected by new changes, and reconcile tasks and blockers with current files. For handoffs, record the recipient and pending process/job state. Release or transfer ownership explicitly.

**Pre-report freshness check:** before substantive progress, findings, decisions, completion, or handoff claims, compare saved state with the latest request and relevant current files/process observations. Recheck affected evidence after changes or context/ownership transitions; reuse still-valid evidence. Update owned writable memory for discovered changes and read back those updates before reporting. Observation/no-writes requests flag stale source records without rewriting them. If current truth cannot be established, report the last observation and uncertainty instead of presenting remembered state as current. Routine messages with no state change need no repeated writes or broad scans.

Record the observation time and relevant evidence basis (affected paths, known revision and uncommitted changes, configuration, or process/job identity as appropriate). A new receipt timestamp is not a new verification result; do not refresh a check's date unless it was actually rerun. Local notes cannot refresh themselves while no agent is running, so freshness must be established when used, not promised permanently.

Before every final response or deliberate pause, update **and read back** the receipt and any work record changed by this request. Ensure saved outcomes, current paths, blockers, ownership, and next actions agree with the response. A write failure means memory is not saved: disclose it and provide the compact checkpoint in chat while continuing safe work when possible.

| Session status | Meaning at handoff/final response |
| --- | --- |
| `complete` | This request's deliverable and required checks are finished. A finished plan/report/diagnosis does not imply implementation. |
| `paused` | Work remains but execution has deliberately stopped or been handed off. Record the next action and recipient, if any. |
| `blocked` | A specific dependency, decision, permission, or failed/unavailable required check prevents completing this request. Record what resolves it. |
| `cancelled` | The user cancelled this request. Preserve any partial result. |
| `interrupted` | A previously active session is confirmed to have ended without finalization; its implementation outcome may remain unknown. |

Never leave the session `active` after relinquishing execution. During an ongoing monitor request it can remain active while this agent is actually monitoring; at a handoff, use `paused` and describe any still-running external job. A persistent terminal left open is not an active task. Clear resolved blockers and obsolete next steps; use `Session next: none` on completion. Keep intentional future work in `Work next / debt`, not as pending execution of a completed session.

Track `Work state` independently: `planned`, `in-progress`, `implemented`, `complete`, `blocked`, `cancelled`, or `unknown`. `implemented` means the requested code is present but validation or required closeout remains. `complete` requires the agreed work scope, required checks, and any required spec/archive reconciliation. A completed planning session normally leaves work `planned`. A diagnosis can be complete while the fix is unimplemented. A completed polish request can leave unrelated debt, and cannot complete unmet original requirements.

Process crashes cannot be guaranteed a final write. On resuming owned work, inspect prior active receipts and live ownership before editing. Never infer completion, interruption, or safe takeover merely from age. If termination is confirmed, mark the abandoned receipt `interrupted` with the observation and link to the recovery session; preserve original results. If liveness is unknown, report `active (liveness unknown)` and resolve overlapping ownership before mutations. Observation-only requests flag stale or inconsistent records without repairing them. Explicit memory-reconciliation requests may repair states from evidence, but must not mark unknown work complete to eliminate pending entries.

## Compact receipt

Omit optional fields that add nothing; keep enough evidence to resume without a transcript.

```markdown
# Session: <request title>
Session: <unique filename stem>
Started: <UTC timestamp> | Updated: <UTC timestamp>
Project: <absolute path or none> | Target: <remote target if applicable>
Skills: <skills actually used> | Mode: planning / implementation / observation
Origin: <change origin or unknown>
Work ID: <stable ID or none> | Work record: <current absolute path, self, or none>
Source: <source session/record path or none> | Previous: <prior receipt path or none>
Session status: active
Work state: unknown
Owner: <agent/session ID while active; none when finished>
Request: <scope and user instructions>
Result: <changed paths or findings; actual outcome>
Checks: <commands/observations and passed, failed, not run, or stale>
Evidence basis: <observation time and relevant files/revision/configuration/process state>
Session next: <next action/blocker or none>
Work next / debt: <remaining feature work, shortcuts, or none>
```

For observation receipts, `Work state` is an explicitly labelled assessment, never a new authoritative lifecycle update. Status must exclude observation receipts from feature counts and must not select them as the latest implementation state. When work lives in receipts, retain the original scope through source links and use the latest relevant implementation/planning continuation supported by evidence; a later timestamp alone does not resolve conflicting concurrent branches. Record known branch/commit and process identifiers only when useful, omit secrets and raw logs, and never fabricate token savings.
