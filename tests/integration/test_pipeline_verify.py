"""Faz 35: LLM bulguları için doğrulama geçişi (FakeProvider, ağsız)."""

from __future__ import annotations

from typing import Any

import pytest

from codementor.config import Settings
from codementor.models.enums import FindingSource, PipelineMode
from codementor.models.llm_output import LLMSocraticOutput, LLMVerifyOutput
from codementor.models.pipeline import StageEvent
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.providers.fake import FakeReply
from codementor.storage.db import Database
from tests.integration.conftest import (
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"
LLM_DESCRIPTION = "Serbest bırakılmış düğümün alanı okunuyor."
HTML = (
    '<!DOCTYPE html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
    "<title>Liste</title>\n</head>\n<body>\n<ul>\n<li>Bir</li>\n</ul>\n</body>\n</html>\n"
)


def _request(**kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate({"code": LINKED_LIST, "question_id": QUESTION, **kw})


def _enabled(settings: Settings, **extra: object) -> Settings:
    pipeline = settings.pipeline.model_copy(update={"verify_findings": True, **extra})
    return settings.model_copy(update={"pipeline": pipeline})


def _verdict(verdict: str = "proven", **kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {"finding": 1, "verdict": verdict, "reason": "Gerekçe."}
    if verdict == "proven":
        base |= {
            "input": "listede tek düğüm ve aranan değer o düğüm",
            "expected": "düğüm silinir, liste boş kalır",
            "actual": "serbest bırakılmış düğümün next alanı okunur",
        }
    return base | kw


def _verify(*verdicts: dict[str, Any]) -> dict[str, Any]:
    return {"verdicts": list(verdicts)}


def _llm_lines(findings: list[Any]) -> list[int]:
    return [f.line_start for f in findings if f.source is FindingSource.LLM]


def _text(call: Any) -> str:
    return "\n".join(m.content for m in call.messages)


async def test_disabled_makes_no_extra_call(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    events: list[StageEvent] = []
    provider = fake(analysis_reply(), socratic_reply())
    orch = orchestrator(settings, db, provider)
    orch.bus.subscribe(events.append)
    report = await orch.analyze(_request())
    assert len(provider.calls) == 2
    assert _llm_lines(report.findings) == [31]
    assert {e.stage for e in events if e.status == "skipped"} >= {"prompt_v", "llm_v", "verify_v"}
    assert report.meta.stage_latency_ms["llm_v"] == 0


async def test_drops_unproven_end_to_end(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_verdict("unproven")), socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(_request())
    assert len(provider.calls) == 3
    assert provider.calls[1].output_model is LLMVerifyOutput
    assert _llm_lines(report.findings) == []
    assert any("31. satır" in w and "atıldı" in w for w in report.meta.warnings)
    assert not report.meta.degraded


async def test_socratic_sees_only_kept_findings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    dropped = fake(analysis_reply(), _verify(_verdict("unproven")), socratic_reply())
    await orchestrator(_enabled(settings), None, dropped).analyze(_request())
    assert dropped.calls[2].output_model is LLMSocraticOutput
    assert LLM_DESCRIPTION not in _text(dropped.calls[2])

    kept = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    report = await orchestrator(_enabled(settings), None, kept).analyze(_request())
    assert LLM_DESCRIPTION in _text(kept.calls[2])
    assert _llm_lines(report.findings) == [31]


async def test_verify_prompt_wraps_user_code_and_lists_findings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    await orchestrator(_enabled(settings), None, provider).analyze(_request())
    prompt = _text(provider.calls[1])
    assert "<user_code>" in prompt
    assert "</user_code>" in prompt
    assert "Bulgu 1" in prompt
    assert "*head = cur->next;" in prompt
    assert LLM_DESCRIPTION in prompt


async def test_static_and_confirmed_not_sent(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Statik bulgular doğrulamaya girmez: yalnız LLM bulgusu (31. satır) listelenir."""
    provider = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    report = await orchestrator(_enabled(settings), None, provider).analyze(_request())
    static = [f for f in report.findings if f.source is not FindingSource.LLM]
    assert static  # bağlı liste kodunda statik bulgu var
    prompt = _text(provider.calls[1])
    assert "Bulgu 2" not in prompt
    for finding in static:
        assert finding.description not in prompt


async def test_skipped_without_llm_findings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    reply = analysis_reply()
    reply["additional_findings"] = []
    provider = fake(reply, socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(_request())
    assert len(provider.calls) == 2
    assert not report.meta.degraded


async def test_schema_failure_keeps_findings_and_warns(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), {"bozuk": 1}, {"bozuk": 2}, socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(_request())
    assert len(provider.calls) == 4  # 1 onarım (max_repair_attempts = 1)
    assert _llm_lines(report.findings) == [31]
    assert any("doğrulama" in w.lower() and "olduğu gibi" in w for w in report.meta.warnings)
    assert not report.meta.degraded


async def test_provider_error_keeps_findings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), FakeReply(error="timeout"), socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(_request())
    assert _llm_lines(report.findings) == [31]
    assert any("olduğu gibi" in w for w in report.meta.warnings)
    assert report.socratic is not None
    assert report.socratic.leak_check == "passed"  # Geçiş B yine çalıştı
    assert not report.meta.degraded


def _single() -> AnalysisRequest:
    return _request(options=AnalysisOptions(mode=PipelineMode.SINGLE_PASS))


async def test_single_pass_regenerates_socratic_when_dropped(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = {"analysis": analysis_reply(), "socratic": socratic_reply("İlk soru burada mı?")}
    second = socratic_reply("Ayrı geçişte üretilen soru hangisi?")
    provider = fake(first, _verify(_verdict("unproven")), second)
    report = await orchestrator(_enabled(settings), db, provider).analyze(_single())
    assert len(provider.calls) == 3
    assert provider.calls[2].output_model is LLMSocraticOutput
    assert report.socratic is not None
    assert report.socratic.guiding_questions == ["Ayrı geçişte üretilen soru hangisi?"]


async def test_single_pass_keeps_socratic_when_nothing_dropped(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = {"analysis": analysis_reply(), "socratic": socratic_reply("İlk soru burada mı?")}
    provider = fake(first, _verify(_verdict()))
    report = await orchestrator(_enabled(settings), db, provider).analyze(_single())
    assert len(provider.calls) == 2
    assert report.socratic is not None
    assert report.socratic.guiding_questions == ["İlk soru burada mı?"]


async def test_markup_verify(settings: Settings, db: Database, fake: FakeFactory) -> None:
    markup = {
        "additional_findings": [
            {
                "category": "design",
                "severity": "low",
                "line_start": 9,
                "line_end": None,
                "evidence": "<li>Bir</li>",
                "description": "Liste tek öğeli; anlamsal olarak liste gerekmiyor olabilir.",
            }
        ]
    }
    provider = fake(markup, _verify(_verdict("unproven")), socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(
        AnalysisRequest.model_validate({"code": HTML, "language": "html"})
    )
    assert provider.calls[1].output_model is LLMVerifyOutput
    assert _llm_lines(report.findings) == []


async def test_cache_not_shared_between_verify_settings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(_request())
    provider = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    report = await orchestrator(_enabled(settings), db, provider).analyze(_request())
    assert not report.meta.cache_hit
    assert len(provider.calls) == 3


# --- Faz 39 ----------------------------------------------------------------------------------


def _scaling_verdict() -> dict[str, Any]:
    return _verdict(input="n = 100000", expected="O(n)", actual="O(n^2)")


def _performance_reply() -> dict[str, Any]:
    reply = analysis_reply()
    reply["additional_findings"][0] |= {"category": "performance", "severity": "medium"}
    return reply


async def test_analyze_traced_returns_checks(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_verdict("unproven")), socratic_reply())
    trace = await orchestrator(_enabled(settings), None, provider).analyze_traced(_request())
    assert _llm_lines(trace.report.findings) == []
    assert [(c.line_start, c.category.value, c.kept, c.basis) for c in trace.finding_checks] == [
        (31, "memory_safety", False, "unproven")
    ]


async def test_analyze_traced_without_verify_has_no_checks(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), socratic_reply())
    trace = await orchestrator(settings, None, provider).analyze_traced(_request())
    assert trace.finding_checks == []


async def test_scaling_verdict_keeps_performance_finding(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(_performance_reply(), _verify(_scaling_verdict()), socratic_reply())
    trace = await orchestrator(_enabled(settings), None, provider).analyze_traced(_request())
    assert _llm_lines(trace.report.findings) == [31]
    assert trace.finding_checks[0].basis == "scaling"


async def test_scaling_verdict_drops_memory_finding(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_scaling_verdict()), socratic_reply())
    trace = await orchestrator(_enabled(settings), None, provider).analyze_traced(_request())
    assert _llm_lines(trace.report.findings) == []
    assert trace.finding_checks[0].basis == "no_demonstration"


async def test_verify_prompt_mentions_scaling_proof(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    await orchestrator(_enabled(settings), None, provider).analyze(_request())
    prompt = _text(provider.calls[1])
    assert "O(n^2)" in prompt
    assert "işlem dizisi" in prompt


async def test_analyze_traced_single_pass_returns_checks(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = {"analysis": analysis_reply(), "socratic": socratic_reply("İlk soru burada mı?")}
    provider = fake(first, _verify(_verdict("unproven")), socratic_reply())
    trace = await orchestrator(_enabled(settings), None, provider).analyze_traced(_single())
    assert [(c.line_start, c.kept) for c in trace.finding_checks] == [(31, False)]


async def test_analyze_traced_provider_error_has_no_checks(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), FakeReply(error="timeout"), socratic_reply())
    trace = await orchestrator(_enabled(settings), None, provider).analyze_traced(_request())
    assert trace.finding_checks == []


async def test_analyze_traced_cache_hit_has_no_checks(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), _verify(_verdict()), socratic_reply())
    orch = orchestrator(_enabled(settings), db, provider)
    first = await orch.analyze_traced(_request())
    second = await orch.analyze_traced(_request())
    assert len(first.finding_checks) == 1
    assert second.report.meta.cache_hit
    assert second.finding_checks == []
