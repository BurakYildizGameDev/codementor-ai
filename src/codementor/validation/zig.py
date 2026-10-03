"""Zig ile derleyicisiz Tier 1 (Faz 29, ADR-0018).

`zig cc -` stdin'i önbellek dizinine `…-stdin.c` dosyası olarak yazar (kullanıcı kodu diske
düşerdi, mimari §5.2.3) ve temizlenmiş ortamda önbellek dizini bulamaz. Bu yüzden zig'in
içindeki clang doğrudan çağrılır: `zig clang <bayraklar> -x c -` → kod yalnızca stdin'de,
tanılar `<stdin>:L:C:` biçiminde (clang ayrıştırıcısı aynen kullanılır).

`zig clang` zig'in libc/libc++ başlık yollarını bilmez; bunlar `zig cc -### -c` sondasının
`-cc1` satırından alınır. `-c` olmadan zig libc++/mingw kütüphanelerini derler (~30 sn,
100 MB); `-c` ile sonda ~0,2 sn sürer ve boş girdiyle, geçici bir önbellekle yapılır.
"""

from __future__ import annotations

import shlex
import tempfile
from itertools import pairwise
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal

from codementor.log import get_logger
from codementor.validation.runner import ProcessLimits, Runner, run_process

ZigLanguage = Literal["c", "c++"]

_PROBE_MEMORY_MB = 1024
log = get_logger("codementor.toolchain")
# cc1 → sürücü bayrağı; hepsi sistem başlık dizini olarak verilir
_INCLUDE_OPTIONS = frozenset({"-isystem", "-internal-isystem", "-internal-externc-isystem"})


def _absolute(path: str) -> bool:
    return PureWindowsPath(path).is_absolute() or PurePosixPath(path).is_absolute()


def parse_cc1_flags(stderr: str) -> list[str] | None:
    """`-###` çıktısındaki `-cc1` satırından `zig clang` bayrakları; okunamazsa `None`.

    Yalnızca hedef üçlüsü, `-isystem` ve `-D` taşınır; çıktı dosyası, stdin kopyasının yolu
    ve hata ayıklama ayarları atılır. Göreli başlık yolu kabul edilmez (çalışma dizinine göre
    çözülürdü).
    """
    line = next((row for row in stderr.splitlines() if '"-cc1"' in row), None)
    if line is None:
        return None
    try:
        tokens = shlex.split(line)
    except ValueError:
        return None
    triple: str | None = None
    flags: list[str] = []
    includes = 0
    for option, value in pairwise(tokens):
        if option == "-triple":
            triple = value
        elif option in _INCLUDE_OPTIONS:
            if not _absolute(value):
                return None
            flags += ["-isystem", value]
            includes += 1
        elif option == "-D":
            flags += ["-D", value]
    # başlık yolu yoksa `-nostdinc` her `#include <…>`'i "bulunamadı"ya çevirirdi: zig kullanılmaz
    if triple is None or includes == 0:
        return None
    return [f"--target={triple}", "-nostdinc", *flags]


def probe_flags(
    zig: str, language: ZigLanguage, *, timeout_s: float, runner: Runner = run_process
) -> list[str] | None:
    """`zig cc|c++ -### -c` ile başlık bayraklarını çıkarır; başarısızsa `None`.

    Girdi boştur (kullanıcı kodu gitmez); zig'in önbelleği geçici dizindedir ve silinir.
    """
    driver = "cc" if language == "c" else "c++"
    argv = [zig, driver, "-x", language, "-c", "-fsyntax-only", "-###", "-"]
    limits = ProcessLimits(timeout_s=timeout_s, memory_mb=_PROBE_MEMORY_MB)
    try:  # keşif hiçbir zaman istisna fırlatmaz (TEMP yazılamazsa da)
        with tempfile.TemporaryDirectory(
            prefix="codementor-zig-", ignore_cleanup_errors=True
        ) as cache:
            env = {"ZIG_GLOBAL_CACHE_DIR": cache, "ZIG_LOCAL_CACHE_DIR": cache}
            result = runner(argv, "", limits, extra_env=env)
    except Exception as exc:
        log.warning("zig_probe_failed", zig=zig, error=type(exc).__name__)
        return None
    if result.error is not None or result.timed_out:
        log.warning("zig_probe_failed", zig=zig, error=result.error, timed_out=result.timed_out)
        return None
    flags = parse_cc1_flags(result.stderr)
    if flags is None:
        log.warning("zig_probe_unparsed", zig=zig, returncode=result.returncode)
    return flags


def zig_executable(directory: Path) -> Path:
    """Kurulum dizinindeki zig çalıştırılabilirinin yolu (platforma göre `.exe`)."""
    exe = directory / "zig.exe"
    return exe if exe.is_file() or not (directory / "zig").is_file() else directory / "zig"
