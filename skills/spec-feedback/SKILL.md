---
name: spec-feedback
description: Ground progress updates, decision requests, completion summaries, and handoffs in the local spec workflow's change records and verification evidence. Use when reporting on a coding change or writing a question into its plan or handoff.
---

# Spec feedback

Let the user understand what works, what remains uncertain, and what decision matters without reconstructing the work. Apply this guidance within planning, implementation, or closeout; it adds no workflow step or report file.

Apply the same standard to questions written into a plan, design document, or handoff: the reader must be able to decide later without reconstructing this conversation.

## Look up the claim, not the whole tree

Use the change named by the user or established in the current task. If selection is ambiguous and changes the answer, clarify which change is meant. Follow existing project conventions; these paths are defaults, relative to the project root:

| What the user needs to know | Where to look |
| --- | --- |
| Intended outcome and scope | Selected `docs/changes/<name>.md`: Why / scope and Behavior |
| Progress, blocker, or next action | The same record: Tasks, Evidence, and Next |
| Existing behavior contract | The specific `docs/specs/<capability>.md` named by the change |
| Why an approach was chosen | Approach and any linked design document |
| What actually works | Relevant code and tests, plus check results valid for the current files |
| What a completed change delivered | Its exact record in `docs/changes/archive/`; inspect current code/specs if asked about behavior today |

Read only what supports the answer. Reuse context already inspected when it remains current. Search filenames or requirement names before reading more files; do not load every spec or scan the archive for a routine update. After closeout, use the record's new archive path.

A proposed requirement describes intent. A baseline spec describes the recorded contract. Neither a checked task nor an archived record proves current behavior. If they disagree with code or evidence, describe the discrepancy instead of claiming completion. Distinguish passed, failed, not run, and stale results. Do not rerun unchanged checks merely to write a summary.

If a tiny fix has no record, use the request, relevant files, and actual checks. Do not create workflow documents just to report. A reporting-only request does not authorize editing records, fixing code, or archiving work; leave those actions to the enclosing task.

## Make the answer usable

- Lead with the observable outcome or blocker. Describe what the user or caller can do, not the internal storage shape.
- Put evidence inside the claim: the scenario exercised, actual result, and any limitation. Include sample size or measurement conditions when they affect the conclusion. Separate observations from inferences; do not present a schema possibility as an observed problem. If inspection rules out the suspected scenario, drop it as a finding.
- When a decision concerns a payload, UI state, or data row, lead with the smallest relevant observed example and explain it afterward. Use an available read-only check when needed; do not expose secrets or unnecessary personal data. Label hypothetical examples and say when the real output has not been observed.
- Ask about concrete behavior and tradeoffs. Recommend an option and explain its consequence. Resolve file ownership, task numbering, and document placement yourself. Reuse decisions already made; reporting adds no approval gate.
- Match detail to the decision. A progress update explains what changed and what happens next. A completion summary states delivered behavior, meaningful verification, and remaining limitations. A handoff points to the selected record and its precise next action.

For example, replace “Should task 2 depend on task 1?” with “Should export include all matching orders or only the visible page? I recommend all matches so downloading does not silently omit orders.” First check whether the existing requirements already answer it.

Before sending or saving a question, check whether the reader must look up an identifier, understand a storage detail, or guess an option's consequence. Rephrase around the actual situation. If a factual claim could stay unchanged with different evidence, make it more specific.

Link the few files that let the user inspect the claim. Keep durable decisions and evidence in the existing change record under the enclosing workflow; do not duplicate them in a new status document or paste a transcript into the response.
