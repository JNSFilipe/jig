# Compact receipt

Use [the shared contract](memory.md). Omit optional fields that add nothing; keep enough to resume without a transcript. Use one receipt for nested skills; only the parent writes it. Observation Work state is an assessment, not an authoritative lifecycle update.

```markdown
# Session: <request title>
Session: <unique filename stem>
Started: <UTC timestamp> | Updated: <UTC timestamp>
Project: <absolute path or none> | Target: <remote target if applicable>
Skills: <skills actually used> | Mode: planning / implementation / observation
Origin: <change origin or unknown>
Work ID: <stable ID or none> | Work record: <current absolute path, self, or none>
Source: <source session/record path or none> | Previous: <prior receipt path or none>
Session status: active
Work state: unknown
Owner: <agent/session ID while active; none when finished>
Request: <scope and user instructions>
Result: <changed paths or findings; actual outcome>
Checks: <commands/observations and passed, failed, not run, or stale>
Evidence basis: <observation time and relevant files/revision/configuration/process state>
Session next: <next action/blocker or none>
Work next / debt: <remaining feature work, shortcuts, or none>
```

At completion or pause, save and read back the final state, current work-record path, checks, owner, and next action. A completed request clears its execution owner and Session next; deferred feature debt remains separate. A new receipt date never refreshes an old check result.
