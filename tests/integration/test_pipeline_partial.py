"""Faz B: LLM'in kısmi başarısızlığında doğrulanmış bulgular korunur, yarım sonuç önbelleğe girmez.

Y3 (onarım), Y4 (Geçiş B / süre sınırı), Y5 (fallback ve yarım rapor önbelleği), O2 (tek geçiş),
O4 (önbellek dönüşünde maliyet). FakeProvider, ağsız.
"""

from __future__ import annotations

from typing import Any

import pytest

from codementor.config import Settings
from codementor.models.enums import FindingSource, PipelineMode
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline import passes
from codementor.pipeline.assemble import from_cache
from codementor.pipeline.events import EventBus, StageTimer
from codementor.pipeline.ids import new_ulid
from codementor.pipeline.orchestrator import Orchestrator
from codementor.pipeline.passes import COMPLEXITY_UNVERIFIED, VERIFY_FAILED
from codementor.prompts.budget import PromptBudgetError, PromptConfigError
from codementor.providers import RetryPolicy
from codementor.providers.factory import FallbackProvider
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import Database
from tests.integration.conftest import (
    DEFAULT_QUESTION,
    LINKED_LIST,
    REPO,
    FakeFactory,
    analysis_reply,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"
CONFLICT = "O(2^n)"  # statik ipucuyla gerekçesiz çelişir → onarım istenir


def _request(**kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate({"code": LINKED_LIST, "question_id": QUESTION, **kw})


def _llm_lines(report: AnalysisReport) -> list[int]:
    return [f.line_start for f in report.findings if f.source is FindingSource.LLM]


def _pipeline(settings: Settings, **update: object) -> Settings:
    return settings.model_copy(update={"pipeline": settings.pipeline.model_copy(update=update)})


async def _served_from_cache(settings: Settings, db: Database, fake: FakeFactory) -> bool:
    """Aynı istek ikinci kez: önbellekten mi döndü (sağlayıcı hiç çağrılmadı mı)?"""
    provider = fake(analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.meta.cache_hit is (not provider.calls)
    return report.meta.cache_hit


def _assert_findings_kept(report: AnalysisReport) -> None:
    assert not report.meta.degraded
    assert 31 in _llm_lines(report)


def _assert_template_questions(report: AnalysisReport) -> None:
    assert report.socratic is not None
    assert report.socratic.leak_check == "skipped"  # şablondan


# --- Y3: onarım başarısız ama ilk yanıt geçerliydi ----------------------------------------------


@pytest.mark.parametrize(
    "repair_reply",
    [FakeReply(raw="bozuk"), FakeReply(error="timeout"), FakeReply(data=analysis_reply(CONFLICT))],
    ids=["bozuk-json", "saglayici-hatasi", "celiski-suruyor"],
)
async def test_failed_repair_keeps_verified_findings(
    settings: Settings, db: Database, fake: FakeFactory, repair_reply: FakeReply
) -> None:
    provider = fake(analysis_reply(CONFLICT), repair_reply, socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    _assert_findings_kept(report)
    assert report.complexity is None
    assert COMPLEXITY_UNVERIFIED in report.meta.warnings
    assert report.meta.repair_attempts == 1
    assert report.socratic is not None
    assert report.socratic.leak_check == "passed"  # Geçiş B yine yapıldı
    prompt_b = provider.calls[2].messages[-1].content
    assert CONFLICT not in prompt_b  # doğrulanmamış karmaşıklık soruya taşınmaz
    assert not await _served_from_cache(settings, db, fake)


async def test_no_valid_reply_still_degrades(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(FakeReply(raw="bozuk"), FakeReply(error="timeout"))
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.meta.degraded
    assert all(f.source is FindingSource.STATIC for f in report.findings)


# --- Y4: Geçiş B hatası Geçiş A'yı silmez -------------------------------------------------------


async def test_pass_b_provider_error_keeps_findings(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), FakeReply(error="500"))
    report = await orchestrator(settings, db, provider).analyze(_request())
    _assert_findings_kept(report)
    assert report.complexity is not None
    _assert_template_questions(report)
    assert any("Mentor soruları üretilemedi" in w for w in report.meta.warnings)
    assert not await _served_from_cache(settings, db, fake)


@pytest.mark.parametrize(
    "error", [PromptBudgetError(99_999, 1_000), PromptConfigError("bağlam yok")]
)
async def test_pass_b_prompt_error_keeps_findings(
    settings: Settings,
    db: Database,
    fake: FakeFactory,
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    def explode(*_a: Any, **_k: Any) -> Any:
        raise error

    monkeypatch.setattr(passes, "build_socratic_messages", explode)
    provider = fake(analysis_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert len(provider.calls) == 1
    _assert_findings_kept(report)
    _assert_template_questions(report)
    assert any("Mentor soruları üretilemedi" in w for w in report.meta.warnings)


async def test_pass_b_schema_failure_not_cached(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(), FakeReply(raw="bozuk"), FakeReply(raw="bozuk"))
    report = await orchestrator(settings, db, provider).analyze(_request())
    _assert_findings_kept(report)
    _assert_template_questions(report)
    assert not await _served_from_cache(settings, db, fake)


def _limited(settings: Settings, monkeypatch: pytest.MonkeyPatch, seconds: float) -> Settings:
    monkeypatch.setattr(Orchestrator, "_remaining", staticmethod(lambda _run, _limit: seconds))
    return _pipeline(settings, analysis_timeout_s=60.0)


async def test_timeout_in_pass_b_keeps_findings(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    limited = _limited(settings, monkeypatch, 0.5)
    provider = fake(analysis_reply(), FakeReply(data=socratic_reply(), delay_ms=10_000))
    report = await orchestrator(limited, db, provider).analyze(_request())
    assert len(provider.calls) == 2
    _assert_findings_kept(report)
    _assert_template_questions(report)
    assert any("bulgular korundu" in w for w in report.meta.warnings)
    assert VERIFY_FAILED not in report.meta.warnings
    monkeypatch.undo()
    assert not await _served_from_cache(settings, db, fake)


async def test_timeout_in_verify_pass_keeps_unverified_findings_with_warning(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    limited = _pipeline(_limited(settings, monkeypatch, 0.5), verify_findings=True)
    provider = fake(analysis_reply(), FakeReply(data={"verdicts": []}, delay_ms=10_000))
    report = await orchestrator(limited, db, provider).analyze(_request())
    _assert_findings_kept(report)
    _assert_template_questions(report)
    assert VERIFY_FAILED in report.meta.warnings


async def test_timeout_in_pass_a_still_degrades(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    limited = _limited(settings, monkeypatch, 0.3)
    provider = fake(FakeReply(data=analysis_reply(), delay_ms=10_000))
    report = await orchestrator(limited, db, provider).analyze(_request())
    assert report.meta.degraded
    assert any("statik analizle" in w for w in report.meta.warnings)


# --- Y5: fallback yanıtı önbelleğe girmez -------------------------------------------------------


def _named(name: str, *replies: FakeReply | dict[str, Any]) -> FakeProvider:
    script = [r if isinstance(r, FakeReply) else FakeReply(data=r) for r in replies]
    return FakeProvider(script=script, retry=RetryPolicy(max_retries=0), name=name)


async def _chain_served_from_cache(settings: Settings, db: Database) -> bool:
    """İkinci istek aynı zincir yapısıyla (anahtar sağlayıcı/model adına bağlı) ve sağlıklı."""
    primary = _named("fake", analysis_reply(), socratic_reply())
    chain = FallbackProvider([primary, _named("yedek", analysis_reply(), socratic_reply())])
    report = await Orchestrator(settings, db, provider_factory=lambda _n: chain).analyze(_request())
    assert report.meta.cache_hit is (not primary.calls)
    return report.meta.cache_hit


async def test_fallback_report_not_cached(settings: Settings, db: Database) -> None:
    primary = _named("fake", FakeReply(error="500"), FakeReply(error="500"))
    backup = _named("yedek", analysis_reply(), socratic_reply())
    chain = FallbackProvider([primary, backup])
    report = await Orchestrator(settings, db, provider_factory=lambda _n: chain).analyze(_request())
    assert report.meta.provider == "yedek"
    assert not report.meta.degraded
    assert not await _chain_served_from_cache(settings, db)


async def test_complete_chain_report_still_cached(settings: Settings, db: Database) -> None:
    primary = _named("fake", analysis_reply(), socratic_reply())
    chain = FallbackProvider([primary, _named("yedek")])
    await Orchestrator(settings, db, provider_factory=lambda _n: chain).analyze(_request())
    assert await _chain_served_from_cache(settings, db)


async def test_complete_report_still_cached(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(_request())
    assert await _served_from_cache(settings, db, fake)


async def test_verify_failed_report_not_cached(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    enabled = _pipeline(settings, verify_findings=True)
    provider = fake(analysis_reply(), FakeReply(error="500"), socratic_reply())
    report = await orchestrator(enabled, db, provider).analyze(_request())
    assert any(VERIFY_FAILED in w for w in report.meta.warnings)
    second = fake(analysis_reply(), {"verdicts": []}, socratic_reply())
    again = await orchestrator(enabled, db, second).analyze(_request())
    assert not again.meta.cache_hit


# --- O2: tek geçişte kanıtsız bulgu → ayrı Geçiş B ----------------------------------------------


async def test_single_pass_unverified_finding_triggers_pass_b(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    analysis = analysis_reply()
    analysis["additional_findings"].append(
        {
            "category": "memory_safety",
            "severity": "high",
            "line_start": 12,
            "line_end": None,
            "evidence": "hayali_satir();",
            "description": "Var olmayan çağrı tehlikeli.",
        }
    )
    single = {"analysis": analysis, "socratic": socratic_reply("hayali_satir neden tehlikeli?")}
    provider = fake(single, socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(
        _request(options=AnalysisOptions(mode=PipelineMode.SINGLE_PASS))
    )
    assert len(provider.calls) == 2  # ayrı Geçiş B
    assert report.socratic is not None
    assert report.socratic.guiding_questions == [DEFAULT_QUESTION]
    assert "hayali_satir" not in provider.calls[1].messages[-1].content


async def test_single_pass_all_verified_stays_single_call(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake({"analysis": analysis_reply(), "socratic": socratic_reply()})
    await orchestrator(settings, db, provider).analyze(
        _request(options=AnalysisOptions(mode=PipelineMode.SINGLE_PASS))
    )
    assert len(provider.calls) == 1


# --- O4: önbellek dönüşünde maliyet yok ---------------------------------------------------------


def test_from_cache_clears_cost() -> None:
    golden = (REPO / "tests" / "golden" / "report_example.json").read_text(encoding="utf-8")
    report = AnalysisReport.model_validate_json(golden)
    report.meta.cost_est = 0.002385
    report.meta.usage_estimated = True
    cached = from_cache(report, new_ulid(), StageTimer(new_ulid(), EventBus()))
    assert cached.meta.cache_hit
    assert cached.meta.cost_est is None
    assert cached.meta.usage_estimated is False
    assert (cached.meta.tokens_in, cached.meta.tokens_out) == (0, 0)
