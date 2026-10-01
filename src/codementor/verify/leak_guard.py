"""Çözüm sızıntısı koruması (mimari §5.6, son satır).

Üç bağımsız kontrol, Sokratik soruların her birine ve `next_step_hint`'e uygulanır:
1. Kod bloğu / kod benzeri satır (öğrencinin kendi kodundan birebir alıntı serbest).
2. Referans çözümle token n-gram örtüşmesi ≥ eşik (öğrenci kodunda da geçen n-gram'lar sayılmaz).
3. Yasaklı tanımlayıcı: referans çözümde geçip öğrenci kodunda, soru metninde ve genel adlar
   listesinde (`data/leak_common_identifiers.yaml`) olmayan ad.
Karar: ihlal varsa 1 kez yeniden üret; yine varsa sorunlu soruyu/ipucunu at.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from codementor.config import VerifySettings, get_settings
from codementor.models.enums import Engine, Language
from codementor.models.llm_output import MAX_QUESTION_CHARS
from codementor.models.verification import (
    CommonIdentifiers,
    LeakCheck,
    LeakDecision,
    LeakField,
    LeakKind,
    LeakViolation,
)
from codementor.questions._loader import DataFileError, load_model


class CommonIdentifiersError(DataFileError):
    """Genel adlar dosyası okunamadı ya da geçersiz."""


FENCE = "```"
MAX_TEXT_CHARS = MAX_QUESTION_CHARS  # soru/ipucu başına; üstü ihlal (şema da sınırlar, Faz 27)
Hit = tuple[LeakKind, str]  # (ihlal türü, ayrıntı)
_WHITESPACE = re.compile(r"\s+")
_ELLIPSIS = re.compile(r"\.\.\.|…")
_MIN_QUOTE_PART = 3
# Kod deyimleri. Türkçe düzyazıdaki `;` tek başına kod değildir: her desen kod sözdizimi ister.
_CODE_PATTERNS = [
    # çağrı deyimi: `list.Add(x);`, `GetComponent<T>();`
    re.compile(r"\b[A-Za-z_][\w.]*(?:<[^<>\n]*>)?\s*\([^()\n]*\)\s*;"),
    # denetim yapısı başlığı + blok: `for (int i = 0; i < n; i++) {`
    re.compile(r"\b(?:for|foreach|while|if|switch)\s*\([^)\n]*\)\s*\{"),
    # bildirim: `int x = 0`, `var seen = ...`, `HashSet<int> s;`
    re.compile(
        r"\b(?:int|var|float|double|bool|string|auto|void|char|long|size_t|const)\s+\**"
        r"[A-Za-z_]\w*\s*(?:=|;|\[)"
    ),
    re.compile(r"\b[A-Z]\w*<[\w\s,*<>]+>\s+[A-Za-z_]\w*\s*[=;]"),
    # C/C++ işaretçi bildirimi: `Node *next = ...`, `char* buf;`
    re.compile(r"\b[A-Za-z_]\w*\s*\*+\s*[A-Za-z_]\w*\s*(?:=[^=;\n][^;\n]*)?;"),
    # fonksiyon tanımı: `void Foo(int x) {`
    re.compile(r"\b[A-Za-z_]\w*\s+[A-Za-z_]\w*\s*\([^)\n]*\)\s*\{"),
    # süslü ayraçlı blok içinde deyim
    re.compile(r"\{[^{}\n]*;[^{}\n]*\}"),
]
# atama deyimi: `x = f(y);`, `total += a[i];` — sağ taraf ayrıca `_code_like_rhs` ile süzülür
_ASSIGNMENT = re.compile(r"[A-Za-z_][\w.\[\]<>]*\s*[+\-*/%|&^]?=\s*([^=\s][^;\n]*);")
_CODE_PUNCTUATION = re.compile(r"[()\[\].+\-*/%<>\"'&|!?:]")
_NON_ASCII = re.compile(r"[^\x00-\x7f]")
_TOKEN = re.compile(r"[A-Za-z_]\w*|\d+|==|!=|<=|>=|&&|\|\||->|::|\+\+|--|[^\s\w]")
_WORD = re.compile(r"\w+")
_ASCII_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_COMMENTS_STRINGS = re.compile(
    r"//[^\n]*|/\*.*?\*/|@?\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'", re.DOTALL
)


@lru_cache(maxsize=4)
def load_common_identifiers(path: Path) -> CommonIdentifiers:
    """`data/leak_common_identifiers.yaml` (önbellekli)."""
    return load_model(path, CommonIdentifiers, CommonIdentifiersError)


def common_names(common: CommonIdentifiers, language: Language, engine: Engine) -> frozenset[str]:
    """Dil + motor için sızıntı sayılmayan adlar."""
    names = set(common.common) | set(getattr(common, language.value, []))
    if engine in (Engine.UNITY, Engine.UNREAL):
        names |= set(getattr(common, engine.value))
    return frozenset(names)


def _squash(text: str) -> str:
    return _WHITESPACE.sub("", text)


def strip_comments_and_strings(code: str) -> str:
    """Referans çözümdeki yorum ve metin sabitleri tanımlayıcı sayılmaz (Türkçe sözcükler)."""
    return _COMMENTS_STRINGS.sub(" ", code)


def identifiers(text: str) -> set[str]:
    """Metindeki tanımlayıcılar; Türkçe sözcüğün parçası (`Listeyi` içindeki `List`) sayılmaz."""
    return {w for w in _WORD.findall(text) if _ASCII_IDENTIFIER.fullmatch(w)}


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    """Ardışık `n`'li token grupları."""
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def tokens(text: str) -> list[str]:
    """Kod tokenları (tanımlayıcı, sayı, çok karakterli işleç, tek simge)."""
    return _TOKEN.findall(text)


