"""Masaüstü: soru bankası okunamazsa görünüm boş/None alır, hata loglanır (Faz 48).

Mantık Faz 54'te Tk'siz `questions_controller`'a taşındı; `App` yalnız ona devreder. Test
doğrudan denetleyiciyi sınar, böylece tkinter'ı olmayan Linux CI'da da toplanır."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from codementor.desktop import questions_controller
from codementor.models.enums import Engine, Language


class _BrokenCore:
    def questions(self) -> Any:
        raise OSError("soru dizini yok")


def test_question_bank_error_logged(captured_logs: Callable[[], list[dict[str, Any]]]) -> None:
    core: Any = _BrokenCore()
    assert questions_controller.questions_for(core, Language.C, Engine.NONE) == []
    assert questions_controller.filtered(core, Language.C, None) is None
    events = [e for e in captured_logs() if e["event"] == "question_bank_unreadable"]
    assert [e["error"] for e in events] == ["OSError", "OSError"]
