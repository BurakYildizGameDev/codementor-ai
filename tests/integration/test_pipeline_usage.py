"""Faz K: aşama başına token, toplam kullanım ve kullanıcı sorusuyla uçtan uca analiz."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.config import Settings
from codementor.models.questions import UserQuestionDraft
from codementor.models.report import TokenSplit
from codementor.models.request import AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeReply
from codementor.questions.user_store import save_question
from codementor.storage.cache import usage_totals
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


def _request(**kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate({"code": LINKED_LIST, "question_id": QUESTION, **kw})


def _sum(stages: dict[str, TokenSplit]) -> tuple[int, int]:
    return sum(s.input for s in stages.values()), sum(s.output for s in stages.values())


async def test_stage_tokens_sum_to_totals(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    report = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    meta = report.meta
    assert set(meta.stage_tokens) == {"llm_a", "llm_b"}
    # FakeProvider yalnız çıkışı bildirir (giriş 0, `estimated`); her aşama yine sayılır
    assert all(s.output > 0 for s in meta.stage_tokens.values())
    assert _sum(meta.stage_tokens) == (meta.tokens_in, meta.tokens_out)


async def test_stage_tokens_with_repair_and_verify(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    enabled = settings.model_copy(
        update={"pipeline": settings.pipeline.model_copy(update={"verify_findings": True})}
    )
    verdict = {
        "finding": 1,
        "verdict": "proven",
        "reason": "Gerekçe.",
        "input": "tek düğüm",
        "expected": "liste boş",
        "actual": "serbest bırakılan düğüm okunur",
    }
    provider = fake(
        FakeReply(raw="bozuk"), analysis_reply(), {"verdicts": [verdict]}, socratic_reply()
    )
    report = await orchestrator(enabled, db, provider).analyze(_request())
    meta = report.meta
    assert meta.repair_attempts == 1
    assert set(meta.stage_tokens) == {"llm_a", "llm_v", "llm_b"}
    assert _sum(meta.stage_tokens) == (meta.tokens_in, meta.tokens_out)


async def test_cache_hit_has_no_stage_tokens(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(_request())
    again = await orchestrator(settings, db, fake()).analyze(_request())
    assert again.meta.cache_hit
    assert again.meta.stage_tokens == {}
    assert (again.meta.tokens_in, again.meta.tokens_out) == (0, 0)


async def test_usage_totals_count_only_spent_tokens(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    assert usage_totals(db).analyses == 0
    first = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    await orchestrator(settings, db, fake()).analyze(_request())  # önbellek: 0 token
    totals = usage_totals(db)
    assert totals.analyses == 2
    assert (totals.tokens_in, totals.tokens_out) == (first.meta.tokens_in, first.meta.tokens_out)
    assert totals.cost is None  # fake sağlayıcının fiyatı yok


def test_usage_totals_sums_cost(db: Database) -> None:
    """Maliyet rapor gövdesinden toplanır; fiyatsız kayıtlar toplamı bozmaz."""
    import json

    from codementor.models.report import AnalysisReport
    from codementor.pipeline.ids import new_ulid
    from codementor.storage.cache import save_analysis

    golden = Path(__file__).resolve().parents[1] / "golden" / "report_example.json"
    base = AnalysisReport.model_validate(json.loads(golden.read_text(encoding="utf-8")))
    for cost in (0.01, None, 0.0025):
        report = base.model_copy(update={"analysis_id": new_ulid()})
        report.meta = base.meta.model_copy(update={"cost_est": cost})
        save_analysis(db, report, key="k", session_id=None, latency_ms=1)
    totals = usage_totals(db)
    assert totals.analyses == 3
    assert totals.tokens_in == 3 * base.meta.tokens_in
    assert totals.cost == pytest.approx(0.0125)


async def test_user_question_end_to_end(
    settings: Settings, db: Database, fake: FakeFactory, tmp_path: Path
) -> None:
    """Kendi sorusu (hedef karmaşıklık ve referans yok) analizde kullanılır, ipucu merdiveni
    genel ipuçlarıyla çalışır."""
    user_dir = tmp_path / "sorularim"
    settings = settings.model_copy(
        update={"data": settings.data.model_copy(update={"user_questions_dir": user_dir})}
    )
    question = save_question(
        UserQuestionDraft(
            title="Bağlı listeden değer silme",
            prompt="Verilen değeri taşıyan düğümleri listeden silen fonksiyonu yazın.",
            language="c",  # type: ignore[arg-type]
            difficulty="medium",  # type: ignore[arg-type]
        ),
        user_dir,
    )
    provider = fake(analysis_reply(), socratic_reply())
    report = await Orchestrator(settings, db, provider_factory=lambda _n: provider).analyze(
        AnalysisRequest(code=LINKED_LIST, question_id=question.id)  # type: ignore[call-arg]
    )
    assert report.question_id == question.id
    assert not report.meta.degraded
    assert report.complexity is not None
    assert report.complexity.is_optimal is None  # hedef verilmedi
    assert question.title in provider.calls[0].messages[-1].content
