# Compact change record

Use the shape below, replacing the instructional text with project facts. Omit optional sections that add nothing. Paths in the record are repository-relative so they remain valid after archiving or switching agents. Status is informational: `planned`, `in-progress`, `blocked`, or `complete`.

```markdown
# <Change title>

Status: planned

## Why / scope
<Problem and intended outcome. Relevant exclusions.>

## Behavior
Target: docs/specs/<capability>.md

### Add: <Stable requirement name>
<Observable contract. Use Modify or Remove for an existing requirement;
use Preserve for a refactor with no contract change.>
- Given <context>, when <action>, then <observable result>.
- Given <meaningful edge/failure case>, when <action>, then <result>.

## Approach
<Relevant code/test paths, constraints, and decisions with brief reasons.>

## Tasks
- [ ] <First working outcome> — check: <test or observable evidence>.
- [ ] <Next outcome> — check: <test or observable evidence>.

## Evidence
<Initially, intended check commands and any required setup. During work,
record actual command, outcome, and the behavior it establishes.
Distinguish passed, failed, and not run. Do not paste full logs.>

## Next
<Next action or blocker; remove when complete.>
```

For multiple capabilities, group requirements by target. Do not create baseline specs while drafting a proposal: these describe the implemented contract in the current project files and are reconciled at close. Existing specs may cover only part of a brownfield system; specify only the area touched.

An existing local plan can serve as the record if it has the same information. Keep one authoritative task list on disk, with enough intent to resume without an external service or prior chat. Version control is optional.
