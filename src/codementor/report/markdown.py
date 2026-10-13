"""Markdown rapor (mimari §5.7): paylaşım için."""

from __future__ import annotations

import re

from codementor.models.enums import FindingKind
from codementor.models.findings import Finding
from codementor.models.report import AnalysisReport

_SEVERITY = {"high": "🔴 yüksek", "medium": "🟠 orta", "low": "🟢 düşük"}
_STATUS = {"passed": "geçti", "warning": "uyarı", "failed": "başarısız", "skipped": "atlandı"}

_CODE_SEGMENT = re.compile(r"(```[\s\S]*?```|`[^`]*`)")


def _escape_html(text: str) -> str:
    """Serbest metindeki HTML özel karakterlerini (&, <, >) kaçışlar (Faz E: E8, D15).

    Kod blokları (```) ve satır içi kod (`…`) içi olduğu gibi korunur.
    """
    parts = _CODE_SEGMENT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(parts)


def _cell(text: str) -> str:
    escaped = _escape_html(text)
    return escaped.replace("|", "\\|").replace("\n", " ")


def _finding_table(findings: list[Finding]) -> list[str]:
    out = ["| # | Satır | Önem | Kategori | Kaynak | Açıklama |", "|---|---|---|---|---|---|"]
    for f in findings:
        lines = f"{f.line_start}" + (f"-{f.line_end}" if f.line_end else "")
        out.append(
            f"| {f.id} | {lines} | {_SEVERITY[f.severity.value]} | {f.category.value} "
            f"| {f.source.value} | {_cell(f.description)} |"
        )
    return out


def _findings(findings: list[Finding]) -> list[str]:
    """Faz 36: önce hatalar; öneriler katlanmış `<details>` içinde (GitHub/VS Code açar)."""
    if not findings:
        return []
    issues = [f for f in findings if f.kind == FindingKind.ISSUE]
    suggestions = [f for f in findings if f.kind == FindingKind.SUGGESTION]
    out = ["## Hatalar", ""]
    out += _finding_table(issues) if issues else ["Hata bulunmadı."]
    out.append("")
    if suggestions:
        out += ["<details>", f"<summary>Öneriler ({len(suggestions)})</summary>", ""]
        out += [*_finding_table(suggestions), "", "</details>", ""]
    return out


def to_markdown(report: AnalysisReport) -> str:
    """Raporu Markdown metnine çevirir. Kavram adı yalnızca ipucu seviyesi 3'te gösterilir."""
    out = ["# CodeMentor raporu", ""]
    target = _escape_html(report.question_id or "serbest mod")
    out.append(f"- **Dil / motor:** {report.language.value} / {report.engine.value}")
    out.append(f"- **Soru:** {target}")
    out.append(f"- **Derleme:** {_STATUS[report.compilation.status.value]}")
    if report.meta.early_exit:
        out.append("- **Not:** kod derlenmediği için analiz derleme aşamasında durdu.")
    if report.meta.degraded:
        out.append("- **Not:** model yanıtı doğrulanamadı; rapor statik analizle hazırlandı.")
    out.append("")

    if report.compilation.diagnostics:
        out += ["## Derleme tanıları", ""]
        out += [
            f"- {d.line}. satır ({d.severity}): {_cell(d.message)}"
            for d in report.compilation.diagnostics
        ]
        out.append("")

    if report.complexity:
        c = report.complexity
        out += ["## Karmaşıklık", "", f"- **Zaman:** {c.display_time}"]
        out.append(f"- **Bellek:** O({c.space_complexity})")
        if c.is_optimal is not None:
            out.append(f"- **Hedefe uygun mu:** {'evet' if c.is_optimal else 'hayır'}")
        if c.static_hint:
            out.append(f"- **Statik ipucu:** O({c.static_hint}) ({c.agreement})")
        out += ["", "Gerekçe:", ""] + [
            f"{i}. {_escape_html(s)}" for i, s in enumerate(c.reasoning_steps, 1)
        ]
        out.append("")

    out += _findings(report.findings)

    if report.socratic:
        s = report.socratic
        out += ["## Mentor soruları", "", f"İpucu seviyesi: {s.hint_level}", ""]
        if s.concept_revealed and s.key_flaw_concept:  # Faz C (Y6): tek kural
            out += [f"**Kavram:** {_escape_html(s.key_flaw_concept)}", ""]
        out += [f"{i}. {_escape_html(q)}" for i, q in enumerate(s.guiding_questions, 1)]
        if s.next_step_hint:
            out += ["", f"> Sonraki adım: {_escape_html(s.next_step_hint)}"]
        out.append("")

    if report.meta.warnings:
        out += ["## Notlar", ""] + [f"- {_escape_html(w)}" for w in report.meta.warnings] + [""]
    out.append(
        f"<sub>{report.analysis_id} · {report.meta.provider or 'LLM yok'} · "
        f"{report.meta.prompt_version} · {report.meta.rules_version}</sub>"
    )
    return "\n".join(out) + "\n"
