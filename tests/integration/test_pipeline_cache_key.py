"""Faz B (O3): raporu etkileyen ayar değişince önbellek ıskalanır, aynı ayarla isabet eder."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from codementor.config import Settings
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.models.validation import Toolchain
from codementor.pipeline.orchestrator import Orchestrator
from codementor.storage.db import Database
from tests.integration.conftest import (
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"


def _request(**kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate({"code": LINKED_LIST, "question_id": QUESTION, **kw})


def _section(name: str, **update: object) -> Callable[[Settings], Settings]:
    def apply(settings: Settings) -> Settings:
        section = getattr(settings, name).model_copy(update=update)
        return settings.model_copy(update={name: section})

    return apply


async def _analyze(
    settings: Settings, db: Database, fake: FakeFactory, request: AnalysisRequest
) -> bool:
    """Analiz eder; önbellekten döndüyse True."""
    provider = fake(analysis_reply(), socratic_reply())
    orch = Orchestrator(settings, db, provider_factory=lambda _n: provider, toolchain=Toolchain())
    report = await orch.analyze(request)
    return report.meta.cache_hit


async def test_same_settings_hit(settings: Settings, db: Database, fake: FakeFactory) -> None:
    assert not await _analyze(settings, db, fake, _request())
    assert await _analyze(settings, db, fake, _request())


@pytest.mark.parametrize(
    "change",
    [
        _section("rules", disabled=["C-MEM-001"]),
        _section("rules", max_findings=5),
        _section("prompts", include_facts=False),
        _section("prompts", numbered_code=False),
        _section("prompts", max_fewshots=0),
        _section("verify", evidence_window=0),
        _section("pipeline", max_repair_attempts=2),
        _section("validation", tier1_enabled=True),
    ],
    ids=[
        "rules.disabled",
        "rules.max_findings",
        "prompts.include_facts",
        "prompts.numbered_code",
        "prompts.max_fewshots",
        "verify.evidence_window",
        "pipeline.max_repair_attempts",
        "validation.tier1_enabled",
    ],
)
async def test_output_affecting_setting_misses(
    settings: Settings,
    db: Database,
    fake: FakeFactory,
    change: Callable[[Settings], Settings],
) -> None:
    assert not await _analyze(settings, db, fake, _request())
    assert not await _analyze(change(settings), db, fake, _request())


async def test_request_tier1_off_misses(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Tier 1 açıkken yapılan analiz, isteğin kapattığı Tier 1 ile aynı rapor değildir."""
    enabled = _section("validation", tier1_enabled=True)(settings)
    assert not await _analyze(enabled, db, fake, _request())
    off = _request(options=AnalysisOptions(tier1=False))
    assert not await _analyze(enabled, db, fake, off)
    assert await _analyze(enabled, db, fake, off)


async def test_request_tier1_off_is_noop_when_config_disabled(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Yapılandırmada zaten kapalıysa isteğin kapatması raporu değiştirmez: isabet."""
    assert not await _analyze(settings, db, fake, _request())
    assert await _analyze(settings, db, fake, _request(options=AnalysisOptions(tier1=False)))


async def test_rules_disabled_order_does_not_matter(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = _section("rules", disabled=["C-MEM-001", "C-MEM-002"])(settings)
    second = _section("rules", disabled=["C-MEM-002", "C-MEM-001"])(settings)
    assert not await _analyze(first, db, fake, _request())
    assert await _analyze(second, db, fake, _request())
