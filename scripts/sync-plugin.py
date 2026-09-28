#!/usr/bin/env python3
"""Sync canonical skills and manifest version into distribution files, or check drift.

Canonical skills are prefixed (jig-plan). The plugin namespace already supplies
that prefix, so the distributed copies drop it (jig:plan) and every reference
between skills is rewritten to match.
"""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/jig"
PREFIX = "jig-"


def canonical_skills(root):
    return sorted(path for path in root.iterdir()
                  if path.is_dir() and (path / "SKILL.md").is_file())


def distributed_name(name):
    return name[len(PREFIX):] if name.startswith(PREFIX) else name


def shared_references(root):
    """Bundle shared instructions into each standalone skill without symlinks."""
    shared = root / "_shared"
    return {
        Path(skill.name) / "references" / path.relative_to(shared): path.read_bytes()
        for skill in canonical_skills(root)
        for path in sorted(shared.rglob("*.md"))
    }


def distribute(root, shared):
    """Expected plugin contents: unprefixed directories and rewritten references."""
    skills = canonical_skills(root)
    prefixed = [skill.name for skill in skills if skill.name.startswith(PREFIX)]
    sources = {}
    for skill in skills:
        for path in sorted(skill.rglob("*")):
            if not path.is_file() or path.name == ".DS_Store" or "__pycache__" in path.parts:
                continue
            sources[Path(skill.name) / path.relative_to(skill)] = path.read_bytes()
    sources.update(shared)
    expected = {}
    for path, data in sources.items():
        text = data.decode()
        for name in prefixed:
            text = text.replace(name, distributed_name(name))
        relative = Path(distributed_name(path.parts[0]), *path.parts[1:])
        expected[relative] = text.encode()
    return expected


def present(root):
    if not root.exists():
        return {}
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
    manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    version = manifest["version"]
    if not isinstance(version, str) or not version.strip():
        parser.error("Plugin manifest must have a nonempty version string")
    marketplace_path = ROOT / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    entries = [entry for entry in marketplace["plugins"] if entry["name"] == manifest["name"]]
    if len(entries) != 1:
        parser.error("Marketplace must contain exactly one entry matching the plugin name")
    version_drift = (marketplace.get("version") != version or entries[0].get("version") != version)
    source_root = ROOT / "skills"
    shared = shared_references(source_root)
    shared_changed = sorted(path for path, data in shared.items()
                            if not (source_root / path).is_file()
                            or (source_root / path).read_bytes() != data)
    expected = distribute(source_root, shared)
    destination = PLUGIN / "skills"
    existing = present(destination)
    changed = sorted(path for path, data in expected.items()
                     if path not in existing or existing[path].read_bytes() != data)
    extra = sorted(set(existing) - set(expected))
    if args.check:
        for path in shared_changed:
            print(f"Missing or different shared reference: skills/{path}")
        for path in changed:
            print(f"Missing or different: {path}")
        for path in extra:
            print(f"Plugin-only file: {path}")
        if version_drift:
            print(f"Marketplace version differs from plugin manifest: expected {version}")
        if not changed and not shared_changed and not extra and not version_drift:
            print(f"Plugin matches {len(expected)} canonical skill files; version {version} is synchronized.")
        return int(bool(changed or shared_changed or extra or version_drift))
    # Do not silently remove plugin-only work. Inspect it before a deliberate deletion.
    if extra:
        for path in extra:
            print(f"Resolve plugin-only file before syncing: {path}")
        return 1
    for path in shared_changed:
        target = source_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(shared[path])
    destination.mkdir(parents=True, exist_ok=True)
    for path in changed:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(expected[path])
    if version_drift:
        marketplace["version"] = entries[0]["version"] = version
        marketplace_path.write_text(json.dumps(marketplace, indent=2) + "\n")
        print(f"Synced marketplace version to {version}.")
    print(f"Synced {len(shared_changed)} shared references and {len(changed)} plugin files; "
          f"{len(expected)} canonical skill files total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
