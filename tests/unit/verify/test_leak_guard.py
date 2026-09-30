"""§5.6 Sızıntı koruması: üç kontrol ayrı ayrı (pozitif + negatif) ve karar akışı."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from codementor.config import VerifySettings
from codementor.models.enums import Engine, Language
from codementor.models.verification import (
    CommonIdentifiers,
    LeakCheck,
    LeakField,
    LeakViolation,
)
from codementor.verify.leak_guard import (
    MAX_TEXT_CHARS,
    check_leaks,
    code_violations,
    decide_leak_action,
    identifiers,
    load_common_identifiers,
    strip_comments_and_strings,
)

REPO = Path(__file__).resolve().parents[3]
STUDENT = """\
List<Transform> enemies = new List<Transform>();
void Update() {
    var nearby = enemies.Where(e => Vector3.Distance(e.position, pos) < radius).ToList();
    if (!enemies.Contains(nearby[i])) OnTargetFound?.Invoke(nearby[i]);
}
"""
REFERENCE = """\
// Görülen hedefleri kümede tut; böylece tekrar tetiklenmez
private readonly HashSet<Transform> seenTargets = new HashSet<Transform>();
void Update() {
    float sqrRadius = radius * radius;
    foreach (var target in nearbyBuffer)
        if (seenTargets.Add(target)) OnTargetFound?.Invoke(target);
}
"""
SETTINGS = VerifySettings(common_identifiers_file=REPO / "data" / "leak_common_identifiers.yaml")


def _check(
    questions: list[str],
    hint: str | None = None,
    *,
    reference: str | None = REFERENCE,
    settings: VerifySettings = SETTINGS,
    question_text: str = "",
) -> LeakCheck:
    return check_leaks(
        questions,
        hint,
        student_code=STUDENT,
        language=Language.CSHARP,
        engine=Engine.UNITY,
        reference=reference,
        question_text=question_text,
        settings=settings,
    )


def _kinds(check: LeakCheck) -> list[str]:
    return [v.kind for v in check.violations]


# --- (1) Kod bloğu / kod benzeri satır --------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "Şunu dene:\n```csharp\nvar s = new HashSet<Transform>();\n```",
        "``` if (x) y(); ```",
    ],
)
def test_code_block_detected(text: str) -> None:
    assert code_violations(text, STUDENT)[0][0] == "code_block"


@pytest.mark.parametrize(
    "text",
    [
        "Neden `foundTargets.Add(t);` yazmıyorsun?",  # çağrı deyimi
        "Önce `int count = 0;` diye bir sayaç tanımlasan?",  # bildirim
        "`for (int k = 0; k < n; k++) {` ile başlayan bir döngü düşün.",  # döngü başlığı
        "Mesafeyi `d = (a - b).sqrMagnitude;` ile hesaplasan?",  # atama deyimi
        "`void Check(Transform t) { ... }` gibi bir yardımcı yaz.",  # fonksiyon tanımı
        "Önce `Node *next = cur->next;` ile sakla.",  # C işaretçi bildirimi
    ],
)
def test_code_line_detected(text: str) -> None:
    assert [k for k, _ in code_violations(text, STUDENT)] == ["code_line"]


@pytest.mark.parametrize(
    "text",
    [
        # Türkçe düzyazıdaki ; kod değildir (Faz 7 dersi)
        "Döngü kaç kez dönüyor; peki bu her karede mi oluyor?",
        "i = n olduğunda ne olur; dizinin sonunu aşar mı?",
        "int türünde bir sayaç yeterli mi; neden?",
        "i = n ise ne olur; dizinin sonu mu?",  # ASCII düzyazı, sağ taraf kod değil
        "x = 0 olsaydı döngü kaç kez dönerdi?",
        "a * b = c eşitliği her zaman doğru mu?",  # düzyazı: ; yok, işaretçi değil
        # öğrencinin kendi kodundan birebir alıntı serbest (Faz 7 dersi)
        "`if (!enemies.Contains(nearby[i])) OnTargetFound?.Invoke(nearby[i]);` koşulu "
        "ne zaman doğru olur?",
        "`List<Transform> enemies = new List<Transform>();` satırı her karede mi çalışıyor?",
        "`var nearby = enemies.Where(...).ToList();` satırı her karede ne ayırıyor?",
        "enemies.Contains(nearby[i]) çağrısı kaç eleman tarıyor?",
    ],
)
def test_prose_and_student_quotes_not_code_leaks(text: str) -> None:
    assert code_violations(text, STUDENT) == []


# --- (2) 5-gram örtüşmesi ---------------------------------------------------------------------


def test_ngram_overlap_detected() -> None:
    # tanımlayıcılar serbest listede olsa bile kod dizisi birebir kopyalanmış
    text = "radius * radius ; foreach ( var target in nearbyBuffer )"
    loose = VerifySettings(
        common_identifiers_file=SETTINGS.common_identifiers_file, leak_min_identifier_length=50
    )
    check = _check([text], settings=loose)
    assert "ngram_overlap" in _kinds(check)
    assert "forbidden_identifier" not in _kinds(check)


def test_ngram_from_student_code_not_counted() -> None:
    text = "Vector3.Distance(e.position, pos) < radius ifadesi neyi ölçüyor?"
    assert "ngram_overlap" not in _kinds(_check([text]))


def test_ngram_threshold_from_config() -> None:
    text = "Bir de radius * radius ; foreach döngüsüne bak, sonra hedeflere geç, ne değişir?"
    strict = VerifySettings(
        common_identifiers_file=SETTINGS.common_identifiers_file,
        leak_ngram_threshold=0.01,
        leak_min_identifier_length=50,
    )
    lax = strict.model_copy(update={"leak_ngram_threshold": 1.0})
    assert "ngram_overlap" in _kinds(_check([text], settings=strict))
    assert "ngram_overlap" not in _kinds(_check([text], settings=lax))


# --- (3) Yasaklı tanımlayıcılar ---------------------------------------------------------------


def test_forbidden_identifier_detected() -> None:
    check = _check(["Görülenleri bir HashSet içinde, seenTargets gibi, tutsan?"])
    (violation,) = check.violations
    assert violation.kind == "forbidden_identifier"
    assert "HashSet" in violation.detail
    assert "seenTargets" in violation.detail


@pytest.mark.parametrize(
    "text",
    [
        "enemies listesinde kaç eleman var?",  # öğrenci kodunda geçen ad
        "Update her karede mi çalışıyor?",  # Unity genel adı
        "Hedef bulunduğunda olay tetikleniyor mu; OnTargetFound ne zaman çağrılır?",
        "Listeyi her seferinde baştan mı tarıyorsun?",  # 'List' Türkçe sözcüğün parçası
        "Görülen hedefleri kümede tutmak işe yarar mı?",  # referans yorumundaki Türkçe sözcükler
    ],
)
def test_allowed_names_not_forbidden(text: str) -> None:
    assert _check([text]).clean, text


def test_question_text_names_allowed() -> None:
    text = "HashSet kullanımı soruda istenmişti; sen nasıl kullandın?"
    assert not _check([text]).clean
    assert _check([text], question_text="HashSet ile tekrarları engelleyin").clean


def test_hint_is_checked_too() -> None:
    check = _check(["Soru?"], "nearbyBuffer diye ayrı bir liste tut.")
    (violation,) = check.violations
    assert violation.field == "next_step_hint"
    assert violation.index is None


def test_without_reference_only_code_check() -> None:
    check = _check(["HashSet kullan: `var s = new HashSet<int>();`"], reference=None)
    assert not check.reference_checked
    assert _kinds(check) == ["code_line"]


def test_reference_comments_and_strings_ignored() -> None:
    clean = strip_comments_and_strings('int a = 1; // HashSet kullan\nvar s = "seenTargets";')
    assert identifiers(clean) == {"int", "a", "var", "s"}


def test_common_identifiers_file_loads() -> None:
    common = load_common_identifiers(SETTINGS.common_identifiers_file)
    assert isinstance(common, CommonIdentifiers)
    assert "List" in common.csharp
    assert "HashSet" not in common.csharp  # çözümü ele veren ad serbest listede olamaz
    assert "true" in common.common


# --- Karar ------------------------------------------------------------------------------------

QUESTIONS = ["İyi soru?", "HashSet kullan?"]


def _violation(index: int | None, field: LeakField = "guiding_questions") -> LeakViolation:
    return LeakViolation(field=field, index=index, kind="forbidden_identifier", detail="x")


def test_clean_passes() -> None:
    decision = decide_leak_action(
        QUESTIONS, "ipucu", LeakCheck(reference_checked=True), regenerated=False
    )
    assert decision.action == "passed"
    assert decision.guiding_questions == QUESTIONS


def test_first_violation_regenerates() -> None:
    check = LeakCheck(violations=[_violation(1)], reference_checked=True)
    decision = decide_leak_action(QUESTIONS, "ipucu", check, regenerated=False)
    assert decision.action == "regenerate"
    assert decision.guiding_questions == []


def test_after_regeneration_bad_question_and_hint_dropped() -> None:
    check = LeakCheck(
        violations=[_violation(1), _violation(None, "next_step_hint")], reference_checked=True
    )
    decision = decide_leak_action(QUESTIONS, "ipucu", check, regenerated=True)
    assert decision.action == "dropped_questions"
    assert decision.guiding_questions == ["İyi soru?"]
    assert decision.next_step_hint is None
    assert not decision.all_dropped


def test_all_questions_dropped() -> None:
    check = LeakCheck(violations=[_violation(0), _violation(1)], reference_checked=True)
    decision = decide_leak_action(QUESTIONS, None, check, regenerated=True)
    assert decision.all_dropped


def test_overlong_text_is_violation_and_fast() -> None:
    """§12: sınırsız uzunluktaki soru regex'lerde karesel süre almamalı."""
    start = time.perf_counter()
    check = _check(["a" * 1_000_000], "b" * 5_000)
    assert time.perf_counter() - start < 1.0
    assert _kinds(check) == ["too_long", "too_long"]


def test_max_length_text_is_fast() -> None:
    start = time.perf_counter()
    code_violations("a" * MAX_TEXT_CHARS, STUDENT)
    assert time.perf_counter() - start < 0.2
