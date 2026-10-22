# Optional ephemeral observations

Default: **recorded**. This is an opt-in instruction policy, not a new setting understood by the installer or a runtime engine. The user can say “Use ephemeral observations for routine read-only status/feedback,” or put that preference in existing project/personal instructions. Do not add configuration files or registries. An unclear preference or uncertain eligibility falls back to a recorded receipt.

## Exact eligibility

Only a top-level **status or feedback** request that merely reads and reports already established state can skip its receipt, and only when all are true:

- The user/project explicitly opted in and did not request durable history.
- No implementation, planning, diagnosis with follow-ups, remote operation, meaningful audit, pause, or handoff is requested.
- No consequential new finding, accepted decision, unresolved discrepancy, blocker needing follow-up, or worker/process ownership needs preserving.
- No material progress or new verification evidence would be lost. Reusing existing valid evidence is fine; new substantive checks/results require recording.

Nested status/feedback always reuses the enclosing receipt and owner; it never creates a receipt or erases a required checkpoint. An enclosing apply/plan/debug/audit cannot become ephemeral by calling feedback. Implementation, plans (even chat-only), debugging, meaningful reviews/audits, pauses, handoffs, and ownership changes remain recorded.

For an eligible observation, do not create a placeholder receipt; deliver the answer and briefly disclose “Ephemeral observation; no receipt saved.” If a consequential finding or uncertainty emerges during inspection, promote to a normal observation receipt before reporting, retaining the inspected sources, finding, and next action without rewriting inspected work. Prefer a normal receipt from the start when such findings are likely.

**Explicit no-writes/read-only wins over promotion**: save nothing, disclose the consequential finding and unsaved follow-up in chat. Do not later backfill without authorization. This is the existing no-writes rule, not a policy failure.

## Coverage

Status and consistency must distinguish **unrecorded observation history** from absent feature work. Report that eligible ephemeral requests may be absent when the preference is known; never invent their count/content or infer that an empty registry means nothing happened. Observation receipts, recorded or omitted, never create feature rows, supersede work state, or change the authoritative Work ID/task list. Ordinary consistency audits themselves remain recorded unless writes were forbidden.

## Evaluation scenarios

| Request / condition | Expected result |
| --- | --- |
| Routine status, default policy | One observation receipt; no source edits |
| Routine status/feedback, explicit opt-in, all criteria met | Zero receipts; disclosure in chat |
| Opt-in feedback discovers a conflicting complete checkbox and failed required check | Promote to one observation receipt; report uncertainty, no source repair |
| Same conflict with explicit no writes | Zero writes; chat finding and unsaved next action |
| Feedback nested in apply | Reuse apply receipt, never skip its checkpoints |
| Planning, debugging with follow-up, meaningful audit, handoff, new evidence, or requested history | Normal receipt; no ephemeral exception |

For N eligible requests the deterministic file-count difference is N receipts versus zero; promotion makes it one for that request. This saves creation/finalization/readback I/O for omitted receipts, but forfeits their historical audit trail. No model-token or latency savings are assumed. Evaluate actual session overhead and recovery needs before opting in broadly; the conservative default preserves compatibility.
