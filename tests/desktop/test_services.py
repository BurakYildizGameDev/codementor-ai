"""Masaüstü servisleri (Tk'siz): derleyici indirme teklifi ve ilerleme metni (Faz 29)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.config import DownloadSource, Settings, ZigSettings
from codementor.desktop.services import describe_progress, offer_compiler_download
from codementor.models.api import CompilerStatus
from codementor.models.validation import DownloadProgress
from codementor.validation.toolchain_install import INSTALL_MARKER, platform_key

_MB = 1024 * 1024


def _with_zig(settings: Settings, toolchain_dir: Path, *, source: bool = True) -> Settings:
    sources = {platform_key(): DownloadSource(url="https://x.test/z.whl", sha256="0" * 64)}
    validation = settings.validation.model_copy(
        update={
            "toolchain_dir": toolchain_dir,
            "zig": ZigSettings(sources=sources if source else {}),
        }
    )
    return settings.model_copy(update={"validation": validation})


def _statuses(c: str | None) -> list[CompilerStatus]:
    return [
        CompilerStatus(target="c", tool=c),
        CompilerStatus(target="cpp", tool=c),
        CompilerStatus(target="unreal", tool=c),
        CompilerStatus(target="csharp", tool=None),  # C# eksikliği zig ile çözülmez
        CompilerStatus(target="python", tool="CPython"),
    ]


def test_offer_only_when_c_family_missing_and_not_installed(
    settings: Settings, tmp_path: Path
) -> None:
    cfg = _with_zig(settings, tmp_path / "tc")
    assert offer_compiler_download(cfg, _statuses(None)) is True
    assert offer_compiler_download(cfg, _statuses("gcc")) is False
    assert (
        offer_compiler_download(_with_zig(settings, tmp_path, source=False), _statuses(None))
        is False
    )

    root = tmp_path / "tc" / "zig"
    root.mkdir(parents=True)
    (root / "zig.exe").write_bytes(b"")
    (root / "zig").write_bytes(b"")
    (root / INSTALL_MARKER).write_text("{}", encoding="utf-8")
    assert offer_compiler_download(cfg, _statuses(None)) is False


@pytest.mark.parametrize(
    ("event", "text", "fraction"),
    [
        (DownloadProgress(stage="download", done=25 * _MB, total=100 * _MB), "25 / 100 MB", 0.25),
        (DownloadProgress(stage="download", done=3 * _MB), "3 MB", None),
        (DownloadProgress(stage="extract", done=50, total=200), "açılıyor", 0.25),
        (DownloadProgress(stage="check", done=0, total=1), "denetleniyor", None),
    ],
)
def test_describe_progress(event: DownloadProgress, text: str, fraction: float | None) -> None:
    label, value = describe_progress(event)
    assert text in label
    assert value == fraction
