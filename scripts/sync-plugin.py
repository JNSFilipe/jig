#!/usr/bin/env python3
"""Sync canonical skills and manifest version into distribution files, or check drift."""

import argparse
import json
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
    manifest = json.loads((ROOT / "plugins/dev-skills/.claude-plugin/plugin.json").read_text())
    version = manifest["version"]
    if not isinstance(version, str) or not version.strip():
        parser.error("Plugin manifest must have a nonempty version string")
    marketplace_path = ROOT / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    entries = [entry for entry in marketplace["plugins"] if entry["name"] == manifest["name"]]
    if len(entries) != 1:
        parser.error("Marketplace must contain exactly one entry matching the plugin name")
    version_drift = (marketplace.get("version") != version or entries[0].get("version") != version)
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
        if version_drift:
            print(f"Marketplace version differs from plugin manifest: expected {version}")
        if not changed and not extra and not version_drift:
            print(f"Plugin matches {len(source)} canonical skill files; version {version} is synchronized.")
        return int(bool(changed or extra or version_drift))
    # Do not silently remove plugin-only work. Inspect it before a deliberate deletion.
    if extra:
        for path in extra:
            print(f"Resolve plugin-only file before syncing: {path}")
        return 1
    for path in changed:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source[path], target)
    if version_drift:
        marketplace["version"] = entries[0]["version"] = version
        marketplace_path.write_text(json.dumps(marketplace, indent=2) + "\n")
        print(f"Synced marketplace version to {version}.")
    print(f"Synced {len(changed)} files; {len(source)} canonical skill files total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
