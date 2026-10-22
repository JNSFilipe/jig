# Context and workflow reminders

Read once and reuse. Reassess at task start, scope changes, settled exploration/planning, meaningful implementation boundaries, context pressure/confusion, and before pause/final report. Reminders do not change authorized scope or override an explicit workflow.

## Plan, apply, close

- Concrete builds/fixes can go directly through apply: small work needs a receipt, not ceremony. Unresolved consequential behavior needs planning within an authorized build; exploring or planning-only requests do not authorize implementation.
- After a planning-only deliverable, give a paste-ready apply prompt for its actual record if useful. Do not require another approval for already authorized implementation.
- Apply normally verifies and closes its own work. Complete required checks, spec reconciliation, and archive before claiming completion; otherwise record the blocker and exact next step. Missing implementation belongs to apply, not premature close. Tiny receipt-only work needs no project archive; crunch/polish do not inherit extra plan/close stages.
- Status/reviews recommend without implementing. Completed work needs no close reminder.

## Routine context decision

| Situation | Action |
| --- | --- |
| Short/coherent task; useful context fits | Keep context; no reset reminder |
| Same task but host pressure or long logs crowd out useful history | Compact for continuity when worthwhile |
| Settled substantial exploration; sufficient executable checkpoint; transfer benefit exceeds cost | Prefer a fresh worker/conversation |
| Unrelated work or superseded decisions repeatedly contaminate reasoning | Consider fresh context after preserving state |
| Constraints only in chat or unaccounted worker/job | Save missing state and resolve ownership before destructive transition |

Use actual host signals, not invented token percentages or turn quotas. Repeated code failures require diagnosis, not automatic resets. Keep the host's configured automatic context management; do not override an extension's compaction policy.

Only when a transition is worthwhile/requested, read [transition procedure and host commands](context-transitions.md). It distinguishes compact/fresh/model switch, Pi/Blackhole behavior, checkpoint freshness, ownership, and resume prompts. Do not load it merely to keep the current conversation. Routine reports use the memory freshness check; load `feedback/SKILL.md` for consequential decisions or complex evidence reporting.
