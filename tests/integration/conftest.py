"""Uçtan uca pipeline testlerinin ortak düzeneği: ağsız (FakeProvider), geçici SQLite,
depodaki `codementor.toml`'dan bağımsız ayarlar, Tier 1 kapalı (derleyici gerekmez)."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

from codementor.analysis.complexity_hint import compute_hint
from codementor.analysis.extractor import extract_facts
from codementor.config import CONFIG_FILE_ENV, Settings, load_settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import Database

REPO = Path(__file__).resolve().parents[2]
LINKED_LIST = (REPO / "tests" / "golden" / "prompts" / "c-medium-linked-list" / "code.c").read_text(
    encoding="utf-8"
)
BROKEN_C = "int main(void) {\n    int x = 1\n    return x;\n}\n"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Settings:
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    monkeypatch.delenv("CODEMENTOR_DB_PATH", raising=False)
    return load_settings(
        data={
            "questions_dir": REPO / "data" / "questions",
            "checklists_dir": REPO / "data" / "checklists",
            "call_costs_file": REPO / "data" / "call_costs.yaml",
            "mentor_templates_file": REPO / "data" / "mentor_templates.yaml",
        },
        prompts={"dir": REPO / "prompts" / "v1"},
        verify={"common_identifiers_file": REPO / "data" / "leak_common_identifiers.yaml"},
        validation={"tier1_enabled": False},
        storage={"db_path": tmp_path / "cm.db"},
        providers={"default": "fake", "fallback": []},
    )


@pytest.fixture
def db(settings: Settings) -> Iterator[Database]:
    database = Database.from_settings(settings)
    yield database
    database.close()


def linked_list_hint() -> str:
    code = normalize(LINKED_LIST, LanguageHint(language=Language.C, engine=Engine.NONE))
    return compute_hint(extract_facts(code)).value


def analysis_reply(time: str | None = None, agreement: str = "agrees") -> dict[str, Any]:
    """Bağlı liste kodu için gerçekçi, doğrulanabilir Geçiş A yanıtı."""
    return {
        "complexity": {
            "reasoning_steps": ["push_back ve remove_value listeyi bir kez gezer."],
            "time_complexity": time or f"O({linked_list_hint()})",
            "space_complexity": "O(n)",
            "optimal_time_target": "O(n)",
            "agreement": agreement,
        },
        "additional_findings": [
            {
                "category": "memory_safety",
                "severity": "high",
                "line_start": 31,
                "line_end": None,
                "evidence": "*head = cur->next;",
                "description": "Serbest bırakılmış düğümün alanı okunuyor.",
            }
        ],
    }


DEFAULT_QUESTION = "Bir düğümü serbest bıraktıktan sonra ona ait hangi bilgiye hâlâ ihtiyacın var?"


def socratic_reply(question: str = DEFAULT_QUESTION) -> dict[str, Any]:
    return {
        "key_flaw_concept": "Serbest bırakılmış belleğe erişim",
        "guiding_questions": [question],
        "next_step_hint": "free çağrısından sonraki satırları tek tek izle.",
    }


FakeFactory = Callable[..., FakeProvider]


@pytest.fixture
def fake() -> FakeFactory:
    def make(*replies: FakeReply | dict[str, Any]) -> FakeProvider:
        script = [r if isinstance(r, FakeReply) else FakeReply(data=r) for r in replies]
        return FakeProvider(script=script, retry=RetryPolicy(max_retries=0))

    return make


def orchestrator(settings: Settings, db: Database | None, provider: FakeProvider) -> Orchestrator:
    return Orchestrator(settings, db, provider_factory=lambda _name: provider)
