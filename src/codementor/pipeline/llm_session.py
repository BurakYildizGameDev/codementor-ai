"""LLM oturumu (mimari §4 adım 6-10, §5.6): bir analizdeki tüm çağrıların token, onarım ve
sağlayıcı uyarı sayaçları.

G0'da `passes.py`'den ayrıldı (dosya 400 satırın altına insin); `passes.py` aynı sınıfı
yeniden dışa aktarır, dolayısıyla `from codementor.pipeline.passes import LLMSession` çalışır.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel

from codementor.config import Settings
from codementor.log import get_logger
from codementor.models.pipeline import Stage
from codementor.models.prompts import BuiltPrompt
from codementor.models.provider import GenerationOptions, ProviderResult, TokenUsage
from codementor.models.report import TokenSplit
from codementor.models.verification import AnalysisVerification
from codementor.pipeline.events import StageTimer
from codementor.prompts.budget import estimate_messages, estimate_tokens
from codementor.providers.base import LLMProvider

log = get_logger("codementor.pipeline")


def _accumulate(current: TokenSplit | None, usage: TokenUsage) -> TokenSplit:
    """Token toplamına ekle (sayaç ilk kez görülüyorsa sıfırdan başlar)."""
    base = current or TokenSplit(input=0, output=0)
    return TokenSplit(
        input=base.input + usage.input_tokens, output=base.output + usage.output_tokens
    )


@dataclass
class LLMSession:
    """Bir analizdeki tüm LLM çağrıları: token, onarım ve sağlayıcı uyarıları birikir."""

    provider: LLMProvider
    settings: Settings
    timer: StageTimer
    tokens_in: int = 0
    tokens_out: int = 0
    repair_attempts: int = 0
    warnings: list[str] = field(default_factory=list)
    provider_name: str | None = None
    model: str | None = None
    usage_estimated: bool = False
    # Faz B: yanıt veren sağlayıcılar (fallback tespiti), LLM'in bir kısmı başarısız mı (rapor
    # önbelleğe alınmaz) ve süre sınırında kullanılacak son doğrulanmış Geçiş A sonucu
    providers: set[str] = field(default_factory=set)
    incomplete: bool = False
    checkpoint: AnalysisVerification | None = None
    checkpoint_verified: bool = True
    stage_tokens: dict[str, TokenSplit] = field(default_factory=dict)  # Faz K
    # Faz G (D6): (aşama, sağlayıcı, model) → token. Fallback'te aynı aşamanın ikinci çağrısı
    # yedeğe düşebilir; maliyet her çağrı grubunu kendi fiyatıyla hesaplar
    # (bkz. `cost.cost_of_stages`). Aşama bazlı toplam `stage_tokens`'ta kalır (rapor alanı).
    stage_usage: dict[tuple[str, str, str], TokenSplit] = field(default_factory=dict)
    # Faz I / İş 11 (ADR-0031): isteğe bağlı bağımsız doğrulama geçişi sağlayıcısı
    verify_provider: LLMProvider | None = None

    def fail_part(self, warning: str) -> None:
        """LLM'in bir kısmı başarısız: uyarı yazılır, rapor önbelleğe alınmaz."""
        self.warnings.append(warning)
        self.incomplete = True

    async def call(
        self,
        stage: Stage,
        built: BuiltPrompt,
        model: type[BaseModel],
        *,
        provider: LLMProvider | None = None,
    ) -> ProviderResult:
        with self.timer.stage(stage):
            active_provider = provider or self.provider
            result = await active_provider.generate_structured(
                built.messages, model, GenerationOptions()
            )
            usage = self._usage(built, result)
            self.tokens_in += usage.input_tokens
            self.tokens_out += usage.output_tokens
            key = (stage, result.provider, result.model)
            self.stage_usage[key] = _accumulate(self.stage_usage.get(key), usage)
            self.stage_tokens[stage] = _accumulate(self.stage_tokens.get(stage), usage)
            self.timer.add_tokens(stage, usage.input_tokens + usage.output_tokens)
        self.warnings.extend(result.warnings)
        self.provider_name, self.model = result.provider, result.model
        self.providers.add(result.provider)
        return result

    def _usage(self, built: BuiltPrompt, result: ProviderResult) -> TokenUsage:
        """Sağlayıcı token bildirmediyse yaklaşık sayım (mimari §13, `usage_estimated`)."""
        usage = result.usage
        if usage.input_tokens or usage.output_tokens:
            self.usage_estimated |= usage.estimated
            _log_calibration(estimate_messages(built.messages), usage.input_tokens)
            return usage
        self.usage_estimated = True
        return TokenUsage(
            input_tokens=estimate_messages(built.messages),
            output_tokens=estimate_tokens(result.raw_text),
            estimated=True,
        )


def _log_calibration(estimated: int, actual: int) -> None:
    """Faz G7: token tahmini (`prompts.budget`) ile sağlayıcının bildirdiği giriş token'ını
    karşılaştırır; yalnız DEBUG'a yazılır, davranışı değiştirmez.

    `ratio = gerçek / tahmin`; 1'e yakınsa `⌈karakter/3⌉` tahmini tutarlı demektir. Oran uzun
    süre 1'den uzaksa bütçe hesabı (`prompts.budget.fit_to_budget`) yeniden ayarlanmalıdır.
    """
    if estimated <= 0 or actual <= 0:  # sayı yoksa oran anlamsız (sağlayıcı bildirmedi)
        return
    log.debug(
        "token_estimate_ratio",
        estimated=estimated,
        actual=actual,
        ratio=round(actual / estimated, 3),
    )
