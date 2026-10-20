"""`test_engine.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import AuditCategory, Engine, Language, Severity
from codementor.models.findings import Finding
from codementor.models.request import LanguageHint
from codementor.models.rules import RuleRunResult
from codementor.rules import run_rules
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule, unregister_rule

_LANG = {".c": Language.C, ".cpp": Language.CPP, ".h": Language.CPP, ".cs": Language.CSHARP}


def run_text(
    text: str, language: Language, engine: Engine = Engine.NONE, **kwargs: list[str]
) -> RuleRunResult:
    code = normalize(text, LanguageHint(language=language, engine=engine))
    return run_rules(code, extract_facts(code), **kwargs)


def run(path: Path, engine: Engine, **kwargs: list[str]) -> RuleRunResult:
    return run_text(path.read_text(encoding="utf-8"), _LANG[path.suffix], engine, **kwargs)


class _Probe(Rule):
    title = "t"
    description = "d"
    languages = frozenset({Language.C})
    category = AuditCategory.DESIGN
    default_severity = Severity.LOW


@pytest.fixture
def probes() -> Iterator[None]:
    @register_rule
    class Crash(_Probe):
        id = "TEST-CRASH-001"

        def check(self, ctx: RuleContext) -> list[Finding]:
            raise RuntimeError("bozuk kural")

    @register_rule
    class Twice(_Probe):
        id = "TEST-TWICE-001"

        def check(self, ctx: RuleContext) -> list[Finding]:
            return [self.finding(ctx, 3), self.finding(ctx, 3), self.finding(ctx, 1)]

    yield
    unregister_rule("TEST-CRASH-001")
    unregister_rule("TEST-TWICE-001")


C_TEXT = """#include <stdio.h>
int main(void) {
    char a[8];
    gets(a);
    return 0;
}
"""


def _timed(text: str, language: Language, engine: Engine) -> float:
    start = time.perf_counter()
    run_text(text, language, engine)
    return time.perf_counter() - start


# --- Faz 31: bulgu üst sınırı ----------------------------------------------------------------


@pytest.fixture
def flood() -> Iterator[None]:
    """Satır başına bir bulgu üreten kural; 3. satırınki yüksek önemli."""

    @register_rule
    class Flood(_Probe):
        id = "TEST-FLOOD-001"

        def check(self, ctx: RuleContext) -> list[Finding]:
            found = [self.finding(ctx, line) for line in range(1, len(ctx.lines) + 1)]
            return [
                f.model_copy(update={"severity": Severity.HIGH}) if f.line_start == 3 else f
                for f in found
            ]

    yield
    unregister_rule("TEST-FLOOD-001")


FLOOD_TEXT = "".join(f"int v{i} = {i};\n" for i in range(40))
