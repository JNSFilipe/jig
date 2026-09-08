# Session protocol

Run these examples in **local Bash**, using actual target names and the same tmux socket throughout. The loop needs tmux, Bash, OpenSSL, Perl, and standard Unix utilities locally. Check availability; do not silently install them. Apply project command wrappers where required.

## 1. Select a fixed pane

Inspect an existing session before sending anything:

~~~bash
JIG_REMOTE_SESSION=cmd-pi
tmux list-panes -s -t "=$JIG_REMOTE_SESSION" \
  -F '#{pane_id} dead=#{pane_dead} command=#{pane_current_command} start=#{pane_start_command}'
~~~

Set JIG_REMOTE_PANE to the verified %N pane ID from that output:

~~~bash
tmux capture-pane -p -J -S -50 -t "$JIG_REMOTE_PANE"
~~~

Stable pane IDs avoid following the user's active-pane selection. Check connection details and, once an idle shell is established, read-only host/user identity. Never probe an authentication prompt, busy command, partially entered line, or unknown application.

For a **new** session, pass SSH arguments separately:

~~~bash
JIG_REMOTE_TARGET=pi
JIG_REMOTE_PANE=$(tmux new-session -d -P -F '#{pane_id}' \
  -s "$JIG_REMOTE_SESSION" -x 200 -y 50 \
  ssh "$JIG_REMOTE_TARGET")
~~~

Use the configured alias and required options. Width reduces wrapping; it does not guarantee byte-exact output. Preserve existing sessions. Optionally enable remain-on-exit on a newly created pane to retain disconnect output; leave global options alone.

Let SSH authenticate first. New host fingerprints need trusted verification; changed keys need investigation. Preserve stricter existing verification settings. For one-shot noninteractive SSH, BatchMode=yes disables password and host-key questions; failures are not readiness.

## 2. Probe an idle compatible shell

After observing an idle Bourne-compatible shell:

~~~bash
JIG_REMOTE_NONCE=$(openssl rand -hex 16)
tmux send-keys -t "$JIG_REMOTE_PANE" -l \
  "printf '\n__READY_$JIG_REMOTE_NONCE\n'"
tmux send-keys -t "$JIG_REMOTE_PANE" Enter
tmux capture-pane -p -J -S -50 -t "$JIG_REMOTE_PANE"
~~~

Look for the exact standalone readiness line. If absent, wait briefly and inspect again. Successful send-keys proves only delivery, not execution. The round trip establishes responsiveness, not host identity. Non-shell programs need their native protocol.

## 3. Log privately

Inspect the pane's pipe first:

~~~bash
tmux display-message -p -t "$JIG_REMOTE_PANE" '#{pane_pipe}'
~~~

If already piped, establish its owner/destination; do not replace it or assume it writes your log. Use an agreed log or bounded pane capture if sufficient. Output lost from scrollback is unavailable evidence.

With no existing pipe, create a private log:

~~~bash
JIG_REMOTE_DIR=$(umask 077; mktemp -d /tmp/jig-pane.XXXXXXXX)
JIG_REMOTE_LOG=$JIG_REMOTE_DIR/output.log
(umask 077; : > "$JIG_REMOTE_LOG")
tmux pipe-pane -O -t "$JIG_REMOTE_PANE" "cat >> '$JIG_REMOTE_LOG'"
~~~

This generated path is safe to quote as shown; arbitrary paths need shell escaping. The -o option **toggles** an existing pipe off: tmux closes the old pipe, then declines to reopen it. The -O option selects output piping and replaces any existing pipe; do not reissue it mid-command or replace another owner's pipe. A pipe is asynchronous: verify markers reach the chosen log before trusting it.

Output may contain secrets. Before manual authentication, stop logging you own and hand control over with tmux attach-session -t <session>, without -r. Hidden password input is usually not echoed, but credentials must still stay out of tool arguments. Resume after the user returns control and the shell is ready.

## 4. Frame one foreground command

Set CMD to short, single-line shell code, then call the sender below. Stage complex multiline scripts through an appropriate file-transfer/execution tool instead; keep content and invocation reviewable.

<!-- protocol-example: sender -->
~~~bash
jig_remote_send() {
  case "$CMD" in
    *$'\n'*|*$'\r'*) printf '%s\n' 'Use a script for multiline commands.' >&2; return 2 ;;
  esac
  JIG_REMOTE_NONCE=$(openssl rand -hex 16) || return
  JIG_REMOTE_OFFSET=$(wc -c < "$JIG_REMOTE_LOG") || return
  local quoted=${CMD//\'/\'\\\'\'}
  local payload="printf '\n__BEGIN_$JIG_REMOTE_NONCE\n'; eval '$quoted'; printf '\n__END_$JIG_REMOTE_NONCE:%d\n' \"\$?\""
  tmux send-keys -t "$JIG_REMOTE_PANE" -l "$payload" || return
  tmux send-keys -t "$JIG_REMOTE_PANE" Enter
}
~~~

