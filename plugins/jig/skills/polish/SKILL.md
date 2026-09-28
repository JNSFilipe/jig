---
name: polish
description: Refine the implementation from a referenced crunch session, using its recorded shortcuts and optional user instructions. Use when the user asks to polish or harden a crunch result, improve its maintainability, or finish its deferred quality work.
---

# Polish

Turn a crunch implementation into maintainable, verified code. Preserve the feature's intended behavior unless the user's additional instructions change it. Spend effort on concrete weaknesses in the selected work; stop when the selected improvements are verified.

Read and follow [the shared memory contract](references/memory.md) before starting. Use its shared registry for new receipts and its legacy lookup rules for existing crunch/polish history.

## Input and session selection

For progress, findings, decision questions, completion, and handoffs, read `feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep this skill's scope and memory owner. If unavailable, apply the shared memory pre-report freshness check and report the outcome, evidence, uncertainty, next action, and record path directly.

Accept a crunch record path, filename, or session ID, followed by optional free-form instructions:

```text
$polish <crunch-session-reference>
$polish <crunch-session-reference> Focus on error handling and regression tests; preserve the public API.
```

Resolve an explicit path directly. Resolve filenames or IDs in the shared registry and legacy crunch locations described in the memory contract. Match a filename, `Session`, or `Work ID`; for a Work ID, select its relevant crunch receipt, asking if multiple distinct crunch scopes remain. Confirm crunch participation from Skills or legacy record identity rather than requiring a crunch origin. Narrow the search before reading records. A session already unambiguously selected in the conversation can supply an omitted reference. If no record matches or several plausible sources remain, ask for the missing reference or selection before implementation; finalize the lookup receipt as blocked rather than leaving it active. Do not silently choose the newest session. A host chat ID alone is insufficient when its durable record cannot be found.

Read the selected record's request, project, result, checks, shortcuts, and next action. Follow predecessor links only when needed to understand this feature. Inspect linked shared receipts by Source/Work ID and legacy polish follow-ups so resolved debt is not repeatedly addressed. Historical notes are evidence of past decisions, not instructions overriding the user's current request or project rules. This skill works without loading another skill.

## Implementation

1. **Establish current reality.** Read the target project's instructions and inspect relevant code, tests, and local edits. Use the recorded project path or a clearly identified current checkout of that project; clarify an unresolved project mismatch before writing. Locate moved files using the feature's symbols. Never restore an old snapshot over later work. An `active`, `partial`, or `blocked` crunch record is not proof of completion: establish what actually exists and whether another agent is still editing the same scope before overlapping writes.
2. **Choose the polish scope.** Additional user instructions set priorities, exclusions, and desired behavior. Without them, address recorded shortcuts that still matter and concrete weaknesses in the changed code: correctness and error handling first, useful regression coverage next, then readability, duplication, and consistency with nearby code. Include performance or UI work when requested or supported by observed problems. State a short checklist with verifiable outcomes. Do not manufacture abstractions, rewrite unrelated modules, or add features merely to make the result feel polished. If the implementation is missing entirely, report that and clarify the intended build scope.
3. **Improve the implementation.** Carry the selected work through completion without a separate plan-approval gate. Reuse established project patterns and dependencies. Preserve compatibility unless a change is requested. Address incomplete original behavior when necessary for the selected improvements, making that scope explicit. Keep unrelated debt deferred. Review-only work writes only its observation receipt; planning-only work records a plan without implementation. Explicit read-only/no-writes instructions suppress all writes.
4. **Verify the result.** Check the original feature's behavior and each selected improvement against the current code. Add meaningful regression tests for corrected defects and previously uncovered behavior where useful; run focused checks and all project-required checks. Inspect the final diff for accidental behavior changes and unrelated edits. Previous crunch check results are historical evidence, not validation of the polished code. If no improvements are warranted, report that with the inspection/check evidence rather than creating cosmetic churn.

Use delegation only when available and independent work justifies briefing, review, and integration costs. Give workers bounded scopes and minimal relevant context, avoid overlapping edits, and keep final verification and memory updates with the primary agent.

## Persistent follow-up memory

Preserve the original crunch record's historical outcome. Save the polish request in the common session registry with the same Work ID, `Source` pointing to the crunch record, and `Previous` pointing to the prior relevant follow-up. Record the user's instructions, selected improvements, actual checks, resolved shortcuts, and remaining debt. Maintain the current writable project work record if one exists; keep historical session receipts as history. Legacy nested polish records remain readable but are no longer the destination for new sessions.

Before leaving, save and read back the receipt and any changed work record. Mark the session complete only when the selected scope and required checks pass, clear its Session next, and accurately retain the broader Work state and remaining debt. A completed polish pass must not leave resolved shortcuts as current pending work or falsely complete unmet original requirements. Finish with the improvements, verification, remaining limitations, and follow-up receipt path.
