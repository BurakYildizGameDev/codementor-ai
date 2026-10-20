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
- stdout ve stderr ayrı ayrı `ProcessLimits.output_limit` baytla sınırlı; fazlası okunup atılır.
  Varsayılan derleyici sınırıdır (`OUTPUT_LIMIT`); CLI ajanları çok satırlı akış yazdığı için
  config'ten daha büyük bir sınır verir (G1).
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
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Protocol

OUTPUT_LIMIT = 64 * 1024
MAX_PROCESSES = 8
_FILE_SIZE_LIMIT = 1024 * 1024
_CHUNK = 8192
_JOIN_TIMEOUT_S = 5.0
_CANCEL_POLL_S = 0.1  # iptal olayı bu aralıkla da denetlenir (süreç bitişi poll ile)

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
    max_processes: int = MAX_PROCESSES  # Windows Job Object; CLI ajanları daha fazlasını açar
    file_size_bytes: int = _FILE_SIZE_LIMIT  # POSIX RLIMIT_FSIZE
    output_limit: int = OUTPUT_LIMIT  # stdout/stderr başına bayt; CLI ajanları daha büyüğünü ister


@dataclass(frozen=True)
class ProcessResult:
    """Alt süreç sonucu. `error` doluysa süreç çalıştırılamadı."""

    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    truncated: bool = False
    error: str | None = None
    cancelled: bool = False  # iptal olayıyla durduruldu (Faz 19)


class _CappedReader(threading.Thread):
    """Akışı sonuna kadar okur (süreç tıkanmasın), ilk `limit` baytı saklar."""

    def __init__(self, stream: IO[bytes], limit: int = OUTPUT_LIMIT) -> None:
        super().__init__(daemon=True)
        self._stream = stream
        self._limit = limit
        self._chunks: list[bytes] = []
        self._size = 0
        self._lock = threading.Lock()
        self.truncated = False

    def run(self) -> None:
        try:
            while chunk := self._stream.read(_CHUNK):
                with self._lock:
                    room = self._limit - self._size
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


def find_on_path(name: str, search_path: str) -> Path | None:
    """Çıplak `name`'i yalnız `search_path`'teki mutlak dizinlerde arar (Faz A2, Y1).

    `shutil.which` Windows'ta `NoDefaultCurrentDirectoryInExePath` yoksa çalışma dizinini başa
    ekler (`path=` verilse bile); öğrenci projesindeki `gcc.bat` derleyici sanılmasın diye
    çalışma dizini ve göreli `PATH` girdileri hiç denenmez. Bulunursa mutlak (çözülmüş) yol.
    """
    suffixes = [""]
    if sys.platform == "win32" and not Path(name).suffix:
        pathext = os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(";")
        suffixes = [s.lower() for s in pathext if s]
    for directory in search_path.split(os.pathsep):
        base = Path(directory)
        if not directory or not base.is_absolute():
            continue
        for suffix in suffixes:
            candidate = base / f"{name}{suffix}"
            try:
                if candidate.is_file() and (
                    sys.platform == "win32" or os.access(candidate, os.X_OK)
                ):
                    return candidate.resolve()
            except (OSError, ValueError):
                continue
    return None


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


def launch_argv(argv: list[str], limits: ProcessLimits) -> list[str]:
    """POSIX'te rlimit başlatıcısını öne ekler; Windows'ta argv aynen kalır."""
    if sys.platform == "win32":
        return argv
    memory = limits.memory_mb * 1024 * 1024 if limits.limit_address_space else 0
    cpu = int(limits.timeout_s) + 1
    limits_args = [str(cpu), str(memory), str(limits.file_size_bytes)]
    return [sys.executable, "-I", "-S", "-c", _RLIMIT_BOOTSTRAP, *limits_args, *argv]


class Runner(Protocol):
    """`run_process` imzası; testlerde sahtesi verilir."""

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult: ...


