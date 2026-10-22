# Context transitions and host commands

Read for a requested reset, meaningful handoff, or context pressure that warrants a transition. Apply [the context core](context.md) and [memory contract](memory.md).

## Checkpoint once, when needed

Ensure the existing work record/receipt contains accepted scope/decisions, current paths, valid/failed/unrun checks, remaining work, exact next action, and worker/job ownership. Update and read back **when relevant state changed or is missing**; reuse a current checkpoint without rewriting it merely because automatic compaction is near. Keep one authoritative task list. If writes are forbidden/unavailable, provide a chat checkpoint and disclose that it is not durable.

Preserve active worker identity and assigned paths, recipient, and any unresolved terminal command (socket, stable pane ID, nonce/log and last observation as relevant). Do not stop jobs just to reset history. Resolve overlapping ownership before new writes. Compaction while the same request continues keeps the receipt active and its owner; relinquishing execution finalizes as paused or complete, releasing/transferring ownership. A new user request in fresh chat creates a linked receipt with the same Work ID.

After any transition, validate relevant current files, checks, and live ownership before resuming. Reuse valid evidence, not assumed success from the summary. Blackhole/other remembered observations remain contextual evidence, never authoritative task updates.

## What changed?

Compaction summarizes history; a genuinely fresh conversation/worker starts without that history but still loads host/project instructions and the work order. A fork, resumed worker, clone, or model switch is not proof of fresh context. Do not claim a reset merely because a checkpoint was written or a slash command printed.

For a worthwhile recommendation give **action, why now, actual checkpoint path, and exact resume prompt**, once unless circumstances change. Optional recommendations do not stop feasible authorized work; explicit fresh-context stopping requirements remain binding. For example:

```text
Use jig-apply in <actual project path>. Read <actual work record> and <receipt>.
Confirm current files and ownership, then continue <next action> through
checks and closeout. Preserve <constraints and stopping restriction>.
```

Only execute transitions through available authorized host controls. User slash commands are not shell commands/tools. Do not edit session files, clear memory, launch nested clients, alter global settings, or stop jobs to simulate a reset. If no control exists, give the manual action/resume prompt once and continue safe work unless the user required fresh context first.

## Host commands

Check the installed host/version and actual command menu; surfaces/extensions differ. The word “clean” does not authorize deleting files or stopping jobs.

- **Pi (checked against installed 1.2.0 docs):** `/compact [instructions]` summarizes while continuing; `/new` starts a new session. `/resume` continues stored history; `/tree`, `/fork`, `/clone`, and `/model` are not empty-history resets. Use `/session` to inspect identity/usage when necessary. Recheck the installed command menu on other versions. [Sessions](https://pi.dev/docs/latest/sessions), [compaction](https://pi.dev/docs/latest/compaction).
- **Codex CLI:** `/compact` summarizes; `/new` starts fresh; `/clear` starts fresh and clears the view. `/clean` aliases `/stop` (background terminals), not context cleanup. [Commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).
- **Claude Code:** `/compact` continues with a summary; `/clear` starts empty-context conversation. [Commands](https://code.claude.com/docs/en/commands).
- **Other surfaces:** use supported compact/new-chat actions; do not infer callable controls from CLI docs.

### Optional Pi extensions

Verified documentation baseline: `pi-blackhole` 0.5.15 and `pi-claude-bridge` 0.9.3. These are optional integrations, not JIG dependencies or instructions to install/configure them.

Blackhole separates deterministic structural compaction from billed Observer/Reflector/Dropper memory calls. Under its default blackhole engine/auto mode it can own Pi's `session_before_compact` hook, including native `/compact`; manual/off/pi-default modes differ. Explicit `/blackhole` invokes its compact path. Use the installed extension's command/config documentation, not an assumption that `/compact` always uses Pi's LLM summarizer. JIG does not replace its hooks, flush its store, mirror observations into receipts, force a manual compact near every automatic event, or change thresholds. A current durable checkpoint needs no duplicate write or blocking observer flush. Works with native Pi alone.

Provider cache behavior is a caveat, not a guarantee: the documented bridge can rebuild its Claude session after history rewrites and miss cache beyond the system prompt; summarization queries may use isolated calls. Other providers differ. Avoid repeated manual compactions and measure total task cost before claiming savings; neither a free deterministic compaction nor a cheaper worker implies a cheaper overall task. No JIG policy depends on Claude Bridge being present.

Sources: installed Pi `docs/sessions.md`, `docs/compaction.md`; [Blackhole README](https://github.com/k0valik/pi-blackhole#compaction-modes); [Claude Bridge README](https://github.com/elidickinson/pi-claude-bridge#known-issues). Revalidate extension behavior against installed documentation after upgrades.
