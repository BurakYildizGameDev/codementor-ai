"""`test_extractor.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

from codementor.analysis._symbols import CallName, call_name
from codementor.analysis.extractor import (
    extract_facts,
)
from codementor.analysis.parsers import get_parser, iter_nodes
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.facts import CodeFacts
from codementor.models.request import LanguageHint

C, CPP, CS = Language.C, Language.CPP, Language.CSHARP


def _facts(text: str, language: Language, engine: Engine = Engine.NONE) -> CodeFacts:
    return extract_facts(normalize(text, LanguageHint(language=language, engine=engine)))


# ---------------------------------------------------------------- çağrı adı (Faz H3)


def _call_names(text: str, language: Language) -> list[CallName]:
    """Metindeki çağrıların adları (argüman metni dahil), belge sırasıyla."""
    root = get_parser(language).parse(text.encode("utf-8")).root_node
    calls = {"call_expression", "invocation_expression", "call"}
    return [call_name(node, language) for node in iter_nodes(root) if node.type in calls]
