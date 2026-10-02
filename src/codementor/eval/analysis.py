"""Denetim precision analizi (Faz 22): yanlış pozitiflerin nereden geldiğini gösterir.

Kayıtlı sonuç dosyası üzerinde çalışır, LLM çağırmaz. §14.2 katı eşleşmesine (aynı kategori,
satır farkı ≤ 2) ek olarak:
- kategorisiz eşleşme (yalnız satır): FP'lerin ne kadarı aslında "doğru yer, yanlış kategori";
- `low` önemli tahminler hariç ölçüm: FP'ler düşük önemli önerilerden mi geliyor;
- kategori karışıklığı: katı eşleşmede kalan beklenen/tahmin çiftlerinin satırla eşleşmesi;
- örnek bazında FP/FN listesi.

Sınır: etiketler koşu anındaki değil güncel veri setinden gelir (bkz. `breakdown`).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Literal

from codementor.eval.compare import pct
from codementor.eval.metrics import AuditScores, Pair, audit_metrics, match_findings
from codementor.models.enums import AuditCategory, FindingSource, Severity
from codementor.models.eval import ExpectedFinding, Label, RunResult
from codementor.models.findings import Finding

TEXT_LIMIT = 80
FpDimension = Literal["category", "severity", "source"]


@dataclass(frozen=True)
class FindingRow:
    """Eşleşmeyen tek bulgu (FP: tahmin, FN: beklenen)."""

    sample_id: str
    line: int
    category: AuditCategory
    severity: Severity | None = None
    source: FindingSource | None = None
    text: str = ""
    confused_with: AuditCategory | None = None


@dataclass(frozen=True)
class PrecisionAnalysis:
    strict: AuditScores
    line_only: AuditScores
    without_low: AuditScores
    predicted_total: int
    expected_total: int
    confusion: dict[tuple[AuditCategory, AuditCategory], int]
    false_positives: list[FindingRow]
    false_negatives: list[FindingRow]
    missing: list[str]

    def fp_by(self, dimension: FpDimension) -> dict[str, int]:
        """FP sayısı, verilen boyuta göre (çoktan aza)."""
        counts = Counter(
            str(value)
            for row in self.false_positives
            if (value := getattr(row, dimension)) is not None
        )
        return dict(counts.most_common())


def _short(text: str) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= TEXT_LIMIT else flat[: TEXT_LIMIT - 1] + "…"


def _unmatched(
    label: Label, findings: list[Finding]
) -> tuple[list[ExpectedFinding], list[Finding]]:
    pairs = match_findings(label.expected.findings, findings)
    used_e = {id(e) for e, _ in pairs}
    used_p = {id(p) for _, p in pairs}
    return (
        [e for e in label.expected.findings if id(e) not in used_e],
        [p for p in findings if id(p) not in used_p],
    )


def _without_low(pairs: list[Pair]) -> list[Pair]:
    filtered: list[Pair] = []
    for label, result in pairs:
        report = result.report
        if report is not None:
            kept = [f for f in report.findings if f.severity is not Severity.LOW]
            report = report.model_copy(update={"findings": kept})
        filtered.append((label, result.model_copy(update={"report": report})))
    return filtered


def analyze(result: RunResult, labels: dict[str, Label]) -> PrecisionAnalysis:
    """Sonuç dosyasının precision analizi; etiketi bulunmayan örnekler `missing`'e."""
    pairs: list[Pair] = []
    missing: list[str] = []
    for sample in result.samples:
        label = labels.get(sample.id)
        if label is None:
            missing.append(sample.id)
        else:
            pairs.append((label, sample))

    confusion: Counter[tuple[AuditCategory, AuditCategory]] = Counter()
    fps: list[FindingRow] = []
    fns: list[FindingRow] = []
    predicted_total = expected_total = 0
    for label, sample in pairs:
        findings = sample.report.findings if sample.report is not None else []
        predicted_total += len(findings)
        expected_total += len(label.expected.findings)
        lost_e, lost_p = _unmatched(label, findings)
        # Katı eşleşmede kalanlar arasında aynı satır = kategori karışıklığı
        crossed = match_findings(lost_e, lost_p, ignore_category=True)
        partner_of_p = {id(p): e.category for e, p in crossed}
        partner_of_e = {id(e): p.category for e, p in crossed}
        for e, p in crossed:
            confusion[(e.category, p.category)] += 1
        fps += [
            FindingRow(
                sample.id,
                p.line_start,
                p.category,
                p.severity,
                p.source,
                _short(p.description),
                partner_of_p.get(id(p)),
            )
            for p in lost_p
        ]
        fns += [
            FindingRow(
                sample.id,
                e.line,
                e.category,
                text=_short(" ".join(x for x in (e.rule_id, e.note) if x)),
                confused_with=partner_of_e.get(id(e)),
            )
            for e in lost_e
        ]
    return PrecisionAnalysis(
        strict=audit_metrics(pairs),
        line_only=audit_metrics(pairs, ignore_category=True),
        without_low=audit_metrics(_without_low(pairs)),
        predicted_total=predicted_total,
        expected_total=expected_total,
        confusion=dict(confusion.most_common()),
        false_positives=fps,
        false_negatives=fns,
        missing=missing,
    )


