"""Kategori sınırları tek yerde (Faz 51): etiket rehberi ile prompt aynı metni kullanır, etiketler
ve few-shot örnekleri bu sınırlara uyar."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
RULES = REPO / "prompts" / "v1" / "_category_rules.j2"
GUIDE = REPO / "docs" / "EVAL_ORNEK_REHBERI.md"
FEWSHOTS = REPO / "prompts" / "v1" / "fewshots"
BLOCK = re.compile(
    r"<!-- kategori-sinirlari:basla -->(.*?)<!-- kategori-sinirlari:bitir -->", re.DOTALL
)
# Geçersiz belleğe/konuma erişim anlatan notlar (her dilde → memory_safety)
MEMORY_HINTS = re.compile(
    r"sarkan|yineleyici|iterator|sınır dışı|dizinin dışında|OutOfRange|IndexError"
    r"|use-after|sonrası .*okunuyor",
    re.IGNORECASE,
)
# CSS/HTML'de dar ekran / taşma / kesilme → edge_case (işaretleme kuralı)
MARKUP_OVERFLOW = re.compile(r"dar ekran|kaydırma|kesilir|taşar", re.IGNORECASE)


def _words(text: str) -> str:
    return " ".join(text.split())


def test_rehber_and_prompt_share_category_rules() -> None:
    match = BLOCK.search(GUIDE.read_text(encoding="utf-8"))
    assert match is not None, "rehberde kategori-sinirlari işaretleri yok"
    guide = _words(match.group(1).replace("```text", "").replace("```", ""))
    assert guide == _words(RULES.read_text(encoding="utf-8"))


def _findings() -> list[tuple[str, dict[str, object]]]:
    found = []
    for path in sorted((REPO / "eval" / "dataset").glob("*/*/label.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for finding in data["expected"]["findings"] or []:
            found.append((f"{path.parent.parent.name}/{path.parent.name}", finding))
    return found


def memory_boundary_violation(sample: str, finding: dict[str, object]) -> bool:
    """Bellek erişimi notlu veya yapısal boundary'li bulgu memory_safety değilse ihlal;
    Unreal'da GC'nin topladığı nesneye kalan sarkan işaretçi `garbage_collection` sayılır
    (yalnız Unreal örneklerinde). Yapısal `boundary` alanı serbest metin sezgisinden önce gelir."""
    boundary = finding.get("boundary")
    if boundary == "ownership_scope":
        return False
    if boundary is not None:
        allowed = {str(boundary)} | (
            {"garbage_collection"} if "unreal-" in sample and boundary == "memory_safety" else set()
        )
        return finding["category"] not in allowed
    if not MEMORY_HINTS.search(str(finding.get("note", ""))):
        return False
    allowed = {"memory_safety"} | ({"garbage_collection"} if "unreal-" in sample else set())
    return finding["category"] not in allowed


@pytest.mark.parametrize(
    ("sample", "finding", "violates"),
    [
        ("dev/cpp-1", {"category": "undefined_behavior", "note": "sarkan referans"}, True),
        ("dev/cpp-1", {"category": "garbage_collection", "note": "sarkan işaretçi"}, True),
        ("dev/unreal-1", {"category": "garbage_collection", "note": "sarkan işaretçi"}, False),
        ("test/cs-1", {"category": "edge_case", "note": "boş listede IndexOutOfRange"}, True),
        ("dev/c-1", {"category": "memory_safety", "note": "sınır dışı okuma"}, False),
        ("dev/c-1", {"category": "performance", "note": "gereksiz kopya"}, False),
        ("dev/cpp-1", {"category": "memory_safety", "boundary": "memory_safety"}, False),
        ("dev/cpp-1", {"category": "performance", "boundary": "memory_safety"}, True),
        ("dev/cpp-1", {"category": "memory_safety", "boundary": "ownership_scope"}, False),
    ],
)
def test_memory_boundary_heuristic(sample: str, finding: dict[str, object], violates: bool) -> None:
    assert memory_boundary_violation(sample, finding) is violates


def test_labels_follow_memory_safety_boundary() -> None:
    wrong = [
        f"{sample} L{finding['line']}: {finding['category']}"
        for sample, finding in _findings()
        if memory_boundary_violation(sample, finding)
    ]
    assert wrong == []


def test_markup_overflow_labels_are_edge_case() -> None:
    """İşaretleme kuralı: dar ekran, taşma, kesilme → edge_case (`_markup_rules.j2`)."""
    wrong = [
        f"{sample} L{finding['line']}: {finding['category']}"
        for sample, finding in _findings()
        if re.search(r"/(css|html)-", sample)
        and MARKUP_OVERFLOW.search(str(finding.get("note", "")))
        and finding["category"] != "edge_case"
    ]
    assert wrong == []


def test_fewshots_follow_category_boundaries() -> None:
    """Few-shot örnekleri kuraldan güçlü örnek olur: sınır dışı/null/Destroy edilmiş nesne
    bulguları kurala uygun kategoride olmalı."""
    expected = {
        "cpp_unreal_uproperty.yaml": "memory_safety",  # null aktör (IsValid yok)
        "csharp_unity_update_alloc.yaml": "engine_best_practice",  # Destroy edilmiş düşman
        "csharp_none_string_concat.yaml": "memory_safety",  # boş listede Substring sınır dışı
    }
    for name, category in expected.items():
        data = yaml.safe_load((FEWSHOTS / name).read_text(encoding="utf-8"))
        categories = [f["category"] for f in data["analysis"]["additional_findings"]]
        assert category in categories, name
        assert "edge_case" not in categories, name
