---
name: spec-close
description: Verify an implemented change against its requirements, reconcile the project's durable specs, and archive the completed change record. Also supports a requested verification-only review without changing files.
---

# Verify and close a change

Close the gap between intended behavior, implemented behavior, and the project's written contract. If the user asked only for verification or review, report findings without editing specs, task state, or archive files. Otherwise close locally when the evidence supports completion.

## Select and verify

Read existing project instructions and inspect relevant files and local edits. Use version-control status when available; a Git repository is not required. Select the named active change or the one unambiguously established in context; ask if several plausible records remain. Default records live at `docs/changes/*.md`. An already archived record needs no second archive; inspect it only if asked to reverify or investigate.

Read the record, affected code/tests, and referenced baseline specs. Follow the project's existing convention, including OpenSpec's schema and installed workflow when present. The compact Markdown format is not an OpenSpec CLI schema.

Assess three things:

- **Coverage:** every in-scope requirement and task has implementation and evidence. Check behavior rather than trusting checked boxes.
- **Correctness:** the implementation satisfies the concrete scenarios, including relevant error paths and compatibility. Tie each requirement to a test or observed check; a passing suite alone does not establish a missing scenario.
- **Consistency:** implementation, stated behavior, and important design decisions agree. Distinguish a legitimate design adjustment from an unrequested behavior change.

Use fresh evidence for the current code. Reuse earlier check results when neither the relevant code nor its dependencies/configuration have changed; rerun checks invalidated by subsequent edits. Run the repository's required checks and any missing scenario checks. Manual verification is valid when appropriate; write the steps and observation. Never describe an unrun check as passed.

For normal closeout, fix scoped defects when authorized, then reverify. For review-only work, report them. Failing or unavailable required checks, incomplete scope, and unresolved spec conflicts keep the change active. Record concrete blockers and next actions during normal closeout. Defer scope only when consistent with user direction, leaving an explicit record of what was excluded.

## Reconcile the durable contract

After verification, update only the affected baseline specs, normally `docs/specs/<capability>.md`:

- Re-read their current contents before writing; another change may have updated them since planning. Compare the intended edits with current requirements and resolve conflicts without discarding unrelated work.
- Add new requirements, replace modified requirements with their complete resulting contract, and remove only explicitly retired behavior. Preserve unrelated scenarios. If a requested addition already exists, reconcile it rather than duplicating it.
- Write current behavior and concrete scenarios in the project's spec style. Leave motivation, task history, and test logs in the change record. Create specs only for touched capabilities; a behavior-preserving refactor may need no baseline edit.
- Read the resulting specs against the implemented behavior. Do not silently rewrite product intent to match a defect or record unimplemented behavior as current.

## Archive and report

When available, use `spec-feedback` to report verified outcomes and limitations, linking the final record location and affected specs. It adds no step or report file.

Record final evidence and mark the record complete only after verification and spec reconciliation succeed. Move it to `docs/changes/archive/YYYY-MM-DD-<name>.md`, or the project's existing archive convention. Preserve its contents and working links. If the destination exists, use a distinct suffix; never overwrite history.

Keep reconciliation and archiving together as one local closeout operation; no Git commit or external tracker is needed. If interrupted after merging specs, resume by inspecting current state and applying only the remaining edits. Do not duplicate requirements or mark failed closeout complete.

Report the implemented outcome, meaningful checks and their results, any limitation, and links to the updated specs and archive. Complete means verified in the current project files, not deployed. No commit, push, or merge is implied by closeout.
