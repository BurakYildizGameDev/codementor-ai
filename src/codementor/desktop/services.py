"""Masaüstünün GUI'siz yardımcıları: derleyici özeti ve rapor dışa aktarma."""

from __future__ import annotations

import json

from codementor.config import Settings
from codementor.languages import CANONICAL_SUFFIX
from codementor.models.api import CompilerStatus
from codementor.models.report import AnalysisReport
from codementor.models.validation import DownloadProgress
from codementor.report.markdown import to_markdown
from codementor.report.sarif import to_sarif
from codementor.validation.toolchain import compiler_statuses as toolchain_statuses
from codementor.validation.toolchain import get_toolchain
from codementor.validation.toolchain_install import (
    installed_zig,
    needs_update,
    platform_key,
    zig_root,
)

_MB = 1024 * 1024
_C_FAMILY = ("c", "cpp", "unreal")


def compiler_statuses(settings: Settings) -> list[CompilerStatus]:
    """`/health/ready` ile aynı derleyici özeti."""
    return [
        *toolchain_statuses(get_toolchain(settings.validation)),
        CompilerStatus(target="python", tool="CPython ayrıştırıcısı (dahili)"),
    ]


def offer_compiler_download(settings: Settings, compilers: list[CompilerStatus]) -> bool:
    """C ailesinde eksik derleyici var, zig kurulu değil ve platform için kaynak tanımlı mı."""
    validation = settings.validation
    missing = any(c.tool is None for c in compilers if c.target in _C_FAMILY)
    return (
        missing
        and platform_key() in validation.zig.sources
        and installed_zig(zig_root(validation.toolchain_dir)) is None
    )


def compiler_update_available(settings: Settings) -> bool:
    """Kurulu zig, yapılandırmadaki sürümden/kaynaktan farklıysa güncelleme düğmesi (F9)."""
    return needs_update(settings.validation)


def describe_progress(event: DownloadProgress) -> tuple[str, float | None]:
    """İlerleme olayı → (Türkçe durum metni, 0-1 oran; bilinmiyorsa None)."""
    if event.stage == "download":
        done = event.done / _MB
        if event.total:
            return f"İndiriliyor… {done:.0f} / {event.total / _MB:.0f} MB", event.done / event.total
        return f"İndiriliyor… {done:.0f} MB", None
    if event.stage == "extract":
        fraction = event.done / event.total if event.total else None
        return "Arşiv açılıyor…", fraction
    return "Derleyici denetleniyor…", None


def render_export(report: AnalysisReport, fmt: str) -> str:
    """Dışa aktarma metni: `md`, `sarif` ya da `json`."""
    if fmt == "md":
        return to_markdown(report)
    if fmt == "sarif":
        uri = f"codementor-{report.analysis_id}{CANONICAL_SUFFIX[report.language]}"
        return json.dumps(to_sarif(report, uri), ensure_ascii=False, indent=2) + "\n"
    return report.model_dump_json(indent=2) + "\n"
