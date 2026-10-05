"""Masaüstü: soru bankası okunamazsa görünüm boş/None alır, hata loglanır (Faz 48).
Tk penceresi açılmaz; yöntemler yalnız `core` alanını kullanır."""

from __future__ import annotations

from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

from codementor.desktop.app import App
from codementor.models.enums import Engine, Language


class _BrokenCore:
    def questions(self) -> Any:
        raise OSError("soru dizini yok")


def test_question_bank_error_logged(captured_logs: Callable[[], list[dict[str, Any]]]) -> None:
    fake_app = SimpleNamespace(core=_BrokenCore())
    assert App.questions_for(fake_app, Language.C, Engine.NONE) == []  # type: ignore[arg-type]
    assert App._filtered_questions(fake_app, Language.C, None) is None  # type: ignore[arg-type]
    events = [e for e in captured_logs() if e["event"] == "question_bank_unreadable"]
    assert [e["error"] for e in events] == ["OSError", "OSError"]
