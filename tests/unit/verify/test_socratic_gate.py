"""Sokratik kalite kapısı testleri (Faz I / İş 11, ADR-0031)."""

from __future__ import annotations

import pytest

from codementor.verify.socratic_gate import (
    deduplicate_questions,
    evaluate_socratic_gate,
    has_repetition_loop,
    jaccard_similarity,
    touches_code,
)

SAMPLE_CODE = """
int binary_search(const int* arr, int size, int target) {
    int low = 0;
    int high = size - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
"""


def test_jaccard_similarity() -> None:
    q1 = "Döngünün son adımında hangi değer döner?"
    q2 = "Döngünün son adımında hangi sonuç döner?"
    sim = jaccard_similarity(q1, q2)
    assert sim >= 0.70

    q3 = "Bellek tahsisi serbest bırakılıyor mu?"
    assert jaccard_similarity(q1, q3) < 0.30


def test_deduplicate_questions() -> None:
    questions = [
        "Döngü her adımda low değerini nasıl günceller?",
        "Döngü her turda low değerini nasıl günceller?",  # neredeyse aynı
        "mid hesaplamasında taşma riski var mı?",
    ]
    deduped = deduplicate_questions(questions, threshold=0.65)
    assert len(deduped) == 2
    assert deduped[0] == questions[0]
    assert deduped[1] == questions[2]


def test_has_repetition_loop() -> None:
    # 3 kelimelik n-gram 3 kez peş peşe tekrarlanıyor
    looped = "Bu işlem adımı bu işlem adımı bu işlem adımı sonucunda ne olur?"
    assert has_repetition_loop(looped)

    # Normal metin
    normal = "Döngü dizinin sınırlarını aşmadan target değerini arayabilir mi?"
    assert not has_repetition_loop(normal)


def test_numeric_sequences_are_not_degeneration() -> None:
    """Tam tarama #5: sayı dizisi meşru girdi örneğidir, tüm çıktıyı şablona düşürmemeli."""
    assert not has_repetition_loop("Dizi 0 0 0 0 0 0 0 0 0 ile başlarsa sum ne olur?")
    assert not has_repetition_loop("Girdi 1 2 3 1 2 3 1 2 3 olduğunda döngü kaç tur döner?")
    # Kelime içeren tekrar hâlâ döngü
    assert has_repetition_loop("x 0 ise x 0 ise x 0 ise ne olur?")


def test_touches_code() -> None:
    identifiers = {"binary_search", "arr", "size", "target", "low", "high", "mid"}

    # Tanımlayıcıya değiyor
    assert touches_code("low değişkeni döngü bittiğinde ne olur?", identifiers)
    assert touches_code("arr dizisinin elemanlarına nasıl erişilir?", identifiers)

    # Satır numarasına değiyor
    assert touches_code("6. satırda yapılan hesaplama doğru mu?", identifiers)
    assert touches_code("line 8 kontrolünü inceleyin.", identifiers)

    # Koda hiç temas etmeyen jenerik soru
    assert not touches_code("Kodunuzun mantığını adım adım inceleyin.", identifiers)


@pytest.mark.parametrize(
    "text",
    [
        "Bu yaklaşım lineer mi?",  # "line" öneki
        "Hangi satır sorunlu olabilir?",  # rakamsız satır
        "Satırlar arasındaki ilişki nedir?",
        "Online bir çözüm düşündün mü?",
    ],
)
def test_generic_line_words_do_not_touch_code(text: str) -> None:
    """Tam tarama #5: jenerik sorular "satır"/"line" kelimesiyle kapıdan geçmemeli."""
    assert not touches_code(text, {"binary_search", "arr", "low"})


@pytest.mark.parametrize(
    "text",
    [
        "12. satırda ne oluyor?",
        "satır 12 neyi döndürür?",
        "line 8 kontrolünü inceleyin.",
        "lines 3 neden gerekli?",
        "3-5. satırlar aynı işi mi yapıyor?",
    ],
)
def test_numbered_line_refs_touch_code(text: str) -> None:
    assert touches_code(text, set())


def test_evaluate_socratic_gate_fails_on_loop() -> None:
    questions = ["tekrar eden soru tekrar eden soru tekrar eden soru nedir?"]
    result = evaluate_socratic_gate(
        questions=questions,
        next_step_hint="İpucu",
        code=SAMPLE_CODE,
        hint_level=1,
    )
    assert not result.passed
    assert result.reason == "repetition_loop"
    assert any("döngüsel tekrar" in w for w in result.warnings)


def test_evaluate_socratic_gate_fails_on_small_profile_without_code_touch() -> None:
    questions = [
        "Kodunuzun çalışma mantığını inceleyin.",
        "Genel yaklaşımınızı gözden geçirin.",
    ]
    result = evaluate_socratic_gate(
        questions=questions,
        next_step_hint="Adımları takip edin.",
        code=SAMPLE_CODE,
        hint_level=2,
        model_profile="small",
    )
    # Küçük profilde ve seviye 2'de koda hiç değmeyen sorular reddedilmeli
    assert not result.passed
    assert result.reason == "no_code_reference"
    assert any("temas etmiyor" in w for w in result.warnings)


def test_evaluate_socratic_gate_passes_valid() -> None:
    questions = [
        "low ve high değişkenleri toplandığında bir tamsayı taşması oluşabilir mi?",
        "mid indeksindeki değer aranan hedefle eşit olmadığında arama aralığı nasıl daralır?",
    ]
    result = evaluate_socratic_gate(
        questions=questions,
        next_step_hint="low + (high - low) / 2 yöntemini düşünün.",
        code=SAMPLE_CODE,
        hint_level=2,
        model_profile="small",
    )
    assert result.passed
    assert len(result.filtered_questions) == 2
    assert result.reason is None
