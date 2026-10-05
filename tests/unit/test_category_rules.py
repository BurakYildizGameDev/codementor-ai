"""Kategori sınırları tek yerde (Faz 51): etiket rehberi ile prompt aynı metni kullanır ve
etiketler bu sınırlara uyar."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
RULES = REPO / "prompts" / "v1" / "_category_rules.j2"
GUIDE = REPO / "docs" / "EVAL_ORNEK_REHBERI.md"
BLOCK = re.compile(
    r"<!-- kategori-sinirlari:basla -->(.*?)<!-- kategori-sinirlari:bitir -->", re.DOTALL
)
# Geçersiz belleğe erişim anlatan notlar (Unreal'da GC'nin topladığı nesneye kalan işaretçi
# `garbage_collection` sayılır: kök neden UPROPERTY eksikliği)
MEMORY_HINTS = re.compile(r"sarkan|yineleyici|iterator|sınır dışı", re.IGNORECASE)


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
        for finding in data["expected"]["findings"]:
            found.append((f"{path.parent.parent.name}/{path.parent.name}", finding))
    return found


def test_labels_follow_memory_safety_boundary() -> None:
    """Sarkan işaretçi/referans, geçersizleşmiş yineleyici ve sınır dışı erişim etiketleri
    `memory_safety` (Unreal GC kaynaklı sarkan işaretçi hariç)."""
    wrong = [
        f"{sample} L{finding['line']}: {finding['category']}"
        for sample, finding in _findings()
        if MEMORY_HINTS.search(str(finding.get("note", "")))
        and finding["category"] not in {"memory_safety", "garbage_collection"}
    ]
    assert wrong == []
