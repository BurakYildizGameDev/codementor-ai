"""Editör için hafif sözdizimi renklendirme: metni (etiket, başlangıç, bitiş) aralıklarına böler.

Tam bir ayrıştırıcı değildir (tree-sitter analiz içindir); amaç okunabilirlik. Yorum ve
dizgiler önce eşleşir, böylece içlerindeki anahtar sözcükler renklenmez.
"""

from __future__ import annotations

import re
from typing import Literal

from codementor.models.enums import Language

Token = Literal["comment", "string", "preproc", "keyword", "type", "number", "function"]
Span = tuple[Token, int, int]

_C_KEYWORDS = (
    "if else for while do switch case default break continue return goto sizeof typedef "
    "struct union enum static const volatile extern register inline restrict"
)
_C_TYPES = (
    "void char short int long float double signed unsigned bool size_t uint8_t uint16_t "
    "uint32_t uint64_t int8_t int16_t int32_t int64_t FILE NULL true false"
)
_CPP_KEYWORDS = (
    " class public private protected virtual override final new delete this namespace using "
    "template typename try catch throw const_cast static_cast dynamic_cast reinterpret_cast "
    "constexpr noexcept nullptr operator friend explicit mutable auto decltype"
)
_CPP_TYPES = " std string vector map unordered_map set unique_ptr shared_ptr TArray FString UObject"
_CS_KEYWORDS = (
    "if else for foreach while do switch case default break continue return goto new class "
    "struct interface enum public private protected internal static readonly const virtual "
    "override abstract sealed async await using namespace try catch finally throw this base "
    "in out ref is as var null true false get set yield lock typeof"
)
_CS_TYPES = (
    "void bool byte char decimal double float int long object sbyte short string uint ulong "
    "ushort List Dictionary HashSet IEnumerable MonoBehaviour GameObject Vector3 Transform"
)

_WORDS: dict[Language, tuple[str, str]] = {
    Language.C: (_C_KEYWORDS, _C_TYPES),
    Language.CPP: (_C_KEYWORDS + _CPP_KEYWORDS, _C_TYPES + _CPP_TYPES),
    Language.CSHARP: (_CS_KEYWORDS, _CS_TYPES),
}


def _pattern(language: Language) -> re.Pattern[str]:
    keywords, types = _WORDS[language]
    preproc = (
        r"^[ \t]*#[^\n]*"
        if language is not Language.CSHARP
        else r"^[ \t]*#(?:region|endregion|if|endif|define)[^\n]*"
    )
    return re.compile(
        "|".join(
            (
                r"(?P<comment>//[^\n]*|/\*.*?(?:\*/|\Z))",
                r"(?P<string>@?\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?)",
                rf"(?P<preproc>{preproc})",
                rf"(?P<keyword>\b(?:{'|'.join(sorted(set(keywords.split())))})\b)",
                rf"(?P<type>\b(?:{'|'.join(sorted(set(types.split())))})\b)",
                r"(?P<number>\b(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d+)?)[uUlLfF]*\b)",
                r"(?P<function>\b[A-Za-z_]\w*(?=\s*\())",
            )
        ),
        re.MULTILINE | re.DOTALL,
    )


_PATTERNS: dict[Language, re.Pattern[str]] = {lang: _pattern(lang) for lang in Language}


def tokenize(code: str, language: Language) -> list[Span]:
    """Örtüşmeyen, sıralı renk aralıkları (karakter ofsetleri, bitiş hariç)."""
    spans: list[Span] = []
    for match in _PATTERNS[language].finditer(code):
        kind = match.lastgroup
        if kind is not None and match.end() > match.start():
            spans.append((kind, match.start(), match.end()))  # type: ignore[arg-type]
    return spans
