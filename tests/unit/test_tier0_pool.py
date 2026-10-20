"""Tier 0 sıcak işçi havuzu testleri (ADR-0032): güvenlik sınırı, yeniden kullanım, eşzamanlılık."""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.models.validation import Tier0Result
from codementor.validation import tier0_isolation, tier0_pool
from codementor.validation.runner import ProcessLimits, ProcessResult
from codementor.validation.tier0_isolation import (
    FAILURE_MESSAGE,
    INFRA_MESSAGE,
    TIMEOUT_MESSAGE,
    check_syntax,
    close_tier0_pool,
    get_tier0_pool,
)
from codementor.validation.tier0_pool import (
    Tier0Worker,
    Tier0WorkerPool,
    WorkerError,
    WorkerStartError,
    worker_limits,
)

VALID = "int main(void) { return 0; }"
_SANITIZED_KEYS = {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR", "LC_ALL", "LANG"}


def _code(text: str = VALID, language: Language = Language.C) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language))


def _limits() -> ProcessLimits:
    return worker_limits(memory_mb=1024, timeout_s=5.0, max_requests=10)


@pytest.fixture(autouse=True)
def _fresh_global_pool() -> Iterator[None]:
    close_tier0_pool()
    yield
    close_tier0_pool()


def test_worker_executes_and_closes_cleanly() -> None:
    worker = Tier0Worker(_limits())
    try:
        assert not worker.execute(_code(), timeout_s=5.0).has_errors
        assert worker.execute(_code("int main(void) { int x = 1 return x; }"), 5.0).has_errors
        assert worker.requests == 2
    finally:
        worker.close()
    # Süreç beklenmiş (POSIX'te zombi yok), borular kapalı (tutamak sızmaz)
    assert not worker.is_alive()
    assert worker.proc.returncode is not None
    assert worker.proc.stdin is not None
    assert worker.proc.stdin.closed
    assert worker.proc.stdout is not None
    assert worker.proc.stdout.closed
    worker.close()  # ikinci çağrı güvenli


def test_worker_starts_inside_runner_sandbox(monkeypatch: pytest.MonkeyPatch) -> None:
    """Soğuk yolla aynı sınır: izin listeli ortam, boş geçici cwd, Job Object / rlimit."""
    monkeypatch.setenv("CODEMENTOR_TEST_SECRET", "gizli-anahtar")
    captured: dict[str, Any] = {}
    real_popen = subprocess.Popen

    def spy(argv: list[str], **kwargs: Any) -> subprocess.Popen[bytes]:
        captured.update(kwargs, argv=argv)
        return real_popen(argv, **kwargs)

    monkeypatch.setattr(tier0_pool.subprocess, "Popen", spy)
    worker = Tier0Worker(_limits())
    try:
        env = captured["env"]
        assert "CODEMENTOR_TEST_SECRET" not in env
        assert set(env) <= _SANITIZED_KEYS
        cwd = Path(captured["cwd"])
        assert cwd.is_dir()
        assert cwd.resolve() != Path.cwd().resolve()
        assert not any(cwd.iterdir())
        assert env["TEMP"] == captured["cwd"]
        assert captured["stderr"] is subprocess.DEVNULL
        if sys.platform == "win32":
            assert captured["creationflags"] & subprocess.CREATE_NO_WINDOW
            assert worker._tree._job is not None  # bellek ve süreç sınırlı iş nesnesinde
        else:
            assert captured["start_new_session"]
            assert "-c" in captured["argv"]  # rlimit başlatıcısı
        assert not worker.execute(_code(), 5.0).has_errors
    finally:
        worker.close()
    assert not cwd.exists()


def test_warm_worker_enforces_memory_cap() -> None:
    """ADR-0024 bombası (~4,2 GB): süre bol olsa da işçi 1024 MB'de ölür, analiz güvenle durur."""
    with Tier0WorkerPool(1, memory_mb=1024, timeout_s=30.0) as pool:
        start = time.perf_counter()
        res = pool.try_check_syntax(_code("a<" * 20000, Language.CSHARP))
        elapsed = time.perf_counter() - start
        assert not pool._idle
    assert res is not None
    assert res.stopped
    assert res.diagnostics[0].message == FAILURE_MESSAGE
    assert elapsed < 20


def test_worker_start_fails_closed_without_job(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tier0_pool.ProcessTree, "started", lambda _self, _proc: False)
    with pytest.raises(WorkerStartError):
        Tier0Worker(_limits())


def test_pool_returns_infra_message_and_frees_slot_when_start_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tier0_pool.ProcessTree, "started", lambda _self, _proc: False)
    with Tier0WorkerPool(1) as pool:
        for _ in range(2):  # ikincisi de INFRA: yuva geri verildi (None değil)
            res = pool.try_check_syntax(_code())
            assert res is not None
            assert res.stopped
            assert res.diagnostics[0].message == INFRA_MESSAGE


