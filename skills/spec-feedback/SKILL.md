---
name: spec-feedback
description: Report status, progress, findings, decisions, or a handoff for a coding change. Use for requests such as "what's done?", "how's it going?", or "what's next?", for completion summaries, and for questions written into a plan or handoff.
---

# Spec feedback

Find the evidence that answers the user's question and make the result understandable without reconstructing the work.

## Rules

- **Separate intent from observation.** Proposed requirements, baseline specs, checkboxes, and archive entries are not proof of current behavior.
- **State verification honestly.** Distinguish passed, failed, not run, and stale evidence. Confirm model/context transitions before describing them as executed; savings need measurements.
- **Keep reporting scoped.** A status-only request leaves project files unchanged. Use existing records; reporting needs no separate document.
- **Ask about behavior.** Resolve task numbering and document placement yourself. Questions in plans and handoffs need the same clarity as chat questions.

## Process

### 1. Identify the question and change

Determine whether the user needs status, a finding, a decision, completion evidence, or a handoff. Use the named change or the one established in the task. Clarify selection only when ambiguity changes the answer.

Follow the project's existing layout. Default active records are `docs/changes/<name>.md`; baseline specs are under `docs/specs/`, and completed records under `docs/changes/archive/`. For a tiny fix with no record, use the request, relevant files, and checks.

### 2. Read only the supporting evidence

| Question | Read |
| --- | --- |
| Intended outcome or scope | Selected record: Why / scope and Behavior |
| Progress, blocker, next action | Tasks, Evidence, and Next |
| Existing behavior contract | The capability spec named by the record |
| Reason for a design choice | Approach and any linked design document |
| What actually works | Relevant code/tests and check results valid for current files |
| What completed work delivered | Its exact archive record; current code/specs for behavior today |
| Model or context transition | Execution notes and actual host results |

Reuse inspected context while current. Search filenames or requirement names before broadening; follow only relevant links. After closeout, use the record's archive path. Rerun checks only when needed to establish missing or invalidated evidence.

### 3. Establish the claim

Check the concrete scenario before presenting it as a finding. Separate observed behavior from inference; if inspection rules out the suspected scenario, drop that finding. Surface disagreement between intent, files, and evidence instead of assuming completion.

Put relevant measurements, sample size, and conditions inside the claim. If the claim would stay unchanged with different evidence, make it more specific. For a payload, UI state, or data-row decision, lead with the smallest useful observed output and explain it afterward. Use an available read-only check when needed; protect secrets and unnecessary personal data. Label hypothetical examples and unobserved output.

### 4. Frame any decision

Describe what happens in a real situation, using terms the user understands rather than storage details. Give each option a concrete consequence and recommend one with a reason. First check whether existing requirements already decide it.

For example: “Should export include all matching orders or only the visible page? I recommend all matches so downloading does not silently omit orders.” This is answerable without looking up a task identifier.

Before sending or saving the question, check whether the reader must look up an identifier, understand a storage detail, or guess an option's consequence. Rephrase where needed. Reporting adds no approval gate.

### 5. Deliver the appropriate response

Lead with the observable outcome or blocker:

- **Progress:** what changed, what remains uncertain, and the next action.
- **Completion:** delivered behavior, meaningful checks, and limitations.
- **Handoff:** selected record, pending action, and any worker/process ownership needed to resume.
- **Context/model transition:** checkpoint and what actually happened, or the manual action still needed; name the model only when confirmed.

Link the few files needed to inspect the claim. Under an enclosing implementation task, keep durable decisions and evidence in the existing record. Avoid duplicating the record or pasting a transcript into the response.