def _quoted_from_student(fragment: str, student_squashed: str) -> bool:
    parts = [_squash(p) for p in _ELLIPSIS.split(fragment)]
    parts = [p.rstrip(";") for p in parts if len(_squash(p)) >= _MIN_QUOTE_PART]
    return bool(parts) and all(p in student_squashed for p in parts)


def _code_like_rhs(rhs: str) -> bool:
    """`n olduğunda ne olur` düzyazı; `new List<int>()`, `0`, `a + b` kod."""
    rhs = rhs.strip()
    if _NON_ASCII.search(rhs):
        return False
    return len(rhs.split()) == 1 or bool(_CODE_PUNCTUATION.search(rhs))


def code_violations(text: str, student_code: str) -> list[Hit]:
    """(tür, ayrıntı) listesi: kod bloğu ya da öğrenci kodunda olmayan kod benzeri parça."""
    if FENCE in text:
        return [("code_block", "``` kod bloğu")]
    student = _squash(student_code)
    fragments = [m.group(0) for p in _CODE_PATTERNS for m in p.finditer(text)]
    fragments += [m.group(0) for m in _ASSIGNMENT.finditer(text) if _code_like_rhs(m.group(1))]
    found: list[Hit] = [
        ("code_line", fragment.strip()[:80])
        for fragment in fragments
        if not _quoted_from_student(fragment, student)
    ]
    return found[:1]  # aynı metin için bir kod ihlali yeterli


class _Reference:
    """Referans çözümden türetilen, sorudan bağımsız veriler (bir kez hesaplanır)."""

    def __init__(
        self,
        reference: str,
        student_code: str,
        question_text: str,
        allowed: frozenset[str],
        settings: VerifySettings,
    ) -> None:
        clean = strip_comments_and_strings(reference)
        student_clean = strip_comments_and_strings(student_code)
        n = settings.leak_ngram_n
        self.n = n
        self.threshold = settings.leak_ngram_threshold
        self.grams = ngrams(tokens(clean), n) - ngrams(tokens(student_clean), n)
        self.forbidden = {
            name
            for name in identifiers(clean)
            - identifiers(student_code)
            - identifiers(question_text)
            - allowed
            if len(name) >= settings.leak_min_identifier_length
        }

    def violations(self, text: str) -> list[Hit]:
        found: list[Hit] = []
        grams = ngrams(tokens(text), self.n)
        if grams:
            leaked = grams & self.grams
            ratio = len(leaked) / len(grams)
            if ratio >= self.threshold:
                sample = " ".join(sorted(leaked)[0])
                found.append(("ngram_overlap", f"%{ratio * 100:.0f} örtüşme, ör. {sample!r}"))
        names = sorted(identifiers(text) & self.forbidden)
        if names:
            found.append(("forbidden_identifier", ", ".join(names[:5])))
        return found


def check_leaks(
    guiding_questions: list[str],
    next_step_hint: str | None,
    *,
    student_code: str,
    language: Language,
    engine: Engine,
    reference: str | None = None,
    question_text: str = "",
    settings: VerifySettings | None = None,
    common: CommonIdentifiers | None = None,
) -> LeakCheck:
    """Soruları ve ipucunu üç kontrolden geçirir. Referans yoksa yalnızca kod kontrolü yapılır.

    `question_text`: sorunun başlık/metin/kısıtları (orada geçen adlar yasaklı değildir).
    """
    settings = settings or get_settings().verify
    ref: _Reference | None = None
    if reference and reference.strip():
        common = common or load_common_identifiers(settings.common_identifiers_file)
        allowed = common_names(common, language, engine)
        ref = _Reference(reference, student_code, question_text, allowed, settings)

    targets: list[tuple[LeakField, int | None, str]] = [
        ("guiding_questions", i, q) for i, q in enumerate(guiding_questions)
    ]
    if next_step_hint:
        targets.append(("next_step_hint", None, next_step_hint))
    violations: list[LeakViolation] = []
    for field, index, text in targets:
        if len(text) > MAX_TEXT_CHARS:
            # Mentor sorusu kısa olmalı; uzun metin hem şüpheli hem de regex'ler için pahalı (§12)
            violations.append(
                LeakViolation(
                    field=field, index=index, kind="too_long", detail=f"{len(text)} karakter"
                )
            )
            continue
        found = code_violations(text, student_code)
        if ref is not None:
            found += ref.violations(text)
        violations += [
            LeakViolation(field=field, index=index, kind=kind, detail=detail)
            for kind, detail in found
        ]
    return LeakCheck(violations=violations, reference_checked=ref is not None)


def decide_leak_action(
    guiding_questions: list[str],
    next_step_hint: str | None,
    check: LeakCheck,
    *,
    regenerated: bool,
) -> LeakDecision:
    """Temizse `passed`; ilk seferde ihlal varsa `regenerate`; yeniden üretimde de varsa
    sorunlu sorular ve ipucu atılır (`dropped_questions`)."""
    if check.clean:
        return LeakDecision(
            action="passed", guiding_questions=guiding_questions, next_step_hint=next_step_hint
        )
    if not regenerated:
        return LeakDecision(action="regenerate", violations=check.violations)
    bad = {v.index for v in check.violations if v.field == "guiding_questions"}
    hint_bad = any(v.field == "next_step_hint" for v in check.violations)
    return LeakDecision(
        action="dropped_questions",
        guiding_questions=[q for i, q in enumerate(guiding_questions) if i not in bad],
        next_step_hint=None if hint_bad else next_step_hint,
        violations=check.violations,
    )
