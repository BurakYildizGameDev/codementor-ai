"""Token ve tahmini maliyet etiketleri (mimari §13, Faz 33; Faz K): CLI, masaüstü ve web aynı
metni gösterir (`web/src/lib/usage.ts`)."""

from __future__ import annotations

from codementor.models.report import ReportMeta
from codementor.storage.cache import UsageTotals

# Faz K: aşama → kullanıcıya görünen ad; sıra raporda bu sıradır
STAGE_NAMES = {"llm_a": "Analiz", "llm_v": "Doğrulama", "llm_b": "Mentor soruları"}


def format_count(value: int) -> str:
    """Binlik ayırıcı nokta: `12.400`."""
    return f"{value:,}".replace(",", ".")


def _cost(value: float) -> str:
    return f"~${value:.4f}"


def usage_label(meta: ReportMeta) -> str:
    """`1.540 token (giriş 1.200 · çıkış 340) · tahmini · ~$0.0123`; model çağrılmadıysa nedeni."""
    if not meta.tokens_in and not meta.tokens_out:
        if meta.cache_hit:
            reason = "önbellekten"
        elif meta.early_exit:
            reason = "derleme hatası; model çağrılmadı"
        elif meta.degraded:
            reason = "model yanıt vermedi"
        else:
            reason = "model çağrılmadı"
        return f"token 0 ({reason})"
    total = meta.tokens_in + meta.tokens_out
    label = (
        f"{format_count(total)} token (giriş {format_count(meta.tokens_in)} · "
        f"çıkış {format_count(meta.tokens_out)})"
    )
    if meta.usage_estimated:
        label += " · tahmini"
    if meta.cost_est is not None:
        label += f" · {_cost(meta.cost_est)}"
    return label


def usage_breakdown(meta: ReportMeta) -> list[str]:
    """Aşama başına `Analiz 1.200/340`; onarım varsa sonda `1 onarım` (Faz K).

    Onarım sayısı tüm aşamaların toplamıdır (`repair_attempts`): bir aşamaya yazılmaz, her
    aşamanın token'ı kendi onarımlarını zaten içerir.
    """
    parts: list[str] = []
    for stage, name in STAGE_NAMES.items():
        split = meta.stage_tokens.get(stage)
        if split is None or not (split.input or split.output):
            continue
        parts.append(f"{name} {format_count(split.input)}/{format_count(split.output)}")
    if parts and meta.repair_attempts:
        parts.append(f"{meta.repair_attempts} onarım")
    return parts


def usage_breakdown_label(meta: ReportMeta) -> str | None:
    """Dağılım tek satırda: `Giriş/çıkış: Analiz 1.200/340 · Mentor soruları 900/200`."""
    parts = usage_breakdown(meta)
    return f"Giriş/çıkış: {' · '.join(parts)}" if parts else None


def usage_totals_label(totals: UsageTotals) -> str:
    """`Toplam: 12 analiz · 18.400 token (giriş 15.000 · çıkış 3.400) · ~$0.0812`."""
    total = totals.tokens_in + totals.tokens_out
    label = (
        f"Toplam: {totals.analyses} analiz · {format_count(total)} token "
        f"(giriş {format_count(totals.tokens_in)} · çıkış {format_count(totals.tokens_out)})"
    )
    if totals.cost is not None:
        label += f" · {_cost(totals.cost)}"
    return label
