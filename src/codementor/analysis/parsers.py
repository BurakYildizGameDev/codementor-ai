"""tree-sitter ayrıştırıcıları ve ayrıştırma öncesi ön işlem (mimari §5.2.1, §5.3).

- Diller modül düzeyinde bir kez yüklenir; `Parser` nesneleri iş parçacığı güvenli
  olmadığından iş parçacığı başına önbelleklenir.
- Unreal makroları (`UCLASS(...)`, `GENERATED_BODY()`, `*_API` ...) tree-sitter-cpp'de
  sahte ERROR düğümleri üretir. Ayrıştırmadan önce **aynı uzunlukta boşlukla**
  değiştirilir; satır sonları korunduğu için satır ve karakter kolonları kaymaz.
"""

from __future__ import annotations

import re
import threading
from bisect import bisect_right
from collections.abc import Callable, Iterator
from dataclasses import dataclass

import tree_sitter_c
import tree_sitter_c_sharp
import tree_sitter_cpp
from tree_sitter import Language as TSLanguage
from tree_sitter import Node, Parser, Tree

from codementor.analysis.lexical import mask_non_code, matching_parens
from codementor.models.enums import Engine, Language
from codementor.models.request import NormalizedCode

_LANGUAGES: dict[Language, TSLanguage] = {
    Language.C: TSLanguage(tree_sitter_c.language()),
    Language.CPP: TSLanguage(tree_sitter_cpp.language()),
    Language.CSHARP: TSLanguage(tree_sitter_c_sharp.language()),
}

_local = threading.local()

UNREAL_MACROS = (
    "UCLASS",
    "USTRUCT",
    "UENUM",
    "UINTERFACE",
    "UPROPERTY",
    "UFUNCTION",
    "UPARAM",
    "UMETA",
    "UDELEGATE",
    "GENERATED_BODY",
    "GENERATED_UCLASS_BODY",
    "GENERATED_USTRUCT_BODY",
    "GENERATED_UINTERFACE_BODY",
    "GENERATED_IINTERFACE_BODY",
)
_MACRO_CALL = re.compile(r"\b(?:" + "|".join(UNREAL_MACROS) + r")\s*\(")
_API_MACRO = re.compile(r"\b[A-Z][A-Z0-9_]*_API\b")


@dataclass(frozen=True, slots=True)
class ParsedSource:
    """Ayrıştırma ağacı ve ağacın üretildiği (gerekirse nötrleştirilmiş) metin."""

    tree: Tree
    text: str


def get_language(language: Language) -> TSLanguage:
    """Dilin tree-sitter dilbilgisi (sorgu derlemek için)."""
    return _LANGUAGES[language]


def get_parser(language: Language) -> Parser:
    """Bu iş parçacığına ait, önbelleklenmiş `Parser`."""
    cache: dict[Language, Parser] | None = getattr(_local, "parsers", None)
    if cache is None:
        cache = {}
        _local.parsers = cache
    parser = cache.get(language)
    if parser is None:
        parser = cache[language] = Parser(_LANGUAGES[language])
    return parser


def _blank(text: str) -> str:
    return "".join("\n" if c == "\n" else " " for c in text)


def neutralize_unreal_macros(text: str) -> str:
    """Unreal yansıma makrolarını aynı uzunlukta boşlukla değiştirir.

    Makrolar yorum/metin dışında aranır ve parantezleri yorum/metin içeriği yok
    sayılarak tek geçişte eşlenir (doğrusal süre; mimari §12). Kapanmayan makro
    çağrısı olduğu gibi bırakılır; hatayı tree-sitter raporlar.
    """
    masked = mask_non_code(text)
    closing = matching_parens(masked)
    spans: list[tuple[int, int]] = []
    cursor = 0
    for match in _MACRO_CALL.finditer(masked):
        close = closing.get(match.end() - 1)
        if match.start() < cursor or close is None:
            continue
        spans.append((match.start(), close + 1))
        cursor = close + 1
    starts = [s for s, _ in spans]  # makro aralıkları sıralı ve çakışmasız

    def _inside_macro(pos: int) -> bool:
        k = bisect_right(starts, pos) - 1
        return k >= 0 and pos < spans[k][1]

    spans += [m.span() for m in _API_MACRO.finditer(masked) if not _inside_macro(m.start())]
    if not spans:
        return text
    parts: list[str] = []
    cursor = 0
    for start, end in sorted(spans):
        parts += [text[cursor:start], _blank(text[start:end])]
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts)


def iter_nodes(root: Node, descend: Callable[[Node], bool] = lambda _: True) -> Iterator[Node]:
    """Ağacı belge sırasıyla (ön-sıra) `TreeCursor` ile gezer.

    `descend(node)` False dönerse o düğümün altına inilmez. `Node.children` ile
    gezinti, tree-sitter 0.26 Python bağlamasında ERROR içeren büyük ağaçlarda
    erişim ihlaliyle çöküyor (Windows'ta yeniden üretildi); bu yüzden tüm ağaç
    gezintileri bu yardımcıyla yapılmalı.
    """
    cursor = root.walk()
    while True:
        node = cursor.node
        if node is None:  # pragma: no cover - kök düğümde cursor her zaman düğüm verir
            return
        yield node
        if descend(node) and cursor.goto_first_child():
            continue
        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                return


def parse_source(text: str, language: Language, engine: Engine) -> ParsedSource:
    """Metni ayrıştırır; Unreal kodunda makroları önce nötrleştirir."""
    source = neutralize_unreal_macros(text) if engine is Engine.UNREAL else text
    return ParsedSource(tree=get_parser(language).parse(source.encode("utf-8")), text=source)


def parse(code: NormalizedCode) -> ParsedSource:
    """Normalize edilmiş kodu ayrıştırır."""
    return parse_source(code.text, code.language, code.engine)
