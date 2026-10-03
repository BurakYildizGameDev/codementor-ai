"""Derleyici indirme ve kurulumu (Faz 29, ADR-0018): ağsız, respx + bellekte üretilen zip."""

from __future__ import annotations

import hashlib
import io
import os
import threading
import zipfile
from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import ValidationError

from codementor.config import DownloadSource, ValidationSettings, ZigSettings
from codementor.models.validation import DownloadProgress
from codementor.validation import toolchain_install
from codementor.validation.archive import safe_extract
from codementor.validation.toolchain_install import (
    INSTALL_MARKER,
    LOCK_FILE,
    InstallCancelledError,
    ToolchainInstallError,
    install_zig,
    installed_zig,
    platform_key,
)

URL = "https://example.test/ziglang.whl"
PLATFORM = "linux-x86_64"
EXE = "zig.exe" if os.name == "nt" else "zig"


def _wheel(
    *, marker: bytes = b"v1", padding: int = 0, extra: dict[str, bytes] | None = None
) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        archive.writestr(f"ziglang/{EXE}", marker)
        archive.writestr("ziglang/lib/include/stdio.h", b"int printf(const char*, ...);\n")
        archive.writestr("ziglang/lib/big.bin", os.urandom(padding))
        archive.writestr("ziglang-0.16.0.dist-info/METADATA", b"Name: ziglang\n")
        for name, data in (extra or {}).items():
            archive.writestr(name, data)
    return buffer.getvalue()


def _settings(tmp_path: Path, payload: bytes, **zig: object) -> ValidationSettings:
    source = DownloadSource(url=URL, sha256=hashlib.sha256(payload).hexdigest())
    return ValidationSettings(
        toolchain_dir=tmp_path / "tc",
        zig=ZigSettings(version="0.16.0", sources={PLATFORM: source}, **zig),  # type: ignore[arg-type]
    )


def _install(settings: ValidationSettings, **kwargs: object) -> Path:
    return install_zig(settings, platform=PLATFORM, verify=lambda _exe: True, **kwargs)  # type: ignore[arg-type]


def _leftovers(settings: ValidationSettings) -> list[str]:
    root = settings.toolchain_dir
    return sorted(
        p.name for p in root.rglob("*") if p.name.endswith(".part") or p.name.startswith(".zig-")
    )


@respx.mock
def test_install_success(tmp_path: Path) -> None:
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    events: list[DownloadProgress] = []

    exe = _install(settings, progress=events.append)

    root = settings.toolchain_dir / "zig"
    assert exe == root / EXE
    assert exe.read_bytes() == b"v1"
    assert (root / "lib" / "include" / "stdio.h").is_file()
    assert not (settings.toolchain_dir / "zig-0.16.0.dist-info").exists()  # yalnız ziglang/
    assert installed_zig(root) == exe
    assert {e.stage for e in events} >= {"download", "extract", "check"}
    assert events[-1].stage == "check"
    assert _leftovers(settings) == []
    if os.name != "nt":
        assert os.access(exe, os.X_OK)


@respx.mock
def test_sha256_mismatch_removes_partial(tmp_path: Path) -> None:
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload + b"x"))
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="sha256 uyuşmuyor"):
        _install(settings)
    assert installed_zig(settings.toolchain_dir / "zig") is None
    assert _leftovers(settings) == []


class _BrokenStream(httpx.SyncByteStream):
    """Bir parça gönderip bağlantıyı koparan akış (yarım indirme)."""

    def __init__(self, first: bytes) -> None:
        self.first = first

    def __iter__(self) -> Iterator[bytes]:
        yield self.first
        raise httpx.ReadError("bağlantı koptu")


@respx.mock
def test_interrupted_download_then_retry(tmp_path: Path) -> None:
    payload = _wheel(padding=200_000)
    route = respx.get(URL)
    route.side_effect = [
        httpx.Response(200, stream=_BrokenStream(payload[:1000])),
        httpx.Response(200, content=payload),
    ]
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="İndirme"):
        _install(settings)
    assert installed_zig(settings.toolchain_dir / "zig") is None
    assert _leftovers(settings) == []

    assert _install(settings).is_file()  # yeniden deneme temiz başlar


@respx.mock
def test_cancel_removes_partial(tmp_path: Path) -> None:
    payload = _wheel(padding=600_000)
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    cancel = threading.Event()

    def on_progress(event: DownloadProgress) -> None:
        if event.stage == "download" and event.done > 0:
            cancel.set()

    with pytest.raises(InstallCancelledError, match="iptal"):
        _install(settings, progress=on_progress, cancel=cancel)
    assert installed_zig(settings.toolchain_dir / "zig") is None
    assert _leftovers(settings) == []


@respx.mock
def test_download_size_cap(tmp_path: Path) -> None:
    payload = _wheel(padding=1_200_000)
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload, max_download_mb=1)
    with pytest.raises(ToolchainInstallError, match="1 MB"):
        _install(settings)
    assert _leftovers(settings) == []