def test_pool_reuses_same_worker_process() -> None:
    with Tier0WorkerPool(1) as pool:
        first = pool.try_check_syntax(_code())
        assert first is not None
        assert not first.has_errors
        pid = pool._idle[0].proc.pid
        second = pool.try_check_syntax(_code("def foo():\n    return 42\n", Language.PYTHON))
        assert second is not None
        assert not second.has_errors
        assert pool._idle[0].proc.pid == pid


def test_pool_recycles_worker_after_request_budget() -> None:
    """POSIX CPU sınırı birikimli: bütçe dolunca işçi kapanır, yenisi açılır."""
    with Tier0WorkerPool(1, max_requests=2) as pool:
        pool.try_check_syntax(_code())
        first = pool._idle[0]
        pool.try_check_syntax(_code())
        assert not pool._idle
        assert not first.is_alive()
        pool.try_check_syntax(_code())
        assert pool._idle[0].proc.pid != first.proc.pid


def test_pool_timeout_stops_analysis_and_kills_worker(monkeypatch: pytest.MonkeyPatch) -> None:
    created: list[Tier0Worker] = []
    with Tier0WorkerPool(1, timeout_s=0.001) as pool:
        original = pool._new_worker

        def tracked() -> Tier0Worker:
            created.append(original())
            return created[-1]

        monkeypatch.setattr(pool, "_new_worker", tracked)
        res = pool.try_check_syntax(_code())
        assert not pool._idle
    assert res is not None
    assert res.stopped
    assert res.diagnostics[0].message == TIMEOUT_MESSAGE.format(seconds="0.001")
    assert not created[0].is_alive()
    assert created[0].proc.returncode is not None


def test_pool_worker_failure_uses_failure_message(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(_self: Tier0Worker, _code: NormalizedCode, _timeout_s: float) -> Tier0Result:
        raise WorkerError("işçi çıktısı geçersiz")

    monkeypatch.setattr(Tier0Worker, "execute", broken)
    with Tier0WorkerPool(1) as pool:
        res = pool.try_check_syntax(_code())
        assert not pool._idle
    assert res is not None
    assert res.stopped
    assert res.diagnostics[0].message == FAILURE_MESSAGE


def test_pool_replaces_dead_idle_worker() -> None:
    with Tier0WorkerPool(1) as pool:
        pool.try_check_syntax(_code())
        dead = pool._idle[0]
        dead.proc.kill()
        dead.proc.wait()
        res = pool.try_check_syntax(_code())
        assert res is not None
        assert not res.has_errors
        assert pool._idle[0] is not dead


def test_pool_never_exceeds_max_workers() -> None:
    with Tier0WorkerPool(2) as pool:
        held = [pool.acquire(), pool.acquire()]
        try:
            assert all(w is not None for w in held)
            assert pool.acquire() is None
            assert pool.try_check_syntax(_code()) is None
        finally:
            for worker in held:
                assert worker is not None
                pool.release(worker)


def test_busy_pool_falls_back_to_cold_path(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = ValidationSettings(tier0_isolation=True, tier0_warm_workers=1, tier0_timeout_s=5.0)
    pool = get_tier0_pool(settings)
    held = pool.acquire()
    assert held is not None
    calls: list[ProcessLimits] = []

    def fake_run(_argv: list[str], _stdin: str, limits: ProcessLimits, **_kw: Any) -> ProcessResult:
        calls.append(limits)
        return ProcessResult(0, Tier0Result(diagnostics=[]).model_dump_json(), "")

    monkeypatch.setattr(tier0_isolation, "run_process", fake_run)
    try:
        res = check_syntax(_code(), settings)
    finally:
        pool.release(held)
    assert not res.has_errors
    assert len(calls) == 1
    assert calls[0].memory_mb == settings.tier0_memory_mb


def test_get_tier0_pool_rebuilds_when_settings_change() -> None:
    first = get_tier0_pool(ValidationSettings(tier0_isolation=True, tier0_warm_workers=1))
    same = get_tier0_pool(ValidationSettings(tier0_isolation=True, tier0_warm_workers=1))
    assert same is first
    second = get_tier0_pool(ValidationSettings(tier0_isolation=True, tier0_warm_workers=2))
    assert second is not first
    assert second.max_workers == 2
    assert first.acquire() is None  # eski havuz kapandı


def test_check_syntax_with_warm_workers() -> None:
    settings = ValidationSettings(
        tier0_isolation=True,
        tier0_warm_workers=1,
        tier0_timeout_s=5.0,
    )
    assert not check_syntax(_code(), settings).has_errors
    assert check_syntax(_code("int main(void) { int a = }"), settings).has_errors
