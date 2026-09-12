"""``runbrief cmd ...`` — capture everything, show a tail."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def _slug(argv: list[str]) -> str:
    raw = "-".join(Path(a).name for a in argv[:3] if a)
    cleaned = "".join(ch if ch.isalnum() or ch in "-._" else "-" for ch in raw)
    return (cleaned.strip("-") or "cmd")[:40]


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_brief(
    argv: list[str],
    *,
    lines: int = 40,
    log_dir: Path,
    cwd: Path | None = None,
) -> tuple[int, Path, str]:
    """Run argv. Return (exit_code, log_path, printed_summary)."""
    if not argv:
        raise ValueError("no command")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{_stamp()}-{_slug(argv)}.log"
    started = time.monotonic()
    proc = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    elapsed = time.monotonic() - started
    body = ""
    if proc.stdout:
        body += proc.stdout
        if not proc.stdout.endswith("\n"):
            body += "\n"
    if proc.stderr:
        if body:
            body += "--- stderr ---\n"
        body += proc.stderr
        if not proc.stderr.endswith("\n"):
            body += "\n"
    header = (
        f"command: {subprocess.list2cmdline(argv)}\n"
        f"exit: {proc.returncode}\n"
        f"seconds: {elapsed:.3f}\n"
        f"cwd: {cwd or Path.cwd()}\n"
        f"---\n"
    )
    log_path.write_text(header + body, encoding="utf-8")
    text_lines = body.splitlines()
    n = len(text_lines)
    tail = text_lines[-lines:] if lines >= 0 else text_lines
    omitted = max(0, n - len(tail))
    summary_lines = [
        f"runbrief: exit {proc.returncode}  {elapsed:.2f}s  {n} lines",
        f"full: {log_path.as_posix()}",
    ]
    if omitted:
        summary_lines.append(f"--- last {len(tail)} of {n} lines ({omitted} omitted) ---")
    else:
        summary_lines.append("--- output ---")
    summary_lines.extend(tail)
    summary = "\n".join(summary_lines) + "\n"
    return proc.returncode, log_path, summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runbrief",
        description="Run a command, keep the full log on disk, print a short tail.",
        epilog="Use -- to stop parsing flags, e.g. runbrief --lines 20 -- pytest -q",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=40,
        metavar="N",
        help="how many trailing lines to print (default: 40)",
    )
    parser.add_argument(
        "--dir",
        dest="log_dir",
        default=".runbrief",
        help="directory for full logs (default: .runbrief)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to run (prefix with -- if it has flags)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(raw)
    cmd = list(args.command)
    if cmd[:1] == ["--"]:
        cmd = cmd[1:]
    if not cmd:
        parser.print_help()
        return 2
    try:
        code, _path, summary = run_brief(
            cmd,
            lines=max(0, args.lines),
            log_dir=Path(args.log_dir),
        )
    except OSError as exc:
        print(f"runbrief: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(summary)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
