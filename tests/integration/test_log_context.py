"""Log bağlamı (Faz 50, mimari §13): analiz sırasında yazılan log satırları `analysis_id` ve
aşama içindeyse `stage` taşır; analiz bitince bağlam temizlenir."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from codementor.config import Settings
from codementor.log import get_logger
from codementor.models.enums import Language
from codementor.models.request import AnalysisRequest
from codementor.pipeline import orchestrator as orchestrator_module
from tests.integration.conftest import (
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    orchestrator,
    socratic_reply,
)

pytestmark = pytest.mark.anyio


async def test_analysis_logs_carry_analysis_id_and_stage(
    settings: Settings,
    fake: FakeFactory,
    monkeypatch: pytest.MonkeyPatch,
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    original = orchestrator_module.check_syntax
    log = get_logger("codementor.test")

    def logging_tier0(*args: Any, **kwargs: Any) -> Any:
        log.info("tier0_logu")  # `with timer.stage("tier0")` içinde, iş parçacığında koşar
        return original(*args, **kwargs)

    monkeypatch.setattr(orchestrator_module, "check_syntax", logging_tier0)
    provider = fake(analysis_reply(), socratic_reply())
    request = AnalysisRequest(code=LINKED_LIST, language=Language.C)
    report = await orchestrator(settings, None, provider).analyze(request)
    log.info("analiz_sonrasi")

    events = {e["event"]: e for e in captured_logs()}
    inside = events["tier0_logu"]
    assert inside["analysis_id"] == report.analysis_id
    assert inside["stage"] == "tier0"
    after = events["analiz_sonrasi"]
    assert "analysis_id" not in after
    assert "stage" not in after
