"""Derleyicileri güvenli alt süreç olarak çalıştırır (mimari §5.2.3, ADR-0009, ADR-0010).

Kullanıcı kodu güvenilmezdir (§12) ve Docker yalıtımı yoktur; önlemler süreç düzeyindedir:

- Kod **yalnızca stdin** ile verilir; kullanıcı kodu diske yazılmaz. Komut her zaman
  liste; kabuk kullanılmaz.
- Çalışma dizini boş bir geçici dizin; iş bitince silinir. `TEMP`/`TMP`/`TMPDIR` de oraya.
- Ortam izin listesiyle kurulur: `PATH` (+ Windows'ta `SYSTEMROOT`/`WINDIR`), geçici dizin
  değişkenleri, `LC_ALL=C` (tanılar İngilizce, ayrıştırılabilir) ve çağıranın ekledikleri.
  `CPATH`, `*_INCLUDE_PATH`, `GCC_EXEC_PREFIX`, API anahtarları vb. geçmez.
- Süreç ağacı her durumda (normal çıkış, zaman aşımı, beklenmedik hata) öldürülür:
  POSIX'te süreç grubu, Windows'ta Job Object.
- stdout ve stderr ayrı ayrı `OUTPUT_LIMIT` baytla sınırlı; fazlası okunup atılır.
- POSIX: `RLIMIT_CPU`, `RLIMIT_CORE=0`, `RLIMIT_FSIZE`, (derleyicilerde) `RLIMIT_AS`.
  Sınırlar `preexec_fn` yerine küçük bir Python başlatıcısında uygulanıp `execv` ile
  derleyiciye geçilir: `preexec_fn` çok iş parçacıklı sunucuda fork sonrası kilitlenebilir.
- Windows: süreç askıda başlatılır, Job Object'e (bellek + süreç sayısı) atanır, sonra
  devam ettirilir. İş kurulamazsa süreç öldürülür ve hata döner (fail-closed).

Hiçbir durumda istisna fırlatmaz (argüman tipi hatası hariç); sonuç `ProcessResult`'tadır.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import IO, Protocol

OUTPUT_LIMIT = 64 * 1024
MAX_PROCESSES = 8
_FILE_SIZE_LIMIT = 1024 * 1024
_CHUNK = 8192
_JOIN_TIMEOUT_S = 5.0

if sys.platform == "win32":
    _PASSTHROUGH_ENV = ("PATH", "SYSTEMROOT", "WINDIR")
else:
    _PASSTHROUGH_ENV = ("PATH",)

# POSIX başlatıcısı: argv = [python, -I, -S, -c, KOD, cpu, bellek(0=yok), fsize, exe, ...]
_RLIMIT_BOOTSTRAP = """\
import os, resource, sys
def cap(kind, value):
    _, hard = resource.getrlimit(kind)
    if hard != resource.RLIM_INFINITY:
        value = min(value, hard)
    resource.setrlimit(kind, (value, value))
cpu, mem, fsize = (int(v) for v in sys.argv[1:4])
cap(resource.RLIMIT_CPU, cpu)
cap(resource.RLIMIT_CORE, 0)
cap(resource.RLIMIT_FSIZE, fsize)
if mem:
    cap(resource.RLIMIT_AS, mem)
