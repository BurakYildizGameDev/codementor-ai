"""Tier 0 sıcak işçi havuzu testleri."""

from __future__ import annotations

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.validation.tier0_isolation import check_syntax, close_tier0_pool
from codementor.validation.tier0_pool import Tier0Worker, Tier0WorkerPool


def _code(text: str, language: Language = Language.C) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language))


def test_tier0_worker_execute_valid() -> None:
    worker = Tier0Worker()
    try:
        assert worker.is_alive()
        res = worker.execute(_code("int main(void) { return 0; }"), timeout_s=5.0)
        assert not res.has_errors
        assert not res.stopped
    finally:
        worker.close()


def test_tier0_worker_execute_syntax_error() -> None:
    worker = Tier0Worker()
    try:
        res = worker.execute(_code("int main(void) { int x = 1 return x; }"), timeout_s=5.0)
        assert res.has_errors
    finally:
        worker.close()


def test_tier0_pool_reuse_worker() -> None:
    with Tier0WorkerPool(max_workers=1) as pool:
        res1 = pool.check_syntax(_code("int main(void) { return 0; }"), timeout_s=5.0)
        assert not res1.has_errors

        py_code = _code("def foo():\n    return 42\n", Language.PYTHON)
        res2 = pool.check_syntax(py_code, timeout_s=5.0)
        assert not res2.has_errors


def test_tier0_pool_crash_recovery() -> None:
    with Tier0WorkerPool(max_workers=1) as pool:
        worker = pool.acquire()
        # force terminate worker to simulate crash
        worker.proc.kill()
        worker.proc.wait()
        pool.release(worker)

        # next call should recover and spawn a fresh worker
        res = pool.check_syntax(_code("int main(void) { return 0; }"), timeout_s=5.0)
        assert not res.has_errors


def test_check_syntax_with_warm_workers() -> None:
    close_tier0_pool()
    try:
        settings = ValidationSettings(
            tier0_isolation=True,
            tier0_warm_workers=1,
            tier0_timeout_s=5.0,
        )
        code = _code("int main(void) { return 0; }")
        res1 = check_syntax(code, settings)
        assert not res1.has_errors

        code_err = _code("int main(void) { int a = }")
        res2 = check_syntax(code_err, settings)
        assert res2.has_errors
    finally:
        close_tier0_pool()
