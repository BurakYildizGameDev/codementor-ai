"""CLI ajanı iptali (Faz 19): asyncio iptali çalıştırıcıya iptal olayı olarak ulaşır."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pytest

from codementor.config import ClaudeCliConfig
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import GenerationOptions
from codementor.providers import RetryPolicy
from codementor.providers.cli_agent import CliAgentProvider
from codementor.providers.factory import FallbackProvider
from codementor.validation.runner import ProcessLimits, ProcessResult
from tests.providers.contract import SleepRecorder
from tests.providers.test_cli_agent import EXE, MESSAGES

pytestmark = pytest.mark.anyio


@dataclass
class BlockingRunner:
    """İptal olayı gelene kadar (en çok 10 sn) bekleyen çalıştırıcı; gerçek süreç yok."""

    started: threading.Event = field(default_factory=threading.Event)
    cancelled: threading.Event = field(default_factory=threading.Event)
    calls: int = 0

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        self.calls += 1
        self.started.set()
        assert cancel is not None, "çalıştırıcıya iptal olayı verilmeli"
        if cancel.wait(10):
            self.cancelled.set()
            return ProcessResult(None, "", "", cancelled=True)
        return ProcessResult(None, "", "", timed_out=True)


def _provider(runner: BlockingRunner, retries: int = 0) -> CliAgentProvider:
    retry = RetryPolicy(max_retries=retries, sleep=SleepRecorder())
    return CliAgentProvider(
        "claude_cli", ClaudeCliConfig(command=EXE, model="m"), retry=retry, runner=runner
    )


async def _cancel_midway(provider: CliAgentProvider, runner: BlockingRunner) -> None:
    task = asyncio.create_task(
        provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    )
    assert await asyncio.to_thread(runner.started.wait, 5)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


async def test_asyncio_cancel_sets_runner_event() -> None:
    runner = BlockingRunner()
    await _cancel_midway(_provider(runner), runner)
    # iş parçacığı zaman aşımını beklemeden iptal olayını görür (süreç ağacı öldürülür)
    assert await asyncio.to_thread(runner.cancelled.wait, 3)


async def test_cancelled_call_not_retried() -> None:
    runner = BlockingRunner()
    await _cancel_midway(_provider(runner, retries=2), runner)
    await asyncio.to_thread(runner.cancelled.wait, 3)
    assert runner.calls == 1


async def test_cancel_does_not_fall_back_to_next_provider() -> None:
    """Denetim: iptal `ProviderError` değildir; fallback zinciri sonraki sağlayıcıya geçmez."""
    first, second = BlockingRunner(), BlockingRunner()
    chain = FallbackProvider([_provider(first), _provider(second)])
    task = asyncio.create_task(
        chain.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    )
    assert await asyncio.to_thread(first.started.wait, 5)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert await asyncio.to_thread(first.cancelled.wait, 3)
    assert second.calls == 0


async def test_cancelled_result_is_not_a_provider_error() -> None:
    """Savunma: çalıştırıcı `cancelled=True` döndürürse bu "JSON yok" hatasına dönüşmez
    (hata olsaydı retry/fallback'e girerdi)."""

    def cancelled_runner(*_args: object, **_kwargs: object) -> ProcessResult:
        return ProcessResult(None, "", "", cancelled=True)

    provider = CliAgentProvider(
        "claude_cli",
        ClaudeCliConfig(command=EXE, model="m"),
        retry=RetryPolicy(max_retries=2, sleep=SleepRecorder()),
        runner=cancelled_runner,
    )
    with pytest.raises(asyncio.CancelledError):
        await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
