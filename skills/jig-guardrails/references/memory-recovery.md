# Recovery and reconciliation

Read when resolving missing/legacy links, an audit, interrupted execution, contradictory continuations, or a cross-host handoff. Follow [the memory core](memory.md); this procedure grants no additional repair authority.

## Find the supported chain

Look up explicit paths first, then shared sessions by Session ID, Work ID, and absolute Project. Inspect relevant project records/archives, legacy `~/.local/share/jig/crunch/sessions/` (or established custom crunch directory), and nested `polish/<crunch-record-stem>/` follow-ups beside their source. A custom crunch directory is a legacy lookup location, not automatically a new shared root. With a nondefault shared root, still check the default legacy path when resolving an old reference. Preserve history in place; no bulk migration or invented missing sessions.

Use native IDs or recorded Work IDs; map an older record by exact path when necessary. Add the ID to writable work records when practical; if a native schema cannot accept it, keep the mapping in the receipt. Resolve old paths through recorded archive moves and Work ID/source chains. `self` and `none` are valid special values, not broken paths.

For receipt-only work, preserve prior receipts and carry current progress in a linked continuation with `Work record: self`, the same Work ID, and source/predecessor links. Retain original scope through these links. Select the latest relevant implementation/planning continuation supported by evidence, not just the latest timestamp; do not merge ambiguous concurrent branches. A later observation receipt cannot supersede work state. Carry unresolved scope forward without reopening completed planning/crunch sessions.

An interrupted closeout may already have moved its work record: inspect active and archive paths before retrying. Recover the same work; do not create a duplicate archive or reopen completed scope. Reuse useful branch/commit identities without equating all checkouts sharing a remote.

## Liveness and safe takeover

On resumption, inspect prior active receipts and live worker/job ownership before editing. Process crashes cannot guarantee a final write. Neither age nor a missing recent message proves interruption, completion, or safe takeover.

If termination is confirmed, mark the abandoned receipt `interrupted` with the observation and link to the recovery session, preserving original outcomes and verification times. If liveness is unknown, report `active (liveness unknown)` and resolve overlapping ownership before mutations. Record pending task identity, assigned paths, tmux socket/pane or remote command/nonce when relevant in the existing receipt. Do not drive an agent pane as a shell, stop workers merely to reset history, or infer remote-job outcome from a dead SSH pane.

Observation requests flag discrepancies without repairing source records. Explicit reconciliation may correct only evidence-supported states and links, re-reading ownership first. Unknown work must not become complete merely to eliminate pending entries. Unresolved conflicts remain findings with a precise next check. Use `jig-consistency/SKILL.md` for a bounded audit when available, not as an automatic recursive stage.

## Cross-host continuation

The registry is machine-local. Transfer relevant records/receipts with the code and project work record using an authorized mechanism, including necessary uncommitted edits. Record the new project/worktree identity and actual archive paths; do not depend on a chat export, Blackhole ledger, or personal installation being present. Inspect current files and processes before resuming; a successful transfer is not new verification evidence.
