"""Faz 60 derleme ve sürüm bilgisi testleri."""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

import codementor
from codementor.buildinfo import build_info, describe, format_cli_version
from codementor.models.build import BuildInfo


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    build_info.cache_clear()


def test_build_info_source_fallback_when_file_absent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """build_info() dosya yokken kaynak bilgisini döndürür."""
    non_existent = tmp_path / "data" / "build_info.json"
    monkeypatch.setattr("codementor.buildinfo.resource_path", lambda _rel: non_existent)

    info = build_info()
    assert info.version == codementor.__version__
    assert info.commit is None
    assert info.built_at is None
    assert info.source == "kaynak"


def test_build_info_reads_valid_exe_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """build_info() geçerli dosya varken exe bilgisini okur."""
    target = tmp_path / "data" / "build_info.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.1.0",
        "commit": "a1b2c3d",
        "built_at": "2026-10-06T14:30:00Z",
        "source": "exe",
    }
    target.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr("codementor.buildinfo.resource_path", lambda _rel: target)

    info = build_info()
    assert info.version == "0.1.0"
    assert info.commit == "a1b2c3d"
    assert info.source == "exe"
    assert info.built_at is not None
    assert info.built_at.year == 2026
    assert info.built_at.month == 10
    assert info.built_at.day == 6


@pytest.mark.parametrize(
    "corrupt_content",
    [
        "bu json degil",  # bozuk JSON
        json.dumps({"version": "0.1.0"}),  # eksik zorunlu alan 'source'
        json.dumps({"source": "bilinmeyen_kaynak", "version": "0.1.0"}),  # geçersiz Literal
        json.dumps({"version": 12345, "source": "exe"}),  # 'version' tipi int
    ],
)
def test_build_info_corrupt_file_falls_back_without_crashing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    corrupt_content: str,
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Olumsuz test: Bozuk dosya veya şema hatasında çökmez, kaynak bilgisi döner."""
    target = tmp_path / "data" / "build_info.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(corrupt_content, encoding="utf-8")
    monkeypatch.setattr("codementor.buildinfo.resource_path", lambda _rel: target)

    info = build_info()
    assert info.version == codementor.__version__
    assert info.commit is None
    assert info.built_at is None
    assert info.source == "kaynak"
    # denetim O4/L3: uyarı loglanır ve hata türünü taşır
    events = [e for e in captured_logs() if e.get("event") == "build_info_unreadable"]
    assert len(events) == 1
    assert events[0]["error"] in {"JSONDecodeError", "ValidationError"}


def test_describe_source_and_exe() -> None:
    """describe() iki biçimi üretir."""
    kaynak_info = BuildInfo(
        version="0.1.0",
        commit=None,
        built_at=None,
        source="kaynak",
    )
    assert describe(kaynak_info) == "0.1.0 · kaynaktan"

    exe_info = BuildInfo(
        version="0.1.0",
        commit="a1b2c3d",
        built_at=datetime(2026, 10, 6, 14, 30, tzinfo=UTC),
        source="exe",
    )
    assert describe(exe_info) == "0.1.0 · a1b2c3d · 06.10.2026"


def test_format_cli_version() -> None:
    """CLI --version çıktısının biçimlendirilmesi."""
    kaynak_info = BuildInfo(
        version="0.1.0",
        commit=None,
        built_at=None,
        source="kaynak",
    )
    assert format_cli_version(kaynak_info) == "codementor 0.1.0 (kaynaktan)"

    exe_info = BuildInfo(
        version="0.1.0",
        commit="a1b2c3d",
        built_at=datetime(2026, 10, 6, 14, 30, tzinfo=UTC),
        source="exe",
    )
    assert format_cli_version(exe_info) == "codementor 0.1.0 (a1b2c3d, 2026-10-06, exe)"
