"""Masaüstünün GUI'siz yardımcıları: derleyici özeti ve rapor dışa aktarma."""

from __future__ import annotations

import json

from codementor.config import Settings
from codementor.models.api import CompilerStatus
from codementor.models.report import AnalysisReport
from codementor.report.markdown import to_markdown
from codementor.report.sarif import to_sarif
from codementor.validation.toolchain import get_toolchain


def compiler_statuses(settings: Settings) -> list[CompilerStatus]:
    """`/health/ready` ile aynı derleyici özeti."""
    toolchain = get_toolchain(settings.validation)
    return [
        CompilerStatus(target=target, tool=tool.name if tool else None)
        for target, tool in (
            ("c", toolchain.c),
            ("cpp", toolchain.cpp),
            ("unreal", toolchain.unreal),
            ("csharp", toolchain.csharp),
        )
    ]


def render_export(report: AnalysisReport, fmt: str) -> str:
    """Dışa aktarma metni: `md`, `sarif` ya da `json`."""
    if fmt == "md":
        return to_markdown(report)
    if fmt == "sarif":
        uri = f"codementor-{report.analysis_id}"
        return json.dumps(to_sarif(report, uri), ensure_ascii=False, indent=2) + "\n"
    return report.model_dump_json(indent=2) + "\n"
