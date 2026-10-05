"""OpenAI Codex CLI'yi sağlayıcı olarak kullanma (`codex exec`, ChatGPT oturumu; ADR-0017).

ADR-0012'deki CLI ajanı kuralları aynen geçerlidir (mesajlar yalnızca stdin'den, mutlak
çalıştırılabilir yolu, Faz 4 çalıştırıcısı, izin listeli ortam). Codex'e özgü olanlar:
- Araçları kapatan bir bayrak yok; `--sandbox read-only` ile dosya okuyabilir. Bu yüzden agy gibi
  yalnızca `[providers.codex] allow_tool_agent = true` ile açıkça etkinleştirilir.
- `--ignore-user-config` + `--ignore-rules`: kullanıcının `~/.codex/config.toml`'undaki MCP
  sunucuları, eklentiler ve kurallar çalışmaz (kimlik yine `CODEX_HOME`'dan okunur).
- `--ephemeral`: oturum diske yazılmaz. `--no-daemon`: paylaşılan arka plan sunucusu kullanılmaz.
- Şema dosyadan verilir (`--output-schema`, OpenAI katı biçimi); dosya ve `--cd` çalışma kökü
  her çağrıda yeni, boş bir geçici dizindir ve çağrıdan sonra silinir.
- Çıktı JSONL olay akışıdır (`--json`): son `agent_message` yanıt, `turn.completed` kullanım,
  `turn.failed` / `error` hata.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from codementor.config import CodexConfig
from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
    TokenUsage,
)
from codementor.providers._common import as_int, as_text, elapsed_ms, require_model
from codementor.providers._http import parse_json_object
from codementor.providers.base import (
    ProviderConfigError,
    ProviderError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderResponseError,
    RetryPolicy,
)
from codementor.providers.cli_agent import (
    CliTimeoutError,
    agent_limits,
    profile_env,
    render_prompt,
    resolve_executable,
    short_error,
)
from codementor.providers.schema_adapter import SchemaAdapter
from codementor.validation.runner import ProcessResult, Runner, run_process

NAME = "codex"
SCHEMA_FILE = "schema.json"
_LOGIN_HINTS = ("not logged in", "codex login", "unauthorized", "401")
_LIMIT_HINTS = ("usage limit", "rate limit", "429", "too many requests")


class CodexUsageLimitError(ProviderRateLimitError):
    """ChatGPT planının kullanım sınırı saatlerce sürer; yeniden denemek boşunadır."""

    retryable = False


def _events(stdout: str) -> list[dict[str, Any]]:
    """JSONL satırları; JSON olmayan bilgi satırları atlanır."""
    found: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except ValueError:
            continue
        if isinstance(data, dict):
            found.append(data)
    return found


def _failure(events: list[dict[str, Any]]) -> str | None:
    """`turn.failed` ya da üst düzey `error` olayının mesajı (öğe düzeyindeki uyarılar değil)."""
    for event in reversed(events):
        kind = event.get("type")
        if kind == "turn.failed":
            error = event.get("error")
            detail = error.get("message") if isinstance(error, dict) else error
            return as_text(detail) or "tur başarısız"
        if kind == "error":
            return as_text(event.get("message")) or "hata"
    return None


def _classify(detail: str) -> ProviderError:
    lowered = detail.lower()
    if any(hint in lowered for hint in _LIMIT_HINTS):
        return CodexUsageLimitError(
            NAME, f"kullanım sınırı: {short_error(detail)}", retry_after=None
        )
    if any(hint in lowered for hint in _LOGIN_HINTS):
        return ProviderConfigError(NAME, "oturum açılmamış; terminalde `codex login` çalıştırın")
    return ProviderRequestError(NAME, f"Codex hatası: {short_error(detail)}")


class CodexCliProvider:
    """`codex exec --json --output-schema` ile yapılandırılmış çıktı."""

    capabilities = ProviderCapabilities(
        native_schema=True, strict_schema=True, seed=False, local=False
    )

    def __init__(
        self,
        config: CodexConfig,
        *,
        retry: RetryPolicy | None = None,
        runner: Runner = run_process,
    ) -> None:
        self.name: str = NAME
        self.config = config
        self.retry = retry or RetryPolicy()
        self.runner = runner

    def build_argv(self, executable: str, workdir: Path, model: str) -> list[str]:
        """Sabit bayraklar, şema dosyası, çalışma kökü, model; mesaj içeriği asla argv'de değil."""
        return [
            executable,
            "--no-daemon",
            "exec",
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--json",
            "--color",
            "never",
            "--output-schema",
            str(workdir / SCHEMA_FILE),
            "--cd",
            str(workdir),
            "--model",
            model,
            "-",
        ]

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        if not self.config.allow_tool_agent:
            raise ProviderConfigError(
                NAME,
                "dosya okuyabilen ajan; kullanmak için [providers.codex] "
                "allow_tool_agent = true (ADR-0017)",
            )
        model = require_model(NAME, self.config)
        executable = resolve_executable(NAME, self.config.command)
        if not any(m.role == "user" and m.content.strip() for m in messages):
            raise ProviderConfigError(NAME, "en az bir kullanıcı mesajı gerekli")
        schema = json.dumps(SchemaAdapter(output_model).openai_strict(), ensure_ascii=False)
        stdin = render_prompt(messages)
        limits = agent_limits(self.config.timeout_s)
        start = time.perf_counter()

        async def once() -> ProviderResult:
            cancel = threading.Event()
            with tempfile.TemporaryDirectory(prefix="codementor-codex-") as tmp:
                workdir = Path(tmp)
                (workdir / SCHEMA_FILE).write_text(schema, encoding="utf-8")
                argv = self.build_argv(executable, workdir, model)
                try:
                    result = await asyncio.to_thread(
                        self.runner, argv, stdin, limits, extra_env=profile_env(), cancel=cancel
                    )
                except asyncio.CancelledError:
                    cancel.set()
                    raise
            return self._result(result, model, start)

        return await self.retry.run(once)

    def _result(self, result: ProcessResult, model: str, start: float) -> ProviderResult:
        if result.cancelled:
            raise asyncio.CancelledError  # retry/fallback'e girmemeli (Faz 19)
        if result.error is not None:
            raise ProviderConfigError(NAME, f"çalıştırılamadı ({short_error(result.error)})")
        if result.timed_out:
            raise CliTimeoutError(NAME, "zaman aşımı")
        events = _events(result.stdout)
        failure = _failure(events)
        if failure is not None:
            raise _classify(failure)
        texts = [
            as_text(item.get("text"))
            for event in events
            if event.get("type") == "item.completed"
            and isinstance(item := event.get("item"), dict)
            and item.get("type") == "agent_message"
        ]
        if not texts:
            if result.returncode not in (0, None) and result.stderr.strip():
                raise _classify(result.stderr)
            if result.truncated:
                raise ProviderResponseError(NAME, "çıktı boyutu sınırı aşıldı")
            raise ProviderResponseError(NAME, f"yanıt alınamadı (çıkış kodu {result.returncode})")
        usage: dict[str, Any] = {}
        for event in events:
            if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
                usage = event["usage"]
        text = texts[-1]
        return ProviderResult(
            raw_text=text,
            parsed=parse_json_object(text),
            usage=TokenUsage(
                input_tokens=as_int(usage.get("input_tokens")),
                output_tokens=as_int(usage.get("output_tokens")),
            ),
            latency_ms=elapsed_ms(start),
            model=model,
            finish_reason=None,
            provider=NAME,
        )
