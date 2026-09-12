---
schema_version: portable-project-memory/v1
handoff_revision: 2
updated_at: "2026-09-13T00:40:00+08:00"
updated_by: "grok-unattended"
base_revision: git:d789192
status: active
---

# Project Handoff

## Current objective

AI **context** tool: `runbrief` runs a command, writes the full log, prints a
short tail so coding-agent transcripts do not swallow pytest dumps.

## Confirmed state

- https://github.com/CAOShurong/runbrief public
- CI was red: setuptools rejected `License :: OSI Approved :: MIT License`
  alongside `license = "MIT"`. Classifier removed.
- Tests no longer share `tests/_scratch` (leftover logs made `len(logs)==1` fail).

## Next actions

1. Confirm CI green after this push.
2. Keep README honest. Do not add flags, JSON, MCP, or a harness.
3. Stop grinding at ~90%.

## User decisions required

None.
