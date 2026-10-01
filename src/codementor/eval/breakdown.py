"""Kayıtlı eval sonucunun dil/motor grubuna göre dökümü (Faz 18).

Sonuç dosyası örnek raporlarını taşıdığından metrikler LLM'e yeniden gitmeden alt kümelerde
hesaplanır. Grup: motorlu kodda motor (`unity`, `unreal`), diğerlerinde dil.

Sınırlar: maliyet (`cost_est`) hesaplanmaz (fiyat dosyası verilmez); etiketler koşu anındaki
değil güncel veri setinden gelir, etiket sonradan değişirse grup metrikleri kayıtlı genel
metriklerden farklı olabilir.
"""

from __future__ import annotations

from codementor.eval.compare import pair, pct
from codementor.eval.metrics import Pair, compute_metrics
from codementor.models.enums import Engine
from codementor.models.eval import Label, Metrics, RunResult


def group_of(label: Label) -> str:
    """Örneğin grup adı: motor varsa motor, yoksa dil."""
    return label.engine.value if label.engine is not Engine.NONE else label.language.value


def breakdown(result: RunResult, labels: dict[str, Label]) -> tuple[dict[str, Metrics], list[str]]:
    """Grup → metrikler (ilk görülme sırasıyla) ve etiketi bulunamayan örnek kimlikleri."""
    pairs: dict[str, list[Pair]] = {}
    missing: list[str] = []
    for sample in result.samples:
        label = labels.get(sample.id)
        if label is None:
            missing.append(sample.id)
            continue
        pairs.setdefault(group_of(label), []).append((label, sample))
    return {group: compute_metrics(items) for group, items in pairs.items()}, missing


def breakdown_table(groups: dict[str, Metrics]) -> str:
    """Grup başına Markdown tablo (Big-O, denetim P/R/F1, satır, sızıntı, injection)."""
    rows = [
        "| Grup | n | Big-O birebir | Denetim P / R / F1 | Satır | Sızıntı | Injection |",
        "|---|---|---|---|---|---|---|",
    ]
    for group, m in groups.items():
        cells = [
            group,
            str(m.samples),
            pct(m.complexity_time_exact_acc),
            pair(m.audit_precision, m.audit_recall, m.audit_f1),
            pct(m.line_accuracy),
            pct(m.leak_rate),
            pct(m.injection_resistance),
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows) + "\n"
