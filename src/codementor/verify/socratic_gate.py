"""Deterministik Sokratik kalite kapısı (Faz I / İş 11, ADR-0031).

Zayıf ve küçük modellerin ürettiği döngüsel tekrarları, kopya soruları
ve koda hiç temas etmeyen jenerik soruları eler; gerekirse şablon sorulara
düşürür.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_WORD_RE = re.compile(r"\b\w+\b", re.IGNORECASE)
# Satır referansı rakam ister: "satır 12", "satırda 12", "line 8", "6. satırda", "3-5. satırlar".
# Rakamsız "Hangi satır?" ya da "lineer" koda temas sayılmaz (tam tarama #5).
_LINE_REF_RE = re.compile(
    r"\b(?:satır\w*|lines?)\s*\d+\b|\b\d+(?:\s*[-\u2013]\s*\d+)?\.\s*satır", re.IGNORECASE
)

# Genel programlama anahtar kelimeleri: koda özgü tanımlayıcı sayılmaz
_COMMON_KEYWORDS = {
    "auto",
    "bool",
    "break",
    "case",
    "char",
    "class",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "false",
    "float",
    "for",
    "goto",
    "if",
    "int",
    "long",
    "namespace",
    "new",
    "null",
    "nullptr",
    "operator",
    "private",
    "protected",
    "public",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "template",
    "this",
    "true",
    "typedef",
    "typename",
    "union",
    "unsigned",
    "using",
    "virtual",
    "void",
    "volatile",
    "while",
    "def",
    "elif",
    "except",
    "finally",
    "import",
    "from",
    "in",
    "is",
    "lambda",
    "none",
    "nonlocal",
    "not",
    "pass",
    "raise",
    "try",
    "with",
    "yield",
    "self",
    "string",
    "var",
    "let",
    "val",
    "function",
    "fn",
}


def _tokenize(text: str) -> set[str]:
    """Küçük harfli kelime kümesi."""
    return {w.lower() for w in _WORD_RE.findall(text) if len(w) > 1}


def jaccard_similarity(text1: str, text2: str) -> float:
    """İki metin arasındaki Jaccard token benzerliği."""
    s1, s2 = _tokenize(text1), _tokenize(text2)
    if not s1 or not s2:
        return 0.0
    union = s1 | s2
    return len(s1 & s2) / len(union) if union else 0.0


def deduplicate_questions(questions: list[str], threshold: float = 0.70) -> list[str]:
    """Neredeyse özdeş soruları eler (Jaccard >= threshold)."""
    unique: list[str] = []
    for q in questions:
        q_strip = q.strip()
        if not q_strip:
            continue
        is_dup = False
        for kept in unique:
            if jaccard_similarity(q_strip, kept) >= threshold:
                is_dup = True
                break
        if not is_dup:
            unique.append(q_strip)
    return unique


def has_repetition_loop(text: str) -> bool:
    """Metinde ardışık n-gram veya cümle döngüsel tekrarı (degeneration) var mı?"""
    if not text:
        return False
    words = _WORD_RE.findall(text.lower())
    if len(words) < 9:
        return False

    # 3'lü, 4'lü ve 5'li n-gram ardışık tekrar kontrolü (3 kez peş peşe). Yalnız rakamlardan
    # oluşan öbekler sayılmaz: "Dizi 0 0 0 0 0 0 0 0 0 ile başlarsa?" meşru bir girdi örneği.
    for n in (3, 4, 5):
        for i in range(len(words) - 3 * n + 1):
            gram1 = words[i : i + n]
            gram2 = words[i + n : i + 2 * n]
            gram3 = words[i + 2 * n : i + 3 * n]
            if gram1 == gram2 == gram3 and not all(w.isdigit() for w in gram1):
                return True
    return False


def extract_code_identifiers(code: str) -> set[str]:
    """Koddaki tanımlayıcıları (değişken, fonksiyon, tür adları) çıkarır."""
    words = {w.lower() for w in _WORD_RE.findall(code) if len(w) >= 3}
    return words - _COMMON_KEYWORDS


def touches_code(
    text: str,
    identifiers: set[str],
) -> bool:
    """Metin koddaki bir tanımlayıcıya veya satır numarasına temas ediyor mu?"""
    if _LINE_REF_RE.search(text):
        return True
    tokens = _tokenize(text)
    return bool(tokens & identifiers)


@dataclass
class SocraticGateResult:
    passed: bool
    filtered_questions: list[str]
    next_step_hint: str | None
    warnings: list[str] = field(default_factory=list)
    reason: str | None = None


def evaluate_socratic_gate(
    questions: list[str],
    next_step_hint: str | None,
    code: str,
    hint_level: int = 1,
    model_profile: str = "standard",
) -> SocraticGateResult:
    """Sokratik çıktıyı kalite kapısından geçirir.

    1. Sorulardaki veya ipucundaki döngüsel tekrarları (repetition loop) yakalar.
    2. Neredeyse özdeş soruları eler.
    3. hint_level >= 2 veya 'small' model profilinde koda temas aranır.
    """
    warnings: list[str] = []

    # 1. Döngüsel dejenerasyon denetimi
    for q in questions:
        if has_repetition_loop(q):
            return SocraticGateResult(
                passed=False,
                filtered_questions=[],
                next_step_hint=None,
                warnings=["Sokratik soruda döngüsel tekrar (degeneration) tespit edildi."],
                reason="repetition_loop",
            )
    if next_step_hint and has_repetition_loop(next_step_hint):
        return SocraticGateResult(
            passed=False,
            filtered_questions=[],
            next_step_hint=None,
            warnings=["İpucu metninde döngüsel tekrar (degeneration) tespit edildi."],
            reason="repetition_loop",
        )

    # 2. Kopya soruları ele
    deduped = deduplicate_questions(questions)
    if len(deduped) < len(questions):
        dropped_count = len(questions) - len(deduped)
        warnings.append(f"{dropped_count} adet birbirini tekrarlayan Sokratik soru elendi.")

    if not deduped:
        return SocraticGateResult(
            passed=False,
            filtered_questions=[],
            next_step_hint=next_step_hint,
            warnings=[*warnings, "Sokratik soru kalmadı."],
            reason="no_questions_left",
        )

    # 3. Koda temas denetimi (hint_level >= 2 veya small profilde)
    identifiers = extract_code_identifiers(code)
    requires_code_touch = (hint_level >= 2) or (model_profile == "small")

    if requires_code_touch and identifiers:
        all_text = " ".join([*deduped, next_step_hint or ""])
        if not touches_code(all_text, identifiers):
            warnings.append("Sokratik sorular koddaki hiçbir öğeye veya satıra temas etmiyor.")
            if model_profile == "small":
                # Küçük profilde koda hiç temas etmeyen sorular reddedilir
                return SocraticGateResult(
                    passed=False,
                    filtered_questions=[],
                    next_step_hint=next_step_hint,
                    warnings=warnings,
                    reason="no_code_reference",
                )

    return SocraticGateResult(
        passed=True,
        filtered_questions=deduped,
        next_step_hint=next_step_hint,
        warnings=warnings,
        reason=None,
    )
