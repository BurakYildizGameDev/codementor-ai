"""`run_process` iptali (Faz 19): iptal olayı süreç ağacını zaman aşımını beklemeden öldürür."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

from codementor.validation.runner import ProcessLimits, ProcessResult, run_process
from tests.unit.test_runner import _alive

PY = sys.executable
LONG = ProcessLimits(timeout_s=60, memory_mb=512)


def _tree(pid_file: Path) -> str:
    """Çocuk bir torun başlatır, torunun PID'ini dosyaya yazar ve bekler."""
    return (
        "import pathlib, subprocess, sys, time\n"
        "p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))\n"
        "time.sleep(60)\n"
    )


def _wait_for(path: Path, timeout: float = 20) -> int:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists() and (text := path.read_text().strip()):
            return int(text)
        time.sleep(0.05)
    raise AssertionError("torun süreç başlamadı")


def test_cancel_event_kills_process_tree_quickly(tmp_path: Path) -> None:
    pid_file = tmp_path / "grandchild.pid"
    cancel = threading.Event()
    out: list[ProcessResult] = []
    thread = threading.Thread(
        target=lambda: out.append(run_process([PY, "-c", _tree(pid_file)], "", LONG, cancel=cancel))
    )
    thread.start()
    pid = _wait_for(pid_file)  # sabit uyku yok: yavaş makinede de torun hazır olunca iptal
    start = time.perf_counter()
    cancel.set()
    thread.join(10)
    elapsed = time.perf_counter() - start
    assert not thread.is_alive()
    (result,) = out
    assert result.cancelled
    assert not result.timed_out
    assert result.returncode is None
    assert elapsed < 3, f"iptal {elapsed:.1f} sn sürdü"
    deadline = time.monotonic() + 5
    while _alive(pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _alive(pid), "torun süreç iptalden sonra hâlâ yaşıyor"


def test_cancel_before_start_returns_cancelled() -> None:
    cancel = threading.Event()
    cancel.set()
    result = run_process([PY, "-c", "import time; time.sleep(60)"], "", LONG, cancel=cancel)
    assert result.cancelled


def test_no_cancel_behaviour_unchanged() -> None:
    start = time.perf_counter()
    result = run_process([PY, "-c", "print('ok')"], "", LONG, cancel=threading.Event())
    assert result.returncode == 0
    assert result.stdout.strip() == "ok"
    assert not result.cancelled
    assert not result.timed_out
    assert time.perf_counter() - start < 10


def test_timeout_with_cancel_event_still_times_out() -> None:
    limits = ProcessLimits(timeout_s=1, memory_mb=512)
    result = run_process(
        [PY, "-c", "import time; time.sleep(30)"], "", limits, cancel=threading.Event()
    )
    assert result.timed_out
    assert not result.cancelled
