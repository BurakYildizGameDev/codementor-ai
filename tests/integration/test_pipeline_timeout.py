"""Analiz süre sınırı (Faz 48): aşımda bozulmuş rapor + uyarı, sağlayıcı alt süreci iptal.

Kalan süre LLM başlangıcında sabitlenir (`Orchestrator._remaining` yamalanır): Tier 0/statik
aşamanın makineye göre değişen süresi testin hangi yolu sınadığını belirlemesin (denetim).
"""

from __future__ import annotations

import time

import pytest

from codementor.config import ClaudeCliConfig, Settings
from codementor.models.enums import Language
from codementor.models.request import AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers import RetryPolicy
from codementor.providers.cli_agent import CliAgentProvider
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import Database
from tests.integration.conftest import (
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    orchestrator,
    socratic_reply,
)
from tests.providers.contract import SleepRecorder
from tests.providers.test_cli_agent import EXE
from tests.providers.test_cli_agent_cancel import BlockingRunner

pytestmark = pytest.mark.anyio

REQUEST = AnalysisRequest(code=LINKED_LIST, language=Language.C, question_id="c-medium-linked-list")
LIMIT = 60.0  # yapılandırmadaki sınır; asıl kalan süre `_fix_remaining` ile verilir


def _limited(settings: Settings, timeout: float | None = LIMIT) -> Settings:
    pipeline = settings.pipeline.model_copy(update={"analysis_timeout_s": timeout})
    return settings.model_copy(update={"pipeline": pipeline})


def _fix_remaining(monkeypatch: pytest.MonkeyPatch, seconds: float) -> None:
    monkeypatch.setattr(Orchestrator, "_remaining", staticmethod(lambda _run, _limit: seconds))


def _slow(fake: FakeFactory, delay_ms: int = 10_000) -> FakeProvider:
    return fake(FakeReply(data=analysis_reply(), delay_ms=delay_ms), socratic_reply())


async def test_slow_provider_times_out_mid_call(
    settings: Settings, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Kabul: yavaş sahte sağlayıcı çağrının ortasında kesilir; `degraded=true` ve uyarı."""
    _fix_remaining(monkeypatch, 0.3)
    provider = _slow(fake)
    start = time.monotonic()
    report = await orchestrator(_limited(settings), None, provider).analyze(REQUEST)
    assert len(provider.calls) == 1  # sağlayıcı gerçekten çağrıldı
    assert time.monotonic() - start < 5
    assert report.meta.degraded is True
    assert any("süre sınırı (60 sn)" in w for w in report.meta.warnings)
    assert report.socratic.guiding_questions  # şablondan bozulmuş Sokratik çıktı


async def test_expired_before_llm_skips_provider(
    settings: Settings, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Süre LLM'den önce bittiyse sağlayıcı hiç çağrılmaz (CLI süreci açılıp öldürülmez)."""
    _fix_remaining(monkeypatch, 0.0)
    provider = _slow(fake)
    report = await orchestrator(_limited(settings), None, provider).analyze(REQUEST)
    assert provider.calls == []
    assert report.meta.degraded is True
    assert any("süre sınırı" in w for w in report.meta.warnings)


async def test_timeout_none_disables_limit(settings: Settings, fake: FakeFactory) -> None:
    provider = fake(FakeReply(data=analysis_reply(), delay_ms=100), socratic_reply())
    report = await orchestrator(_limited(settings, None), None, provider).analyze(REQUEST)
    assert report.meta.degraded is False
    assert not any("süre sınırı" in w for w in report.meta.warnings)


class _ForeignTimeout(FakeProvider):
    async def generate_structured(self, *_args: object, **_kwargs: object) -> object:  # type: ignore[override]
        raise TimeoutError("sağlayıcı dışı zaman aşımı")


@pytest.mark.parametrize("limit", [None, LIMIT])
async def test_foreign_timeout_error_not_reported_as_limit(
    settings: Settings, limit: float | None
) -> None:
    """Yalnız kendi sınırımızın aşımı bozulmaya döner; başka `TimeoutError` gizlenmez."""
    provider = _ForeignTimeout(script=[])
    orch = orchestrator(_limited(settings, limit), None, provider)
    with pytest.raises(TimeoutError, match="sağlayıcı dışı"):
        await orch.analyze(REQUEST)


async def test_timeout_report_not_cached(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fix_remaining(monkeypatch, 0.3)
    first = await orchestrator(_limited(settings), db, _slow(fake)).analyze(REQUEST)
    assert first.meta.degraded is True
    monkeypatch.undo()
    fresh = fake(analysis_reply(), socratic_reply())
    second = await orchestrator(_limited(settings), db, fresh).analyze(REQUEST)
    assert second.meta.degraded is False  # bozulmuş rapor önbellekten dönmedi
    assert fresh.calls


async def test_timeout_cancels_cli_subprocess(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Süre aşımı asyncio iptali olarak CLI çalıştırıcısına ulaşır (süreç ağacı öldürülür)."""
    _fix_remaining(monkeypatch, 1.0)
    runner = BlockingRunner()  # iptal gelmezse 10 sn bekler
    provider = CliAgentProvider(
        "claude_cli",
        ClaudeCliConfig(command=EXE, model="m"),
        retry=RetryPolicy(max_retries=0, sleep=SleepRecorder()),
        runner=runner,
    )
    orch = Orchestrator(_limited(settings), None, provider_factory=lambda _name: provider)
    report = await orch.analyze(REQUEST)
    assert report.meta.degraded is True
    assert runner.started.is_set()
    assert runner.cancelled.wait(5), "çalıştırıcıya iptal olayı ulaşmadı"
    assert runner.calls == 1
