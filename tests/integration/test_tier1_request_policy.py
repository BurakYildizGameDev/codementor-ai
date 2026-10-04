"""İstek Tier 1'i yalnız kapatabilir, sunucu yapılandırmasını aşamaz (Faz 47, ADR-0023)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pytest

from codementor.config import Settings
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.models.validation import CompilerTool, Toolchain
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeProvider
from codementor.validation.runner import ProcessLimits, ProcessResult
from tests.integration.conftest import LINKED_LIST

pytestmark = pytest.mark.anyio

GCC = Toolchain(c=CompilerTool(name="gcc", kind="gcc", command=["/usr/bin/gcc"]))


@dataclass
class RecordingRunner:
    """Derleyici yerine geçer; çağrıldığı her komutu kaydeder."""

    calls: list[Sequence[str]] = field(default_factory=list)

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: object = None,
    ) -> ProcessResult:
        self.calls.append(list(argv))
        return ProcessResult(0, "", "")


def _orchestrator(settings: Settings, enabled: bool, runner: RecordingRunner) -> Orchestrator:
    cfg = settings.model_copy(
        update={"validation": settings.validation.model_copy(update={"tier1_enabled": enabled})}
    )
    return Orchestrator(
        cfg,
        None,
        provider_factory=lambda _name: FakeProvider(script=[]),
        toolchain=GCC,
        tier1_runner=runner,
    )


async def _run(settings: Settings, enabled: bool, tier1: bool | None) -> RecordingRunner:
    runner = RecordingRunner()
    request = AnalysisRequest(
        code=LINKED_LIST,
        language="c",  # type: ignore[arg-type]
        options=AnalysisOptions(tier1=tier1),
    )
    await _orchestrator(settings, enabled, runner).analyze(request)
    return runner


async def test_request_tier1_cannot_enable_when_config_disabled(settings: Settings) -> None:
    runner = await _run(settings, enabled=False, tier1=True)
    assert runner.calls == []


async def test_request_tier1_false_disables_when_config_enabled(settings: Settings) -> None:
    runner = await _run(settings, enabled=True, tier1=False)
    assert runner.calls == []


async def test_config_enabled_and_request_silent_runs_tier1(settings: Settings) -> None:
    runner = await _run(settings, enabled=True, tier1=None)
    assert runner.calls
