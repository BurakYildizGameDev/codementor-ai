"""Uçtan uca pipeline (Faz 10 kabul kriterleri): FakeProvider, ağsız, geçici SQLite."""

from __future__ import annotations

import pytest

from codementor.config import Settings
from codementor.models.enums import CompilationStatus, FindingSource, PipelineMode
from codementor.models.pipeline import ALL_STAGES, StageEvent
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator, PipelineError
from codementor.providers.fake import FakeReply
from codementor.rules.registry import all_rules
from codementor.storage.db import Database
from tests.integration.conftest import (
    BROKEN_C,
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    linked_list_hint,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"  # orta zorluk: ipucu seviyesi 1 → 2 → 3


def _request(code: str = LINKED_LIST, **kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate({"code": code, "question_id": QUESTION, **kw})


async def test_happy_path(settings: Settings, db: Database, fake: FakeFactory) -> None:
    provider = fake(analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert len(provider.calls) == 2
    assert not report.meta.degraded
    assert not report.meta.early_exit
    assert report.meta.provider == "fake"
    assert report.meta.tokens_out > 0
    assert report.complexity is not None
    assert report.complexity.time_complexity == linked_list_hint()
    assert report.complexity.agreement == "agrees"
    assert any(f.source is FindingSource.LLM and f.line_start == 31 for f in report.findings)
    assert report.socratic is not None
    assert report.socratic.leak_check == "passed"
    assert report.socratic.hint_level == 1
    assert report.compilation.status is CompilationStatus.SKIPPED  # Tier 1 kapalı
    assert len(report.analysis_id) == 26


async def test_all_stage_latencies_present(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    report = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    assert set(report.meta.stage_latency_ms) == set(ALL_STAGES)
    assert all(v >= 0 for v in report.meta.stage_latency_ms.values())


async def test_early_exit_never_calls_provider(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake()
    report = await orchestrator(settings, db, provider).analyze(
        AnalysisRequest(code=BROKEN_C, language="c")  # type: ignore[arg-type]
    )
    assert provider.calls == []  # kabul: çağrı sayacı 0
    assert report.meta.early_exit
    assert report.compilation.status is CompilationStatus.FAILED
    assert report.socratic is not None
    assert report.socratic.leak_check == "skipped"
    assert "2. satır" in report.socratic.guiding_questions[0]
    assert "`;`" in report.socratic.guiding_questions[0]
    assert report.meta.provider is None
    assert set(report.meta.stage_latency_ms) == set(ALL_STAGES)


async def test_repair_succeeds(settings: Settings, db: Database, fake: FakeFactory) -> None:
    provider = fake({"complexity": {}}, analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.meta.repair_attempts == 1
    assert not report.meta.degraded
    assert len(provider.calls) == 3
    repair_prompt = provider.calls[1].messages[-1].content
    assert "complexity.reasoning_steps" in repair_prompt
    assert report.complexity is not None
    assert report.complexity.confidence < 1.0  # şema ilk denemede geçmedi


@pytest.mark.parametrize("max_repairs", [0, 1, 2])
async def test_repair_bounded_then_degraded(
    settings: Settings, db: Database, fake: FakeFactory, max_repairs: int
) -> None:
    settings = settings.model_copy(
        update={
            "pipeline": settings.pipeline.model_copy(update={"max_repair_attempts": max_repairs})
        }
    )
    provider = fake(*[{"bozuk": True}] * (max_repairs + 1))
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert len(provider.calls) == max_repairs + 1  # en fazla max_repair_attempts onarım
    assert report.meta.repair_attempts == max_repairs
    assert report.meta.degraded
    assert report.socratic is not None
    assert report.socratic.leak_check == "skipped"  # şablondan
    assert report.complexity is not None
    assert report.complexity.time_complexity == linked_list_hint()  # statik ipucu
    assert all(f.source is FindingSource.STATIC for f in report.findings)
    assert any("statik analizle" in w for w in report.meta.warnings)


async def test_unjustified_conflict_repaired(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    provider = fake(analysis_reply(time="O(2^n)"), analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.meta.repair_attempts == 1
    assert "conflicts" in provider.calls[1].messages[-1].content


async def test_provider_failure_degrades(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    report = await orchestrator(settings, db, fake(FakeReply(error="timeout"))).analyze(_request())
    assert report.meta.degraded
    assert any("Model kullanılamadı" in w for w in report.meta.warnings)
    assert report.socratic is not None


async def test_leak_regenerates_once(settings: Settings, db: Database, fake: FakeFactory) -> None:
    leaky = socratic_reply("Şunu dene:\n```c\nNode *next = cur->next;\nfree(cur);\n```")
    provider = fake(analysis_reply(), leaky, socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert len(provider.calls) == 3
    assert report.socratic is not None
    assert report.socratic.leak_check == "regenerated"
    assert "```" not in report.socratic.guiding_questions[0]


async def test_leak_twice_falls_back_to_template(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    leaky = socratic_reply("```c\nfree(cur);\n```")
    provider = fake(analysis_reply(), leaky, leaky)
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.socratic is not None
    assert report.socratic.leak_check == "skipped"  # tümü atıldı → şablon
    assert not report.meta.degraded
    assert any("tümü" in w for w in report.meta.warnings)


async def test_cache_hit_skips_provider(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    idle = fake()
    second = await orchestrator(settings, db, idle).analyze(_request())
    assert idle.calls == []
    assert second.meta.cache_hit
    assert not first.meta.cache_hit
    assert second.analysis_id != first.analysis_id
    assert second.findings == first.findings
    assert second.meta.tokens_in == 0


async def test_cache_disabled_by_option(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(_request())
    provider = fake(analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(
        _request(options=AnalysisOptions(use_cache=False))
    )
    assert len(provider.calls) == 2
    assert not report.meta.cache_hit


async def test_degraded_report_not_cached(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    await orchestrator(settings, db, fake(FakeReply(error="timeout"))).analyze(_request())
    provider = fake(analysis_reply(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert not report.meta.cache_hit
    assert len(provider.calls) == 2


async def test_hint_level_rises_per_session_submission(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    levels = []
    for _ in range(3):
        provider = fake(analysis_reply(), socratic_reply())
        report = await orchestrator(settings, db, provider).analyze(_request(session_id="s-1"))
        assert report.socratic is not None
        levels.append(report.socratic.hint_level)
        assert f"İpucu seviyesi: {levels[-1]}" in provider.calls[-1].messages[-1].content
    assert levels == [1, 2, 3]  # kabul: 3. gönderimde hint_level=3


async def test_single_pass_mode(settings: Settings, db: Database, fake: FakeFactory) -> None:
    provider = fake({"analysis": analysis_reply(), "socratic": socratic_reply()})
    report = await orchestrator(settings, db, provider).analyze(
        _request(options=AnalysisOptions(mode=PipelineMode.SINGLE_PASS))
    )
    assert len(provider.calls) == 1
    assert report.socratic is not None
    assert report.socratic.leak_check == "passed"
    assert report.meta.stage_latency_ms["llm_b"] == 0


async def test_events_published(settings: Settings, db: Database, fake: FakeFactory) -> None:
    events: list[StageEvent] = []
    orch = orchestrator(settings, db, fake(analysis_reply(), socratic_reply()))
    orch.bus.subscribe(events.append)
    orch.bus.subscribe(lambda _e: 1 / 0)  # hatalı abone analizi bozmaz
    report = await orch.analyze(_request())
    done = {e.stage for e in events if e.status == "completed"}
    assert {"ingest", "tier0", "facts", "rules", "llm_a", "llm_b", "report"} <= done
    assert all(e.analysis_id == report.analysis_id for e in events)
    llm_a = next(e for e in events if e.stage == "llm_a" and e.status == "completed")
    assert llm_a.tokens > 0


async def test_without_db_no_cache_no_session(settings: Settings, fake: FakeFactory) -> None:
    orch = Orchestrator(
        settings, None, provider_factory=lambda _n: fake(analysis_reply(), socratic_reply())
    )
    report = await orch.analyze(_request(session_id="s"))
    assert report.socratic is not None
    assert report.socratic.hint_level == 1


async def test_unknown_question_is_pipeline_error(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    with pytest.raises(PipelineError, match="yok-boyle"):
        await orchestrator(settings, db, fake()).analyze(
            AnalysisRequest(code="int x;", question_id="yok-boyle")
        )


async def test_reasoning_step_leak_scrubbed(
    settings: Settings,
    db: Database,
    fake: FakeFactory,
    tmp_path: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Faz 9 gözlemi: gerekçede kod benzeri çözüm varsa o adım rapora girmez."""
    reply = analysis_reply()
    reply["complexity"]["reasoning_steps"].append("Çözüm: `Node *next = cur->next;` ile sakla.")
    provider = fake(reply, socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert report.complexity is not None
    assert all("Node *next" not in s for s in report.complexity.reasoning_steps)
    assert any("gerekçesinden" in w for w in report.meta.warnings)


SUGGESTION_TEXT = "Önceki düğüm adı daha açıklayıcı olabilir."


def _with_suggestion(*, keep_issue: bool = True) -> dict[str, object]:
    reply = analysis_reply()
    suggestion = {
        "category": "design",
        "severity": "low",
        "line_start": 27,
        "line_end": None,
        "evidence": "Node *prev = NULL;",
        "description": SUGGESTION_TEXT,
        "kind": "suggestion",
    }
    reply["additional_findings"] = [
        *(reply["additional_findings"] if keep_issue else []),
        suggestion,
    ]
    return reply


def _prompt_b(provider: object) -> str:
    calls = provider.calls  # type: ignore[attr-defined]
    return "\n".join(m.content for m in calls[-1].messages)


async def test_socratic_input_excludes_suggestions(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Faz 36: öneri raporda kalır ama Geçiş B'ye (Sokratik) gitmez."""
    provider = fake(_with_suggestion(), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    kinds = {f.line_start: f.kind for f in report.findings if f.source is FindingSource.LLM}
    assert kinds == {31: "issue", 27: "suggestion"}
    prompt = _prompt_b(provider)
    assert "*head = cur->next;" in prompt
    assert SUGGESTION_TEXT not in prompt


async def test_only_suggestions_uses_no_findings_branch(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Statik bulgu da yoksa ve LLM yalnız öneri verdiyse Geçiş B "bulgu yok" dalını görür."""
    settings.rules.disabled = [rule.id for rule in all_rules()]
    provider = fake(_with_suggestion(keep_issue=False), socratic_reply())
    report = await orchestrator(settings, db, provider).analyze(_request())
    assert [f.kind for f in report.findings] == ["suggestion"]
    prompt = _prompt_b(provider)
    assert SUGGESTION_TEXT not in prompt
    assert "Doğrulanmış bulgu yok" in prompt


async def test_tier0_isolation_stop_ends_analysis_early(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 59: alt süreçteki Tier 0 süre sınırını aşarsa analiz erken biter, LLM çağrılmaz."""
    from codementor.validation import tier0_isolation
    from codementor.validation.runner import ProcessResult

    monkeypatch.setattr(
        tier0_isolation,
        "run_process",
        lambda *_args: ProcessResult(None, "", "", timed_out=True),
    )
    validation = settings.validation.model_copy(update={"tier0_isolation": True})
    provider = fake()
    report = await orchestrator(
        settings.model_copy(update={"validation": validation}), db, provider
    ).analyze(_request())
    assert provider.calls == []
    assert report.meta.early_exit
    assert report.compilation.status is CompilationStatus.FAILED
    (diagnostic,) = report.compilation.diagnostics
    assert "süre sınırını aştı" in diagnostic.message
    assert report.findings == []  # statik aşama aynı girdiyi yeniden ayrıştırmadı
    assert any(
        "eksik" in w for w in report.meta.warnings
    )  # denetim Ö3: rapor eksik olduğunu söyler
    assert report.socratic is not None
    (question,) = report.socratic.guiding_questions
    assert "süre ya da bellek sınırını" in question
    assert "satır" not in question  # sorun bir satırda değil
