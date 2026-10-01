"""Python, HTML ve CSS uçtan uca (ADR-0015): FakeProvider, ağsız, Tier 1 kapalı ayarlarla."""

from __future__ import annotations

from typing import Any

import pytest

from codementor.config import Settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import CompilationStatus, Engine, FindingSource, Language
from codementor.models.llm_output import LLMAnalysisOutput, LLMMarkupAnalysisOutput
from codementor.models.request import AnalysisRequest, LanguageHint
from codementor.storage.db import Database
from codementor.validation.python_check import check_python
from tests.integration.conftest import FakeFactory, orchestrator, socratic_reply

pytestmark = pytest.mark.anyio

PYTHON = """def has_duplicate(items):
    seen = []
    for item in items:
        if item in seen:
            return True
        seen.append(item)
    return False
"""
HTML = """<!DOCTYPE html>
<html>
<body>
  <img src="profil.png">
  <form>
    <input type="email" name="email">
  </form>
</body>
</html>
"""
CSS = """.kart {
  padding: 16px;
  padding: 24px;
}
.bos {}
"""


def python_reply() -> dict[str, Any]:
    return {
        "complexity": {
            "reasoning_steps": ["Dış döngü n kez döner, `in` listede n eleman tarar."],
            "time_complexity": "O(n^2)",
            "space_complexity": "O(n)",
            "optimal_time_target": "O(n)",
            "agreement": "agrees",
        },
        "additional_findings": [],
    }


def markup_reply(line: int, evidence: str) -> dict[str, Any]:
    return {
        "additional_findings": [
            {
                "category": "design",
                "severity": "medium",
                "line_start": line,
                "line_end": None,
                "evidence": evidence,
                "description": "Sayfanın ana içeriği hangi anlamsal bölgede duruyor?",
            }
        ]
    }


def request(code: str, language: Language) -> AnalysisRequest:
    return AnalysisRequest(code=code, language=language, engine="none")  # type: ignore[arg-type]


async def test_python_full_pipeline_with_complexity(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(python_reply(), socratic_reply("Bir öğeyi gördüğünü nasıl hatırlıyorsun?"))
    report = await orchestrator(settings, db, provider).analyze(request(PYTHON, Language.PYTHON))
    assert report.language is Language.PYTHON
    assert report.complexity is not None
    assert report.complexity.time_complexity == "n^2"
    assert report.complexity.static_hint == "n^2"
    assert report.complexity.agreement == "agrees"
    assert {f.rule_id for f in report.findings} == {"PY-PERF-001"}
    assert report.socratic is not None
    assert provider.calls[0].output_model is LLMAnalysisOutput


async def test_html_uses_markup_schema_and_has_no_complexity(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(markup_reply(3, "<body>"), socratic_reply("Bu formu kim, nasıl gönderir?"))
    report = await orchestrator(settings, db, provider).analyze(request(HTML, Language.HTML))
    assert report.complexity is None
    assert report.compilation.status is CompilationStatus.SKIPPED
    assert not any("derleyici" in w.lower() for w in report.meta.warnings)
    rules = {f.rule_id for f in report.findings if f.rule_id}
    assert rules == {"HTML-ACC-001", "HTML-ACC-002", "HTML-ACC-003"}
    assert any(f.source is FindingSource.LLM and f.line_start == 3 for f in report.findings)
    assert provider.calls[0].output_model is LLMMarkupAnalysisOutput
    system = provider.calls[0].messages[0].content
    assert "HTML ve CSS" in system
    assert "karmaşıklık" not in provider.calls[0].messages[1].content.split("## Görev")[0].lower()
    assert report.socratic is not None
    assert not report.meta.degraded


async def test_css_static_rules_and_markup_pass(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake({"additional_findings": []}, socratic_reply("Hangi padding değeri geçerli?"))
    report = await orchestrator(settings, db, provider).analyze(request(CSS, Language.CSS))
    assert report.complexity is None
    assert {f.rule_id for f in report.findings} == {"CSS-STD-001", "CSS-MAINT-002"}
    assert provider.calls[0].output_model is LLMMarkupAnalysisOutput


async def test_markup_degrades_without_complexity(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    from codementor.providers.fake import FakeReply

    provider = fake(FakeReply(error="500"), FakeReply(error="500"))
    report = await orchestrator(settings, db, provider).analyze(request(CSS, Language.CSS))
    assert report.meta.degraded
    assert report.complexity is None
    assert report.socratic is not None  # şablon sorular


async def test_python_syntax_error_exits_early_without_llm(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    tier1_on = settings.model_copy(
        update={"validation": settings.validation.model_copy(update={"tier1_enabled": True})}
    )
    provider = fake()
    code = "def f(xs):\n    for x in xs:\n    print(x)\n"  # girinti hatası: tree-sitter kaçırır
    report = await orchestrator(tier1_on, db, provider).analyze(request(code, Language.PYTHON))
    assert report.meta.early_exit
    assert report.compilation.status is CompilationStatus.FAILED
    assert any(d.tool == "python" for d in report.compilation.diagnostics)
    assert provider.calls == []


def _code(text: str) -> Any:
    return normalize(text, LanguageHint(language=Language.PYTHON, engine=Engine.NONE))


def test_python_check_reports_errors_and_warnings_without_running_code() -> None:
    assert check_python(_code("x = 1\n")).status is CompilationStatus.PASSED
    failed = check_python(_code("def f(:\n    pass\n"))
    assert failed.status is CompilationStatus.FAILED
    assert failed.diagnostics[0].line == 1
    warned = check_python(_code('path = "C:\\d"\n'))
    assert warned.status is CompilationStatus.WARNING
    assert "SyntaxWarning" in warned.diagnostics[0].message
    # çalıştırılsaydı dosya oluştururdu; yalnızca ayrıştırılır (ADR-0005)
    effect = check_python(_code("open('BU_DOSYA_OLUSMAMALI.txt', 'w').write('x')\n"))
    assert effect.status is CompilationStatus.PASSED
    from pathlib import Path

    assert not Path("BU_DOSYA_OLUSMAMALI.txt").exists()
