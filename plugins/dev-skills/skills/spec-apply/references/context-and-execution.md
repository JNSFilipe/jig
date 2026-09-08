# Context and execution

Use spec-apply's situation/action table for routine context decisions. Read this reference when carrying out a handoff/reset or responding to a requested transition; reuse it once loaded.

## 1. Save a checkpoint

Update the existing record with decisions, relevant paths, completed/pending work, actual checks, and the next bounded action. Include active worker/process ownership and the stop condition in Next; reference other sections instead of duplicating them. Finish or stop active operations before replacing their context. After a transition, inspect current files before resuming.

## 2. Choose the transition

Compaction summarizes history; a fresh worker starts without the planning conversation but still loads project instructions. Switching models does neither; forks/resumed workers may retain history. Use only authorized, exposed controls. Keep host auto-compaction enabled.

If the desired control is unavailable, checkpoint and supply the record path plus a resume prompt once. Continue feasible work unless fresh context is explicitly required or reliable continuation is impossible. Do not simulate resets by editing session state, or launch new user-facing tasks/nested CLIs/change global settings without a separate request.

## 3. Dispatch one worker

Delegate only a settled, verifiable task whose expected benefit exceeds startup, rereading, and review. Keep difficult decisions with the parent. Related tasks can share one work order; avoid a worker per checkbox. Respect planning-only requests, stopping points, and budgets.

Choose the user's model preference first, then an existing execution setting, then a suitable economical model from the host catalogue. Use supported default/moderate effort for routine execution. If availability or relative cost is unknown, retain the current model unless the user supplied a valid choice; disclose the limitation without repeated pricing lookups.

Use a native write-capable worker with fresh history and access to the actual project files:

- **Codex:** use the callable tool's model/effort controls and no-history option (`fork_turns: "none"` when exposed). Honor any requirement for useful independent parent work.
- **Claude Code:** use a non-fork implementation agent with a supported model override or configured execution agent. Pass the skill path; loaded skills may not propagate.

Send actual paths and constraints, not the planning transcript:

```text
Work in <project root>. Read project instructions, <record>, and
<spec-apply SKILL.md>. You are the implementation worker.
Implement <outcome>; read <paths>; edit only <scope>.
Follow the recorded decisions and scenarios; run <checks>.
Update assigned tasks/evidence. Stop at <boundary>.
Do not redelegate, reconcile baseline specs, archive, or publish.
Return changed files, actual check results, and blockers.
```

Pass permissions and non-file constraints the host does not propagate. For a separate workspace, transfer the record and relevant uncommitted files through supported mechanisms; reconcile returned edits before verification.

## 4. Verify or escalate

While the worker writes, the parent performs only independent read-only work and leaves its files and record alone. Wait for completion, inspect actual changes, reuse valid checks, and verify missing scenarios/integration before owning closeout. A worker's success message is not evidence by itself.

Inspect failures before retrying. Allow one focused correction when the approach is sound; a repeated behavioral failure returns to the capable parent instead of another cheap-worker loop. Fix environment/permission causes directly. Record the outcome and escalation concisely.

Report only confirmed context transitions and observable model choices. Model inheritance is not proof of lower cost, and savings require measurement.
