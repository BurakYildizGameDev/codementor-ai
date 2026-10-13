"""Soru oturumu davranışı — Faz 54 bölmesi (`app.py`'den).

Soru bankası sorguları, soruya başlama ve ipucu merdiveni sıfırlama. `App` aynı yöntem
adlarıyla ince sarmalayıcılar tutar; böylece test yüzeyi (bağımsız çağrılar dâhil) değişmez.
Faz K (ADR-0028): kendi sorunu ekleme/düzenleme/silme; form doğrulaması burada (Tk'siz test).
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Mapping
from typing import TYPE_CHECKING

from pydantic import ValidationError

from codementor.desktop import runtime
from codementor.desktop.viewmodel import (
    DIFFICULTY_LABELS,
    ENGINE_LABELS,
    LANGUAGE_LABELS,
    SAMPLES,
)
from codementor.desktop.views.question_form import QuestionForm, draft_values
from codementor.log import get_logger
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import (
    DEFAULT_USER_HINTS,
    Question,
    QuestionPublic,
    UserQuestionDraft,
)
from codementor.questions.user_store import (
    UserQuestionError,
    delete_question,
    get_question,
    save_question,
    slugify,
)

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


# --- Faz K: kendi soruların -------------------------------------------------------------------

_FIELD_NAMES = {
    "title": "Başlık",
    "prompt": "Görev açıklaması",
    "language": "Dil",
    "engine": "Motor",
    "difficulty": "Zorluk",
    "constraints": "Kısıtlar",
    "expected_time": "Hedef zaman",
    "expected_space": "Hedef bellek",
    "concept_tags": "Kavram etiketleri",
    "hints": "İpuçları",
}


def _lookup[K](labels: Mapping[K, str], text: str) -> K | str:
    """Etiketten enum; bulunamazsa metin olduğu gibi (doğrulama hatası verir)."""
    return next((key for key, label in labels.items() if label == text), text)


def _tag(text: str) -> str:
    """`Bellek Yönetimi` → `bellek-yonetimi` (etiket deseni küçük harf, rakam, tire)."""
    return slugify(text) if re.search(r"[a-zA-Z0-9]", text) else text


def draft_from_form(values: Mapping[str, str]) -> UserQuestionDraft:
    """Form metinlerinden taslak; geçersizse `ValidationError` (bkz. `form_error`)."""
    hints = [values.get(key, "") for key in ("hint1", "hint2", "hint3")]
    while hints and not hints[-1].strip():
        hints.pop()
    tags = [t.strip() for t in values.get("concept_tags", "").split(",") if t.strip()]
    return UserQuestionDraft.model_validate(
        {
            "title": values.get("title", ""),
            "prompt": values.get("prompt", ""),
            "language": _lookup(LANGUAGE_LABELS, values.get("language", "")),
            "engine": _lookup(ENGINE_LABELS, values.get("engine", ENGINE_LABELS[Engine.NONE])),
            "difficulty": _lookup(DIFFICULTY_LABELS, values.get("difficulty", "")),
            "constraints": values.get("constraints", "").splitlines(),
            "expected_time": values.get("expected_time") or None,
            "expected_space": values.get("expected_space") or None,
            "concept_tags": [_tag(t) for t in tags],
            # aradaki boş seviye kaymasın: genel ipucuyla dolar
            "hints": [h.strip() or DEFAULT_USER_HINTS[i] for i, h in enumerate(hints)],
        }
    )


def form_error(exc: ValidationError) -> str:
    """Pydantic hatalarından kullanıcıya Türkçe, alan adlı kısa metin."""
    lines: list[str] = []
    for error in exc.errors():
        field = str(error["loc"][0]) if error["loc"] else ""
        name = _FIELD_NAMES.get(field, "")
        kind = error["type"]
        if kind in {"missing", "string_too_short"}:
            message = "boş bırakılamaz"
        elif kind == "string_too_long":
            message = "çok uzun"
        elif kind in {"enum", "literal_error"}:
            message = "geçerli bir seçenek değil"
        elif kind == "string_pattern_mismatch":
            message = "yalnız küçük harf, rakam ve tire içerebilir"
        elif kind == "too_long":
            message = "en fazla 3 ipucu verilebilir"
        else:
            message = str(error["msg"]).removeprefix("Value error, ")
        lines.append(f"{name}: {message}" if name else message)
    return "\n".join(dict.fromkeys(lines))


def save_user(app: App, values: Mapping[str, str], question_id: str | None = None) -> str | None:
    """Formu kaydeder; hata metni ya da başarıda None (banka ve listeler yenilenir)."""
    try:
        draft = draft_from_form(values)
    except ValidationError as exc:
        return form_error(exc)
    core = app.core
    try:
        builtin = {q.id for q in core.questions() if q.origin == "builtin"}
        question = save_question(
            draft, core.settings.data.user_questions_dir, question_id=question_id, taken=builtin
        )
    except UserQuestionError as exc:
        return str(exc)
    _reload(app)
    app.toast(f"Soru kaydedildi: {question.title}")
    return None


def user_question(app: App, question_id: str) -> Question | None:
    """Düzenlenecek kullanıcı sorusu; bulunamazsa None."""
    try:
        return get_question(question_id, app.core.settings.data.user_questions_dir)
    except UserQuestionError as exc:
        log.warning("user_question_unreadable", error=str(exc)[:200])
        return None


def delete_user(app: App, question: QuestionPublic) -> bool:
    """Onay alıp kullanıcı sorusunu siler; silindiyse True."""
    if not app.confirm(
        "Soruyu sil", f"“{question.title}” sorusu silinsin mi? Bu işlem geri alınamaz."
    ):
        return False
    try:
        delete_question(question.id, app.core.settings.data.user_questions_dir)
    except UserQuestionError as exc:
        app.toast(str(exc))
        return False
    _reload(app)
    app.toast("Soru silindi.")
    return True


def open_add(app: App) -> QuestionForm:
    """Boş soru formu."""
    return QuestionForm(app, lambda values: save_user(app, values))


def open_edit(app: App, question: QuestionPublic) -> QuestionForm | None:
    """Kullanıcı sorusunu düzenleme formu; soru okunamazsa None (bildirim gösterilir)."""
    stored = user_question(app, question.id)
    if stored is None:
        app.toast("Soru okunamadı; dosyası silinmiş ya da bozulmuş olabilir.")
        return None
    try:
        initial = draft_values(UserQuestionDraft.from_question(stored))
    except ValidationError as exc:  # elle yazılmış dosya formun kurallarını aşıyor (denetim D-2)
        app.toast(f"Bu soru formla düzenlenemiyor: {form_error(exc)}")
        return None
    return QuestionForm(app, lambda values: save_user(app, values, question.id), initial=initial)


def bank_warnings(core: ApiState) -> list[str]:
    """Atlanan kendi soru dosyaları (ADR-0028 §6); banka okunamazsa boş."""
    try:
        return list(core.questions().warnings)
    except Exception:
        return []


def _reload(app: App) -> None:
    """Bankayı yeniden okur; soru ekranı ve analiz ekranındaki soru listesi yenilenir."""
    app.core.reload_questions()
    app.questions_view.refresh()
    app.analyze_view.refresh_questions()
