"""tree-sitter sorgu dosyaları (`{dil}/{ad}.scm`) ve önbellekli yükleyici.

Sorgular Python'a gömülmez (Faz 5 görev metni); yalnızca bu dizindeki `.scm`
dosyalarından okunur. Bir dilde karşılığı olmayan sorgu (ör. C'de `fields`) boş döner.
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

from tree_sitter import Node, Query, QueryCursor

from codementor.analysis.parsers import get_language
from codementor.models.enums import Language

QUERY_DIR = Path(__file__).resolve().parent
QUERY_NAMES = ("functions", "loops", "calls", "memory", "fields")
_DIRS = {Language.C: "c", Language.CPP: "cpp", Language.CSHARP: "csharp", Language.PYTHON: "python"}


@cache
def load_query(language: Language, name: str) -> Query | None:
    """`{dil}/{ad}.scm` derlenmiş sorgusu; dosya yoksa None."""
    folder = _DIRS.get(language)  # HTML/CSS: olgu sorgusu yok (ADR-0015)
    path = QUERY_DIR / folder / f"{name}.scm" if folder else None
    if path is None or not path.is_file():
        return None
    return Query(get_language(language), path.read_text(encoding="utf-8"))


def captures(language: Language, name: str, root: Node) -> dict[str, list[Node]]:
    """Sorguyu çalıştırır; yakalama adı → düğümler (kaynak sırasına göre)."""
    query = load_query(language, name)
    if query is None:
        return {}
    found = QueryCursor(query).captures(root)
    return {capture: sorted(nodes, key=_source_order) for capture, nodes in found.items()}


def _source_order(node: Node) -> tuple[int, int, str]:
    """Kaynak sırası; başlangıcı aynı iç içe düğümlerde (`f()->g()`) dıştaki önce."""
    return (node.start_byte, -node.end_byte, node.type)
