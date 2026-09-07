---
name: spec-apply
description: Implement or resume a planned change in small verified slices. Use when the user asks to build from a spec or change record, or to run the lean spec workflow from a concrete request through completion.
---

# Apply a change

Carry the requested change through implementation and verification. A clear build request authorizes routine planning and local closeout; it does not require the user to invoke each workflow action separately.

## Establish context

Read existing project instructions and inspect relevant files and local edits before changing them. Use version-control status when available; a Git repository is not required. Select the record named by the user or unambiguously established in the conversation. Otherwise list active records (`docs/changes/*.md` by default); infer the target only if it matches the request. Ask when multiple plausible changes remain, rather than picking the newest. Never resume an archived change implicitly.

Read only the selected record, its linked constraints, relevant baseline specs, and affected code/tests. Use current files as working state; reconcile them with the user's latest instructions. Check completed tasks against the actual code instead of trusting checkboxes or repeating completed work.

If no record exists:

- Handle a trivial localized change directly and run its appropriate check. No new paperwork is needed; keep any affected existing spec accurate.
- For a substantive change, use `spec-plan` if available. Otherwise write one `docs/changes/<verb-noun>.md` with purpose/scope, concrete behavior scenarios, approach, a verifiable task checklist, evidence, and next action. Continue when the requested behavior is clear.

If the project already uses OpenSpec or another planning convention, use its existing artifacts and available tooling. Respect its schema; do not create compact records alongside it or invent CLI commands.

## Implement a working slice

Choose the smallest pending outcome that exercises the real path through the affected layers. Implement and check that outcome before taking the next one.

- Derive checks from the behavior scenarios, including meaningful failure cases. Reuse the project's test framework and commands.
- For a bug, reproduce the failure and add a regression test when it provides lasting value. When test-first development is requested, work one behavior at a time: observe the intended test failure, implement until it passes, then refactor while keeping it green.
- Test observable contracts rather than internal call sequences. Use focused checks while iterating, then the required integration/build/lint checks appropriate to the change. Documentation or mechanical edits may need inspection instead of new automated tests.
- Mark a task complete only when its outcome and check are satisfied. Record concise evidence: command or manual procedure, actual result, and relevant scenario. A missing dependency or unavailable service means not verified, not passed.

Update the record when implementation teaches you something. Revise routine design decisions and remaining tasks in place. If desired behavior changes, reconcile it with the user's intent before coding the new scope; never weaken a requirement merely to make a failing test pass. Reopen affected tasks and invalidate stale evidence.

## Finish or leave a resumable state

When available, use `spec-feedback` for progress updates, blockers, and handoffs, drawing on this record and actual check results. It adds no step or report file.

After implementation, use `spec-close` if available: verify behavior against code, reconcile baseline specs, and archive the completed record. If unavailable, perform those steps directly, merging only verified requirement changes into their named specs before moving the record to `docs/changes/archive/YYYY-MM-DD-<name>.md`. Re-read baseline specs before merging; preserve unrelated requirements and resolve overlapping edits. Never overwrite an archive entry. Do not archive with failing or missing required checks, unresolved tasks, or conflicting specs.

Respect a request to stop before closeout or to implement only a particular slice. On a blocker or partial stop, leave the record active with actual progress, failed/unrun checks, and a precise next action. Keep task tracking in that local file. Report what works and what remains. Local completion describes the current project files; it does not imply deployment or permission to publish or merge.