Review CMD under the current permission rules before calling. Literal sending avoids tmux key-name interpretation. Quoted eval keeps comments/quotes inside the command and preserves shell state such as cd; the local shell does not execute the payload. Marker-leading newlines handle prompts and output without trailing newlines, adding separator blank lines.

Shell exit/replacement, errexit, persistent output redirection, and interactive programs may prevent completion markers; handle them as explicit transitions. Background launches report only launch status and may interleave later output. Pipelines report the configured shell status, usually the last stage. Check relevant stages explicitly or use a scoped shell with pipefail; do not silently change the user's shell options.

## 5. Read output and completion

Read bytes appended since the command started. Normalize common CSI/OSC sequences and carriage returns for line-oriented output:

<!-- protocol-example: reader -->
~~~bash
jig_remote_output() {
  tail -c "+$((JIG_REMOTE_OFFSET + 1))" "$JIG_REMOTE_LOG" |
    perl -pe 's/\e\](?:[^\a\e]|\e(?!\\))*(?:\a|\e\\)//g; s/\e\[[0-?]*[ -\/]*[@-~]//g; s/\r//g'
}
jig_remote_status() {
  jig_remote_output | awk -v n="$JIG_REMOTE_NONCE" '
    $0 == "__BEGIN_" n { begun=1; next }
    begun && $0 ~ ("^__END_" n ":[0-9]+$") {
      sub("^__END_" n ":", ""); print; exit
    }'
}
~~~

Poll jig_remote_status in short waits, backing off for long work. A nonempty result, including 0, is the shell exit status. Yield each tool call within a few seconds to keep progress and user input responsive.

Require BEGIN before the matching standalone END. The echoed command contains marker text but is not completion. Extract text between these markers and report a relevant excerpt. Normalization is not a terminal emulator or byte-exact capture: TUIs, binary/control output, and concurrent writers need another observation method.

On a deadline, inspect recent output and pane_dead. Without END, the outcome is **unconfirmed**: running, awaiting input, disconnected, or lost logging are all possible. Do not send the next command or automatically retry. Interrupt only when authorized, then inspect effects.

## 6. Stop logging or recover

Close only your pipe with tmux pipe-pane -t "$JIG_REMOTE_PANE". Retain needed logs for a handoff; remove only task-owned temporary logs when no longer needed. Start a fresh log between commands if needed, never mid-command.

Inspect the exact pane:

~~~bash
tmux display-message -p -t "$JIG_REMOTE_PANE" '#{pane_dead}'
~~~

If dead and reconnection is authorized, use tmux respawn-pane -t "$JIG_REMOTE_PANE" ssh ... with the original arguments. Omit -k, which can kill a live pane. A pane exists after exit only if tmux retained it; if gone, create a replacement deliberately and capture its ID. Recheck target, authentication, readiness, and pipe state. Reconnection says nothing about the previous command's effects.

Local tmux cannot ensure remote-job survival. Verify a remote supervisor or tmux/screen job where persistence matters. Neither background & nor systemd-run --scope alone establishes persistence.

## Authentication and recovery

Pause agent input before handing the keyboard over. Preserve existing authorization and never retry an unconfirmed mutation automatically.

| Observed state | Next step |
| --- | --- |
| Encrypted-key passphrase prompt | Let the user unlock the key in their terminal, or load that key into their existing agent with `ssh-add <private-key-path>`; then recheck authentication. |
| Account password prompt | Offer writable attachment for manual authentication. If the intended public key is absent on the device and the user wants key login, suggest they run `ssh-copy-id -i <public-key-path> <target>` with the required connection options. It changes authorized keys and needs an existing login method; it is not a remedy for every password prompt. |
| Permission denied | Check the configured user, host, identity, and authentication method before proposing a remedy. Do not keep retrying or replace keys blindly. |
| New or changed host key | Ask the user to verify the fingerprint through a trusted source; investigate changes rather than bypassing verification. |
| No readiness marker | Inspect the last pane output for a busy program, authentication prompt, or failed connection. Resolve that state before sending shell code. |
| No END marker or dead pane | Inspect pane and pipe state, preserve partial output, and establish whether the prior command had effects before reconnecting or retrying. |

Sources: [tmux manual](https://man.openbsd.org/tmux.1), [SSH configuration](https://man.openbsd.org/ssh_config). Repository protocol tests exercise local shell behavior, not device authentication or remote-job survival.
