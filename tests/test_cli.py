import sys
from pathlib import Path

from runbrief.cli import main, run_brief


def test_run_brief_writes_log_and_tail(tmp_path: Path):
    code, log_path, summary = run_brief(
        [sys.executable, "-c", "print('keep-me'); print('tail-line')"],
        lines=1,
        log_dir=tmp_path,
    )
    assert code == 0
    text = log_path.read_text(encoding="utf-8")
    assert "keep-me" in text
    assert "tail-line" in text
    assert "keep-me" not in summary.split("---")[-1]
    assert "tail-line" in summary
    assert "exit 0" in summary
    assert log_path.name in summary


def test_nonzero_exit(tmp_path: Path):
    code, _log, summary = run_brief(
        [sys.executable, "-c", "raise SystemExit(7)"],
        lines=10,
        log_dir=tmp_path,
    )
    assert code == 7
    assert "exit 7" in summary


def test_stderr_is_logged_after_marker(tmp_path: Path):
    code, log_path, summary = run_brief(
        [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"],
        lines=10,
        log_dir=tmp_path,
    )
    assert code == 0
    text = log_path.read_text(encoding="utf-8")
    assert "--- stderr ---" in text
    assert "out" in text
    assert "err" in text
    assert "err" in summary


def test_main_requires_command():
    assert main([]) == 2


def test_main_forwards_exit(tmp_path: Path):
    rc = main(["--dir", str(tmp_path), "--", sys.executable, "-c", "print(1)"])
    assert rc == 0
    logs = list(tmp_path.glob("*.log"))
    assert len(logs) == 1


def test_main_missing_executable(tmp_path: Path):
    rc = main(["--dir", str(tmp_path), "--", "runbrief-no-such-cmd-xyz"])
    assert rc == 1


def test_omitted_banner(tmp_path: Path):
    code, log_path, summary = run_brief(
        [sys.executable, "-c", "print('\\n'.join('L%d' % i for i in range(10)))"],
        lines=3,
        log_dir=tmp_path,
    )
    assert code == 0
    assert "last 3 of 10 lines (7 omitted)" in summary
    assert "L9" in summary
    assert "L0" not in summary.split("---")[-1]
    header = log_path.read_text(encoding="utf-8").split("---", 1)[0]
    assert "exit: 0" in header
    assert "command:" in header
