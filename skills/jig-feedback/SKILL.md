---
name: jig-feedback
description: Provide evidence-based reporting and memory freshness checks for every workflow skill's progress, findings, decisions, completion, and handoffs. Also answer change-specific status questions directly; jig-status owns repository-wide inventory discovery and uses this skill to report it.
---

# Feedback

Find the evidence that answers the user's question and make the result understandable without reconstructing the work.

Read and follow [the shared memory contract](references/memory.md) before starting. Resolve work through the shared registry and project/legacy records. Standalone feedback maintains only its observation receipt; within authorized implementation, update the existing receipt instead.

## Use from another skill

Read these instructions once before the first substantive report or decision question and reuse them throughout the request. This is a reporting procedure within the calling skill, not a separate agent, invocation, approval step, or new receipt. Preserve the caller's scope, output format, brevity, and ownership. Repository status keeps its multi-change inventory; remote work keeps its target and process evidence; crunch keeps concise updates. Do not redirect a calling skill back to itself or require one selected change for a repository-wide report.

Keep memory updates with the existing owner. Workers return findings to their parent without creating or finalizing receipts. Intermediate progress reports checkpoint meaningful changes but do not complete an ongoing session. A final report follows the caller's actual exit state; reporting itself cannot close unfinished implementation or broaden write authority.

## Rules

- **Separate intent from observation.** Proposed requirements, baseline specs, checkboxes, and archive entries are not proof of current behavior.
- **State verification honestly.** Distinguish passed, failed, not run, and stale evidence. Confirm model/context transitions before describing them as executed; savings need measurements.
- **Keep reporting scoped.** A status-only request leaves project work records unchanged. It saves only its compact observation receipt; explicit read-only/no-writes requests suppress that too.
- **Ask about behavior.** Resolve task numbering and document placement yourself. Questions in plans and handoffs need the same clarity as chat questions.

## Process

### 1. Identify the question and change

Determine whether the user needs status, a finding, a decision, completion evidence, or a handoff. Use the named change or the scope established by the caller, including a repository inventory or remote target. Clarify selection only when ambiguity changes the answer; do not narrow an intentional multi-item report to one change.

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

Apply the shared contract's pre-report freshness check before presenting substantive state claims. Compare the latest request and current relevant files/process observations with the saved scope, task state, checks, blockers, next steps, and ownership. After a handoff, external edit, new result, or changed requirement, refresh affected evidence rather than relying on the previously loaded record. A receipt's Updated timestamp alone does not make its evidence current.

When the caller owns writable work, reconcile supported changes in that work record and receipt before reporting; clear resolved blockers, invalidate affected check results, and read back changed memory. In observation/no-writes mode, preserve source records and label discrepancies or stale evidence in the report and any permitted observation receipt. If freshness cannot be established, state what was last observed and what remains unverified; do not claim completion from stale memory or run an unrequested broad audit. Avoid rereading unchanged context or rerunning still-valid checks for routine conversational updates.

Check the concrete scenario before presenting it as a finding. Separate observed behavior from inference; if inspection rules out the suspected scenario, drop that finding. Surface disagreement between intent, files, and evidence instead of assuming completion.

Put relevant measurements, sample size, and conditions inside the claim. If the claim would stay unchanged with different evidence, make it more specific. For a payload, UI state, or data-row decision, lead with the smallest useful observed output and explain it afterward. Use an available read-only check when needed; protect secrets and unnecessary personal data. Label hypothetical examples and unobserved output.

### 4. Frame any decision

Describe what happens in a real situation, using terms the user understands rather than storage details. Give each option a concrete consequence and recommend one with a reason. First check whether existing requirements already decide it.

For example: “Should export include all matching orders or only the visible page? I recommend all matches so downloading does not silently omit orders.” This is answerable without looking up a task identifier.

Before sending or saving the question, check whether the reader must look up an identifier, understand a storage detail, or guess an option's consequence. Rephrase where needed. Reporting adds no approval gate.

### 5. Deliver the appropriate response

Apply the shared [context and workflow reminders](references/context.md) at relevant boundaries. If action is needed, include one concise next-skill or context recommendation with the reason, real checkpoint path, and paste-ready continuation. Distinguish compact from fresh context and use the actual host's command names; never suggest `/clean` as context cleanup. Do not remind the user to perform closeout already completed, introduce extra workflow stages, repeat an unchanged reminder, or pause authorized work just to demand a skill mention.

Lead with the observable outcome or blocker:

- **Progress:** what changed, what remains uncertain, and the next action.
- **Completion:** delivered behavior, meaningful checks, and limitations.
- **Handoff:** selected record, pending action, and any worker/process ownership needed to resume.
- **Context/model transition:** checkpoint and what actually happened, or the manual action still needed; name the model only when confirmed.

Link the few files needed to inspect the claim, including the current receipt/work-record path at completion or handoff. Under an enclosing implementation task, keep durable decisions and evidence in the existing record and receipt without finalizing ongoing execution prematurely. Before a final response, save and read back owned memory, checking that the reported state matches it. A delivered standalone report completes its observation session only; flag stale work states without repairing them unless requested. Disclose failed or prohibited memory writes rather than implying the report was persisted. Avoid duplicating the record or pasting a transcript into the response.
