"""Faz C (Y6, mimari §5.4.3): kavram adı yalnız açılması gereken denemede rapora girer.

Orta zorluk: kavram 2. denemeden itibaren adlandırılır. Kural kaynağında uygulandığı için API
yanıtı (rapor JSON'u), Markdown ve CLI aynı sonucu görür.
"""

from __future__ import annotations

import pytest

from codementor.config import Settings
from codementor.models.request import AnalysisRequest
from codementor.report.cli_render import render_report
from codementor.report.markdown import to_markdown
from codementor.storage.db import Database
from tests.integration.conftest import (
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
CONCEPT = "Serbest bırakılmış belleğe erişim"  # socratic_reply()'deki kavram


def _request() -> AnalysisRequest:
    return AnalysisRequest.model_validate(
        {"code": LINKED_LIST, "question_id": "c-medium-linked-list", "session_id": "oturum-1"}
    )


async def test_concept_hidden_on_first_attempt_then_revealed(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    first = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    assert first.socratic is not None
    assert first.socratic.hint_level == 1
    assert first.socratic.concept_revealed is False
    assert CONCEPT not in first.model_dump_json()  # API / JSON indirme
    assert CONCEPT not in to_markdown(first)
    assert all(CONCEPT not in str(part) for part in render_report(first, None))

    second = await orchestrator(settings, db, fake(analysis_reply(), socratic_reply())).analyze(
        _request()
    )
    assert second.socratic is not None
    assert second.socratic.hint_level == 2
    assert second.socratic.concept_revealed is True
    assert second.socratic.key_flaw_concept == CONCEPT
    assert f"**Kavram:** {CONCEPT}" in to_markdown(second)


async def test_degraded_template_concept_is_generic_and_shown(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    from codementor.providers.fake import FakeReply

    report = await orchestrator(settings, db, fake(FakeReply(error="timeout"))).analyze(_request())
    assert report.meta.degraded
    assert report.socratic is not None
    assert report.socratic.concept_revealed is True
    assert report.socratic.key_flaw_concept  # kategori adı ya da genel şablon adı
