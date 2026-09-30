"""Markdown rapor (mimari §5.7): paylaşım için."""

from __future__ import annotations

from codementor.models.report import AnalysisReport

_SEVERITY = {"high": "🔴 yüksek", "medium": "🟠 orta", "low": "🟢 düşük"}
_STATUS = {"passed": "geçti", "warning": "uyarı", "failed": "başarısız", "skipped": "atlandı"}


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def to_markdown(report: AnalysisReport) -> str:
    """Raporu Markdown metnine çevirir. Kavram adı yalnızca ipucu seviyesi 3'te gösterilir."""
    out = ["# CodeMentor raporu", ""]
    target = report.question_id or "serbest mod"
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
        out += ["", "Gerekçe:", ""] + [f"{i}. {s}" for i, s in enumerate(c.reasoning_steps, 1)]
        out.append("")

    if report.findings:
        out += ["## Bulgular", "", "| # | Satır | Önem | Kategori | Kaynak | Açıklama |"]
        out.append("|---|---|---|---|---|---|")
        for f in report.findings:
            lines = f"{f.line_start}" + (f"-{f.line_end}" if f.line_end else "")
            out.append(
                f"| {f.id} | {lines} | {_SEVERITY[f.severity.value]} | {f.category.value} "
                f"| {f.source.value} | {_cell(f.description)} |"
            )
        out.append("")

    if report.socratic:
        s = report.socratic
        out += ["## Mentor soruları", "", f"İpucu seviyesi: {s.hint_level}", ""]
        if s.hint_level >= 3:
            out += [f"**Kavram:** {s.key_flaw_concept}", ""]
        out += [f"{i}. {q}" for i, q in enumerate(s.guiding_questions, 1)]
        if s.next_step_hint:
            out += ["", f"> Sonraki adım: {s.next_step_hint}"]
        out.append("")

    if report.meta.warnings:
        out += ["## Notlar", ""] + [f"- {w}" for w in report.meta.warnings] + [""]
    out.append(
        f"<sub>{report.analysis_id} · {report.meta.provider or 'LLM yok'} · "
        f"{report.meta.prompt_version} · {report.meta.rules_version}</sub>"
    )
    return "\n".join(out) + "\n"
