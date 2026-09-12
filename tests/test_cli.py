from pathlib import Path

from runbrief.cli import main, run_brief

SCRATCH = Path(__file__).resolve().parent / "_scratch"


def _scratch() -> Path:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    return SCRATCH


def test_run_brief_writes_log_and_tail():
    log_dir = _scratch() / "t1"
    log_dir.mkdir(exist_ok=True)
    code, log_path, summary = run_brief(
        ["python", "-c", "print('keep-me'); print('tail-line')"],
        lines=1,
        log_dir=log_dir,
    )
    assert code == 0
    text = log_path.read_text(encoding="utf-8")
    assert "keep-me" in text
    assert "tail-line" in text
    assert "keep-me" not in summary.split("---")[-1]
    assert "tail-line" in summary
    assert "exit 0" in summary
    assert log_path.name in summary


def test_nonzero_exit():
    log_dir = _scratch() / "t2"
    log_dir.mkdir(exist_ok=True)
    code, _log, summary = run_brief(
        ["python", "-c", "raise SystemExit(7)"],
        lines=10,
        log_dir=log_dir,
    )
    assert code == 7
    assert "exit 7" in summary


def test_main_requires_command():
    assert main([]) == 2


def test_main_forwards_exit():
    log_dir = _scratch() / "t3"
    rc = main(["--dir", str(log_dir), "--", "python", "-c", "print(1)"])
    assert rc == 0
    logs = list(log_dir.glob("*.log"))
    assert len(logs) == 1
