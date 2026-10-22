---
name: feedback
description: Provide evidence-based progress, findings, decisions, completion, and handoffs. Answer change-specific status questions; status owns repository-wide inventory discovery. Use complex reporting guidance inside other workflows without a new receipt or approval step.
---

# Feedback

Answer from evidence without making the user reconstruct the work.

Read and follow [the shared memory contract](references/memory.md). Standalone feedback is an observation: it changes no inspected work records. Default to its own receipt; explicit blanket no-writes/read-only suppresses it. A prohibition only on editing source or inspected work records does not prohibit this receipt; do not invent a no-writes constraint. For explicitly opted-in routine ephemeral feedback, read [observation policy](references/observation-policy.md); promote consequential findings to a receipt unless writes are forbidden.

## Within another workflow

Routine reports need only the shared freshness check and a concise outcome, evidence, uncertainty, next action, and record path. Load this procedure for consequential decisions, complex findings, or when directly requested, and reuse it. It is not another agent, request, approval gate, or receipt. Preserve the caller's scope, format, brevity, Work ID, and owner. Workers return evidence to the parent; reporting cannot close unfinished implementation.

## 1. Identify the claim and evidence

Use the named record or established scope, including multi-item inventories and remote targets. Clarify selection only if ambiguity changes the answer. Follow project conventions; default active records are `docs/changes/`, archives under `docs/changes/archive/`, baseline specs under `docs/specs/`. Tiny work can use the request and receipt.

| Claim | Supporting evidence |
| --- | --- |
| Intent / scope | Why, behavior, accepted decisions in selected work record |
| Progress / next | Tasks, evidence, blockers, Next |
| Current behavior | Relevant current code and valid check results, not checkboxes alone |
| Existing contract | Linked baseline spec; intent is not proof of implementation |
| Design reason | Approach and relevant design links |
| Completed delivery | Exact archive record; current files for behavior today |
| Context/model transition | Actual host results, not recommendations or inferred savings |

Search filenames/requirements before broadening. Read only supporting sections and links. Reuse inspected context and checks while current; rerun when evidence is missing or invalidated. Do not run a broad audit or expose secrets for a narrow report.

## 2. Establish freshness

Apply the shared **pre-report freshness check** against the latest request, files, and process state. External edits, worker results, or revised requirements invalidate affected evidence. Reconcile owned writable memory and read back updates before substantive claims; observations flag discrepancies without repairing sources. A receipt's Updated timestamp is not a new test result.

Separate passed, failed, not run, and stale checks; intent from observation; observed behavior from inference. Check the actual scenario before calling it a finding, dropping hypotheses ruled out by inspection. If current truth cannot be established, give the last observation and uncertainty rather than asserting completion.

Put measurements, conditions, and sample size inside the claim. Lead with the smallest useful observed output for payload/UI/data-row decisions. Label hypothetical examples and unobserved output. Model/context changes need confirmed host results; savings need measurements.

## 3. Frame consequential decisions

First check whether context already resolves the choice. Ask about behavior, not task numbering or storage details. Describe concrete consequences and recommend a default with a reason. Resolve routine implementation choices yourself. Planning-only, no-writes, no-approval, and autonomous requests retain their boundaries; reporting adds no approval gate.

For example: should export contain all filtered matches (recommended, avoids silently omitting orders) or only the visible page (smaller, matches the current screen)? This is an unresolved requirements question, not confirmation of already agreed scope.

**Optional Pi presentation:** if `ask_user_question` is exposed and structured presentation improves clarity, use its actual schema for two or more consequential alternatives. The installed tool supports 1–4 questions, 2–4 options each, concise labels (header at most 16 characters, option labels at most 60), and a description per option. Put the recommended option first with `(Recommended)`. Use `multiSelect` only for independent choices; no authored “Other”/“Type something.” row (the UI adds custom input). A single straightforward question stays conversational. If absent/unusable, ask plainly; never require/install the extension or call a guessed tool. Cancellation/default/timeout is not an accepted decision: preserve uncertainty rather than infer approval.

Representative options for “Which orders should export include?”: `All filtered matches (Recommended)` — exports every authorized match across pages; `Visible page only` — exports only rows shown now. Record the consequential accepted choice in the existing work record/receipt, not a separate list. The extension owns presentation/input only; JIG owns decision framing and write authority.

Before sending/saving a question, ensure the reader need not look up an identifier or guess an option's effect. A simple missing target/name can be one plain question. Ask nothing for settled decisions.

## 4. Deliver and finish

Lead with the observable outcome or blocker, then meaningful checks, limitations, and the exact next action if any. Link only useful files, including the current record/receipt path at completion or handoff. Handoffs include recipient and pending worker/process ownership.

Apply [context reminders](references/context.md) at meaningful boundaries; load its transition reference only when a transition is warranted. A recommendation includes why now, the actual checkpoint path and paste-ready resume prompt. Distinguish compact from fresh; never suggest `/clean` for context cleanup, repeat unchanged reminders, or demand closeout already finished.

Before the final response, finalize and read back owned memory per the contract. A delivered report completes only its observation session, not feature work. For an eligible ephemeral/no-writes request there is no receipt to finalize: disclose the omission. Unsaved writes are a limitation, never claim persistence. Do not duplicate the record or paste transcripts into chat.