# --- Markdown -----------------------------------------------------------------------------------


def _cell(value: object) -> str:
    text = "—" if value is None else str(value)
    return text.replace("|", "\\|") or "—"


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(_cell(v) for v in row) + " |" for row in rows]
    return lines


def _scores(name: str, scores: AuditScores) -> list[object]:
    return [name, pct(scores.precision), pct(scores.recall), pct(scores.f1)]


def analysis_markdown(analysis: PrecisionAnalysis) -> str:
    """Analizin Markdown dökümü (özet, FP dağılımı, karışıklık, FP/FN listeleri)."""
    a = analysis
    lines = ["## Özet", ""]
    lines += _table(
        ["Ölçüm", "P", "R", "F1"],
        [
            _scores("Katı", a.strict),
            _scores("Kategorisiz (yalnız satır)", a.line_only),
            _scores("Katı, `low` hariç", a.without_low),
        ],
    )
    lines += [
        "",
        f"Tahmin {a.predicted_total} · beklenen {a.expected_total} · "
        f"FP {len(a.false_positives)} · FN {len(a.false_negatives)}",
    ]
    if a.missing:
        lines.append(f"Etiketi bulunamayan örnekler: {', '.join(a.missing)}")
    dims: list[tuple[str, FpDimension]] = [
        ("Kategori", "category"),
        ("Önem", "severity"),
        ("Kaynak", "source"),
    ]
    lines += ["", "## Yanlış pozitif dağılımı", ""]
    lines += _table(
        ["Boyut", "Değer", "FP"],
        [[name, value, n] for name, dim in dims for value, n in a.fp_by(dim).items()],
    )
    lines += ["", "## Kategori karışıklığı", ""]
    lines += _table(
        ["Beklenen → tahmin", "n"],
        [[f"{e} → {p}", n] for (e, p), n in a.confusion.items()],
    )
    lines += ["", "## Yanlış pozitifler", ""]
    lines += _table(
        ["Örnek", "Satır", "Kategori", "Önem", "Kaynak", "Beklenen (aynı satır)", "Açıklama"],
        [
            [r.sample_id, r.line, r.category, r.severity, r.source, r.confused_with, r.text]
            for r in a.false_positives
        ],
    )
    lines += ["", "## Yanlış negatifler", ""]
    lines += _table(
        ["Örnek", "Satır", "Kategori", "Tahmin (aynı satır)", "Kural / not"],
        [[r.sample_id, r.line, r.category, r.confused_with, r.text] for r in a.false_negatives],
    )
    return "\n".join(lines) + "\n"