@respx.mock
def test_http_error_is_turkish(tmp_path: Path) -> None:
    respx.get(URL).mock(return_value=httpx.Response(404))
    settings = _settings(tmp_path, b"")
    with pytest.raises(ToolchainInstallError, match="HTTP 404"):
        _install(settings)


@respx.mock
def test_verify_failure_keeps_nothing(tmp_path: Path) -> None:
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="çalıştırılamadı"):
        install_zig(settings, platform=PLATFORM, verify=lambda _exe: False)
    assert not (settings.toolchain_dir / "zig").exists()
    assert _leftovers(settings) == []


@respx.mock
def test_reinstall_atomic(tmp_path: Path) -> None:
    first, second = _wheel(marker=b"v1"), _wheel(marker=b"v2")
    respx.get(URL).mock(return_value=httpx.Response(200, content=first))
    _install(_settings(tmp_path, first))
    (tmp_path / "tc" / "zig" / "eski.txt").write_text("kalmamalı", encoding="utf-8")

    respx.get(URL).mock(return_value=httpx.Response(200, content=second))
    settings = _settings(tmp_path, second)
    exe = _install(settings)
    assert exe.read_bytes() == b"v2"
    assert not (exe.parent / "eski.txt").exists()
    assert hashlib.sha256(second).hexdigest() in (exe.parent / INSTALL_MARKER).read_text("utf-8")
    assert _leftovers(settings) == []


def test_unsupported_platform_message(tmp_path: Path) -> None:
    settings = _settings(tmp_path, b"")
    with pytest.raises(ToolchainInstallError, match="linux-riscv64"):
        install_zig(settings, platform="linux-riscv64")


def test_non_https_url_rejected() -> None:
    with pytest.raises(ValidationError, match="https"):
        DownloadSource(url="http://example.test/zig.whl", sha256="0" * 64)


@pytest.mark.parametrize(
    ("system", "machine", "expected"),
    [
        ("Windows", "AMD64", "windows-x86_64"),
        ("Linux", "x86_64", "linux-x86_64"),
        ("Linux", "aarch64", "linux-aarch64"),
        ("Darwin", "arm64", "macos-aarch64"),
    ],
)
def test_platform_key(system: str, machine: str, expected: str) -> None:
    assert platform_key(system, machine) == expected


# --- Arşiv güvenliği ---------------------------------------------------------------------


def _zip(tmp_path: Path, entries: list[zipfile.ZipInfo | tuple[str, bytes]]) -> Path:
    path = tmp_path / "a.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            if isinstance(entry, zipfile.ZipInfo):
                archive.writestr(entry, b"/etc/passwd")
            else:
                archive.writestr(*entry)
    return path


def _extract(archive: Path, dest: Path, **limits: int) -> None:
    safe_extract(
        archive,
        dest,
        prefix="ziglang/",
        max_bytes=limits.get("max_bytes", 10_000_000),
        max_files=limits.get("max_files", 100),
    )


@pytest.mark.parametrize(
    "name",
    [
        "ziglang/../kacak.txt",
        "ziglang/lib/../../kacak.txt",
        "ziglang//etc/kacak.txt",
        "ziglang/C:/kacak.txt",
        "ziglang/lib\\..\\..\\kacak.txt",
        "ziglang/lib/dosya.txt:gizli",
        "ziglang/lib/sonu-nokta.",
        "ziglang/lib/sonu-bosluk ",
        "ziglang/lib/CON",
        "ziglang/lib/nul.h",
        "ziglang/COM1.txt/x.h",
    ],
)
def test_zip_traversal_rejected(tmp_path: Path, name: str) -> None:
    archive = _zip(tmp_path, [("ziglang/zig", b"z"), (name, b"x")])
    dest = tmp_path / "out"
    with pytest.raises(ToolchainInstallError, match="güvenli değil"):
        _extract(archive, dest)
    assert not (tmp_path / "kacak.txt").exists()


def test_zip_symlink_rejected(tmp_path: Path) -> None:
    link = zipfile.ZipInfo("ziglang/lib/bag")
    link.external_attr = (0o120777 & 0xFFFF) << 16
    archive = _zip(tmp_path, [("ziglang/zig", b"z"), link])
    with pytest.raises(ToolchainInstallError, match="bağlantı"):
        _extract(archive, tmp_path / "out")


def test_zip_bomb_cap(tmp_path: Path) -> None:
    archive = _zip(tmp_path, [("ziglang/zig", b"z"), ("ziglang/bomba.bin", bytes(3_000_000))])
    assert archive.stat().st_size < 100_000  # sıkıştırılmış hâli küçük
    with pytest.raises(ToolchainInstallError, match="çok büyük"):
        _extract(archive, tmp_path / "out", max_bytes=1_000_000)


def test_zip_file_count_cap(tmp_path: Path) -> None:
    archive = _zip(tmp_path, [(f"ziglang/f{i}.h", b"") for i in range(5)])
    with pytest.raises(ToolchainInstallError, match="çok fazla"):
        _extract(archive, tmp_path / "out", max_files=3)


