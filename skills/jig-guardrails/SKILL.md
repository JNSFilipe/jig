---
name: jig-guardrails
description: Route ordinary coding requests to the appropriate jig workflow even when no skill is named, and remind the user about planning, closeout, and context transitions. Use for feature/fix/refactor requests without a selected workflow or when the user asks which skill or context action to use. Do not turn explanations, reviews, or status questions into implementation.
---

# Workflow guardrails

Help the user follow the workflow without remembering its commands. Prefer selecting and using the appropriate installed skill immediately over asking the user to repeat an already clear request. Preserve explicit skill choices, project conventions, authorization, and stopping points; this router adds no approval gate or mandatory planning phase.

Read and follow [the shared memory contract](references/memory.md) before starting. Routing and nested skills share one receipt and owner. Routing a build is implementation mode, planning-only work uses planning mode, and a request only for workflow advice is observation mode. Do not create an extra guardrails work item or reset a selected work ID/origin.

For progress, questions, completion, and handoffs, read `jig-feedback/SKILL.md` from the installed sibling skill before the first report and reuse it. Keep the caller's scope and memory owner. If unavailable, apply the shared memory freshness check and report outcome, evidence, uncertainty, next action, and record path directly.

## Route the request

Choose the user's explicit skill or an already active workflow first. Otherwise use the request's intent:

| Intent | Action |
| --- | --- |
| Build a feature, make a code change, fix a known issue, or resume implementation | Read `jig-apply/SKILL.md` and proceed. Small features still use apply, with a compact receipt and proportionate checks. No prior plan or explicit skill mention is required. |
| Explore requirements, compare approaches, or plan without coding | Read `jig-plan/SKILL.md`; stop after the requested planning deliverable. If the request also authorizes implementation, plan only as needed inside apply and continue without another approval. |
| Investigate an unexplained failure | Read `jig-debug/SKILL.md`. Diagnosis-only stays diagnosis-only; authorized repair can proceed through apply and closeout. |
| Verify and reconcile implemented work, or finish a selected change's closeout | Read `jig-close/SKILL.md`; preserve review-only restrictions. Do not infer closeout authority from a bare status question. |
| Explicitly prioritize fast-and-dirty delivery | Read `jig-crunch/SKILL.md`. Do not select crunch merely because a feature is small. |
| Refine a referenced crunch session | Read `jig-polish/SKILL.md`, carrying the supplied reference and instructions. |
| Inventory repository work / explain one change / audit memory | Read `jig-status/SKILL.md`, `jig-feedback/SKILL.md`, or `jig-consistency/SKILL.md` respectively. Keep their observation scope. |
| Work on a remote device or a requested persistent terminal | Read `jig-remote/SKILL.md` within the requested task. |
| Explain code or answer a conceptual question | Answer directly; do not start apply or create a feature plan. |

Announce the chosen workflow briefly, then do the work. Read sibling instructions directly when exposed skills are files; a special invocation API is not required. Load only the selected skill and required references. Do not route back through guardrails once another workflow owns the task.

If an installed skill requires an explicit host invocation, explain that limitation and provide one paste-ready prompt carrying the user's actual request or record path in the supported syntax. If the skill is absent or unreadable, say so and identify that missing dependency; repeating its name will not install it. Use an appropriate direct fallback or continue independent safe work within scope without claiming the missing workflow was used. Do not make the user re-prompt merely because they omitted a skill name, or repeatedly advertise a missing skill.

Build snippets from the actual installed skill name and host namespace: `$<installed-skill-name> <request>` in Codex, `/<installed-skill-name> <request>` for a direct Claude Code install, or `/jig:<short-name> <request>` for this plugin. Standalone names already contain the collection prefix; the plugin namespace supplies it for distributed short names. Host built-ins such as `/plan` are not substitutes for this collection's plan skill. Confirm the installed naming/host when uncertain.

## Remind at useful boundaries

Read [context and workflow reminders](references/context.md) and reuse it. At a material scope change, finished plan, implementation/closeout boundary, pause, or final report, check the next workflow step and whether context should stay, compact, or start fresh. Provide at most one concise, actionable reminder for that boundary, with a reason and actual record/receipt path. Do not nag on every turn or add a plan/close step to work that does not need it.

Planning reminders explain the unsettled behavior, not just the command. Closeout normally happens automatically inside apply; remind the user to call close only when required closeout remains and cannot appropriately be completed now. Read-only reports suggest the next step without performing it. Context transitions first preserve a resumable checkpoint and ownership; never equate a recommendation with a completed reset.

## Activation limits

The description and implicit-invocation policy enable normal skill discovery; they are not an always-running hook. If the host never loads this skill, it cannot issue a reminder. For stronger routing, the user can opt to add a short preference to their existing personal/project instructions: “For coding change requests, use the installed jig-guardrails skill even when I omit a skill name; preserve explicit workflow choices and read-only requests.” Do not modify those instructions, install hooks, or change host settings just by running this skill. It remains optional and works without project initialization.
