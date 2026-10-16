"""Token muhasebesi ve maliyet tahmini (Faz 25, mimari §13)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from codementor.config import Settings
from codementor.models.eval import ModelPrice, PricingFile
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.prompts import BuiltPrompt
from codementor.models.provider import ChatMessage, GenerationOptions, ProviderResult, TokenUsage
from codementor.models.report import ReportMeta, TokenSplit
from codementor.pipeline.cost import cost_of_stages, estimate_cost, load_pricing
from codementor.pipeline.events import EventBus, StageTimer
from codementor.pipeline.passes import LLMSession
from codementor.providers.fake import FakeProvider

pytestmark = pytest.mark.anyio

PRICING = PricingFile(
    version=1,
    prices=[ModelPrice(provider="openai", model="m", input_per_mtok=2.0, output_per_mtok=8.0)],
)


@dataclass
class _Silent(FakeProvider):
    """Token sayısı bildirmeyen ya da kendisi tahmin eden sağlayıcı."""

    reply_usage: TokenUsage = field(default_factory=TokenUsage)

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: Any, options: GenerationOptions
    ) -> ProviderResult:
        return ProviderResult(
            raw_text='{"yanit": "' + "x" * 400 + '"}',
            parsed={},
            usage=self.reply_usage,
            latency_ms=1,
            model="m",
            finish_reason="stop",
            provider="openai",
        )


def _built() -> BuiltPrompt:
    messages = [ChatMessage(role="user", content="y" * 4000)]
    return BuiltPrompt(
        messages=messages, prompt_version="v1", estimated_tokens=1000, budget_tokens=4000
    )


def _session(provider: FakeProvider, settings: Settings) -> LLMSession:
    return LLMSession(provider, settings, StageTimer("01TEST", EventBus()))


async def test_missing_usage_is_estimated() -> None:
    session = _session(_Silent(script=[]), Settings())
    await session.call("llm_b", _built(), LLMSocraticOutput)
    assert session.usage_estimated
    assert session.tokens_in >= 1000  # 4000 karakter ≈ 1000+ token
    assert session.tokens_out >= 100


async def test_reported_usage_kept() -> None:
    session = _session(
        _Silent(script=[], reply_usage=TokenUsage(input_tokens=12, output_tokens=3)), Settings()
    )
    await session.call("llm_b", _built(), LLMSocraticOutput)
    assert not session.usage_estimated
    assert (session.tokens_in, session.tokens_out) == (12, 3)


async def test_provider_estimate_flag_propagates() -> None:
    usage = TokenUsage(input_tokens=0, output_tokens=40, estimated=True)
    session = _session(_Silent(script=[], reply_usage=usage), Settings())
    await session.call("llm_b", _built(), LLMSocraticOutput)
    assert session.usage_estimated
    assert session.tokens_out == 40


# --- Faz G7: token tahmininin gerçek `usage` ile kalibrasyonu ---------------------------------


async def test_estimate_ratio_logged_when_usage_reported(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """G7: sağlayıcı gerçek token bildirdiğinde tahmin/oran DEBUG'a yazılır; muhasebe değişmez."""
    session = _session(
        _Silent(script=[], reply_usage=TokenUsage(input_tokens=900, output_tokens=3)), Settings()
    )
    await session.call("llm_b", _built(), LLMSocraticOutput)
    entries = [e for e in captured_logs() if e["event"] == "token_estimate_ratio"]
    assert len(entries) == 1
    assert entries[0]["actual"] == 900
    assert entries[0]["estimated"] > 0
    assert entries[0]["ratio"] == round(900 / entries[0]["estimated"], 3)
    assert (session.tokens_in, session.tokens_out) == (900, 3)


