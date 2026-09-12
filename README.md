# runbrief

[![ci](https://github.com/CAOShurong/runbrief/actions/workflows/ci.yml/badge.svg)](https://github.com/CAOShurong/runbrief/actions/workflows/ci.yml)

**Agents should not eat a 4 000-line pytest dump.** Wrap the command: full log on disk, last 40 lines in the transcript.

```bash
pip install git+https://github.com/CAOShurong/runbrief.git
runbrief pytest -q
```

Captured locally wrapping a 50-line command that exits 1 (`runbrief --lines 5`):

```text
runbrief: exit 1  0.05s  50 lines
full: .runbrief/20260912T164838Z-python-_demo.py.log
--- last 5 of 50 lines (45 omitted) ---
line-46
line-47
line-48
line-49
line-50
```

This is **context control**, not a test runner. The child is unchanged; only
what the coding agent *sees* is shortened. Open the file at `full:` when the
tail is not enough.

Skill file: [`skills/runbrief/SKILL.md`](skills/runbrief/SKILL.md).

## Flags

```bash
runbrief --lines 20 -- pytest -q
runbrief --dir .runbrief -- npm test
```

`--` stops `runbrief` from eating the child's flags. Exit code is the child's
exit code. Stdout and stderr both go in the log (stderr after `--- stderr ---`).

`--lines` and `--dir` are the only flags. There is no JSON mode, no live
follow, no sandbox.

## Why this and not `pytest -q`

Quiet mode still dumps failures in full. Agents then paste the dump into the
next turn. `runbrief` always has a hard line budget for the transcript.

Not a sandbox. Not an MCP server. Not a harness. One process, no dependencies.
The child is not rewritten, stubbed, or timeout-killed.

## Install the skill

Copy `skills/runbrief/SKILL.md` into `.agents/skills/runbrief/` (Grok),
`.claude/skills/runbrief/` (Claude Code), or your agent's skill directory.
