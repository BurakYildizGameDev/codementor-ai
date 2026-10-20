"""Tier 0 sıcak işçi havuzu (Faz J, ADR-0025 günceller).

Her analizde yeni Python süreci açmanın (~280 ms) önüne geçmek için
arka planda yaşayan `--pool` modundaki işçi süreçlerini yönetir.
"""

from __future__ import annotations

import subprocess
import sys
import threading
from typing import Self

from pydantic import ValidationError

from codementor.log import get_logger
from codementor.models.findings import Diagnostic
from codementor.models.request import NormalizedCode
from codementor.models.validation import Tier0Result

WORKER_MODULE = "codementor.validation.tier0_worker"
log = get_logger("codementor.tier0.pool")


class Tier0Worker:
    """Tek bir sıcak işçi süreci."""

    def __init__(self) -> None:
        argv = [sys.executable, "-I", "-m", WORKER_MODULE, "--pool"]
        self.proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def is_alive(self) -> bool:
        return self.proc.poll() is None

    def execute(self, code: NormalizedCode, timeout_s: float) -> Tier0Result:
        if not self.is_alive():
            raise RuntimeError("İşçi süreci çalışmıyor.")
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None

        payload = code.model_dump_json().encode("utf-8") + b"\n"
        self.proc.stdin.write(payload)
        self.proc.stdin.flush()

        line_container: list[bytes] = []
        error_container: list[Exception] = []

        def _reader() -> None:
            try:
                assert self.proc.stdout is not None
                out = self.proc.stdout.readline()
                line_container.append(out)
            except Exception as exc:
                error_container.append(exc)

        thread = threading.Thread(target=_reader, daemon=True)
        thread.start()
        thread.join(timeout=timeout_s)

        if thread.is_alive():
            self.close()
            raise TimeoutError(f"Tier 0 işçisi {timeout_s} saniyede yanıt vermedi.")

        if error_container:
            self.close()
            raise error_container[0]

        if not line_container or not line_container[0]:
            self.close()
            raise RuntimeError("İşçi çıktısı boş (süreç kapandı).")

        raw = line_container[0].decode("utf-8", "replace").strip()
        try:
            return Tier0Result.model_validate_json(raw)
        except ValidationError as exc:
            self.close()
            raise ValueError(f"Geçersiz Tier0 JSON çıktısı: {raw[:100]}") from exc

    def close(self) -> None:
        try:
            if self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
        except OSError:
            pass


class Tier0WorkerPool:
    """İşçi süreçlerini yeniden kullanan thread-safe havuz."""

    def __init__(self, max_workers: int = 1) -> None:
        self.max_workers = max(1, max_workers)
        self._lock = threading.Lock()
        self._pool: list[Tier0Worker] = []
        self._closed = False

    def acquire(self) -> Tier0Worker:
        with self._lock:
            if self._closed:
                raise RuntimeError("İşçi havuzu kapatılmış.")
            while self._pool:
                worker = self._pool.pop()
                if worker.is_alive():
                    return worker
                worker.close()
            return Tier0Worker()

    def release(self, worker: Tier0Worker) -> None:
        with self._lock:
            if self._closed or not worker.is_alive():
                worker.close()
                return
            if len(self._pool) < self.max_workers:
                self._pool.append(worker)
            else:
                worker.close()

    def check_syntax(self, code: NormalizedCode, timeout_s: float) -> Tier0Result:
        try:
            worker = self.acquire()
        except Exception as exc:
            log.error("tier0_pool_acquire_failed", error=str(exc))
            return Tier0Result(
                diagnostics=[
                    Diagnostic(
                        tool="tree-sitter",
                        severity="error",
                        line=1,
                        column=None,
                        message="Sözdizimi denetimi başlatılamadı; daha sonra yeniden dene.",
                    )
                ],
                stopped=True,
            )

        healthy = False
        try:
            res = worker.execute(code, timeout_s)
            healthy = True
            return res
        except TimeoutError:
            log.warning("tier0_pool_timeout", timeout_s=timeout_s)
            msg = (
                f"Kodun sözdizimi denetimi {timeout_s:g} saniyelik süre sınırını aştı; "
                "analiz durduruldu."
            )
            return Tier0Result(
                diagnostics=[
                    Diagnostic(
                        tool="tree-sitter",
                        severity="error",
                        line=1,
                        column=None,
                        message=msg,
                    )
                ],
                stopped=True,
            )
        except Exception as exc:
            log.warning("tier0_pool_worker_failed", error=str(exc))
            return Tier0Result(
                diagnostics=[
                    Diagnostic(
                        tool="tree-sitter",
                        severity="error",
                        line=1,
                        column=None,
                        message="Kodun sözdizimi denetimi tamamlanamadı; analiz durduruldu.",
                    )
                ],
                stopped=True,
            )
        finally:
            if healthy:
                self.release(worker)
            else:
                worker.close()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            for w in self._pool:
                w.close()
            self._pool.clear()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
