# Context and workflow reminders

Use this policy across skills; read once and reuse. Reassess at task start, a material scope change, completed planning/exploration, a meaningful implementation boundary, context pressure/confusion, and before a pause or final report. Reminders guide the user's next action and do not change the authorized scope. Preserve an explicitly selected workflow rather than rerouting it on every turn.

## Plan, apply, and close

- A concrete feature/fix request can go directly through apply without an explicit skill mention or a separate planning approval. A small change needs a receipt, not ceremony.
- If desired behavior or a consequential design decision is unresolved, identify that decision and use planning within an authorized build, or suggest plan when the user is only exploring. Do not turn “plan only” into implementation. Once a planning-only request is delivered, give a paste-ready apply prompt for its actual record if implementation is the next useful step.
- Apply normally verifies and closes its own work. Before claiming completion, check whether required verification, spec reconciliation, and archiving are finished. If those remain, carry them out within the authorized task; if blocked or deliberately stopped, give the exact blocker and a close prompt when closeout is the appropriate next action. Missing implementation belongs to apply, not a premature close reminder.
- Respect lightweight alternatives: receipt-only tiny work does not need a project archive, and crunch/polish do not inherit a separate plan/close ceremony unless the project or user requires it. Status and reviews recommend actions without implementing them. Completed work needs no close reminder.

## Keep, compact, or start fresh

| Observed situation | Recommendation |
| --- | --- |
| Short/coherent task; useful context fits comfortably | Keep the current conversation. No reset reminder is needed unless the user asks. |
| Same task, valuable reasoning still relevant, but host reports context pressure or long logs/exploration crowd out current work | Compact after checkpointing to retain continuity with less history. |
| Exploration is settled into a sufficient durable plan, and the next substantial implementation phase would benefit from discarding obsolete alternatives | Start a fresh conversation/worker from the checkpoint when the benefit exceeds the handoff cost. A small plan-to-code transition does not justify a reset. |
| Starting unrelated work, or superseded decisions repeatedly contaminate the current task despite correction | Prefer a fresh conversation after preserving the current task's state. Establish the actual cause; repeated code failures alone do not justify clearing context. |
| Important constraints exist only in chat, or an active worker/job has unaccounted ownership | Save and verify the checkpoint and resolve ownership before recommending a destructive context transition. Do not interrupt jobs merely to reset context. |

Compaction summarizes history; fresh context discards it from the new conversation. A fork, a resumed chat, or a model switch is not proof of fresh context. Use actual host pressure signals or concrete confusion; do not invent token percentages, exact remaining capacity, or fixed turn-count thresholds. Keep host auto-compaction enabled.

When a transition is worthwhile, feedback should say **which action, why now, the saved checkpoint path, and the exact resume prompt**. Prefer a single line plus the prompt, not a recurring warning. Record the recommendation and whether it was actually performed in the receipt; repeat only when the situation materially changes. An optional recommendation should not stop feasible authorized work. If the user requires a fresh context before proceeding, honor that stopping point.

## Checkpoint before transition

Save and read back scope, accepted decisions, current paths, verified/failed/unrun checks, remaining work, exact next action, and owner/job state in the existing work record/receipt. Keep one authoritative task list. If writes are forbidden or unavailable, provide the checkpoint in chat for the user to carry forward and disclose that it is not durable.

Use a resume prompt containing the real project and record/receipt paths, the selected workflow, next action, and any stopping restriction. For example, adapt this to the actual host and task:

```text
Use the apply skill in <project path>. Read <work record> and <receipt>.
Confirm current files and ownership, then continue <next action> through
the authorized checks and closeout. Preserve <constraints>.
```

When the current agent relinquishes execution, finalize the receipt as paused (or complete if its request is done) and release/transfer ownership. Compaction while the same request continues keeps the same session. A new user request in a fresh chat gets a linked receipt with the same Work ID. Inspect current files again after a transition.

Only perform a context transition through an available, authorized host control. A manual slash command printed in chat is guidance to the user, not an executed tool or shell command. Do not manipulate host session files, clear durable memory, start nested clients, or stop background jobs to simulate a reset. If controls are unavailable, give the manual action and resume prompt once.

## Host command names

Use the actual host's command menu when available; availability can vary by surface/version. Do not treat the user's word “clean” as authorization to stop jobs or delete files.

- **Codex CLI:** `/compact` summarizes the current conversation; `/new` starts a fresh chat, and `/clear` also starts fresh while clearing the terminal view. `/clean` is an alias for `/stop`, which stops background terminals; it is not context cleanup. [Official commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).
- **Claude Code:** `/compact` summarizes while continuing the conversation; `/clear` starts an empty-context conversation. [Official commands](https://code.claude.com/docs/en/commands).
- **Other surfaces:** use the supported compact or new-chat action. Do not guess a slash command or claim a tool exists from CLI documentation alone.
