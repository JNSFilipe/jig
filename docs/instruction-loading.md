# Instruction loading and live evaluation

## Static instruction budget

Baseline: pre-Pi commit `daee4a3` (`archive/claude-codex`). Revised: canonical files on `main`. Reproduce without model calls or writes:

```bash
python3 scripts/measure-instructions.py --baseline daee4a3
```

The script deduplicates instruction files and counts UTF-8 bytes. Approximate tokens are **ceil(characters / 4)**, not provider/tokenizer measurements. These are instruction-input budgets, not billing, latency or accuracy. Project instructions, source/test reads, tool schemas, host-discovered skill descriptions, output and retries are excluded equally. Revised paths include the first-receipt template; baseline had it inline in memory.

Load sets through first report/handoff:

- Tiny fix: apply + memory + context; baseline additionally required full feedback, revised adds the lazy receipt template.
- Crunch: crunch + memory + context; same feedback/template difference.
- Standalone feedback: feedback + memory + context, revised adds receipt template.
- Substantial change with consequential decision and worker handoff: tiny-fix set + plan + plan template + execution reference; revised additionally loads feedback and detailed transition guidance. This intentionally counts the expensive path, including the optional Pi agent example, rather than hiding safety detail.

| Scenario | Baseline bytes / ~tokens | Revised bytes / ~tokens | Byte reduction |
| --- | ---: | ---: | ---: |
| tiny fix | 33,662 / 8,413 | 19,901 / 4,976 | 40.9% |
| crunch | 29,726 / 7,429 | 15,634 / 3,909 | 47.4% |
| feedback | 25,541 / 6,383 | 18,223 / 4,551 | 28.7% |
| substantial change + handoff | 46,017 / 11,501 | 49,637 / 12,403 | -7.9% |

Common paths shrink; the fully detailed handoff path grows with Pi support. Recovery/audit paths intentionally load more: legacy/liveness recovery, receipt format, observation policy and host transition mechanics remain bundled and explicitly routed. Single writer/Work ID, work versus session state, pre-report freshness, final readback and ownership checkpoints remain in the always-read core.

## Live before/after comparison

Executed on 2026-10-22 with Pi 1.2.0, `openai/gpt-6.1-sol`, thinking `low`. Each run used a new disposable project and private agent directory, identical fixture instructions, no personal skill/settings/session fixtures, and explicit baseline/revised skill paths. The native comparison runs disabled extensions on both sides. These are small controlled samples, not a benchmark of every user's complete extension setup.

[Machine-readable comparison results](evaluation-comparison-final.json) record provider-reported usage, actual tool calls, required check invocations, independently verified behavior, finalized receipt readback, protected-file changes and closeout. Input below is `usage.input + usage.cacheRead + usage.cacheWrite`; all components remain separate in JSON so cached tokens are not misrepresented as uncached/billed input.

| Scenario / revision | Input incl. cache | Output | Total reported tokens | Tool calls | Required suite invocations | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tiny / baseline | 119,273 | 1,328 | 120,601 | 17 | 2 | 70.29 |
| Tiny / revised | 104,832 | 1,340 | 106,172 | 17 | 2 | 78.88 |
| Substantial / baseline | 188,250 | 2,720 | 190,970 | 25 | 1 | 116.55 |
| Substantial / revised | 146,667 | 2,655 | 149,322 | 25 | 1 | 119.01 |

The final paired tiny fix reduced total reported tokens by **12.0%**, substantial change by **21.8%**, with no omitted required checks or observed correctness/receipt/closeout regression. Neither run was faster. Uncached input increased for the substantial revised sample even while total input fell; cache mix and pricing matter, so this is **not** a guaranteed billing saving. One final pair per scenario cannot establish statistical quality or cost superiority. Earlier exploratory runs informed the harness/policy corrections below, rather than being silently counted as successful validations.

### Correctness and lifecycle rubric

- Tiny: blank/whitespace names become `Hello, world!`, named greetings remain trimmed; a frozen two-case independent oracle passes. Both revisions ran the required suite, saved exactly one complete receipt, cleared Session next and read back the finalized contents. No project archive was required.
- Substantial: authorized CSV rows, exact optional status filter, all matching rows/order, header-only empty result, CSV quoting and input immutability pass a frozen six-case oracle. Both revisions updated the supplied change record, reconciled `docs/specs/export.md`, archived exactly once, and saved/read back one complete receipt. No required check was omitted.
- Frozen oracle files live outside the agent's editable project and are run independently after completion. Verification does not rely only on tests the model could weaken. The evaluator compares all protected fixture files, including additions, deletions, modes and symlinks; only explicitly authorized implementation/receipt/runtime artifacts are excluded.

## Observation and worker evaluation

