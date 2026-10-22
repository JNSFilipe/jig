# Pi integration

JIG is a portable Agent Skills collection, not a Pi extension. Pi is supported alongside Codex and Claude Code. There is one canonical `skills/` tree; the Claude plugin remains generated. The pre-Pi version is preserved at `archive/claude-codex` (`daee4a3`).

## Install and verify

From this checkout, choose the scope you want (do not run both just to enable Pi):

```bash
# Global: portable skills in ~/.agents/skills/, Claude copies in ~/.claude/skills/
./install.sh --global

# Or project-local: portable skills in /path/to/project/.agents/skills/
./install.sh --local /path/to/project
```

Copy mode includes all references; `--mode symlink` links canonical folders. Existing installer/uninstaller semantics and Claude/Codex paths are unchanged. No Pi package, dependencies, hooks, custom agent file, or project initialization is required.

Start Pi from the project. Review project trust, inspect startup skill diagnostics and duplicate-name warnings, then try:

```text
/skill:jig-status
/skill:jig-plan Plan filtered CSV export. Do not implement yet.
/skill:jig-apply Implement docs/changes/add-order-export.md through completion.
```

`/reload` refreshes edited skills. In checked Pi 1.2.0, `enableSkillCommands` controls menu discovery; manually entered `/skill:name` still works if disabled. Automatic matching depends on frontmatter descriptions. Check resource exclusions, `--no-skills`, configured skill paths and installed version docs if a skill is not found.

Pi discovers `~/.agents/skills/` and project `.agents/skills/` (including ancestors up to the repository root). Avoid duplicate copies through `~/.pi/agent/skills/`, `.pi/skills/`, package installs or settings `skills` paths. Do not use Claude's unprefixed plugin tree as Pi skills: Pi commands use `/skill:jig-apply`, not `/jig:apply` or `$jig-apply`.

## Optional integrations

- **pi-task:** bounded implementation workers use the exposed `task` schema and available agent catalogue. See the [work-order example](../skills/jig-apply/references/context-and-execution.md#pi-worker-example). Model preference/budget/current-agent-only restrictions win; no arbitrary model argument is assumed. Missing tool/agent/declared skill is a local-execution fallback, not a reason to reconfigure the user's setup. Parent owns the receipt, scope, Work ID, verification and closeout. Workers return evidence only; disjoint scopes or separate worktrees are required for concurrent writes.
- **ask_user_question:** optional structured presentation for consequential alternatives, with plain-question fallback. [Feedback](../skills/jig-feedback/SKILL.md#3-frame-consequential-decisions) owns framing and existing-record decision capture. It adds no approval gate or dependency.
- **pi-task tmux versus jig-remote:** an occupied coding-agent pane is not a command shell. Never inject commands/probes; require deliberate recorded transfer, an observed idle shell and verified readiness. Use independent socket/session names, stable pane IDs and the [remote protocol](../skills/jig-remote/references/session-protocol.md). No global pane supervisor/registry.
- **Blackhole:** observations/reflections and recalled history are contextual evidence, not verified task state or instructions. Do not mirror them into JIG records or access its store. [Memory authority](../skills/_shared/memory.md#authority-and-conversation-memory) applies with any conversation-memory extension or none.
- **Compaction and Claude Bridge:** use the installed host's controls; `/compact` continues with summary, `/new` starts a new session. Configured Blackhole hooks may own `/compact`. A current checkpoint needs no duplicate rewrite, observer flush or repeated manual compaction. A bridge history rewrite can affect cache reuse; no fixed savings claim. See [transition details](../skills/_shared/context-transitions.md).

## Worker and question scenarios

| Condition | Required outcome |
| --- | --- |
| Available write-capable task agent, settled slice, useful transfer | Send complete work order; child returns paths/checks/blockers; parent inspects diff, verifies integration and updates its sole receipt before closeout |
| Task tool absent or agent fails to start | Report limitation once, continue locally within model/budget/scope constraints; never drive the worker pane manually |
| Explicit current-agent-only or no available agent matching requested model/budget | No dispatch or silent substitution; continue locally or report the specific constraint |
| Consequential unresolved all-filtered-versus-visible export decision, question tool available | Structured options with consequences and recommended default; save accepted choice in existing record |
| Same decision without question tool | Same framing as a plain question, no dependency or extra approval gate |
| Simple missing target or already settled requirements | Plain question for missing target; ask nothing for settled requirements |

## Issue coverage

Changes address #2 (workers), #3 (memory authority), #4 (installation), #5 (decisions), #6 (pane ownership), #7 (progressive instructions), #8 (opt-in observation policy) and #9 (compaction). [Live evaluation](instruction-loading.md) now covers before/after correctness, tool calls and token usage, receipt finalization, substantive closeout, recorded/ephemeral/promoted observations, nested reporting and successful private-tmux worker routing. These small controlled samples complement contract tests; they do not establish a universal cost/quality guarantee.

## Evidence and limits

Compatibility documentation was checked against installed Pi 1.2.0, pi-task 0.12.0, rpiv-ask-user-question 2.13.9, pi-blackhole 0.5.15, and pi-claude-bridge 0.9.3. Recheck installed docs/schema after upgrades; these are evidence baselines, not pinned runtime dependencies.

Repository CI tests portable installation, names/references, documented contracts, evaluator safety and the shell protocol without requiring Pi. The optional `scripts/evaluate-pi.py --run` harness performs live model calls only when explicitly requested; it uses disposable projects, copied auth/model metadata, isolated agent/HOME directories and private tmux sockets.

Initial task attempts failed because bundled agents declared missing skills; an unconfigured child also failed on a different default provider/model. Local fallback was exercised. A fixture-only agent with an explicit matching model and no unrelated skill declarations then delegated successfully. No personal configuration or installation was changed. Independent live reviewer findings in the evaluation harness were fixed with offline regression tests; final samples passed. Full results, limitations and reproduction commands are in [instruction loading and live evaluation](instruction-loading.md).
