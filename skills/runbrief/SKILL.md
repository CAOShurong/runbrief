---
name: runbrief
description: Wrap test/build/lint commands so the full log stays on disk and the agent transcript only gets a short tail.
---

# runbrief

Coding-agent transcripts die when `pytest` or a compiler dumps thousands of
lines into context. Run those commands through `runbrief`.

```bash
runbrief pytest -q
runbrief --lines 20 -- npm test
```

You get: exit code, duration, line count, path to the full log, last N lines.
Read the file at `full:` only if you need more than the tail.

Do not re-run the same command without `runbrief` "to see the rest" unless
the tail is actually insufficient. Open the log file instead.