os.execv(sys.argv[4], sys.argv[4:])
"""


@dataclass(frozen=True)
class ProcessLimits:
    """Tek bir çağrının kaynak sınırları."""

    timeout_s: float
    memory_mb: int
    limit_address_space: bool = True  # dotnet gibi büyük sanal alan ayıranlar için False


@dataclass(frozen=True)
class ProcessResult:
    """Alt süreç sonucu. `error` doluysa süreç çalıştırılamadı."""

    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    truncated: bool = False
    error: str | None = None


class _CappedReader(threading.Thread):
    """Akışı sonuna kadar okur (süreç tıkanmasın), ilk `OUTPUT_LIMIT` baytı saklar."""

    def __init__(self, stream: IO[bytes]) -> None:
        super().__init__(daemon=True)
        self._stream = stream
        self._chunks: list[bytes] = []
        self._size = 0
        self._lock = threading.Lock()
        self.truncated = False

    def run(self) -> None:
        try:
            while chunk := self._stream.read(_CHUNK):
                with self._lock:
                    room = OUTPUT_LIMIT - self._size
                    if len(chunk) > room:
                        self.truncated = True
                        chunk = chunk[:room]
                    if chunk:
                        self._chunks.append(chunk)
                        self._size += len(chunk)
        except (OSError, ValueError):
            pass

    def text(self) -> str:
        with self._lock:
            return b"".join(self._chunks).decode("utf-8", errors="replace")


def _feed_stdin(stream: IO[bytes], data: bytes) -> None:
    try:
        stream.write(data)
    except (OSError, ValueError):
        pass  # süreç stdin'i okumadan çıktı
    finally:
        with contextlib.suppress(OSError):
            stream.close()


def sanitized_env(temp_dir: str, extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """İzin listesiyle kurulmuş alt süreç ortamı."""
    env = {name: os.environ[name] for name in _PASSTHROUGH_ENV if name in os.environ}
    env.update(TEMP=temp_dir, TMP=temp_dir, TMPDIR=temp_dir, LC_ALL="C", LANG="C")
    if extra:
        env.update(extra)
    return env


def _launch_argv(argv: list[str], limits: ProcessLimits) -> list[str]:
    """POSIX'te rlimit başlatıcısını öne ekler; Windows'ta argv aynen kalır."""
    if sys.platform == "win32":
        return argv
    memory = limits.memory_mb * 1024 * 1024 if limits.limit_address_space else 0
    cpu = int(limits.timeout_s) + 1
    limits_args = [str(cpu), str(memory), str(_FILE_SIZE_LIMIT)]
    return [sys.executable, "-I", "-S", "-c", _RLIMIT_BOOTSTRAP, *limits_args, *argv]


class _Job(Protocol):
    def terminate(self) -> None: ...
    def close(self) -> None: ...


class _Tree:
    """Platforma göre süreç ağacı yönetimi."""

    def __init__(self, limits: ProcessLimits) -> None:
        self._limits = limits
        self._job: _Job | None = None

    def creationflags(self) -> int:
        """Windows: askıda başlat (Job Object ataması için), konsol penceresi açma."""
        if sys.platform == "win32":
            from codementor.validation._winjob import CREATE_SUSPENDED

            return CREATE_SUSPENDED | subprocess.CREATE_NO_WINDOW
        return 0

    def started(self, proc: subprocess.Popen[bytes]) -> bool:
        """Windows: askıdaki süreci Job Object'e atayıp devam ettirir; başarısızsa False."""
        if sys.platform != "win32":
            return True
        from codementor.validation import _winjob

        try:
            job = _winjob.Job(self._limits.memory_mb * 1024 * 1024, MAX_PROCESSES)
        except OSError:
            return False
        try:
            job.assign_and_resume(proc.pid)
        except OSError:
            job.close()
            return False
        self._job = job
        return True

    def kill(self, proc: subprocess.Popen[bytes]) -> None:
        """Süreci ve tüm alt süreçlerini öldürür (çıkmış süreçte de güvenli)."""
        if self._job is not None:
            self._job.terminate()
        elif sys.platform != "win32":
            import signal

            with contextlib.suppress(OSError):
                os.killpg(proc.pid, signal.SIGKILL)
        with contextlib.suppress(OSError):
            proc.kill()

    def close(self) -> None:
        if self._job is not None:
            self._job.close()  # KILL_ON_JOB_CLOSE: artakalan torunlar da ölür
            self._job = None


def run_process(
    argv: Sequence[str],
    stdin: str,
    limits: ProcessLimits,
    *,
    extra_env: Mapping[str, str] | None = None,
) -> ProcessResult:
    """`argv`'yi boş geçici dizinde, temiz ortamda, `stdin` ile çalıştırır."""
    if isinstance(argv, str) or not argv or not all(isinstance(a, str) for a in argv):
        raise TypeError("argv boş olmayan bir dizge listesi olmalı; kabuk komutu kabul edilmez")
    if shutil.which(argv[0]) is None:
        return ProcessResult(None, "", "", error=f"çalıştırılabilir bulunamadı: {argv[0]}")
    with tempfile.TemporaryDirectory(prefix="cm-t1-", ignore_cleanup_errors=True) as work:
        tree = _Tree(limits)
        try:
            proc = subprocess.Popen(
                _launch_argv(list(argv), limits),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=work,
                env=sanitized_env(work, extra_env),
                close_fds=True,
                creationflags=tree.creationflags(),
                start_new_session=sys.platform != "win32",  # ağaç için süreç grubu
            )
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            return ProcessResult(None, "", "", error=f"{type(exc).__name__}: {exc}")
        try:
            if not tree.started(proc):
                tree.kill(proc)
                proc.wait()
                return ProcessResult(None, "", "", error="Job Object kurulamadı")
            return _supervise(proc, tree, stdin.encode("utf-8"), limits.timeout_s)
        except Exception as exc:  # sözleşme: istisna fırlatma, süreci asla sızdırma
            tree.kill(proc)
            return ProcessResult(None, "", "", error=f"{type(exc).__name__}: {exc}")
        except BaseException:
            tree.kill(proc)
            raise
        finally:
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream is not None:
                    with contextlib.suppress(OSError):
                        stream.close()
            tree.close()


def _supervise(
    proc: subprocess.Popen[bytes], tree: _Tree, data: bytes, timeout_s: float
) -> ProcessResult:
    assert proc.stdin is not None
    assert proc.stdout is not None
    assert proc.stderr is not None
    out, err = _CappedReader(proc.stdout), _CappedReader(proc.stderr)
    feeder = threading.Thread(target=_feed_stdin, args=(proc.stdin, data), daemon=True)
    for thread in (feeder, out, err):
        thread.start()
    timed_out = False
    try:
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
    # Normal çıkışta da: artakalan torunlar pipe'ları açık tutmasın, yaşamasın
    tree.kill(proc)
    with contextlib.suppress(subprocess.TimeoutExpired):
        proc.wait(timeout=_JOIN_TIMEOUT_S)
    for thread in (feeder, out, err):
        thread.join(_JOIN_TIMEOUT_S)
    return ProcessResult(
        returncode=None if timed_out else proc.returncode,
        stdout=out.text(),
        stderr=err.text(),
        timed_out=timed_out,
        truncated=out.truncated or err.truncated,
    )
