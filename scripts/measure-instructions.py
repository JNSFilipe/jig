#!/usr/bin/env python3
"""Compare documented instruction-load paths, not measured model billing/quality.

Run from a clone containing the pre-Pi baseline commit. No files are written.
Token estimates use ceil(UTF-8 character count / 4), not a model tokenizer.
"""

import argparse
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CORE = ["skills/_shared/memory.md", "skills/_shared/context.md"]
FEEDBACK = "skills/jig-feedback/SKILL.md"
RECEIPT = "skills/_shared/receipt-format.md"
EXECUTION = "skills/jig-apply/references/context-and-execution.md"
TRANSITION = "skills/_shared/context-transitions.md"


def load_paths():
    """Unique files loaded through first report/handoff, excluding project code.

    Revised paths conservatively include the first-receipt template. A substantial
    change includes planning, a consequential decision and a worker handoff, so it
    loads both detailed feedback and transition guidance rather than hiding cost.
    """
    paths = {}
    for skill in ("apply", "crunch", "feedback"):
        entry = f"skills/jig-{skill}/SKILL.md"
        paths["tiny fix" if skill == "apply" else skill] = (
            list(dict.fromkeys([entry, *CORE, FEEDBACK])),
            list(dict.fromkeys([entry, *CORE, RECEIPT])),
        )
    extra = ["skills/jig-plan/SKILL.md", "skills/jig-plan/references/change-template.md",
             EXECUTION]
    paths["substantial change + handoff"] = (
        [*paths["tiny fix"][0], *extra],
        [*paths["tiny fix"][1], FEEDBACK, *extra, TRANSITION],
    )
    return paths


def measure(paths, baseline=None):
    contents = []
    for path in paths:
        if baseline:
            contents.append(subprocess.check_output(
                ["git", "show", f"{baseline}:{path}"], cwd=ROOT).decode())
        else:
            contents.append((ROOT / path).read_text())
    return sum(len(s.encode()) for s in contents), math.ceil(sum(map(len, contents)) / 4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="daee4a3")
    args = parser.parse_args()
    print("| Scenario | Baseline bytes / ~tokens | Revised bytes / ~tokens | Byte reduction |")
    print("| --- | ---: | ---: | ---: |")
    for name, (before, after) in load_paths().items():
        old_bytes, old_tokens = measure(before, args.baseline)
        new_bytes, new_tokens = measure(after)
        print(f"| {name} | {old_bytes:,} / {old_tokens:,} | "
              f"{new_bytes:,} / {new_tokens:,} | {100 * (1 - new_bytes / old_bytes):.1f}% |")


if __name__ == "__main__":
    main()
