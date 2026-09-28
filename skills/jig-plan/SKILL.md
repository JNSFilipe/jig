---
name: jig-plan
description: Plan or refine a feature, behavior change, or substantial refactor before coding. Use when the user asks for a change plan, design approach, or an executable plan for another agent.
---

# Plan a change

Leave enough intent on disk for another agent to implement without reconstructing the conversation.

Read and follow [the shared memory contract](references/memory.md) before starting. Reuse it across nested skills. Record even a small chat plan in the shared session receipt; a project plan file remains optional for trivial work.

## Rules

For progress, findings, decision questions, completion, and handoffs, read `jig-feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep this skill's scope and memory owner. If unavailable, apply the shared memory pre-report freshness check and report the outcome, evidence, uncertainty, next action, and record path directly.

- **Respect the request.** Planning-only work ends with the plan. A request that also includes implementation can continue without another approval gate.
- **Keep intent explicit.** Resolve decisions that materially change behavior, compatibility, scope, or cost before treating the plan as executable.
- **Preserve existing work.** Never overwrite an unrelated change record or replace the project's planning convention.
- **Use one local task list.** Create workflow files only as needed; Git, a tracker, and an initialization step are unnecessary.

## Process

### 1. Establish scope

Read existing project instructions and the relevant code, tests, and specs. Reuse decisions from the conversation and infer routine implementation choices from the project. Investigate in code before asking the user.

For an obvious localized fix with no design decision, give a short plan in chat and save its scope and next step in the session receipt; create a separate project record only if requested. Keep any affected existing spec accurate. For substantive work, identify the smallest useful outcome. Split outcomes only when they can be delivered independently.

### 2. Select or create the record

Use the record named by the user or unambiguously established in context. Ask if several plausible records remain. Inspect active filenames before naming a new record.

Follow the project's existing convention. In OpenSpec projects, use the native schema and artifacts; this compact format is not OpenSpec CLI input. Otherwise create `docs/changes/<verb-noun>.md` using [the compact template](references/change-template.md). Keep it roughly one screen to one page when the scope allows.

### 3. Describe testable outcomes

Write:

- **Why / scope:** the problem, desired outcome, and relevant exclusions.
- **Behavior:** named requirements with concrete context/action/result scenarios. Identify Add, Modify, Remove, or Preserve and the target capability spec. A modification describes the full resulting requirement, including unaffected cases; a removal explains replacement or migration. Refactors can preserve the contract.
- **Approach:** relevant code/test paths, constraining decisions with reasons, and necessary compatibility or rollout details. Distinguish facts from assumptions.
- **Tasks:** a small ordered checklist of verifiable outcomes and their checks. Prefer a working path through affected layers before extending it.
- **Evidence / Next:** planned checks, actual results as work proceeds, and the exact next action or blocker.

Add a linked design document only when alternatives, migration, or cross-system interactions need space. Verify that scenarios distinguish correct from incorrect behavior and tasks cover them. Mark consequential unresolved decisions as blocked.

### 4. Checkpoint and hand off

Before leaving substantial planning, preserve decisions that otherwise exist only in chat, file paths, checks, and the first pending action in the record. Checkpoint before a long detour or context reset.

If the host signals context pressure or obsolete decisions repeatedly confuse the task, use an authorized exposed compaction control after checkpointing. Otherwise recommend the host action once with the record path and resume prompt; continue feasible planning. Saving a checkpoint is not proof of a reset.

Use the feedback reporting procedure to present intended behavior, outstanding decisions, and the current record path.

For planning-only work, finalize and read back the receipt: a delivered executable plan completes the planning session while its work remains `planned`; record unresolved decisions as blockers. When implementation is authorized, continue with `jig-apply` when available using the same receipt and Work ID, or implement from the record. Leave unresolved product decisions with the planning agent; a cheaper worker needs a settled task.
