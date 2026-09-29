"""Güvenli alt süreç çalıştırıcısı testleri (mimari §5.2.3).

Gerçek derleyici yerine `sys.executable -c ...` ile sahte süreçler kullanılır.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from codementor.validation import runner
from codementor.validation.runner import OUTPUT_LIMIT, ProcessLimits, run_process

LIMITS = ProcessLimits(timeout_s=10, memory_mb=512)
PY = sys.executable


def _py(code: str, stdin: str = "", limits: ProcessLimits = LIMITS) -> runner.ProcessResult:
    return run_process([PY, "-c", code], stdin, limits)


def _alive(pid: int) -> bool:
    if sys.platform == "win32":
        import ctypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        kernel32.CloseHandle(handle)
        return code.value == 259  # STILL_ACTIVE
    import os

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def test_stdin_delivered_and_stdout_captured() -> None:
    code = "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"
    result = _py(code, stdin="int ğ = 1;\n// çıktı\n")
    assert result.error is None
    assert result.returncode == 0
    assert result.stdout == "int ğ = 1;\n// çıktı\n"


def test_stderr_captured_separately() -> None:
    result = _py("import sys; print('out'); print('err', file=sys.stderr)")
    assert result.stdout.strip() == "out"
    assert result.stderr.strip() == "err"


def test_cwd_is_empty_temp_dir_and_removed() -> None:
    result = _py("import os, json; print(json.dumps([os.getcwd(), os.listdir('.')]))")
    cwd, listing = json.loads(result.stdout)
    assert listing == []
    assert Path(cwd).resolve() != Path.cwd().resolve()
    assert not Path(cwd).exists()


def test_env_sanitized(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "SECRET_TOKEN",
        "CPATH",
        "C_INCLUDE_PATH",
        "CPLUS_INCLUDE_PATH",
        "GCC_EXEC_PREFIX",
    ):
        monkeypatch.setenv(name, "/etc")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    result = _py("import os, json; print(json.dumps(dict(os.environ)))")
    env = {k.upper(): v for k, v in json.loads(result.stdout).items()}
    for name in ("SECRET_TOKEN", "CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "OPENAI_API_KEY"):
        assert name not in env
    assert "GCC_EXEC_PREFIX" not in env
    assert env["LC_ALL"] == "C"
    assert "PATH" in env
    assert env["TEMP"] == env["TMP"]


def test_temp_vars_point_to_private_dir() -> None:
    code = "import os, json; print(json.dumps([os.getcwd(), os.environ['TMP']]))"
    cwd, tmp = json.loads(_py(code).stdout)
    assert Path(tmp).resolve() == Path(cwd).resolve()


def test_extra_env_is_passed() -> None:
    result = run_process(
        [PY, "-c", "import os; print(os.environ['DOTNET_NOLOGO'])"],
        "",
        LIMITS,
        extra_env={"DOTNET_NOLOGO": "1"},
    )
    assert result.stdout.strip() == "1"


def test_timeout_kills_process_tree() -> None:
    grandchild = "import time; time.sleep(60)"
    code = (
        "import subprocess, sys, time\n"
        f"p = subprocess.Popen([sys.executable, '-c', {grandchild!r}])\n"
        "print(p.pid, flush=True)\n"
        "time.sleep(60)\n"
    )
    start = time.perf_counter()
    result = _py(code, limits=ProcessLimits(timeout_s=2, memory_mb=512))
    elapsed = time.perf_counter() - start
    assert result.timed_out
    assert elapsed < 15
    pid = int(result.stdout.split()[0])
    deadline = time.monotonic() + 5
    while _alive(pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _alive(pid), "torun süreç zaman aşımından sonra hâlâ yaşıyor"


def test_output_capped() -> None:
    code = "import sys; sys.stdout.write('x' * 300_000); sys.stderr.write('y' * 300_000)"
    result = _py(code)
    assert result.returncode == 0
    assert result.truncated
    assert len(result.stdout.encode()) == OUTPUT_LIMIT
    assert len(result.stderr.encode()) == OUTPUT_LIMIT


def test_process_not_reading_stdin_does_not_deadlock() -> None:
    result = _py("print('ok')", stdin="x" * 2_000_000)
    assert result.stdout.strip() == "ok"
    assert not result.timed_out


def test_missing_executable_no_exception(tmp_path: Path) -> None:
    result = run_process([str(tmp_path / "yok-derleyici")], "", LIMITS)
    assert result.error is not None
    assert result.returncode is None
    assert not result.timed_out


def test_memory_limit_enforced() -> None:
    code = "b = bytearray(1024 * 1024 * 1024); print(len(b))"
    result = _py(code, limits=ProcessLimits(timeout_s=20, memory_mb=256))
    assert not result.timed_out
    assert result.returncode != 0


def test_memory_limit_can_skip_address_space() -> None:
    """dotnet sanal adres alanı ayırır; RLIMIT_AS ona uygulanmaz (Job Object commit sınırı)."""
    limits = ProcessLimits(timeout_s=10, memory_mb=256, limit_address_space=False)
    assert _py("print(1)", limits=limits).returncode == 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows Job Object")
def test_windows_job_limits_process_count() -> None:
    code = (
        "import subprocess, sys\n"
        "procs = []\n"
        "try:\n"
        f"    for _ in range({runner.MAX_PROCESSES + 4}):\n"
        "        cmd = [sys.executable, '-c', 'import time; time.sleep(5)']\n"
        "        procs.append(subprocess.Popen(cmd))\n"
        "    print('all')\n"
        "except OSError:\n"
        "    print('limited')\n"
        "for p in procs: p.kill()\n"
    )
    assert _py(code).stdout.strip() == "limited"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX rlimit")
def test_posix_rlimits_applied() -> None:
    code = (
        "import resource, json\n"
        "print(json.dumps([resource.getrlimit(resource.RLIMIT_CPU)[0],"
        " resource.getrlimit(resource.RLIMIT_CORE)[0]]))"
    )
    cpu, core = json.loads(_py(code).stdout)
    assert 0 < cpu <= LIMITS.timeout_s + 1
    assert core == 0


def test_never_uses_shell() -> None:
    source = Path(runner.__file__).read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "os.system" not in source


def test_argv_must_be_list() -> None:
    with pytest.raises(TypeError):
        run_process("gcc -fsyntax-only -", "", LIMITS)  # type: ignore[arg-type]


# ------------------------------------------------------------------ güvenlik denetimi regresyonları


def test_grandchild_killed_after_normal_exit() -> None:
    """Denetim D2: ana süreç normal çıksa da torunlar yaşamaya devam etmemeli."""
    grandchild = "import time; time.sleep(60)"
    code = (
        "import subprocess, sys\n"
        f"p = subprocess.Popen([sys.executable, '-c', {grandchild!r}],"
        " stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
        "print(p.pid, flush=True)\n"
    )
    result = _py(code)
    assert not result.timed_out
    pid = int(result.stdout.split()[0])
    deadline = time.monotonic() + 5
    while _alive(pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _alive(pid)


def test_unexpected_error_kills_process(monkeypatch: pytest.MonkeyPatch) -> None:
    """Denetim D1: denetim sırasında beklenmedik hata → süreç öldürülür, istisna yok."""
    started: list[int] = []

    def boom(proc: object, *_args: object) -> runner.ProcessResult:
        started.append(proc.pid)  # type: ignore[attr-defined]
        raise RuntimeError("iç hata")

    monkeypatch.setattr(runner, "_supervise", boom)
    result = _py("import time; time.sleep(60)")
    assert result.error is not None
    assert "RuntimeError" in result.error
    deadline = time.monotonic() + 5
    while _alive(started[0]) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _alive(started[0])


@pytest.mark.skipif(sys.platform != "win32", reason="Windows Job Object")
def test_windows_job_failure_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Denetim D3: Job Object kurulamazsa süreç sınırsız çalıştırılmaz."""
    from codementor.validation import _winjob

    def no_job(*_args: object) -> None:
        raise OSError("iş kurulamadı")

    monkeypatch.setattr(_winjob, "Job", no_job)
    result = _py("print('ran')")
    assert result.error is not None
    assert "ran" not in result.stdout


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX başlatıcısı")
def test_posix_uses_bootstrap_not_preexec(monkeypatch: pytest.MonkeyPatch) -> None:
    """Denetim O3: rlimit'ler preexec_fn yerine exec öncesi başlatıcıda uygulanır."""
    import subprocess

    seen: dict[str, object] = {}
    real = subprocess.Popen

    def spy(args: list[str], **kwargs: object) -> object:
        seen.update(kwargs, args=args)
        return real(args, **kwargs)  # type: ignore[call-overload]

    monkeypatch.setattr(subprocess, "Popen", spy)
    assert _py("print(1)").stdout.strip() == "1"
    assert seen.get("preexec_fn") is None
    assert seen["start_new_session"] is True
    args = seen["args"]
    assert isinstance(args, list)
    assert args[:4] == [sys.executable, "-I", "-S", "-c"]


def test_empty_argv_rejected() -> None:
    with pytest.raises(TypeError):
        run_process([], "", LIMITS)


def test_posix_bootstrap_is_valid_python() -> None:
    compile(runner._RLIMIT_BOOTSTRAP, "<bootstrap>", "exec")
    assert "os.execv(sys.argv[4], sys.argv[4:])" in runner._RLIMIT_BOOTSTRAP


@pytest.mark.parametrize("command", ["python", "gcc", "./gcc", "bin/gcc"])
def test_bare_or_relative_executable_rejected(command: str) -> None:
    # çıplak ad Windows'ta çalışma dizininde de aranır (öğrenci projesindeki gcc.exe)
    result = run_process([command, "--version"], "", LIMITS)
    assert result.returncode is None
    assert result.error is not None
    assert "mutlak yol" in result.error
