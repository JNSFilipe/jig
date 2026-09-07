#!/usr/bin/env python3
"""Copy canonical skills into the standalone plugin, or check for drift."""

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]


def inventory(root):
    return {
        path.relative_to(root): path
        for skill in root.iterdir()
        if skill.is_dir() and (skill / "SKILL.md").is_file()
        for path in skill.rglob("*")
        if path.is_file() and path.name != ".DS_Store" and "__pycache__" not in path.parts
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without writing")
    args = parser.parse_args()
    source = inventory(ROOT / "skills")
    destination = ROOT / "plugins/dev-skills/skills"
    destination.mkdir(parents=True, exist_ok=True) if not args.check else None
    existing = inventory(destination) if destination.exists() else {}
    changed = sorted(path for path, src in source.items()
                     if path not in existing or src.read_bytes() != existing[path].read_bytes())
    extra = sorted(set(existing) - set(source))
    if args.check:
        for path in changed:
            print(f"Missing or different: {path}")
        for path in extra:
            print(f"Plugin-only file: {path}")
        if not changed and not extra:
            print(f"Plugin matches {len(source)} canonical skill files.")
        return int(bool(changed or extra))
    # Do not silently remove plugin-only work. Inspect it before a deliberate deletion.
    if extra:
        for path in extra:
            print(f"Resolve plugin-only file before syncing: {path}")
        return 1
    for path in changed:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source[path], target)
    print(f"Synced {len(changed)} files; {len(source)} canonical skill files total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
