---
name: cmd-remote
description: Run SSH commands on a remote device in a local tmux pane the user can watch, or resume a named authenticated session. Use for remote inspection, configuration, long-running commands, or interactive device work. Also supports explicitly requested persistent local terminals; use the ordinary command tool for one-shot local work.
---

# Remote commands in a watchable session

Use local tmux to keep a visible terminal for the target. SSH targets need a compatible shell for the marker loop; they need no remote tmux unless work must survive losing SSH.

## Rules

- **Keep commands reviewable.** State the target and intended operation. Apply host execution permissions to both transport and payload; tmux grants no additional authority and must not bypass a rejected command.
- **Pin ownership to a pane.** Inspect before sending and use its stable pane ID, never whichever pane is active. One writer at a time; a session name alone verifies neither host nor readiness.
- **Keep secrets out of tool calls and logs.** Use existing authentication. Hand credential entry to the user through a writable attachment, pausing logging you own. A password/passphrase prompt does not prove keys are missing.
- **Preserve access.** Before operations that can remove data or connectivity, establish that the specific effect is authorized and arrange recovery where needed. Reuse explicit authorization; ask only about unresolved scope or risk.
- **Missing completion means unknown.** A deadline without a marker proves neither success, failure, nor continued execution. Inspect before retrying or reconnecting; never replay an unconfirmed mutation automatically.
- **Report what was verified.** A marker gives the foreground shell status, not background-job completion, every pipeline stage, or the device's resulting health.

## Process

### 1. Choose the simplest transport

Use the ordinary command tool for local commands and one-shot SSH checks. Use a pane when the user wants to watch/intervene, work needs an interactive terminal, or a named session should be reused. Native persistent terminals also work when shared tmux visibility is unnecessary.

Prefer the user's authenticated session. Otherwise reuse a verified idle session for the target or create a descriptive one such as cmd-pi. Preserve named sessions and existing configuration. Read [the session protocol](references/session-protocol.md) before creating or driving a pane.

### 2. Establish readiness

Inspect the exact pane, current screen, and transport; confirm an idle shell prompt before sending a probe. An SSH process name alone identifies neither the remote host nor whether its shell is idle.

Handle host-key/authentication prompts explicitly. Preserve host verification and configured aliases, ports, jump hosts, and authentication. Do not automatically install keys or loosen sudo policy. Resolve an unclear target or current program before typing.

The marker loop requires a Bourne-compatible shell. Router CLIs, REPLs, database clients, serial login screens, and full-screen applications need their own interaction protocol. Serial transport can carry a normal shell; compatibility depends on the current program.

### 3. Execute and observe

After readiness, start private output logging when useful and available. Tell the user how to watch once: tmux attach-session -r -t <session>. Manual input needs a writable attachment; suspend agent input until control returns.

Send one bounded foreground command, then poll in short waits and read its output. Keep the nonce and log offset across tool calls. For interactive commands or TUIs, use supported terminal interaction or hand control to the user; linear logs do not represent screen state reliably.

Stop sending when credentials, an unexpected program, or uncertain ownership appear. Check the device's actual state when exit status alone does not establish the outcome.

### 4. Leave recoverable state

Leave the user's session available. Stop only the logging this task owns when finished. For a handoff, preserve the target, socket if nondefault, pane ID, log path, pending command/nonce, and observed state in the existing task record.

If SSH drops, remote work may terminate or continue. Determine its state before repeating work. Local tmux preserves the local terminal, not remote process lifetime. Jobs that must survive need an available remote supervisor or remote tmux/screen session, with verified job status.

Reconnect after inspecting the old pane and accounting for any unconfirmed command. Destroy sessions or interrupt active work only within the user's authorization.
