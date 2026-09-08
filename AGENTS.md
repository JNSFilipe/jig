# Repository maintenance

- Edit canonical skills under `skills/`; generate `plugins/jig/skills/` with `python3 scripts/sync-plugin.py`. Keep standalone skills self-contained and the workflow lightweight.
- Canonical skill directories and `name:` values carry the `jig-` prefix; sync strips it for the plugin, which supplies its own namespace, and rewrites cross-references between skills. Refer to sibling skills as `jig-<name>/SKILL.md` so the rewrite finds them, and never edit the generated copies.
- For a release, change the version only in `plugins/jig/.claude-plugin/plugin.json`; sync updates the marketplace copies. Do not bump versions for every intermediate edit.
- After edits, run `python3 scripts/sync-plugin.py`, `python3 -m unittest discover -s tests -v`, and `bash -n install.sh uninstall.sh`. The tests include the read-only sync/version check; CI also runs it explicitly.
- Protocol examples named by `protocol-example` comments are executed by tests. Preserve their names; either Markdown fence style is supported. Test with local tmux, Bash, OpenSSL, and Perl available; a skip does not verify terminal behavior.
- Use temporary projects and a private tmux socket for tests. Never use real devices, existing sessions, or personal skill installations as fixtures.
- These instructions maintain this collection. The installer must not add repository maintenance instructions or initialization requirements to consumer projects.
