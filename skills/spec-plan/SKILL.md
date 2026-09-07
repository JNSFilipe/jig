---
name: spec-plan
description: Write or refine a small, testable change plan before coding when the user asks to plan a feature, behavior change, or substantial refactor. Use an existing change record when supplied.
---

# Plan a change

Leave enough intent on disk for another session or coding agent to implement the change without reconstructing the conversation. This skill plans; it does not implement unless the user also requested implementation.

## Find the smallest useful scope

Read repository instructions, the relevant code and tests, and any existing plan or specs for the affected behavior. Search first; do not survey the whole repository. Reuse decisions already made in the conversation.

No initialization step is required. Use existing project instructions and build/test configuration when present; otherwise infer only what this change needs. Create the change directory when first writing a record and capability specs at closeout. Do not add workflow configuration, initialize Git for this workflow, or require a tracker to start work.

- For a typo, mechanical edit, or obvious localized fix with no design decision, give a short plan in chat. Do not create a change record unless requested. Update an existing spec if the fix changes its contract.
- For work with meaningful behavior, uncertainty, or multiple steps, use one change record. Split independent outcomes only when they can be delivered separately.
- Investigate uncertainty in code first. Ask only about decisions that materially change behavior, scope, compatibility, or cost. State reasonable implementation assumptions and proceed. Do not turn planning into a mandatory interview.

## Write the record

Follow the project's existing planning convention. In an OpenSpec project, use its schema, artifacts, and available workflow; do not introduce a competing directory or feed this skill's compact format to its CLI.

Otherwise create `docs/changes/<verb-noun>.md`, or update the explicitly selected active record. Inspect active filenames before choosing a name; never overwrite an unrelated change. Use [the compact template](references/change-template.md) when creating a record. Create directories lazily.

Keep it roughly one screen to one page when the scope allows. Include:

- **Why and scope:** the problem, intended outcome, and relevant exclusions.
- **Behavior:** stable requirement names with concrete input/action/result examples. Identify added, modified, or removed behavior and its target capability spec, normally `docs/specs/<capability>.md`. For modifications, describe the complete resulting requirement, preserving unaffected cases. For removals, state what replaces it or how existing users migrate. A pure refactor records preserved behavior instead of inventing a product change.
- **Approach:** only decisions that constrain implementation, relevant code/test paths, and necessary compatibility or rollout details. Separate observed facts from assumptions.
- **Tasks:** a small ordered checklist of verifiable outcomes, each tying behavior to its check. Prefer a working path through the affected layers over separate database/API/UI batches.
- **Evidence and next step:** checks to run, then their actual results as work proceeds; record any blocker and the exact next action when pausing.

Add a separate design document only when alternatives, migration, or cross-system interactions need space. Link it instead of repeating it. Track work in the local change record; do not generate tracker issues or a project-wide spec inventory.

## Hand off

Check that the scenarios can distinguish correct from incorrect behavior and that tasks cover them. Leave unresolved consequential decisions visibly blocked; do not hide them in an executable plan.

Link the record and summarize the intended behavior and any decision needed. If the request includes implementation, continue into it using the record; the file's existence is not a new approval gate. For a planning-only request, stop here.