[Workflow results](evaluation-workflows-final.json) contain the final lifecycle/ownership scenarios and an independent reviewer run. [The stricter promotion rerun](evaluation-promotion-final.json) additionally requires an evidence-selected feature-verification classification and preserved failed-check receipt, so a finalized report alone cannot pass a false-completion claim.

| Scenario | Receipt count | Tool calls | Total tokens | Seconds | Observed result |
| --- | ---: | ---: | ---: | ---: | --- |
| Default recorded feedback | 1 | 14 | 58,016 | 60.43 | Finalized/read-back observation; no source/work edits |
| Opted-in eligible ephemeral feedback | 0 | 10 | 30,725 | 28.28 | Omission disclosed; inspected work unchanged |
| Explicit no writes | 0 | 10 | 30,649 | 33.68 | No project additions/changes/deletions; omission disclosed |
| Consequential discrepancy under opt-in (stricter rerun) | 1 | 14 | 62,669 | 58.94 | Promoted to recorded finding; reported failing feature without repairing it |
| Feedback nested in apply | 1 | 19 | 123,293 | 96.09 | Reused enclosing receipt; fix/oracle/checks/final readback passed |
| pi-task implementation worker | 1 | 17 parent | 164,715 combined | 125.50 | Successful private-tmux child; parent inspected edits, reran checks and finalized sole receipt |

The promoted fixture deliberately contains a broken blank-name implementation and conflicting complete/failed-check record. Its independent feature oracle is expected to fail: acceptance means correctly reporting/preserving that finding, not falsely fixing or completing the feature.

Worker evaluation used pi-task 0.12.0 with a fixture-only agent explicitly configured to `openai/gpt-6.1-sol`, no unresolved `skills:` dependencies, and a private tmux socket/session. The successful child used the configured model. Combined usage includes **48,504 child tokens** measured from the finished fixture transcript, not just the parent. It cost more than direct execution of this tiny fix: this supports keeping delegation optional, not a blanket worker preference.

Default versus ephemeral feedback avoided one receipt and four tool calls in this sample. It also removed the historical observation trail; source feature records remained intact. For N eligible routine requests the policy avoids N receipt files, while consequential findings still promote and nested reporting adds no extra receipt. Do not extrapolate these single-sample latency/token differences to every model or extension configuration. Recorded remains the compatibility default.

### Defects found and corrected during evaluation

1. An early observation run treated “do not edit source/work records” as a blanket no-writes instruction, omitting both default and consequential receipts. The core/feedback instructions now explicitly distinguish that restriction from all-writes/read-only. Final default and promotion reruns passed; explicit no-writes still saved nothing.
2. An unconfigured tmux child selected a different provider/model and failed rather than proving inheritance. Final fixture agents explicitly configure the requested model. The execution reference now warns against assuming inheritance and includes an optional agent example without unrelated missing skill dependencies. No personal config was changed.
3. Independent reviewer found the first evaluator protected only two source paths, allowing other prohibited changes to escape detection. The evaluator now compares every protected file/addition/deletion/mode/symlink, with offline regression tests. The final recorded/no-writes/worker results all have no unauthorized changes. A second review identified that receipt finalization alone did not establish the promoted report acknowledged failed feature verification; the stricter classification/receipt rubric and negative false-completion regression now cover that gap.

## Recovery and boundary coverage

Repository tests execute real copy/symlink installation and shell sender/reader/ownership guards on private tmux. They also check example JSON, available/unavailable tool routes, decisions, authoritative memory, progressive links and standalone/plugin bundles. An occupied fixture coding-agent pane rejects input before command injection; original quoting/status/missing-completion tests remain intact.

Legacy crunch/polish lookup, interrupted-session liveness, archive-move recovery and memory audits remain explicitly routed in the core and covered by contract tests and the documented recovery scenarios. Those checks establish discoverability/policy, not a claim that a real crashed personal session was repaired. Context tests do not force live Blackhole compaction, alter provider caches or promise autonomous final writes after crashes.

## Reproduce live checks (opt-in, may incur provider charges)

```bash
python3 scripts/evaluate-pi.py --run --provider <provider> --model <model> \
  --cases tiny substantial --output /tmp/jig-comparison.json

python3 scripts/evaluate-pi.py --run --provider <provider> --model <model> \
  --cases recorded ephemeral no-writes promoted nested worker \
  --task-extension /absolute/path/to/pi-task/dist/index.js \
  --output /tmp/jig-workflows.json
```

The script requires `--run`, copies only auth/model metadata into private temporary agent/HOME directories (removed afterward), and loads only explicit repository skills/optional task extension. No normal CI/model calls, personal configuration repair, real devices or existing tmux sessions are used. It returns nonzero on a failed rubric, timeout, model error or unauthorized fixture change. It is a local evaluation harness, **not an OS security sandbox**. Keep inspecting real outcomes; instruction adherence and provider/cache behavior can vary.
