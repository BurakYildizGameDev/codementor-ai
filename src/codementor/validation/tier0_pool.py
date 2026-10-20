"""Tier 0 sıcak işçi havuzu (Faz J, ADR-0032; ADR-0025'i genişletir).

Her yalıtılmış analizde yeni Python süreci açmanın (~280 ms) önüne geçmek için `--pool`
modundaki işçiler yaşatılır. İşçi soğuk yolla (`runner.run_process`) **aynı güvenlik
sınırlarıyla** başlar: boş geçici çalışma dizini, izin listeli ortam (API anahtarları geçmez),
Windows'ta askıda başlatma + Job Object (bellek, süreç sayısı; kurulamazsa fail-closed), POSIX'te
rlimit başlatıcısı. POSIX `RLIMIT_CPU` süreç ömrü boyunca biriktiği için işçi en fazla
`MAX_REQUESTS_PER_WORKER` istekten sonra geri dönüştürülür; ömür CPU sınırı istek sayısı ×
istek süresidir (her istek duvar saatiyle `timeout_s`'e bağlı, işçi tek iş parçacıklı).

Canlı işçi sayısı `max_workers` ile sınırlıdır; hepsi meşgulse havuz `None` döner ve çağıran
soğuk yola düşer (sınırsız sıcak süreç yok, yanlış durdurma yok).
"""

from __future__ import annotations

import contextlib
import subprocess
import sys
import tempfile
import threading
from typing import Self

from pydantic import ValidationError

from codementor.log import get_logger
from codementor.models.request import NormalizedCode
from codementor.models.validation import Tier0Result
from codementor.validation.runner import (
    OUTPUT_LIMIT,
    ProcessLimits,
    ProcessTree,
    launch_argv,
    sanitized_env,
)
from codementor.validation.tier0_isolation import (
    FAILURE_MESSAGE,
    INFRA_MESSAGE,
    TIMEOUT_MESSAGE,
    WORKER_MODULE,
    stopped_result,
)

MAX_REQUESTS_PER_WORKER = 100
_CLOSE_WAIT_S = 1.0
log = get_logger("codementor.tier0.pool")


class WorkerStartError(RuntimeError):
    """İşçi güvenlik sınırlarıyla başlatılamadı (çalıştırılabilir yok, Job Object kurulamadı)."""


class WorkerError(RuntimeError):
    """İşçi geçerli yanıt vermedi (çöktü, bellek sınırı, bozuk ya da sınırı aşan çıktı)."""


def worker_limits(memory_mb: int, timeout_s: float, max_requests: int) -> ProcessLimits:
    """İşçi ömrünün sınırları; `timeout_s` POSIX'te birikimli CPU bütçesine çevrilir."""
    return ProcessLimits(timeout_s=max_requests * timeout_s, memory_mb=memory_mb)


class Tier0Worker:
    """Tek bir sıcak işçi süreci; aynı anda tek çağıran kullanır."""

    def __init__(self, limits: ProcessLimits, max_requests: int = MAX_REQUESTS_PER_WORKER) -> None:
        self.max_requests = max_requests
        self.requests = 0
        self._closed = False
        self._work = tempfile.TemporaryDirectory(prefix="cm-t0-", ignore_cleanup_errors=True)
        self._tree = ProcessTree(limits)
        argv = [sys.executable, "-I", "-m", WORKER_MODULE, "--pool"]
        try:
            self.proc = subprocess.Popen(
                launch_argv(argv, limits),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,  # okunmayan boru dolup işçiyi tıkamasın
                cwd=self._work.name,
                env=sanitized_env(self._work.name),
                close_fds=True,
                creationflags=self._tree.creationflags(),
                start_new_session=sys.platform != "win32",
            )
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            self._closed = True
            self._work.cleanup()
            raise WorkerStartError(type(exc).__name__) from exc
        if not self._tree.started(self.proc):
            self.close(force=True)
            raise WorkerStartError("Job Object kurulamadı")

    @property
    def exhausted(self) -> bool:
        """İstek bütçesi doldu mu (geri dönüştürülmeli)."""
        return self.requests >= self.max_requests

    def is_alive(self) -> bool:
        return not self._closed and self.proc.poll() is None

    def execute(self, code: NormalizedCode, timeout_s: float) -> Tier0Result:
        """Tek istek; süre aşımında `TimeoutError`, geçersiz yanıtta `WorkerError` (işçi kapanır)"""
        if not self.is_alive():
            raise WorkerError("işçi çalışmıyor")
        self.requests += 1
        stdin, stdout = self.proc.stdin, self.proc.stdout
        assert stdin is not None
        assert stdout is not None
        payload = code.model_dump_json().encode("utf-8") + b"\n"
        lines: list[bytes] = []

        def exchange() -> None:
            # Yazma da iş parçacığında: büyük girdi boruyu doldurursa süre sınırı yine işler
            try:
                stdin.write(payload)
                stdin.flush()
                lines.append(stdout.readline(OUTPUT_LIMIT + 1))
            except (OSError, ValueError):
                pass

        thread = threading.Thread(target=exchange, daemon=True)
        thread.start()
        thread.join(timeout_s)
        if thread.is_alive():
            self.close(force=True)  # süreç ölünce readline döner, iş parçacığı biter
            raise TimeoutError(f"Tier 0 işçisi {timeout_s:g} sn'de yanıt vermedi")
        line = lines[0] if lines else b""
        if not line.endswith(b"\n"):  # süreç kapandı ya da çıktı sınırı aşıldı
            self.close(force=True)
            raise WorkerError("işçi çıktısı yok ya da sınırı aştı")
        try:
            return Tier0Result.model_validate_json(line)
        except ValidationError as exc:
            self.close(force=True)
            raise WorkerError("işçi çıktısı geçersiz") from exc  # ham çıktı loglanmaz (§12)

    def close(self, *, force: bool = False) -> None:
        """İşçiyi kapatır; `force` değilse önce stdin kapatılıp kendi çıkması beklenir."""
        if self._closed:
            return
        self._closed = True
        proc = self.proc
        if not force:
            with contextlib.suppress(OSError, ValueError):
                if proc.stdin is not None:
                    proc.stdin.close()  # işçi EOF ile döngüden çıkar
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=_CLOSE_WAIT_S)
        if proc.poll() is None:
            self._tree.kill(proc)
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=_CLOSE_WAIT_S)
        # Süreç ölmediyse boruları kapatma: `exchange` iş parçacığı `readline`/`write` içinde
        # akışın kilidini tutar, `close()` çağıranı askıda bırakırdı. Job Object kapanışı
        # (KILL_ON_JOB_CLOSE) süreci yine öldürür; borular süreçle birlikte serbest kalır.
        if proc.poll() is not None:
            for stream in (proc.stdin, proc.stdout):
                if stream is not None:
                    with contextlib.suppress(OSError, ValueError):
                        stream.close()
        self._tree.close()
        self._work.cleanup()


