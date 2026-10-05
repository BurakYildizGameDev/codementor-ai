"""Oturum denemeleri (Faz 49): eşzamanlı gönderimler ayrı deneme alır; iptal/hata ayrılan
denemeyi geri verir (ipucu merdiveni ilerlemez, Faz 19)."""

from __future__ import annotations

import asyncio

import pytest

from codementor.config import Settings
from codementor.models.enums import Language
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator, PipelineError
from codementor.providers.base import ProviderConfigError
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.questions import QuestionBank, QuestionBankError
from codementor.storage import sessions
from codementor.storage.db import Database
from tests.integration.conftest import LINKED_LIST, FakeFactory, analysis_reply, socratic_reply

pytestmark = pytest.mark.anyio

QUESTION = "c-medium-linked-list"


def _request(*, cache: bool = True) -> AnalysisRequest:
    return AnalysisRequest(
        code=LINKED_LIST,
        language=Language.C,
        question_id=QUESTION,
        session_id="oturum-1",
        options=AnalysisOptions(use_cache=cache),
    )


def _fresh(fake: FakeFactory, delay_ms: int = 50) -> FakeProvider:
    return fake(FakeReply(data=analysis_reply(), delay_ms=delay_ms), socratic_reply())


async def test_concurrent_submissions_get_attempts_1_and_2(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Kabul: `asyncio.gather` ile iki gönderim deneme 1 ve 2 alır, istisna yok."""
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake))
    first, second = await asyncio.gather(
        orch.analyze(_request(cache=False)),
        orch.analyze(_request(cache=False)),
    )
    assert sorted([first.socratic.hint_level, second.socratic.hint_level]) == [1, 2]
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 3


async def test_cancelled_analysis_releases_attempt(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = _fresh(fake, delay_ms=10_000)
    orch = Orchestrator(settings, db, provider_factory=lambda _n: provider)
    task = asyncio.create_task(orch.analyze(_request()))
    for _ in range(200):  # sağlayıcı çağrılana (deneme ayrılmış olana) kadar bekle
        if provider.calls:
            break
        await asyncio.sleep(0.01)
    assert provider.calls
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1


async def test_pipeline_error_releases_attempt(settings: Settings, db: Database) -> None:
    def broken(_name: str) -> FakeProvider:
        raise ProviderConfigError("fake", "yapılandırma yok")

    orch = Orchestrator(settings, db, provider_factory=broken)
    with pytest.raises(PipelineError):
        await orch.analyze(_request())
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1


async def test_injected_question_bank_is_used(settings: Settings, fake: FakeFactory) -> None:
    """Soru bankası enjekte edilince her istekte diskten yüklenmez."""
    bank = QuestionBank.load(settings.data.questions_dir)
    calls: list[int] = []

    def questions() -> QuestionBank:
        calls.append(1)
        return bank

    orch = Orchestrator(
        settings, None, provider_factory=lambda _n: _fresh(fake, 0), questions=questions
    )
    await orch.analyze(_request())
    assert calls == [1]


async def test_question_bank_error_is_unavailable(settings: Settings, fake: FakeFactory) -> None:
    def broken() -> QuestionBank:
        raise QuestionBankError("bozuk.yaml: geçersiz")

    orch = Orchestrator(settings, None, provider_factory=lambda _n: _fresh(fake), questions=broken)
    with pytest.raises(PipelineError) as info:
        await orch.analyze(_request())
    assert info.value.kind == "unavailable"
    assert "Soru bankası okunamadı" in str(info.value)


async def test_error_after_save_keeps_attempt(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim O1: analiz kaydedildikten sonra çıkan hata denemeyi geri almaz (kayıt geçmişte
    duruyor; aynı deneme ikinci kez verilmemeli)."""

    def broken_record(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("database is locked")

    monkeypatch.setattr(sessions, "record_attempt", broken_record)
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    with pytest.raises(RuntimeError, match="locked"):
        await orch.analyze(_request())
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 2


async def test_release_failure_does_not_mask_original_error(
    settings: Settings, db: Database, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim O2: geri alma da patlarsa asıl istisna (ör. iptal, sağlayıcı hatası) korunur."""

    def broken_release(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("database is locked")

    def broken_provider(_name: str) -> FakeProvider:
        raise ProviderConfigError("fake", "yapılandırma yok")

    monkeypatch.setattr(sessions, "release_attempt", broken_release)
    orch = Orchestrator(settings, db, provider_factory=broken_provider)
    with pytest.raises(PipelineError):
        await orch.analyze(_request())
