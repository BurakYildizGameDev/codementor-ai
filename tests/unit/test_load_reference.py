"""K5 referans çözüm okuma (Faz 30): yol kaynak köküne göre çözülür, `private/` dışına çıkamaz."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import Question
from codementor.pipeline import stages
from codementor.pipeline.stages import load_reference
from codementor.questions.reference import MAX_REFERENCE_BYTES


def _question(path: str | None) -> Question:
    return Question.model_validate(
        {
            "id": "py-easy-sample",
            "version": 1,
            "language": Language.PYTHON,
            "engine": Engine.NONE,
            "difficulty": Difficulty.EASY,
            "title": "Örnek",
            "prompt": "Bir fonksiyon yazın.",
            "constraints": ["Doğru çalışmalı"],
            "expected": {"time": {"f": "n"}, "space": "1"},
            "concept_tags": ["strings", "edge-cases"],
            "hint_ladder": {1: "a", 2: "b", 3: "c"},
            "reference_solution_path": path,
        }
    )


def _write(root: Path, rel: str, text: str) -> None:
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text, encoding="utf-8")


def test_resolved_against_root_not_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write(tmp_path, "private/solutions/a.py", "def gizli(): ...\n")
    monkeypatch.chdir(tmp_path.parent)  # çalışma dizini kaynak kökü değil
    text, notes = load_reference(_question("private/solutions/a.py"), root=tmp_path)
    assert text == "def gizli(): ...\n"
    assert notes == []


def test_missing_file_returns_none(tmp_path: Path) -> None:
    assert load_reference(_question("private/solutions/yok.py"), root=tmp_path) == (None, [])
    assert load_reference(_question(None), root=tmp_path) == (None, [])
    assert load_reference(None, root=tmp_path) == (None, [])


def test_symlink_outside_private_is_refused(tmp_path: Path) -> None:
    _write(tmp_path, "secret.txt", "GIZLI-ANAHTAR")
    link = tmp_path / "private" / "solutions" / "a.py"
    link.parent.mkdir(parents=True)
    try:
        os.symlink(tmp_path / "secret.txt", link)
    except (OSError, NotImplementedError):
        pytest.skip("bu sistemde sembolik bağlantı oluşturulamıyor")
    assert load_reference(_question("private/solutions/a.py"), root=tmp_path) == (None, [])


def _symlink(target: Path, link: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError):
        pytest.skip("bu sistemde sembolik bağlantı oluşturulamıyor")


def test_symlink_inside_private_is_allowed(tmp_path: Path) -> None:
    _write(tmp_path, "private/solutions/gercek.py", "x = 1\n")
    _symlink(
        tmp_path / "private" / "solutions" / "gercek.py",
        tmp_path / "private" / "solutions" / "a.py",
    )
    assert load_reference(_question("private/solutions/a.py"), root=tmp_path)[0] == "x = 1\n"


def test_private_dir_linked_elsewhere_is_allowed(tmp_path: Path) -> None:
    """Çözümleri başka bir diske taşıyıp private/'ı bağlayan geliştirici reddedilmez."""
    _write(tmp_path, "baska-disk/solutions/a.py", "y = 2\n")
    root = tmp_path / "repo"
    root.mkdir()
    _symlink(tmp_path / "baska-disk", root / "private")
    assert load_reference(_question("private/solutions/a.py"), root=root)[0] == "y = 2\n"


def test_symlink_loop_does_not_raise(tmp_path: Path) -> None:
    solutions = tmp_path / "private" / "solutions"
    _symlink(solutions / "b.py", solutions / "a.py")
    _symlink(solutions / "a.py", solutions / "b.py")
    assert load_reference(_question("private/solutions/a.py"), root=tmp_path) == (None, [])


def test_oversized_and_non_utf8_refused(
    tmp_path: Path, captured_logs: Callable[[], list[dict[str, Any]]]
) -> None:
    _write(tmp_path, "private/solutions/a.py", "x" * (MAX_REFERENCE_BYTES + 1))
    assert load_reference(_question("private/solutions/a.py"), root=tmp_path) == (None, [])
    (tmp_path / "private" / "solutions" / "a.py").write_bytes(b"\xff\xfe\x00bozuk")
    assert load_reference(_question("private/solutions/a.py"), root=tmp_path) == (None, [])
    events = [e for e in captured_logs() if e.get("event") == "reference_solution_unreadable"]
    assert len(events) == 2
    assert "x" * 50 not in str(events)  # çözüm içeriği loga yazılmaz


def test_default_root_is_resource_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Varsayılan kök `resource_root()` (exe'de _MEIPASS; private/ pakette yok → None)."""
    _write(tmp_path, "private/solutions/a.py", "z = 3\n")
    monkeypatch.setattr(stages, "resource_root", lambda: tmp_path)
    assert load_reference(_question("private/solutions/a.py"))[0] == "z = 3\n"
    monkeypatch.setattr(stages, "resource_root", lambda: tmp_path / "meipass")
    assert load_reference(_question("private/solutions/a.py")) == (None, [])


def test_missing_file_logged_at_debug_only(
    tmp_path: Path, captured_logs: Callable[[], list[dict[str, Any]]]
) -> None:
    """Faz 31: dağıtımda `private/` yok; her analizde WARNING basmak gürültü. Yok → DEBUG,
    okunamayan/şüpheli dosya → WARNING."""
    assert load_reference(_question("private/solutions/yok.py"), root=tmp_path) == (None, [])
    events = [e for e in captured_logs() if e.get("event") == "reference_solution_unreadable"]
    assert [e["level"] for e in events] == ["debug"]


def test_validate_and_load_share_resolver(tmp_path: Path) -> None:
    """`questions validate` ile analiz aynı kuralla çözer: büyük dosya ikisinde de reddedilir."""
    from codementor.questions.reference import ReferenceError, resolve_reference

    _write(tmp_path, "private/solutions/b.py", "x" * (MAX_REFERENCE_BYTES + 1))
    with pytest.raises(ReferenceError, match="büyük"):
        resolve_reference("private/solutions/b.py", tmp_path)
    assert load_reference(_question("private/solutions/b.py"), root=tmp_path) == (None, [])
