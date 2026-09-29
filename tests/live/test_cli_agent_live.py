"""CLI ajanlarına gerçek çağrı (`@pytest.mark.live`; ADR-0012). Abonelik kotası harcar.

- `claude_cli`: `claude` PATH'te ve model tanımlıysa.
- `agy`: model tanımlı değilse ya da oturum açılmamışsa (boş yanıt) atlanır.
"""

from __future__ import annotations

import pytest

from codementor.config import load_settings
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import ProviderConfigError, ProviderUnavailableError, build_provider
from codementor.providers.cli_agent import resolve_executable

pytestmark = [pytest.mark.live, pytest.mark.anyio]

MESSAGES = [
    ChatMessage(role="system", content="Sokratik programlama mentorusun; kodu düzeltme."),
    ChatMessage(
        role="user",
        content="Öğrenci kodu:\n  1 | int f(int *a, int n) { return a[n]; }\n"
        "Temel kavram hatasını ve yönlendirici soruları ver.",
    ),
]


@pytest.mark.parametrize("name", ["claude_cli", "agy"])
async def test_cli_agent_live(name: str) -> None:
    cfg = getattr(load_settings().providers, name)
    if not cfg.model:
        pytest.skip(f"{name}: model tanımlı değil")
    try:
        resolve_executable(name, cfg.command)
    except ProviderConfigError as exc:
        pytest.skip(str(exc))
    try:
        result = await build_provider(name).generate_structured(
            MESSAGES, LLMSocraticOutput, GenerationOptions()
        )
    except ProviderUnavailableError as exc:
        if name == "agy":
            pytest.skip(f"agy kullanılamıyor: {exc}")
        raise
    assert result.parsed is not None, result.raw_text[:300]
    LLMSocraticOutput.model_validate(result.parsed)
