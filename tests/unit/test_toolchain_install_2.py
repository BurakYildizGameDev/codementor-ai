"""Derleyici indirme ve kurulumu (Faz 29, ADR-0018): ağsız, respx + bellekte üretilen zip.

Bölüm 2/2.
"""

from __future__ import annotations

import os
import threading
from pathlib import Path

import httpx
import pytest
import respx

from codementor.validation import toolchain_install
from codementor.validation.toolchain_install import (
    INSTALL_MARKER,
    LOCK_FILE,
    InstallCancelledError,
    ToolchainInstallError,
    install_zig,
    installed_zig,
    needs_update,
)
from tests.unit.toolchain_install_support import (
    EXE,
    PLATFORM,
    URL,
    _fake_install,
    _flaky_staging_rename,
    _install,
    _leftovers,
    _settings,
    _wheel,
)

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


@respx.mock
def test_transient_rename_lock_is_retried(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Yeni açılan zig.exe'yi tarayıcı kısa süre tutunca taşıma geçici olarak reddedilir."""
    payload = _wheel()
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    left = _flaky_staging_rename(monkeypatch, failures=2)
    settings = _settings(tmp_path, payload)
    exe = _install(settings)
    assert left == [0]
    assert exe.read_bytes() == b"v1"
    assert _leftovers(settings) == []


@respx.mock
def test_persistent_rename_lock_keeps_previous_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first, second = _wheel(marker=b"v1"), _wheel(marker=b"v2")
    respx.get(URL).mock(return_value=httpx.Response(200, content=first))
    exe = _install(_settings(tmp_path, first))

    respx.get(URL).mock(return_value=httpx.Response(200, content=second))
    _flaky_staging_rename(monkeypatch, failures=100)
    settings = _settings(tmp_path, second)
    with pytest.raises(ToolchainInstallError, match="taşınamadı"):
        _install(settings)
    assert exe.read_bytes() == b"v1"  # önceki kurulum yerinde
    assert installed_zig(settings.toolchain_dir / "zig") == exe
    assert _leftovers(settings) == []


# --- Faz F (F9): kurulu zig güncel mi -------------------------------------------------------


def test_needs_update_only_when_marker_differs(tmp_path: Path) -> None:
    """Faz F (F9): işaretçideki sürüm/kaynak yapılandırmadan farklıysa güncelleme önerilir."""
    settings = _settings(tmp_path, _wheel())
    current = settings.zig.sources[PLATFORM].sha256

    assert needs_update(settings) is False  # kurulum yok → güncelleme değil, eksik kurulum
    _fake_install(settings, version=settings.zig.version, sha256=current)
    assert needs_update(settings, platform=PLATFORM) is False  # güncel
    _fake_install(settings, version="0.15.0", sha256=current)
    assert needs_update(settings, platform=PLATFORM) is True  # eski sürüm
    _fake_install(settings, version=settings.zig.version, sha256="0" * 64)
    assert needs_update(settings, platform=PLATFORM) is True  # aynı sürüm, kaynak değişti


def test_needs_update_false_on_missing_or_broken_marker(tmp_path: Path) -> None:
    """Faz F (F9): yarım kurulum (işaretçisiz) ve bozuk işaretçi güncelleme sayılmaz."""
    settings = _settings(tmp_path, _wheel())
    root = settings.toolchain_dir / "zig"
    root.mkdir(parents=True, exist_ok=True)
    (root / EXE).write_bytes(b"v1")
    assert needs_update(settings) is False  # işaretçi yok: kurulum tamamlanmamış
    (root / INSTALL_MARKER).write_text("bozuk", encoding="utf-8")
    assert needs_update(settings) is False
    (root / INSTALL_MARKER).write_text("[1, 2]", encoding="utf-8")
    assert needs_update(settings) is False


def test_needs_update_false_without_configured_source(tmp_path: Path) -> None:
    """Faz F (F9): bu platform için kaynak yoksa (adres/sha256) güncelleme önerilmez."""
    settings = _settings(tmp_path, _wheel())
    _fake_install(settings, version="0.15.0", sha256="0" * 64)
    assert needs_update(settings) is False  # host platformu kaynak listesinde yok
    assert needs_update(settings, platform="linux-aarch64") is False


def test_rename_retry_is_bounded_and_only_for_permission(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim: yeniden deneme sınırlı; başka OSError ve Windows dışı hemen düşer."""
    calls: list[str] = []

    def failing(error: OSError) -> object:
        def rename(self: Path, target: str | os.PathLike[str]) -> Path:
            calls.append(self.name)
            raise error

        return rename

    monkeypatch.setattr(toolchain_install, "_RENAME_DELAYS_S", (0.0,) * 4)
    monkeypatch.setattr(toolchain_install, "_RETRY_RENAME", True)
    monkeypatch.setattr(Path, "rename", failing(PermissionError(13, "kilit")))
    with pytest.raises(PermissionError):
        toolchain_install._rename(tmp_path / "a", tmp_path / "b")
    assert len(calls) == 5  # 4 bekleme + son deneme

    calls.clear()
    monkeypatch.setattr(Path, "rename", failing(FileNotFoundError(2, "yok")))
    with pytest.raises(FileNotFoundError):
        toolchain_install._rename(tmp_path / "a", tmp_path / "b")
    assert len(calls) == 1

    calls.clear()
    monkeypatch.setattr(toolchain_install, "_RETRY_RENAME", False)
    monkeypatch.setattr(Path, "rename", failing(PermissionError(13, "kilit")))
    with pytest.raises(PermissionError):
        toolchain_install._rename(tmp_path / "a", tmp_path / "b")
    assert len(calls) == 1


@respx.mock
def test_leftover_restore_failure_keeps_only_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim Ö4: `.zig-old-*` tek geçerli kurulumsa geri taşınamasa bile silinmez."""
    payload = _wheel(marker=b"v1")
    respx.get(URL).mock(return_value=httpx.Response(200, content=payload))
    settings = _settings(tmp_path, payload)
    _install(settings)
    old = settings.toolchain_dir / ".zig-old-deadbeef"
    (settings.toolchain_dir / "zig").rename(old)  # iki taşıma arasında çökmüş gibi

    real = Path.rename

    def locked(self: Path, target: str | os.PathLike[str]) -> Path:
        if self.name.startswith(".zig-old-"):
            raise PermissionError(13, "Erişim engellendi")
        return real(self, target)

    monkeypatch.setattr(Path, "rename", locked)
    monkeypatch.setattr(toolchain_install, "_RENAME_DELAYS_S", (0.0,) * 2)
    toolchain_install._clean_leftovers(settings.toolchain_dir)
    assert installed_zig(old) is not None  # kurulum yerinde, silinmedi
