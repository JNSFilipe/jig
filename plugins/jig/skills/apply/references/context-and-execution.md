# Context and execution

Use apply's situation/action table together with [the shared context policy](context.md) for routine context decisions, reminders, and host command names. Read this reference for implementation-worker mechanics when carrying out a handoff/reset or responding to a requested transition; reuse it once loaded.

## 1. Save a checkpoint

Ensure the existing record has decisions, relevant paths, completed/pending work, actual checks, and the next bounded action. Update/read back when relevant state changed or is missing; do not rewrite an already current checkpoint just because automatic compaction is near. Include active worker/process ownership and the stop condition in Next; reference other sections instead of duplicating them. Finish or stop active operations before replacing their context. After a transition, inspect current files before resuming.

Follow [the shared memory contract](memory.md): checkpoint the same receipt and Work ID, keep its owner accurate, and finalize as paused if execution is being relinquished. Compaction during continuing execution does not create a new session. Pass the receipt path and ownership boundary to the next agent; only the current primary owner writes it.

## 2. Choose the transition

Compaction summarizes history; a fresh worker starts without the planning conversation but still loads project instructions. Switching models does neither; forks/resumed workers may retain history. Use only authorized, exposed controls. Keep the host's configured automatic context management; do not override Blackhole or other extension hooks. See [transition procedure](context-transitions.md) for verified Pi compact/new-session commands and provider-cache caveats.

If the desired control is unavailable, checkpoint and supply the record path plus a resume prompt once. Continue feasible work unless fresh context is explicitly required or reliable continuation is impossible. Do not simulate resets by editing session state, or launch new user-facing tasks/nested CLIs/change global settings without a separate request.

## 3. Dispatch one worker

Delegate only a settled, verifiable task whose expected benefit exceeds startup, rereading, and review. Keep difficult decisions with the parent. Related tasks can share one work order; avoid a worker per checkbox. Respect planning-only requests, stopping points, budgets, and explicit current-agent-only preferences. No worker is required when transfer/review cost outweighs benefit.

Choose the user's model preference first, then an existing execution setting, then a suitable economical model from the host catalogue. Use supported default/moderate effort for routine execution. If availability or relative cost is unknown, retain the current model unless the user supplied a valid choice; disclose the limitation without repeated pricing lookups.

Use a native write-capable worker with fresh history and access to the actual project files:

- **Codex:** use the callable tool's model/effort controls and no-history option (`fork_turns: "none"` when exposed). Honor any requirement for useful independent parent work.
- **Claude Code:** use a non-fork implementation agent with a supported model override or configured execution agent. Pass the skill path; loaded skills may not propagate.
- **Pi / pi-task:** use the exposed `task` tool (possibly renamed) and its current agent catalogue. Choose an available write-capable implementation agent, e.g. `general` when advertised for that scope, not a read-only explore/reviewer. Read the installed task skill when available. Its `prompt` is the complete handoff: goal, references, scope/non-goals, write policy, acceptance, verification, and stop condition. `cwd` must be an existing absolute project/worktree path; pi-task does not create worktrees. `thinking` is effort, not a model selector; frontmatter wins. This contract has no arbitrary `model`/`fork_turns` argument: use an already configured agent/model that satisfies explicit constraints or continue locally. Do not silently choose a conflicting model/budget. Do not assume an omitted agent model inherits the parent's effective model: verify the configured agent/actual launch. If a requested worker model cannot be established, use a matching configured agent or continue locally.

### Pi worker example

Adapt all paths, agent names and commands to the real project and exposed schema; placeholders below are illustrative, not a tool call to execute unchanged:

```json
{
  "agent_type": "general",
  "description": "Implement filtered CSV export",
  "cwd": "/absolute/project",
  "prompt": "Goal: implement authorized filtered CSV export. Read AGENTS.md, /absolute/project/docs/changes/export.md, /absolute/receipt.md and the installed apply/SKILL.md. Parent Work ID: export-42; parent owns the sole receipt/task list. Scope: edit only src/export.ts and tests/export.test.ts; exclude pagination UI, dependencies and unrelated files. Honor the recorded all-filtered-matches decision. Write policy: no competing receipt, redelegation, baseline reconciliation, archiving, commit or publication; do not finalize parent tasks. Acceptance: authorized filtered rows, header-only empty results and correct CSV quoting. Verification: npm test -- tests/export.test.ts; report actual results, not assumed success. Stop after this slice and checks, or on scope conflict, missing dependency or unresolved requirement. Return changed paths, evidence and blockers; parent integrates, verifies and closes."
}
```

The parent keeps scope decisions, authoritative task updates, Work ID, verification, integration and closeout. Returned evidence goes into that existing record; a child success message alone does not complete it. Do not require a custom `jig-implementer` agent file; an optional configured agent can bound writes/use an economical model if the installed backend supports it.

An optional project/user agent definition can avoid unrelated bundled skill dependencies. Create one only when requested; JIG never installs it automatically. For example, adapt `.pi/agents/jig-implementer.md` to a real available model (the model value below is a placeholder):

```yaml
---
description: Bounded JIG implementation worker; parent owns records and closeout
model: provider/configured-model
thinking: low
tools: read,bash,edit,write
---
Follow the parent work order and its exact editable scope and checks.
Return changed paths, actual checks and blockers. Do not write/finalize receipts,
redelegate, reconcile specs, archive or publish.
```

No `skills:` declaration is required: the handoff supplies the actual installed JIG paths. If declaring native skills, every declared name must resolve in Pi's registry; a missing name fails launch. Confirm the new agent appears in the current task catalogue before using it.

Background execution is normally the tool default; results arrive automatically. Do not poll task/session files or imitate a spawn/wait CLI. Use `task_id` to resume the same child for a focused correction when supported. `workspace_group` groups panes, not files. Concurrent writers need disjoint scopes or explicitly prepared separate worktrees with planned integration. Never reuse a pi-task pane as a remote shell or send it commands directly. If the tool/agent cannot start (including missing declared skills), report the limitation and continue locally; do not install/configure agents without authorization.

Send actual paths and constraints, not the planning transcript:

```text
Work in <project root>. Read project instructions, <record>, <session receipt>, and
<apply SKILL.md>. You are the implementation worker.
Implement <outcome>; read <paths>; edit only <scope>.
Follow the recorded decisions and scenarios; run <checks>.
Update assigned tasks/evidence. Stop at <boundary>.
Do not create/finalize session receipts, redelegate, reconcile baseline specs,
archive, or publish. The parent owns receipt writes.
Return changed files, actual check results, and blockers.
```

Pass permissions and non-file constraints the host does not propagate. For a separate workspace, transfer the record and relevant uncommitted files through supported mechanisms; reconcile returned edits before verification.

## 4. Verify or escalate

While the worker writes, the parent leaves its files and assigned record sections alone; independent read-only work is safe, and disjoint mutation is allowed only with explicit scope separation or separate worktrees. Wait for completion, inspect actual changes, reuse valid checks, and verify missing scenarios/integration before owning closeout. A worker's success message is not evidence by itself.

Inspect failures before retrying. Allow one focused correction when the approach is sound; a repeated behavioral failure returns to the capable parent instead of another cheap-worker loop. Fix environment/permission causes directly. Record the outcome and escalation concisely.

Report only confirmed context transitions and observable model choices. Model inheritance is not proof of lower cost, and savings require measurement.
