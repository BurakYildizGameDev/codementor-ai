"""Rich terminal görünümü (mimari §5.7): paneller; bulgular satır numarasıyla, kod vurgulu."""

from __future__ import annotations

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from codementor.models.enums import FindingKind, Language
from codementor.models.findings import Finding
from codementor.models.report import AnalysisReport
from codementor.report.usage import usage_breakdown_label, usage_label

CONTEXT_LINES = 1
_LEXERS = {Language.C: "c", Language.CPP: "cpp", Language.CSHARP: "csharp"}
_SEVERITY_STYLE = {"high": "bold red", "medium": "yellow", "low": "green"}
_SEVERITY_TEXT = {"high": "YÜKSEK", "medium": "ORTA", "low": "DÜŞÜK"}
_STATUS_STYLE = {"passed": "green", "warning": "yellow", "failed": "bold red", "skipped": "dim"}
_STATUS_TEXT = {"passed": "geçti", "warning": "uyarı", "failed": "başarısız", "skipped": "atlandı"}


def _summary(report: AnalysisReport) -> Panel:
    status = report.compilation.status.value
    table = Table.grid(padding=(0, 2))
    table.add_row("Dil / motor", f"{report.language.value} / {report.engine.value}")
    table.add_row("Soru", report.question_id or "serbest mod")
    table.add_row("Derleme", Text(_STATUS_TEXT[status], style=_STATUS_STYLE[status]))
    if report.complexity:
        c = report.complexity
        hint = f"  (statik ipucu O({c.static_hint}), {c.agreement})" if c.static_hint else ""
        table.add_row("Zaman", Text(c.display_time + hint, style="bold"))
        table.add_row("Bellek", f"O({c.space_complexity})")
        if c.is_optimal is not None:
            table.add_row("Hedefe uygun", "evet" if c.is_optimal else "hayır")
    if report.meta.degraded:
        table.add_row("Durum", Text("statik analiz (model doğrulanamadı)", style="yellow"))
    return Panel(table, title="CodeMentor", border_style="cyan")


def _snippet(code: str, language: Language, start: int, end: int) -> Syntax:
    total = code.count("\n") + 1
    return Syntax(
        code,
        _LEXERS[language],
        line_numbers=True,
        line_range=(max(1, start - CONTEXT_LINES), min(total, end + CONTEXT_LINES)),
        highlight_lines=set(range(start, end + 1)),
        word_wrap=True,
    )


def _findings(report: AnalysisReport, code: str | None) -> list[RenderableType]:
    """Faz 36: önce hatalar, sonra soluk bir "Öneriler" başlığı altında öneriler."""
    issues = [f for f in report.findings if f.kind == FindingKind.ISSUE]
    suggestions = [f for f in report.findings if f.kind == FindingKind.SUGGESTION]
    items = _panels(report, issues, code)
    if suggestions:
        items.append(Text(f"Öneriler ({len(suggestions)})", style="bold dim"))
        items += _panels(report, suggestions, code)
    return items


def _panels(
    report: AnalysisReport, findings: list[Finding], code: str | None
) -> list[RenderableType]:
    items: list[RenderableType] = []
    for f in findings:
        severity = f.severity.value
        title = Text.assemble(
            (f"{f.id} ", "bold"),
            (f"[{_SEVERITY_TEXT[severity]}] ", _SEVERITY_STYLE[severity]),
            f"{f.line_start}. satır · {f.category.value} · {f.rule_id or f.source.value}",
        )
        body: list[RenderableType] = [Text(f.description)]
        if code is not None:
            body.insert(
                0, _snippet(code, report.language, f.line_start, f.line_end or f.line_start)
            )
        items.append(Panel(Group(*body), title=title, title_align="left", border_style="dim"))
    return items


def render_report(report: AnalysisReport, code: str | None = None) -> list[RenderableType]:
    """Raporun Rich parçaları; `code` verilirse bulgular kod parçasıyla gösterilir."""
    parts: list[RenderableType] = [_summary(report)]
    if report.compilation.diagnostics:
        diag = Table(title="Derleme tanıları", show_header=True, header_style="bold")
        diag.add_column("Satır", justify="right")
        diag.add_column("Araç")
        diag.add_column("Mesaj")
        for d in report.compilation.diagnostics:
            diag.add_row(str(d.line), d.tool, d.message)
        parts.append(diag)
    if report.complexity and report.complexity.reasoning_steps:
        steps = "\n".join(f"{i}. {s}" for i, s in enumerate(report.complexity.reasoning_steps, 1))
        parts.append(Panel(steps, title="Karmaşıklık gerekçesi", border_style="dim"))
    parts += _findings(report, code)
    if report.socratic:
        s = report.socratic
        lines = [f"{i}. {q}" for i, q in enumerate(s.guiding_questions, 1)]
        if s.next_step_hint:
            lines += ["", f"→ {s.next_step_hint}"]
        title = f"Mentor soruları (ipucu seviyesi {s.hint_level})"
        if s.hint_level >= 3:
            title += f" · {s.key_flaw_concept}"
        parts.append(Panel("\n".join(lines), title=title, border_style="magenta"))
    if report.meta.warnings:
        parts.append(Text("\n".join(f"• {w}" for w in report.meta.warnings), style="dim"))
    meta = report.meta
    footer = (
        f"{report.analysis_id} · {meta.provider or 'LLM yok'} · {meta.prompt_version}"
        f" · {usage_label(meta)}"
    )
    parts.append(Text(footer, style="dim"))
    if breakdown := usage_breakdown_label(meta):  # Faz K
        parts.append(Text(breakdown, style="dim"))
    return parts


def print_report(report: AnalysisReport, console: Console, code: str | None = None) -> None:
    """Raporu konsola basar."""
    for part in render_report(report, code):
        console.print(part)