class Tier0WorkerPool:
    """Canlı işçi sayısı `max_workers` ile sınırlı, iş parçacığı güvenli havuz."""

    def __init__(
        self,
        max_workers: int = 1,
        *,
        memory_mb: int = 1024,
        timeout_s: float = 5.0,
        max_requests: int = MAX_REQUESTS_PER_WORKER,
    ) -> None:
        self.max_workers = max(1, max_workers)
        self.memory_mb = memory_mb
        self.timeout_s = timeout_s
        self.max_requests = max(1, max_requests)
        self._slots = threading.BoundedSemaphore(self.max_workers)
        self._lock = threading.Lock()
        self._idle: list[Tier0Worker] = []
        self._closed = False

    @property
    def key(self) -> tuple[int, int, float]:
        """Havuzu belirleyen ayarlar; değişirse havuz yeniden kurulur."""
        return (self.max_workers, self.memory_mb, self.timeout_s)

    def _new_worker(self) -> Tier0Worker:
        limits = worker_limits(self.memory_mb, self.timeout_s, self.max_requests)
        return Tier0Worker(limits, self.max_requests)

    def acquire(self) -> Tier0Worker | None:
        """Boşta ya da yeni işçi; yuva yoksa veya havuz kapandıysa `None`.

        `WorkerStartError` yuvayı geri verip yükselir.
        """
        if not self._slots.acquire(blocking=False):
            return None
        try:
            with self._lock:
                if self._closed:
                    self._slots.release()
                    return None
                while self._idle:
                    worker = self._idle.pop()
                    if worker.is_alive():
                        return worker
                    worker.close()
            return self._new_worker()
        except BaseException:
            self._slots.release()
            raise

    def release(self, worker: Tier0Worker) -> None:
        """İşçiyi havuza döndürür; ölü, bütçesi dolmuş ya da havuz kapalıysa kapatır."""
        try:
            with self._lock:
                if not self._closed and worker.is_alive() and not worker.exhausted:
                    self._idle.append(worker)
                    return
            worker.close()
        finally:
            self._slots.release()

    def try_check_syntax(self, code: NormalizedCode) -> Tier0Result | None:
        """Sıcak işçide Tier 0; tüm işçiler meşgulse `None` (çağıran soğuk yola düşer)."""
        try:
            worker = self.acquire()
        except WorkerStartError as exc:
            log.error("tier0_worker_unavailable", error=str(exc), pool=True)
            return stopped_result(INFRA_MESSAGE)
        if worker is None:
            log.info("tier0_pool_busy", max_workers=self.max_workers)
            return None
        try:
            return worker.execute(code, self.timeout_s)
        except TimeoutError:
            log.warning("tier0_timeout", timeout_s=self.timeout_s, pool=True)
            return stopped_result(TIMEOUT_MESSAGE.format(seconds=f"{self.timeout_s:g}"))
        except Exception as exc:
            log.warning("tier0_worker_failed", error_type=type(exc).__name__, pool=True)
            worker.close(force=True)
            return stopped_result(FAILURE_MESSAGE)
        finally:
            self.release(worker)

    def close(self) -> None:
        with self._lock:
            self._closed = True
            idle, self._idle = self._idle, []
        for worker in idle:
            worker.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