async def test_estimate_ratio_not_logged_without_usage(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Karşılaştıracak gerçek sayı yoksa (sağlayıcı bildirmedi) log yazılmaz."""
    session = _session(_Silent(script=[]), Settings())
    await session.call("llm_b", _built(), LLMSocraticOutput)
    assert [e for e in captured_logs() if e["event"] == "token_estimate_ratio"] == []


def test_cost_from_pricing() -> None:
    cost = estimate_cost(PRICING, "openai", "m", 1_000_000, 500_000)
    assert cost == pytest.approx(2.0 + 4.0)


def test_unpriced_model_cost_none(tmp_path: Path) -> None:
    assert estimate_cost(PRICING, "openai", "baska", 10, 10) is None
    assert estimate_cost(PRICING, "openai", "m", 0, 0) is None
    assert estimate_cost(None, "openai", "m", 10, 10) is None
    assert load_pricing(tmp_path / "yok.yaml") is None


STAGE_PRICING = PricingFile(
    version=1,
    prices=[
        ModelPrice(provider="a", model="m", input_per_mtok=1.0, output_per_mtok=2.0),
        ModelPrice(provider="b", model="m", input_per_mtok=10.0, output_per_mtok=20.0),
    ],
)


def test_cost_of_stages_prices_each_stage_with_its_provider() -> None:
    """D6: geçişler farklı sağlayıcıya düşerse her geçiş kendi modelin fiyatıyla hesaplanır."""
    usage = {
        ("llm_a", "a", "m"): TokenSplit(input=0, output=1_000_000),
        ("llm_b", "b", "m"): TokenSplit(input=0, output=1_000_000),
    }
    assert cost_of_stages(STAGE_PRICING, usage) == pytest.approx(22.0)
    # hepsi son sağlayıcının fiyatıyla hesaplansaydı 40.0 çıkardı (eski davranış)
    all_backup = {
        ("llm_a", "b", "m"): TokenSplit(input=0, output=1_000_000),
        ("llm_b", "b", "m"): TokenSplit(input=0, output=1_000_000),
    }
    assert cost_of_stages(STAGE_PRICING, all_backup) == pytest.approx(40.0)


def test_cost_of_stages_splits_same_stage_by_provider() -> None:
    """D6: aynı geçişin ikinci çağrısı yedeğe düştüyse iki fiyat ayrı ayrı toplanır."""
    usage = {
        ("llm_b", "a", "m"): TokenSplit(input=0, output=1_000_000),
        ("llm_b", "b", "m"): TokenSplit(input=0, output=1_000_000),
    }
    assert cost_of_stages(STAGE_PRICING, usage) == pytest.approx(22.0)


def test_cost_of_stages_none_when_a_stage_is_unpriced() -> None:
    """Fiyatsız bir geçiş varsa kısmi toplam yanıltıcı olur: None."""
    usage = {
        ("llm_a", "openai", "m"): TokenSplit(input=0, output=10),
        ("llm_b", "bilinmeyen", "m"): TokenSplit(input=0, output=10),
    }
    assert cost_of_stages(PRICING, usage) is None


def test_cost_of_stages_none_without_spending() -> None:
    assert cost_of_stages(PRICING, {}) is None
    zero = {("llm_a", "openai", "m"): TokenSplit(input=0, output=0)}
    assert cost_of_stages(PRICING, zero) is None


def test_repo_pricing_file_loads() -> None:
    pricing = load_pricing(Settings().data.pricing_file)
    assert pricing is not None
    assert pricing.currency == "USD"


def test_old_report_without_new_fields_parses() -> None:
    """Önbellekteki eski raporlar (Faz 25 öncesi) yeni alanlar olmadan da okunur."""
    old: dict[str, Any] = {
        "provider": "fake",
        "model": "m",
        "prompt_version": "v1",
        "rules_version": "r1",
        "schema_version": "1.0",
        "tokens_in": 1,
        "tokens_out": 2,
        "stage_latency_ms": {},
        "early_exit": False,
        "cache_hit": False,
        "degraded": False,
        "repair_attempts": 0,
        "warnings": [],
    }
    meta = ReportMeta.model_validate(old)
    assert meta.usage_estimated is False
    assert meta.cost_est is None


def test_eval_reads_configured_pricing_file(tmp_path: Path) -> None:
    from codementor.eval.runner import pricing_for

    path = tmp_path / "fiyat.yaml"
    path.write_text(
        "version: 1\nprices:\n"
        "  - {provider: openai, model: m, input_per_mtok: 1, output_per_mtok: 2}\n",
        encoding="utf-8",
    )
    settings = Settings(data={"pricing_file": path})  # type: ignore[arg-type]
    pricing = pricing_for(settings)
    assert pricing is not None
    assert pricing.prices[0].output_per_mtok == 2