class _Job(Protocol):
    def terminate(self) -> None: ...
    def close(self) -> None: ...


class ProcessTree:
    """Platforma göre süreç ağacı yönetimi (sıcak Tier 0 işçisi de kullanır, ADR-0032)."""

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
            job = _winjob.Job(self._limits.memory_mb * 1024 * 1024, self._limits.max_processes)
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
    cancel: threading.Event | None = None,
) -> ProcessResult:
    """`argv`'yi boş geçici dizinde, temiz ortamda, `stdin` ile çalıştırır.

    `cancel` set edilirse süreç ağacı zaman aşımını beklemeden öldürülür ve sonuç
    `cancelled=True` döner (ör. kullanıcı analizi durdurdu).
    """
    if isinstance(argv, str) or not argv or not all(isinstance(a, str) for a in argv):
        raise TypeError("argv boş olmayan bir dizge listesi olmalı; kabuk komutu kabul edilmez")
    # Yalnızca mutlak yol: çıplak ad verilirse Windows'ta CreateProcess önce çalışma dizinine
    # bakar (öğrenci projesindeki `gcc.exe` çalışabilirdi). Keşif `toolchain`'in işidir.
    executable = Path(argv[0])
    if not executable.is_absolute():
        return ProcessResult(None, "", "", error=f"çalıştırılabilir mutlak yol olmalı: {argv[0]}")
    if not executable.is_file():
        return ProcessResult(None, "", "", error=f"çalıştırılabilir bulunamadı: {argv[0]}")
    if cancel is not None and cancel.is_set():
        return ProcessResult(None, "", "", cancelled=True)
    with tempfile.TemporaryDirectory(prefix="cm-t1-", ignore_cleanup_errors=True) as work:
        tree = ProcessTree(limits)
        try:
            proc = subprocess.Popen(
                launch_argv(list(argv), limits),
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
            return _supervise(
                proc, tree, stdin.encode("utf-8"), limits.timeout_s, cancel, limits.output_limit
            )
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


def _wait(
    proc: subprocess.Popen[bytes], timeout_s: float, cancel: threading.Event | None
) -> tuple[bool, bool]:
    """Süreç bitene, zaman aşımına ya da iptale kadar bekler → (zaman aşımı, iptal)."""
    if cancel is None:
        try:
            proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return True, False
        return False, False
    deadline = time.monotonic() + timeout_s
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return True, False
        try:
            proc.wait(timeout=min(_CANCEL_POLL_S, remaining))
        except subprocess.TimeoutExpired:
            if cancel.is_set():
                return False, True
            continue
        return False, False


def _supervise(
    proc: subprocess.Popen[bytes],
    tree: ProcessTree,
    data: bytes,
    timeout_s: float,
    cancel: threading.Event | None = None,
    output_limit: int = OUTPUT_LIMIT,
) -> ProcessResult:
    assert proc.stdin is not None
    assert proc.stdout is not None
    assert proc.stderr is not None
    out, err = _CappedReader(proc.stdout, output_limit), _CappedReader(proc.stderr, output_limit)
    feeder = threading.Thread(target=_feed_stdin, args=(proc.stdin, data), daemon=True)
    for thread in (feeder, out, err):
        thread.start()
    timed_out, cancelled = _wait(proc, timeout_s, cancel)
    # Normal çıkışta da: artakalan torunlar pipe'ları açık tutmasın, yaşamasın
    tree.kill(proc)
    with contextlib.suppress(subprocess.TimeoutExpired):
        proc.wait(timeout=_JOIN_TIMEOUT_S)
    for thread in (feeder, out, err):
        thread.join(_JOIN_TIMEOUT_S)
    return ProcessResult(
        returncode=None if timed_out or cancelled else proc.returncode,
        stdout=out.text(),
        stderr=err.text(),
        timed_out=timed_out,
        truncated=out.truncated or err.truncated,
        cancelled=cancelled,
    )
