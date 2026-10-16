"""Oturum denemeleri (Faz 49): eşzamanlı gönderimler ayrı deneme alır; iptal/hata ayrılan
denemeyi geri verir (ipucu merdiveni ilerlemez, Faz 19)."""

from __future__ import annotations

import asyncio

import pytest

from codementor.config import DataSettings, Settings
from codementor.models.enums import Language
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline import orchestrator as orchestrator_module
from codementor.pipeline import versions
from codementor.pipeline.orchestrator import Orchestrator
from codementor.pipeline.run_state import PipelineError
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


async def test_question_bank_loaded_once_per_orchestrator(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D11: banka enjekte edilmemişse aynı orkestratörde diskten bir kez okunur."""
    loads: list[int] = []
    original = QuestionBank.load_all.__func__

    def counting(cls: type[QuestionBank], data: DataSettings) -> QuestionBank:
        loads.append(1)
        return original(cls, data)

    monkeypatch.setattr(QuestionBank, "load_all", classmethod(counting))
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    await orch.analyze(_request(cache=False))
    await orch.analyze(_request(cache=False))
    assert loads == [1]


async def test_rules_version_reads_data_files_once_per_analysis(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D11: maliyet tablosu ve mentor şablonları aynı analizde bir kez okunur (anahtar + meta)."""
    calls: list[int] = []
    original = versions.rules_version

    def counting(*args: object, **kwargs: object) -> str:
        calls.append(1)
        return original(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(orchestrator_module, "rules_version", counting)
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
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


# --- Faz 61: sayılan denemeler ve advance_hint --------------------------------------------


async def test_provider_error_degraded_does_not_advance_attempt(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 61 (K1): Sağlayıcı hatası (degraded rapor) sayacı artırmaz, sonraki başarılı gönderim
    aynı ipucu seviyesinde döner."""
    broken = fake(FakeReply(error="500"))
    orch = Orchestrator(settings, db, provider_factory=lambda _n: broken)
    rep1 = await orch.analyze(_request(cache=False))
    assert rep1.meta.degraded is True
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1

    # Sonraki başarılı gönderim aynı seviyede (1) gelir ve ardından sayaç 2 olur:
    orch_ok = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    rep2 = await orch_ok.analyze(_request(cache=False))
    assert rep2.meta.degraded is False
    assert rep2.socratic.hint_level == 1
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 2


async def test_analysis_timeout_does_not_advance_attempt(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 61 (K1): Analiz süre sınırı aşıldığında sayaç değişmez."""
    stalling = _fresh(fake, delay_ms=500)
    settings.pipeline.analysis_timeout_s = 0.01
    orch = Orchestrator(settings, db, provider_factory=lambda _n: stalling)
    rep = await orch.analyze(_request(cache=False))
    assert rep.meta.degraded is True
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1


async def test_schema_repair_exhausted_does_not_advance_attempt(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 61 (K1): Şema onarımı tükendiğinde (iki kez bozuk JSON) sayaç değişmez."""
    broken = fake(FakeReply(raw="{bozuk json"), FakeReply(raw="{hala bozuk"))
    orch = Orchestrator(settings, db, provider_factory=lambda _n: broken)
    rep = await orch.analyze(_request(cache=False))
    assert rep.meta.degraded is True
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1


async def test_syntax_error_early_exit_does_not_advance_attempt(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 61 (K2): Sözdizimi hatası (erken çıkış) sayacı ilerletmez; düzeltilmiş kodla
    ilk başarılı analiz seviye 1 alır."""
    syntax_req = AnalysisRequest(
        code="int main() { return 0",
        language=Language.C,
        question_id=QUESTION,
        session_id="oturum-1",
        options=AnalysisOptions(use_cache=False),
    )
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    rep1 = await orch.analyze(syntax_req)
    assert rep1.meta.early_exit is True
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 1

    # Düzeltilmiş kodla ilk gönderim seviye 1 alır:
    rep2 = await orch.analyze(_request(cache=False))
    assert rep2.meta.early_exit is False
    assert rep2.socratic.hint_level == 1
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 2


async def test_advance_hint_false_preserves_attempt_and_hint_level(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 61 (K3): advance_hint=False ile sayaç ve seviye değişmez; oturum hiç yokken seviye 1
    ve sayaç 0 kalır."""
    req_no_adv = AnalysisRequest(
        code=LINKED_LIST,
        language=Language.C,
        question_id=QUESTION,
        session_id="oturum-no-adv",
        options=AnalysisOptions(use_cache=False, advance_hint=False),
    )
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    rep = await orch.analyze(req_no_adv)
    assert rep.socratic.hint_level == 1
    # Oturum hiç ayrılmadı / kaydedilmedi: sıradaki deneme hâlâ 1:
    assert sessions.next_attempt(db, "oturum-no-adv", QUESTION) == 1


async def test_advance_hint_false_with_existing_session_keeps_level_and_counter(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Denetim O4 (Faz 61, K3): 2 sayılan denemeden sonra aynı kodla gönderim seviyeyi ve sayacı
    değiştirmez (orchestrator'daki `next_attempt - 1` yolu)."""
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    await orch.analyze(_request(cache=False))
    second = await Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0)).analyze(
        _request(cache=False)
    )
    assert second.socratic is not None
    level = second.socratic.hint_level
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 3
    same = AnalysisRequest(
        code=LINKED_LIST,
        language=Language.C,
        question_id=QUESTION,
        session_id="oturum-1",
        options=AnalysisOptions(use_cache=False, advance_hint=False),
    )
    for _ in range(2):
        rep = await Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0)).analyze(
            same
        )
        assert rep.socratic is not None
        assert rep.socratic.hint_level == level
        assert sessions.next_attempt(db, "oturum-1", QUESTION) == 3


async def test_advance_hint_false_cancellation_does_not_corrupt_counter(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 61 (K3): advance_hint=False analiz iptal edildiğinde release_attempt çağrılmaz."""
    # Önce 1 başarılı gönderimle sayacı 2'ye taşı
    orch = Orchestrator(settings, db, provider_factory=lambda _n: _fresh(fake, 0))
    await orch.analyze(_request(cache=False))
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 2

    def fail_on_release(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("advance_hint=False iptal yolunda release_attempt çağrılmamalı")

    monkeypatch.setattr(sessions, "release_attempt", fail_on_release)

    stalling = _fresh(fake, delay_ms=10_000)
    orch_stall = Orchestrator(settings, db, provider_factory=lambda _n: stalling)
    req = AnalysisRequest(
        code=LINKED_LIST,
        language=Language.C,
        question_id=QUESTION,
        session_id="oturum-1",
        options=AnalysisOptions(use_cache=False, advance_hint=False),
    )
    task = asyncio.create_task(orch_stall.analyze(req))
    for _ in range(200):
        if stalling.calls:
            break
        await asyncio.sleep(0.01)
    assert stalling.calls
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    # Sayaç hâlâ 2 olarak kalmalı:
    assert sessions.next_attempt(db, "oturum-1", QUESTION) == 2
