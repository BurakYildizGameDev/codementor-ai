"""Dosya işlemleri (Faz 24): sürükle-bırak verisi ve son dosyalar listesi."""

from __future__ import annotations

from pathlib import Path

from codementor.desktop import runtime
from codementor.desktop.files import (
    MAX_FOLDER_FILES,
    folder_sources,
    parse_drop_data,
    recent_label,
)
from codementor.models.desktop import DesktopPrefs


def test_parse_drop_data_braced_paths() -> None:
    data = r"{C:/Users/Ad Soyad/Ödev 1/main.c}"
    assert parse_drop_data(data) == ["C:/Users/Ad Soyad/Ödev 1/main.c"]
    assert parse_drop_data("C:/a/b.c") == ["C:/a/b.c"]


def test_parse_drop_data_multiple_takes_order() -> None:
    data = "{C:/iki kelime/a.c} C:/b.cpp {C:/c d/e.cs}"
    assert parse_drop_data(data) == ["C:/iki kelime/a.c", "C:/b.cpp", "C:/c d/e.cs"]
    assert parse_drop_data("") == []
    assert parse_drop_data("   ") == []


def test_forget_file() -> None:
    prefs = DesktopPrefs(recent_files=["a.c", "b.c", "c.c"])
    assert runtime.forget_file(prefs, "b.c").recent_files == ["a.c", "c.c"]
    assert runtime.forget_file(prefs, "yok.c").recent_files == ["a.c", "b.c", "c.c"]


def test_recent_label_shows_name_and_folder() -> None:
    assert recent_label("C:/proje/src/main.c") == "main.c  —  C:/proje/src"
    long_folder = "C:/" + "/".join(["klasor"] * 12)
    label = recent_label(f"{long_folder}/x.py")
    assert label.startswith("x.py  —  …")
    assert len(label) <= 70


def test_folder_sources_lists_known_languages_sorted(tmp_path: Path) -> None:
    """Faz 33: bırakılan klasördeki kaynak dosyaları (alt klasörler ve bilinmeyen uzantı yok)."""
    for name in ("b.cs", "A.c", "notes.txt", "style.css"):
        (tmp_path / name).write_text("x", encoding="utf-8")
    (tmp_path / "alt").mkdir()
    (tmp_path / "alt" / "c.py").write_text("x", encoding="utf-8")
    assert [Path(p).name for p in folder_sources(tmp_path)] == ["A.c", "b.cs", "style.css"]


def test_folder_sources_limited(tmp_path: Path) -> None:
    for i in range(MAX_FOLDER_FILES + 5):
        (tmp_path / f"f{i:03d}.c").write_text("x", encoding="utf-8")
    assert len(folder_sources(tmp_path)) == MAX_FOLDER_FILES