def test_zip_without_prefix_rejected(tmp_path: Path) -> None:
    archive = _zip(tmp_path, [("baska/zig", b"z")])
    with pytest.raises(ToolchainInstallError, match="beklenen"):
        _extract(archive, tmp_path / "out")


def test_corrupt_archive_is_turkish(tmp_path: Path) -> None:
    archive = tmp_path / "bozuk.zip"
    archive.write_bytes(b"PK\x03\x04 bozuk")
    with pytest.raises(ToolchainInstallError, match="açılamadı"):
        _extract(archive, tmp_path / "out")


def test_zip_case_insensitive_duplicate_rejected(tmp_path: Path) -> None:
    """Windows'ta `A.h` ile `a.h` aynı dosyadır; sonuncu sessizce kazanmasın."""
    archive = _zip(tmp_path, [("ziglang/zig", b"z"), ("ziglang/A.h", b"1"), ("ziglang/a.h", b"2")])
    with pytest.raises(ToolchainInstallError, match="aynı ada"):
        _extract(archive, tmp_path / "out")


def test_unsupported_compression_is_turkish(tmp_path: Path) -> None:
    archive = _zip(tmp_path, [("ziglang/zig", b"z" * 100)])
    data = bytearray(archive.read_bytes())
    # yerel ve merkezi başlıktaki sıkıştırma yöntemini bilinmeyen bir değere (99) çevir
    for signature, offset in ((b"PK\x03\x04", 8), (b"PK\x01\x02", 10)):
        at = data.index(signature) + offset
        data[at : at + 2] = (99).to_bytes(2, "little")
    archive.write_bytes(bytes(data))
    with pytest.raises(ToolchainInstallError, match="açılamadı"):
        _extract(archive, tmp_path / "out")


# --- Denetim düzeltmeleri: yönlendirme, kilit, son anda iptal, çökme artıkları --------------


@respx.mock
def test_redirect_to_http_rejected(tmp_path: Path) -> None:
    payload = _wheel()
    respx.get(URL).mock(
        return_value=httpx.Response(302, headers={"Location": "http://example.test/z.whl"})
    )
    http_route = respx.get("http://example.test/z.whl").mock(
        return_value=httpx.Response(200, content=payload)
    )
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="https olmayan"):
        _install(settings)
    assert not http_route.called  # güvensiz adrese istek hiç gitmedi
    assert _leftovers(settings) == []


@respx.mock
def test_concurrent_install_blocked_by_lock(tmp_path: Path) -> None:
    payload = _wheel()
    route = respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    settings.toolchain_dir.mkdir(parents=True)
    with (
        toolchain_install._install_lock(settings.toolchain_dir),
        pytest.raises(ToolchainInstallError, match="Başka bir derleyici kurulumu"),
    ):
        _install(settings)
    assert not route.called
    assert (settings.toolchain_dir / LOCK_FILE).exists()
    assert _install(settings).is_file()  # kilit bırakılınca kurulum yapılır


@respx.mock
def test_cancel_during_check_installs_nothing(tmp_path: Path) -> None:
    """Sonda sırasında gelen iptal, işaret ve taşımadan önce yakalanır (denetim O2)."""
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    cancel = threading.Event()

    def slow_verify(_exe: Path) -> bool:
        cancel.set()  # kullanıcı sonda sürerken İptal'e basar
        return True

    with pytest.raises(InstallCancelledError):
        install_zig(settings, platform=PLATFORM, verify=slow_verify, cancel=cancel)
    assert installed_zig(settings.toolchain_dir / "zig") is None
    assert _leftovers(settings) == []


@respx.mock
def test_archive_changed_on_disk_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    monkeypatch.setattr(toolchain_install, "_file_sha256", lambda _path: "0" * 64)
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="diskte değişmiş"):
        _install(settings)
    assert _leftovers(settings) == []


@respx.mock
def test_crash_between_renames_restores_old_install(tmp_path: Path) -> None:
    """İki taşıma arasında çökülmüşse tek geçerli kurulum `.zig-old-*`'tır: silinmez."""
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    _install(settings)
    root = settings.toolchain_dir
    (root / "zig").rename(root / ".zig-old-deadbeef")  # çökme anı
    respx.get(URL).mock(return_value=httpx.Response(404))
    with pytest.raises(ToolchainInstallError, match="HTTP 404"):
        _install(settings)
    assert installed_zig(root / "zig") is not None  # eski kurulum geri geldi


@respx.mock
def test_default_verify_probes_c_and_cpp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    probed: list[str] = []

    def probe(_zig: str, language: str, *, timeout_s: float) -> list[str] | None:
        probed.append(language)
        return ["--target=x"] if language == "c" else None  # C++ sondası bozuk

    monkeypatch.setattr(toolchain_install, "probe_flags", probe)
    settings = _settings(tmp_path, payload)
    with pytest.raises(ToolchainInstallError, match="çalıştırılamadı"):
        install_zig(settings, platform=PLATFORM)
    assert probed == ["c", "c++"]
    assert installed_zig(settings.toolchain_dir / "zig") is None
