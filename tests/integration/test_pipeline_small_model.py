"""Faz I / İş 11: Küçük model profili, kalite kapısı ve verify_provider entegrasyon testleri."""

from __future__ import annotations

import json

import pytest

from codementor.config import Settings
from codementor.models.enums import FindingSource
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import Database
from tests.integration.conftest import (
    LINKED_LIST,
    analysis_reply,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"


def _request(**kw: object) -> AnalysisRequest:
    return AnalysisRequest.model_validate(
        {
            "code": LINKED_LIST,
            "question_id": QUESTION,
            "options": AnalysisOptions(use_cache=False),
            **kw,
        }
    )


async def test_small_model_caps_findings_and_prefers_static_complexity(
    settings: Settings, db: Database
) -> None:
    code = (
        "int calc(int a, int b) {\n"
        "    int x = a + 1;\n"
        "    int y = b + 2;\n"
        "    int z = x + y;\n"
        "    int w = z * 2;\n"
        "    return w;\n"
        "}\n"
    )
    raw_findings = [
        {
            "category": "performance",
            "severity": "low",
            "line_start": 2,
            "evidence": "int x = a + 1;",
            "description": "Hata 1",
        },
        {
            "category": "edge_case",
            "severity": "high",
            "line_start": 3,
            "evidence": "int y = b + 2;",
            "description": "Hata 2",
        },
        {
            "category": "design",
            "severity": "high",
            "line_start": 4,
            "evidence": "int z = x + y;",
            "description": "Hata 3",
        },
        {
            "category": "input_handling",
            "severity": "medium",
            "line_start": 5,
            "evidence": "int w = z * 2;",
            "description": "Hata 4",
        },
    ]
    a_dict = {
        "complexity": {
            "reasoning_steps": ["Hesaplama O(1)"],
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)",
            "optimal_time_target": "O(1)",
            "agreement": "conflicts",
        },
        "additional_findings": raw_findings,
    }
    s_dict = {
        "key_flaw_concept": "Gereksiz hesaplama",
        "guiding_questions": ["x ve y degiskenlerinin degeri 4. satirda nasil toplanir?"],
        "next_step_hint": "z degiskenini izleyin.",
    }

    fake = FakeProvider(
        script=[FakeReply(raw=json.dumps(a_dict)), FakeReply(raw=json.dumps(s_dict))]
    )

    small_settings = settings.model_copy(
        update={
            "pipeline": settings.pipeline.model_copy(
                update={"model_profile": "small", "verify_findings": False, "use_cache": False}
            )
        }
    )
    orch = Orchestrator(small_settings, db, provider_factory=lambda _n: fake)
    req = AnalysisRequest.model_validate(
        {"code": code, "language": "c", "options": AnalysisOptions(use_cache=False)}
    )
    report = await orch.analyze(req)

    # 1. Karmaşıklık statik ipucuyla düzeltilmiş olmalı
    assert report.complexity is not None
    assert report.complexity.time_complexity == "1"
    assert report.complexity.display_time == "O(1)"
    assert report.complexity.agreement == "agrees"
    assert any("Deterministik Statik Analiz" in step for step in report.complexity.reasoning_steps)

    # 2. LLM bulguları 3 ile sınırlandırılmış olmalı (low elendi, 3 adet kaldı)
    llm_findings = [f for f in report.findings if f.source is FindingSource.LLM]
    assert len(llm_findings) == 3
    assert any("Küçük model profilinde" in w for w in report.meta.warnings)


async def test_verify_provider_routes_verification_to_separate_provider(
    settings: Settings, db: Database
) -> None:
    a_dict = analysis_reply()
    v_reply = json.dumps(
        {
            "verdicts": [
                {
                    "finding": 1,
                    "verdict": "proven",
                    "reason": "31. satır serbest bırakma sonrası",
                    "input": "tek eleman",
                    "expected": "silinir",
                    "actual": "okunur",
                }
            ]
        }
    )
    s_dict = socratic_reply(question="head işaretçisi serbest bırakıldıktan sonra ne olur?")

    primary_fake = FakeProvider(
        script=[FakeReply(raw=json.dumps(a_dict)), FakeReply(raw=json.dumps(s_dict))]
    )
    verifier_fake = FakeProvider(script=[FakeReply(raw=v_reply)])

    def factory(name: str) -> FakeProvider:
        if name == "gemini":
            return verifier_fake
        return primary_fake

    custom_settings = settings.model_copy(
        update={
            "pipeline": settings.pipeline.model_copy(
                update={
                    "verify_findings": True,
                    "verify_provider": "gemini",
                    "use_cache": False,
                }
            )
        }
    )

    orch = Orchestrator(custom_settings, db, provider_factory=factory)
    report = await orch.analyze(_request())

    assert len(report.findings) > 0
    # Doğrulama geçişi verifier_fake tarafından karşılanmış olmalı
    assert len(verifier_fake.calls) == 1
    # Ana sağlayıcı analiz ve sokratik geçişi yapmış olmalı
    assert len(primary_fake.calls) == 2


async def test_socratic_gate_loop_falls_back_to_template_questions(
    settings: Settings, db: Database
) -> None:
    a_dict = analysis_reply()
    # Tekrar eden döngüsel dejenerasyon sorusu
    s_dict = socratic_reply(question="aynı cümle tekrar aynı cümle tekrar aynı cümle tekrar nedir?")

    fake = FakeProvider(
        script=[FakeReply(raw=json.dumps(a_dict)), FakeReply(raw=json.dumps(s_dict))]
    )
    small_settings = settings.model_copy(
        update={
            "pipeline": settings.pipeline.model_copy(
                update={"verify_findings": False, "use_cache": False}
            )
        }
    )
    orch = orchestrator(small_settings, db, fake)

    report = await orch.analyze(_request())

    # Kapı reddettiği için şablon sorulara düşmeli
    assert report.socratic is not None
    assert any("döngüsel tekrar" in w for w in report.meta.warnings)
    # Şablon sorular devreye girmiştir ve döngüsel soru elenmiştir
    assert not any("aynı cümle tekrar" in q for q in report.socratic.guiding_questions)
