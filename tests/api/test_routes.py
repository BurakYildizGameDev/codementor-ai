"""§9 uç noktaları: mutlu yol + hata; referans çözüm sızmıyor; problem+json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft4Validator

from codementor.api import routes
from codementor.config import Settings
from codementor.models.validation import CompilerTool, Toolchain
from codementor.providers.fake import FakeReply
from tests.api.conftest import ClientFactory
from tests.integration.conftest import (
    BROKEN_C,
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
PROBLEM = "application/problem+json"
SARIF_SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "fixtures" / "sarif-schema-2.1.0.json").read_text(
        encoding="utf-8"
    )
)
BODY = {"code": LINKED_LIST, "question_id": "c-medium-linked-list"}


async def test_analyze_returns_report(client_for: ClientFactory, fake: FakeFactory) -> None:
    provider = fake(analysis_reply(), socratic_reply())
    response = await client_for(provider).post("/v1/analyze", json=BODY)
    assert response.status_code == 200
    report = response.json()
    assert report["meta"]["provider"] == "fake"
    assert report["socratic"]["leak_check"] == "passed"
    assert len(provider.calls) == 2


async def test_all_providers_failed_is_200_degraded(
    client_for: ClientFactory, fake: FakeFactory
) -> None:
    """§9: bozulmuş rapor döndürülebiliyorsa 502 yerine 200 + degraded."""
    response = await client_for(fake(FakeReply(error="500"))).post("/v1/analyze", json=BODY)
    assert response.status_code == 200
    assert response.json()["meta"]["degraded"] is True


async def test_early_exit_via_api(client_for: ClientFactory, fake: FakeFactory) -> None:
    provider = fake()
    response = await client_for(provider).post(
        "/v1/analyze", json={"code": BROKEN_C, "language": "c"}
    )
    assert response.json()["meta"]["early_exit"] is True
    assert provider.calls == []


async def test_stored_report_and_sarif(client_for: ClientFactory, fake: FakeFactory) -> None:
    client = client_for(fake(analysis_reply(), socratic_reply()))
    report = (await client.post("/v1/analyze", json=BODY)).json()
    stored = await client.get(f"/v1/analyses/{report['analysis_id']}")
    assert stored.status_code == 200
    assert stored.json() == report
    sarif = await client.get(f"/v1/analyses/{report['analysis_id']}/sarif")
    assert sarif.status_code == 200
    assert sarif.headers["content-type"].startswith("application/sarif+json")
    Draft4Validator(SARIF_SCHEMA).validate(sarif.json())
    uri = sarif.json()["runs"][0]["artifacts"][0]["location"]["uri"]
    assert uri == f"{report['analysis_id']}.c"
    markdown = await client.get(f"/v1/analyses/{report['analysis_id']}/markdown")
    assert markdown.status_code == 200
    assert markdown.headers["content-type"].startswith("text/markdown")
    assert report["analysis_id"] in markdown.text
    assert report["findings"][0]["id"] in markdown.text


@pytest.mark.parametrize(
    "path",
    [
        "/v1/analyses/yok",
        "/v1/analyses/yok/sarif",
        "/v1/analyses/yok/markdown",
        "/v1/analyses/01J9ZK4M8Q3W6Y2T5R7N1B0C9D",  # biçim geçerli, kayıt yok (Faz 27)
        "/v1/analyses/01j9zk4m8q3w6y2t5r7n1b0c9d",  # küçük harf: biçim dışı
    ],
)
async def test_missing_analysis_404(client_for: ClientFactory, path: str) -> None:
    response = await client_for().get(path)
    assert response.status_code == 404
    assert response.headers["content-type"] == PROBLEM
    assert response.json()["instance"] == path


async def test_questions_list_and_filters(client_for: ClientFactory) -> None:
    client = client_for()
    everything = (await client.get("/v1/questions")).json()
    assert len(everything) >= 14
    unity = (await client.get("/v1/questions", params={"engine": "unity"})).json()
    assert unity
    assert all(q["engine"] == "unity" for q in unity)
    hard_c = await client.get("/v1/questions", params={"language": "c", "difficulty": "hard"})
    assert [q["id"] for q in hard_c.json()] == ["c-hard-hash-table", "c-hard-stack"]
    bad = await client.get("/v1/questions", params={"difficulty": "imkansiz"})
    assert bad.status_code == 422
    assert bad.headers["content-type"] == PROBLEM


async def test_question_detail_hides_solution_and_mentor_data(client_for: ClientFactory) -> None:
    response = await client_for().get("/v1/questions/unity-hard-inventory")
    assert response.status_code == 200
    body = response.json()
    assert body["title"]
    for hidden in ("reference_solution_path", "hint_ladder", "concept_tags", "checklist_extra"):
        assert hidden not in body
    assert "private/" not in response.text
    assert "solution" not in response.text.lower()


async def test_unknown_question_404(client_for: ClientFactory) -> None:
    response = await client_for().get("/v1/questions/yok-boyle")
    assert response.status_code == 404
    assert response.headers["content-type"] == PROBLEM
    assert "yok-boyle" in response.json()["detail"]


async def test_rules_catalog_filtered(client_for: ClientFactory) -> None:
    client = client_for()
    rules = (await client.get("/v1/rules")).json()
    assert {r["id"] for r in rules} >= {"UNITY-GC-001", "C-MEM-001"}
    unreal = (await client.get("/v1/rules", params={"engine": "unreal"})).json()
    assert unreal
    assert all(r["engines"] in (["unreal"], []) for r in unreal)
    assert any(r["engines"] == ["unreal"] for r in unreal)


async def test_providers_without_secrets(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "sk-gizli-deger-123")
    cfg = settings.model_copy(
        update={
            "providers": settings.providers.model_copy(
                update={
                    "default": "gemini",
                    "fallback": ["anthropic"],
                    "gemini": settings.providers.gemini.model_copy(update={"model": "gemini-x"}),
                }
            )
        }
    )
    response = await client_for(cfg=cfg).get("/v1/providers")
    statuses = response.json()
    assert [s["name"] for s in statuses] == ["gemini", "anthropic"]
    assert statuses[0]["ready"] is True
    assert statuses[1]["ready"] is False
    assert "sk-gizli" not in response.text


async def test_health_and_ready(client_for: ClientFactory, settings: Settings) -> None:
    client = client_for()
    health = await client.get("/health")
    assert health.json()["status"] == "ok"
    cfg = settings.model_copy(
        update={
            "providers": settings.providers.model_copy(
                update={"default": "anthropic", "fallback": []}
            )
        }
    )
    ready = (await client_for(cfg=cfg).get("/health/ready")).json()
    assert ready["ready"] is False  # anthropic model/anahtar yok
    assert {c["target"] for c in ready["compilers"]} == {"c", "cpp", "unreal", "csharp"}


async def test_ready_reports_compiler_origin(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 29: hangi derleyicinin PATH'ten, hangisinin indirilenden geldiği görünür."""
    chain = Toolchain(
        c=CompilerTool(name="gcc", kind="gcc", command=["/usr/bin/gcc"]),
        cpp=CompilerTool(
            name="zig", kind="clang", command=["/z/zig", "clang"], origin="downloaded"
        ),
    )
    monkeypatch.setattr(routes, "get_toolchain", lambda _settings: chain)
    cfg = settings.model_copy(
        update={
            "providers": settings.providers.model_copy(
                update={"default": "anthropic", "fallback": []}
            )
        }
    )
    ready = (await client_for(cfg=cfg).get("/health/ready")).json()
    by_target = {c["target"]: (c["tool"], c["origin"]) for c in ready["compilers"]}
    assert by_target == {
        "c": ("gcc", "system"),
        "cpp": ("zig", "downloaded"),
        "unreal": (None, None),
        "csharp": (None, None),
    }
