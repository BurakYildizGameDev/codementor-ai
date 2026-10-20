"""Faz K: masaüstünde kendi sorunu ekle/düzenle/sil, form doğrulaması ve Geçmiş toplamı."""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from pathlib import Path

import pytest

from codementor.api.state import ApiState
from codementor.desktop import questions_controller as controller
from codementor.desktop.app import App
from codementor.desktop.connections import KeyStore
from codementor.desktop.views.questions_view import MINE
from codementor.models.enums import Engine, Language
from codementor.models.questions import DEFAULT_USER_HINTS
from tests.desktop.app_support import _open, pump

VALUES = {
    "title": "Dizideki en büyük iki sayı",
    "prompt": "En büyük iki farklı değeri bulan fonksiyonu yazın.",
    "language": "C",
    "engine": "Motor yok",
    "difficulty": "Kolay",
    "constraints": "O(1) ek bellek\n\n",
    "expected_time": "O(n)",
    "expected_space": "O(1)",
    "concept_tags": "Diziler, edge-cases",
    "hint1": "",
    "hint2": "Kaç kez geziyorsun?",
    "hint3": "",
}
QUESTION_ID = "kullanici-dizideki-en-buyuk-iki-sayi"


@pytest.fixture
def user_app(core: ApiState, prefs_dir: Path, store: KeyStore, tmp_path: Path) -> Iterator[App]:
    data = core.settings.data.model_copy(update={"user_questions_dir": tmp_path / "sorularim"})
    core.settings = core.settings.model_copy(update={"data": data})
    core.reload_questions()
    yield from _open(core, prefs_dir, store)


def _user_dir(app: App) -> Path:
    return app.core.settings.data.user_questions_dir


# --- form doğrulaması ---------------------------------------------------------------------------


def test_draft_from_form_normalizes() -> None:
    draft = controller.draft_from_form(VALUES)
    assert draft.language is Language.C
    assert draft.engine is Engine.NONE
    assert draft.constraints == ["O(1) ek bellek"]
    assert draft.expected_time == "n"
    assert draft.concept_tags == ["diziler", "edge-cases"]
    # boş 1. seviye kaymaz: genel ipucuyla dolar; sondaki boş seviye atılır
    assert draft.hints == [DEFAULT_USER_HINTS[0], "Kaç kez geziyorsun?"]


def test_form_error_is_turkish_and_names_fields() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as info:
        controller.draft_from_form(VALUES | {"title": " ", "prompt": ""})
    message = controller.form_error(info.value)
    assert message.splitlines() == ["Başlık: boş bırakılamaz", "Görev açıklaması: boş bırakılamaz"]
    # alanlar geçerliyse model düzeyi kural (yarım hedef karmaşıklık) Türkçe gelir
    with pytest.raises(ValidationError) as info:
        controller.draft_from_form(VALUES | {"expected_space": ""})
    assert "hem zaman hem bellek" in controller.form_error(info.value)


# --- ekle / düzenle / sil -----------------------------------------------------------------------


def test_save_adds_question_everywhere(user_app: App) -> None:
    assert controller.save_user(user_app, VALUES) is None
    assert (_user_dir(user_app) / f"{QUESTION_ID}.yaml").is_file()
    assert QUESTION_ID in user_app.core.questions()
    assert "kaydedildi" in user_app.toast_label.cget("text")
    user_app.analyze_view.select(Language.C, Engine.NONE, None)
    titles = [q.title for q in user_app.analyze_view._questions]
    assert VALUES["title"] in titles


def test_save_invalid_returns_error_and_writes_nothing(user_app: App) -> None:
    error = controller.save_user(user_app, VALUES | {"prompt": ""})
    assert error is not None
    assert "Görev açıklaması" in error
    assert not _user_dir(user_app).exists()


def test_form_submit_saves_and_closes(user_app: App) -> None:
    form = controller.open_add(user_app)
    form.set_values(VALUES)
    form.submit()
    assert not form.winfo_exists()
    assert QUESTION_ID in user_app.core.questions()


def test_form_submit_error_keeps_window_open(user_app: App) -> None:
    form = controller.open_add(user_app)
    form.set_values(VALUES | {"title": ""})
    form.submit()
    assert form.winfo_exists()
    assert "Başlık" in form.error_label.cget("text")
    form.destroy()


def test_html_form_disables_complexity(user_app: App) -> None:
    form = controller.open_add(user_app)
    form.set_values(VALUES | {"language": "HTML", "expected_time": "", "expected_space": ""})
    assert str(form.time_entry.cget("state")) == "disabled"
    assert form.values()["expected_time"] == ""
    form.destroy()


def test_edit_prefills_and_updates(user_app: App) -> None:
    controller.save_user(user_app, VALUES)
    question = user_app.core.questions().public(QUESTION_ID)
    form = controller.open_edit(user_app, question)
    assert form is not None
    values = form.values()
    assert values["title"] == VALUES["title"]
    assert values["hint2"] == "Kaç kez geziyorsun?"
    form.title_entry.delete(0, "end")
    form.title_entry.insert(0, "Yeni başlık")
    form.submit()
    stored = user_app.core.questions().get(QUESTION_ID)
    assert (stored.title, stored.version) == ("Yeni başlık", 2)


def test_delete_asks_and_removes(user_app: App) -> None:
    controller.save_user(user_app, VALUES)
    question = user_app.core.questions().public(QUESTION_ID)
    user_app.confirm = lambda *_a, **_k: False
    assert not controller.delete_user(user_app, question)
    assert QUESTION_ID in user_app.core.questions()
    user_app.confirm = lambda *_a, **_k: True
    assert controller.delete_user(user_app, question)
    assert QUESTION_ID not in user_app.core.questions()


def test_mine_filter_and_owner_buttons(user_app: App) -> None:
    user_app.navigate("questions")
    view = user_app.questions_view
    view.origin_filter.set(MINE)
    view.refresh()
    texts = [str(w.cget("text")) for w in view.grid_area.winfo_children()]
    assert any("Henüz kendi sorun yok" in t for t in texts)
    controller.save_user(user_app, VALUES)
    view.refresh()
    assert view.count_label.cget("text") == "1 soru"
    card = view.grid_area.winfo_children()[0]
    buttons: list[str] = []

    def walk(widget: object) -> None:
        for child in widget.winfo_children():  # type: ignore[attr-defined]
            if hasattr(child, "cget"):
                with contextlib.suppress(Exception):  # metni olmayan çerçeveler
                    buttons.append(str(child.cget("text")).strip())
            walk(child)

    walk(card)
    assert {"Düzenle", "Sil", "Kendi sorum"} <= set(buttons)


def test_history_shows_totals(user_app: App) -> None:
    user_app.navigate("history")
    pump(user_app, lambda: not user_app.history_view.loading)  # F11: liste arka planda okunur
    assert user_app.history_view.totals_label.cget("text").startswith("Toplam: 0 analiz")
