# Context and execution

Use this at a substantial plan-to-build boundary, when context is becoming unhelpful, or when the user requests an execution handoff. The default is adaptive: preserve state automatically, delegate suitable implementation through available native tools, and keep small or tightly coupled work local. Do not add a setup phase.

## Checkpoint before shedding context

Maintain the existing change record at useful boundaries: after resolving a substantial plan, after a meaningful verified slice, before pausing/resetting, or before a detour likely to generate extensive unrelated output. Update facts in their existing sections. In Next, keep the pending action and only the handoff details not already elsewhere:

- Project root and selected record; relevant specs, design, code, and tests to read.
- Assigned outcome and editable scope, constraints, accepted decisions, and unresolved questions.
- Checks and their actual state; enough information to reproduce a failure, without full logs.
- Active worker/process identifiers and owned files, if any; the stop condition and who verifies/closes the change.

Do not discard context mid-edit or launch a replacement while another worker may still be writing. Finish or stop the active operation through supported controls, inspect partial changes, then record the state. After compaction or a handoff, re-read the record and inspect actual files before resuming. Do not blindly rerun completed tasks.

## Choose the appropriate context action

| Situation | Action |
| --- | --- |
| Short, coherent task; useful context already loaded | Continue in place |
| Plan settled after substantial exploration | Checkpoint; consider a fresh implementation worker |
| Host reports context pressure, or repeated confusion mixes obsolete decisions into the task | Checkpoint; compact for continuity or use fresh task history if the durable record is sufficient |
| A slice repeatedly fails for the same reason | Preserve the failure and revisit the approach; a reset alone is not a fix |
| Unrelated new work | Prefer a new context if the user/host authorizes it; retain the prior task's checkpoint |

Compaction summarizes history. A fresh worker/session starts without the previous conversation but still loads applicable instructions and tools. Model switching alone does neither. Use an actual exposed context-control tool when authorized; text such as `/compact` in an assistant response is not execution. A conversation fork or resumed worker may retain history, so do not label it clean.

If the host cannot perform the desired action programmatically, state that limitation once, give the checkpoint path and a ready-to-use resume prompt, and continue when practical. Stop for manual reset only if work cannot proceed reliably or the user required fresh context. Never delete transcripts, rewrite hidden session state, or bypass permissions to simulate a reset.

## Delegate only when the plan can travel

Use one implementation worker when all are true: the task is bounded and verifiable; the record captures the relevant decisions; the tool can start it without inherited conversation; it can access the correct project files; and delegation's expected benefit exceeds startup, rereading, and parent-review cost. When required by the host, the parent must have useful independent work, such as checking acceptance coverage while the worker implements.

Choose a supported model using explicit user preferences first, then an existing execution-model setting, then the host's current model catalogue. Prefer an economical coding model adequate for the slice. Use a supported moderate/default effort for routine implementation; reserve deeper reasoning for ambiguity, difficult debugging, or consequential design. Do not hardcode a universally cheapest model or assume the inherited model is cheaper. If availability or relative cost is unknown, say so and keep the current model unless the user supplied a valid choice. Avoid a pricing lookup for every slice.

Keep difficult design decisions with the planning agent. For tightly coupled or high-risk work where review and retries would dominate, retaining the capable agent can be more economical. Do not spin up a pool of workers merely to change models.

A work order can cover several consecutive tasks or the whole plan when it remains bounded and verifiable. Keep related work together to avoid paying startup and rereading costs for every checkbox.

Send a short work order, using actual paths and available skill names:

```text
Work in <project root>. Read project instructions, <change record>, and
<spec-apply SKILL.md path>. You are the implementation worker.
Implement <bounded task/outcome>. Read <relevant files>; edit only <scope>.
Use the record's constraints and acceptance scenarios. Run <checks>.
Update the assigned tasks and evidence in the record. Stop at <boundary>.
Do not redelegate, reconcile baseline specs, archive, or publish changes.
Return changed files, verified outcomes, failed/unrun checks, and blockers.
```

Do not include the planning transcript. Pass non-file constraints explicitly, including permission boundaries the host does not propagate. If using a separate workspace, transfer the record and relevant uncommitted files through supported mechanisms and reconcile the returned edits before verifying; sharing a repository name is insufficient.

While the worker runs, the parent may do independent read-only work but must not edit the worker's files or task record. Wait for completion, inspect changes and evidence, then own `spec-close`. Do not accept a worker's success message as verification. Reuse valid checks, adding those needed to cover missing scenarios or integration.

If the worker fails, inspect the actual failure first. Allow a focused correction when the approach is sound. If the same behavioral failure persists after that correction, return it to the parent/capable model instead of looping through cheap workers. Permission or environment failures need their underlying cause resolved, not a different model. Respect budget limits and record escalations concisely.

## Host capabilities

- **Codex:** use the callable subagent tool and its advertised model/effort parameters. With `fork_turns`, choose `"none"`; if a different control is exposed, use its documented no-history setting. Do not assume all Codex clients expose identical tools. Explicitly select a supported economical model when known; default inheritance does not establish savings.
- **Claude Code:** use a non-fork, write-capable subagent and a supported model override or configured execution agent. Read-only exploration/planning agents cannot implement. Pass the skill path because the worker may not inherit loaded skills. Host configuration can override model selection; record the actual model when observable, otherwise mark it unconfirmed.
- **Unavailable controls:** continue locally with a checkpoint and explain the missing capability. Do not create user-visible tasks, change global settings, or launch nested CLI sessions merely to work around a missing subagent/reset tool unless separately authorized by the user and allowed by the host.

Keep ordinary host auto-compaction enabled. Skills guide when to checkpoint and request a transition; they cannot guarantee exact context usage, model selection, or a reset that the host does not expose. Report what actually happened.
