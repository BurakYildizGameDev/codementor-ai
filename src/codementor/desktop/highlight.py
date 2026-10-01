"""Editör için hafif sözdizimi renklendirme: metni (etiket, başlangıç, bitiş) aralıklarına böler.

Tam bir ayrıştırıcı değildir (tree-sitter analiz içindir); amaç okunabilirlik. Yorum ve
dizgiler önce eşleşir, böylece içlerindeki anahtar sözcükler renklenmez. HTML ve CSS'te
etiketler tema renklerine eşlenir: HTML etiket adı → keyword, öznitelik → type; CSS seçici →
function, özellik → type, @kural → preproc, `!important` → keyword.
"""

from __future__ import annotations

import re
from typing import Literal, cast

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
_PY_KEYWORDS = (
    "if elif else for while break continue return def class import from as with try except "
    "finally raise pass lambda yield global nonlocal assert del in is not and or async await "
    "match case"
)
_PY_TYPES = (
    "None True False int float str bool list dict set tuple bytes object range len print self "
    "enumerate zip map filter sorted sum min max any all open isinstance super"
)

_WORDS: dict[Language, tuple[str, str]] = {
    Language.C: (_C_KEYWORDS, _C_TYPES),
    Language.CPP: (_C_KEYWORDS + _CPP_KEYWORDS, _C_TYPES + _CPP_TYPES),
    Language.CSHARP: (_CS_KEYWORDS, _CS_TYPES),
}


def _words(words: str) -> str:
    return "|".join(sorted(set(words.split())))


def _c_family(language: Language) -> list[str]:
    keywords, types = _WORDS[language]
    preproc = (
        r"^[ \t]*#[^\n]*"
        if language is not Language.CSHARP
        else r"^[ \t]*#(?:region|endregion|if|endif|define)[^\n]*"
    )
    return [
        r"(?P<comment>//[^\n]*|/\*.*?(?:\*/|\Z))",
        r"(?P<string>@?\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?)",
        rf"(?P<preproc>{preproc})",
        rf"(?P<keyword>\b(?:{_words(keywords)})\b)",
        rf"(?P<type>\b(?:{_words(types)})\b)",
        r"(?P<number>\b(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d+)?)[uUlLfF]*\b)",
        r"(?P<function>\b[A-Za-z_]\w*(?=\s*\())",
    ]


_PYTHON = [
    r"(?P<string>[rRbBfFuU]{0,2}(?:\"\"\".*?(?:\"\"\"|\Z)|'''.*?(?:'''|\Z)"
    r"|\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?))",
    r"(?P<comment>#[^\n]*)",
    r"(?P<preproc>^[ \t]*@[\w.]+)",
    rf"(?P<keyword>\b(?:{_words(_PY_KEYWORDS)})\b)",
    rf"(?P<type>\b(?:{_words(_PY_TYPES)})\b)",
    r"(?P<number>\b(?:0[xXoObB][0-9a-fA-F_]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?)j?\b)",
    r"(?P<function>\b[A-Za-z_]\w*(?=\s*\())",
]
_HTML = [
    r"(?P<comment><!--.*?(?:-->|\Z))",
    r"(?P<preproc><!DOCTYPE[^>]*>)",
    r"(?P<keyword>(?<=</)[A-Za-z][\w-]*|(?<=<)[A-Za-z][\w-]*)",
    r"(?P<string>\"[^\"]*\"?|'[^']*'?)",
    r"(?P<type>\b[A-Za-z_:][\w:.-]*(?=\s*=))",
    r"(?P<number>&#?\w+;)",
]
_CSS = [
    r"(?P<comment>/\*.*?(?:\*/|\Z))",
    r"(?P<string>\"[^\"\n]*\"?|'[^'\n]*'?)",
    r"(?P<preproc>@[\w-]+)",
    r"(?P<keyword>!\s*important\b)",
    r"(?P<type>(?<![\w-])-{0,2}[A-Za-z][\w-]*(?=\s*:(?!:)[^{;]*(?:;|\}|$)))",
    r"(?P<number>#[0-9a-fA-F]{3,8}\b|(?<![\w-])-?\d+(?:\.\d+)?(?:px|rem|em|vh|vw|%|ms|s|deg|fr)?)",
    r"(?P<function>[.#]?[A-Za-z_][\w-]*(?=[^{};]*\{)|[\w-]+(?=\())",
]


def _pattern(language: Language) -> re.Pattern[str]:
    if language is Language.PYTHON:
        parts, flags = _PYTHON, re.MULTILINE | re.DOTALL
    elif language is Language.HTML:
        parts, flags = _HTML, re.DOTALL | re.IGNORECASE
    elif language is Language.CSS:
        parts, flags = _CSS, re.MULTILINE | re.DOTALL
    else:
        parts, flags = _c_family(language), re.MULTILINE | re.DOTALL
    return re.compile("|".join(parts), flags)


_PATTERNS: dict[Language, re.Pattern[str]] = {lang: _pattern(lang) for lang in Language}


def tokenize(code: str, language: Language) -> list[Span]:
    """Örtüşmeyen, sıralı renk aralıkları (karakter ofsetleri, bitiş hariç)."""
    spans: list[Span] = []
    for match in _PATTERNS[language].finditer(code):
        kind = match.lastgroup
        if kind is not None and match.end() > match.start():
            spans.append((cast(Token, kind), match.start(), match.end()))
    return spans
