"""Soru oturumu davranışı — Faz 54 bölmesi (`app.py`'den).

Soru bankası sorguları, soruya başlama ve ipucu merdiveni sıfırlama. `App` aynı yöntem
adlarıyla ince sarmalayıcılar tutar; böylece test yüzeyi (bağımsız çağrılar dâhil) değişmez.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from codementor.desktop import runtime
from codementor.desktop.viewmodel import SAMPLES
from codementor.log import get_logger
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import QuestionPublic

if TYPE_CHECKING:
    from codementor.api.state import ApiState
    from codementor.desktop.app import App

log = get_logger("codementor.desktop")


def questions_for(core: ApiState, language: Language, engine: Engine) -> list[QuestionPublic]:
    """Seçili dil/motor için sorular; banka okunamazsa boş liste (hata loglanır)."""
    try:
        return core.questions().filter(language, engine)
    except Exception as exc:
        log.warning("question_bank_unreadable", error=type(exc).__name__)
        return []


def filtered(
    core: ApiState, language: Language | None, difficulty: Difficulty | None
) -> list[QuestionPublic] | None:
    """Filtrelenmiş sorular; banka okunamazsa None (görünüm 'okunamadı' der)."""
    try:
        return core.questions().filter(language, None, difficulty)
    except Exception as exc:
        log.warning("question_bank_unreadable", error=type(exc).__name__)
        return None


def start(app: App, question: QuestionPublic) -> None:
    """Soruyu editöre taşır ve analiz sayfasına geçer."""
    view = app.analyze_view
    view.select(question.language, question.engine, question.id)
    if view.editor.get().strip() in {s.strip() for s in SAMPLES.values()}:
        view.editor.set("", question.language)
    view.reset_results()
    app.navigate("analyze")
    view.editor.text.focus_set()


def load_sample(app: App) -> None:
    """Editörü seçili dilin örneğiyle doldurur ve sonuçları sıfırlar."""
    view = app.analyze_view
    view.editor.set(SAMPLES[view.language], view.language)
    view.reset_results()


def new_session(app: App) -> None:
    """Yeni ipucu oturumu açar ve tercihlere yazar."""
    app.prefs = app.prefs.model_copy(update={"session_id": f"desktop-{uuid.uuid4()}"})
    runtime.save_prefs(app.prefs, app.prefs_dir)


def restart(app: App) -> None:
    """İpucu merdivenini sıfırlar: yeni oturum, bir sonraki analiz 1. seviyeden başlar."""
    new_session(app)
    app.analyze_view.reset_results()
    app.toast("İpucu merdiveni sıfırlandı. Bir sonraki denetim ilk seviyeden başlar.")
