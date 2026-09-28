---
name: jig-status
description: Inventory repository plans, independent applies, crunch sessions, and polish follow-ups without changing project work, showing implementation, verification, blockers, and remaining work. Use when the user asks for the repo's overall work status or which planned and direct changes have been executed.
---

# Repository status

Answer what work exists, what has been implemented, what remains, and how well each conclusion is supported. Default to the current repository and all discoverable work, including completed history. Accept a project path or filters such as `unfinished only`, `plans only`, or a named feature. This is an inventory, not a request to implement, reconcile, archive, or publish anything.

Read and follow [the shared memory contract](references/memory.md) before starting. This report records only its own observation receipt; explicit read-only/no-writes instructions suppress that too. Do not let report receipts create feature rows or supersede implementation state.

## Discover the records

For progress, findings, decision questions, completion, and handoffs, read `jig-feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep this skill's repository-wide scope, inventory format, and memory owner. If unavailable, apply the shared memory pre-report freshness check and report the outcome, evidence, uncertainty, next action, and record path directly.

Read project instructions and identify the project root and its actual tracking conventions. Git is optional; when available, inspect the branch and working-tree summary without fetching or changing branches. Distinguish local implementation from commit, merge, or deployment state; a clean working tree does not mean all work is done.

Enumerate candidate records before reading their relevant sections. Include untracked records and the known local memory directories even when ignored by Git. Avoid dependencies, generated distributions, skill instruction files, templates, and example plans as work items. Follow established alternate layouts, including OpenSpec, rather than requiring a new schema.

| Source | What to inspect |
| --- | --- |
| Plans and change records | Project planning directories; by default `docs/changes/` and `docs/changes/archive/`. Read intent, status, tasks, evidence, next action, and links. Include independent apply records even when there was no separate planning session. |
| Other local task records | Existing plans, TODOs, implementation notes, and handoffs identified by project conventions. Treat a multi-file change as one item, not a row per artifact. |
| Shared sessions | `<memory-root>/sessions/` from the shared contract, including small plans/applies, debugging, and remote work. Filter Project metadata first, then group by Work ID and source links; separate Session status from Work state. Observation receipts provide findings only and do not change feature counts or authoritative state. |
| Legacy crunch/polish memory | The old crunch registry and nested polish follow-ups described in the shared contract. Include matching-project follow-ups with missing sources, flagging broken links. New receipts may continue this history; do not count old and new locations as separate changes. |
| Specs and current implementation | Linked capability specs, changed paths, tests, and relevant code. These help assess a record; a spec alone is not proof of a completed apply. |

Match external records by resolved project path or established repository/worktree identity, never just the directory basename. Do not import other projects' work. If a moved checkout cannot be confidently matched, report the coverage gap. Missing or inaccessible memory is a limitation, not proof that no sessions occurred. Do not search unrelated personal files or assume access to past chats or remote issue trackers.

## Reconcile work and evidence

When linked records contradict each other and ordinary inspection cannot support a reliable state, use an installed `jig-consistency/SKILL.md` for a bounded audit of that chain. Reuse this report's observation receipt and return to the inventory with findings; do not repair source records. Skip the extra audit when the normal freshness check suffices. If unavailable, inspect the conflict directly and report unresolved uncertainty.

- Link plans, applies, archives, crunch continuations, and polish passes using explicit references, stable IDs, and matching scope. Avoid merging unrelated work merely because titles resemble each other. Group linked phases under the same change, retaining links and the status of each recorded execution attempt. Count distinct changes separately from session attempts.
- Classify origin as `plan-led`, `independent apply`, `crunch`, or `unknown` only when evidence supports it. An apply can create its own plan record; the presence of a plan does not prove a separate planning session. Use `change (origin unknown)` when invocation history is unavailable. An absent apply record does not prove a plan was never implemented.
- Compare tasks and claimed results with the current affected files. Inspect enough code to support an implementation claim; filenames, checkboxes, a `complete` label, an archive location, and a commit message alone are insufficient. If that assessment would require a substantial audit, retain the recorded claim and mark current implementation `unknown` instead of overstating certainty.
- Keep implementation and verification separate. Describe implementation as `not started`, `partial`, `implemented`, or `unknown`, with the evidence basis. Use `not started` only when the record and inspected code support it. A failed check can coexist with implementation; it prevents calling the work verified complete.
- Describe checks as `passed for current code`, `recorded pass (not revalidated)`, `failed`, `not run`, or `unknown`. Reuse evidence only when its applicability is established. Default to inspection; do not run the entire test suite, install dependencies, or start services for an overview. Use a small non-mutating diagnostic only when it materially resolves uncertainty.
- Preserve lifecycle qualifiers such as `blocked`, `archived`, `cancelled`, or `superseded` separately. Session completion is not work completion: a completed plan can leave planned work, and a completed review leaves implementation unchanged. An old `active` session may be interrupted; call it currently running only with live evidence, otherwise label liveness unknown. A completed polish pass covers its own selected scope, not every shortcut in its source session. Report resolved debt from later supported continuations as resolved, retaining historical evidence. Show unresolved debt and conflicting records explicitly.

## Report

Start with the project/branch, a concise working-tree summary, and counts of distinct changes by assessed implementation state. Then show every discovered in-scope change in a compact table, ordering blocked and unfinished work before completed history:

| Work / record | Origin / linked sessions | Recorded state | Implementation | Verification | Remaining / next |
| --- | --- | --- | --- | --- | --- |

Use descriptive clickable record links and concrete evidence in cells, or a short note below a row when needed. Show task counts only when the record contains meaningful tasks; they measure recorded progress, not proof of implementation. Keep multiple session outcomes identifiable within a grouped row or a compact linked follow-up list. If the inventory is large, use compact sections or output batches and disclose any omitted range; never silently truncate an `all` request to recent work.

End with material discrepancies, blockers, and coverage limitations, including which sources were inspected and unavailable. Legacy tiny applies and chat-only plans may never have been recorded; new ones should have shared receipts unless writes were prohibited or failed. Missing history cannot be exhaustively reconstructed. Current unlinked edits can be reported as unattributed work, but do not invent an apply session or infer its intended scope. An empty inventory means no records were found in the inspected sources, not that the repository has no pending work.

Use the feedback reporting procedure to present this inventory and recommend the next action for unfinished items without executing it. Leave code, work records, historical receipts, checkboxes, and archives unchanged. Finalize and read back this report's observation receipt with the inspected sources, findings, limitations, and `Session next: none` when delivered; do not store a duplicate authoritative task inventory. Feedback supplies evidence and freshness discipline without starting a second report or receipt.
