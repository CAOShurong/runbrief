---
name: runbrief
description: Wrap noisy test/build/lint commands so the full log stays on disk and the transcript only gets a short tail.
---

# runbrief

Use this for commands that often dump hundreds of lines (`pytest`, compilers,
linters, package installs). Do not wrap interactive or TTY tools.

```bash
runbrief pytest -q
runbrief --lines 20 -- npm test
```

The printed block is: exit code, duration, line count, `full:` log path, last N
lines (default N=40). Open that file if the tail is not enough. Do not re-run
the same command without `runbrief` just to see the rest.

`--` is required when the child has flags. `--lines` and `--dir` are the only
`runbrief` flags.
