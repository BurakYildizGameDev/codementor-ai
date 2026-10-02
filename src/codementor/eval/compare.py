"""Koşu karşılaştırması (mimari §14.3): sonuç dosyalarından Markdown tablo."""

from __future__ import annotations

from pathlib import Path

from codementor.models.eval import RunResult

HEADERS = (
    "Koşu",
    "Mod",
    "Ablasyon",
    "Örnek",
    "Şema (ilk / onarım sonrası)",
    "Erken çıkış P / R",
    "Big-O birebir / sınıf",
    "Denetim P / R / F1",
    "Satır doğruluğu",
    "Sızıntı",
    "Injection direnci",
    "p50 / p95 (sn)",
    "Token ort.",
)


def load_results(paths: list[Path]) -> list[RunResult]:
    """Sonuç dosyaları, başlangıç zamanına göre sıralı."""
    results = [RunResult.model_validate_json(p.read_text(encoding="utf-8")) for p in paths]
    return sorted(results, key=lambda r: r.config.started_at)


def pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.0f}%"


def pair(*values: float | None) -> str:
    return " / ".join(pct(v) for v in values)


def seconds(value: float | None) -> str:
    return "—" if value is None else f"{value / 1000:.1f}"


def tokens(value: float | None) -> str:
    return "—" if value is None else f"{value:.0f}"


def _label(result: RunResult) -> str:
    config = result.config
    if config.static_only:
        return "Yalnızca statik (LLM yok)"
    return f"{config.provider} / {config.model or '?'}"


def row(result: RunResult) -> list[str]:
    """Bir koşunun tablo satırı."""
    m, c = result.metrics, result.config
    return [
        _label(result),
        c.mode,
        ", ".join(c.ablations) or "—",
        f"{m.samples} ({c.split})" + ("" if c.reviewed_only else " ⚠ incelenmemiş"),
        pair(m.schema_valid_first_try, m.schema_valid_after_repair),
        pair(m.early_exit_precision, m.early_exit_recall),
        pair(m.complexity_time_exact_acc, m.complexity_time_class_acc),
        pair(m.audit_precision, m.audit_recall, m.audit_f1),
        pct(m.line_accuracy),
        pct(m.leak_rate),
        pct(m.injection_resistance),
        f"{seconds(m.latency_p50_ms)} / {seconds(m.latency_p95_ms)}",
        tokens(m.tokens_mean),
    ]


def compare_table(results: list[RunResult]) -> str:
    """Markdown karşılaştırma tablosu + sürüm dipnotu."""
    lines = [
        "| " + " | ".join(HEADERS) + " |",
        "|" + "|".join("---" for _ in HEADERS) + "|",
    ]
    lines += ["| " + " | ".join(row(r)) + " |" for r in results]
    versions = sorted(
        {
            (r.config.prompt_version, r.config.rules_version, r.config.schema_version)
            for r in results
        }
    )
    lines.append("")
    lines += [f"Sürümler: prompt {p} · kurallar {k} · şema {s}" for p, k, s in versions]
    splits = {r.config.split for r in results}
    if len(splits) > 1:
        lines.append(
            "⚠ Tabloda farklı bölümler (dev/test) karışık; satırlar doğrudan kıyaslanamaz."
        )
    return "\n".join(lines) + "\n"
