"""Dosya işlemleri (Faz 24): sürükle-bırak verisi ve son dosyalar listesi."""

from __future__ import annotations

from codementor.desktop import runtime
from codementor.desktop.files import parse_drop_data, recent_label
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
