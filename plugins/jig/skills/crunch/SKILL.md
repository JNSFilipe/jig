---
name: crunch
description: Implement a requested feature quickly with minimal token use, accepting rough code and documented shortcuts. Use when the user asks for crunch mode, a fast-and-dirty implementation, or prioritizes delivery speed and token savings over polish.
---

# Crunch

Ship the smallest working implementation of the requested behavior. Optimize total elapsed time and tokens, including tool output, delegation, and likely rework. Accept local duplication, direct code, and limited extensibility when they shorten delivery. Stop once the feature works and required checks pass.

Read and follow [the shared memory contract](references/memory.md) before starting. All new crunch receipts use its common registry and lifecycle, reachable from every skill.

## Execution

For progress, findings, decision questions, completion, and handoffs, read `feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep this skill's scope, brevity, and memory owner. If unavailable, apply the shared memory pre-report freshness check and report the outcome, evidence, uncertainty, next action, and record path directly.

- Read project instructions, inspect local edits, and locate the nearest existing implementation and its callers. Search narrowly; expand only when evidence requires it. Reuse context and batch independent reads with bounded output.
- Settle routine choices yourself. Ask only when missing information materially changes the requested behavior or authority. Keep any plan to a few lines; create no separate planning, design, spec, or archive documents unless the user or project requires them. Use the session record below for continuity.
- Patch the direct path through the existing code. Prefer existing dependencies and conventions. Skip speculative abstractions, unrelated cleanup, architectural improvements, extra configuration, and polish. A shortcut may sacrifice elegance; it must still deliver the requested behavior and preserve access controls, data integrity, and unrelated user work.
- Run the cheapest meaningful check of the changed behavior, plus project-required checks. Add tests only when required or when their expected regression/rework savings justify the cost. Do not repeat passing checks without a relevant change. Report unverified behavior honestly; never silently omit requested scope to finish sooner.
- Keep updates and the final answer short: delivered behavior, check result, material shortcuts or limitations, and the session record's path. Complete authorized implementation work without adding review gates.

## Delegation

Work locally by default. Spawn a subagent only when available and a bounded independent task is expected to reduce **both** completion time and total tokens after briefing, review, and integration costs. A small or tightly coupled change usually stays local.

Give each worker only its goal, relevant paths, constraints, and expected evidence; avoid copying full conversation history. Assign disjoint edits and do useful independent work alongside it. Workers return concise results and do not redelegate or maintain separate session records. The primary agent reviews the result and owns completion. Do not claim measured savings without actual usage data.

## Persistent session memory

For new work, create the shared receipt with `Origin: crunch`; when continuing a change, preserve its existing origin and Work ID. With no project work record, use the receipt itself for scope and progress. Include actual changes/checks, accepted shortcuts in `Work next / debt`, and any delegation scope and reason. A later polish request refers to this receipt's path or ID.

Checkpoint before a handoff or pause and save/read back before the final response. When requested behavior and required checks pass, complete the session and work, clear `Session next`, and retain deliberately accepted polish debt. If requirements or required checks remain, use the appropriate unfinished state rather than hiding omissions as debt. Legacy crunch records remain readable at their old locations; do not create new records there or rewrite their history to claim completion.
