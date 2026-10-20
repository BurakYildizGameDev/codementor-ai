"""Masaüstünün GUI'siz yardımcıları: derleyici özeti, rapor dışa aktarma, `ollama pull`."""

from __future__ import annotations

import json
import re
import threading
from collections.abc import Callable
from dataclasses import dataclass

from codementor.config import Settings
from codementor.languages import CANONICAL_SUFFIX
from codementor.models.api import CompilerStatus
from codementor.models.report import AnalysisReport
from codementor.models.validation import DownloadProgress
from codementor.report.markdown import to_markdown
from codementor.report.sarif import to_sarif
from codementor.validation.runner import (
    ProcessLimits,
    ProcessResult,
    find_on_path,
    run_process,
)
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

# F10: `ollama pull` — model adı harf/rakamla başlamalıdır; argv liste, kabuk yok.
OLLAMA_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
OLLAMA_PULL_TIMEOUT_S = 3600  # büyük modeller dakikalarca inebilir
_PULL_LIMITS = ProcessLimits(
    timeout_s=OLLAMA_PULL_TIMEOUT_S, memory_mb=2048, limit_address_space=False
)


class OllamaPullError(Exception):
    """`ollama pull` isteği geçersiz (eksik ollama ya da güvensiz model adı)."""


@dataclass(frozen=True)
class PullOutcome:
    """İndirme sonucu: başarılı mı, kullanıcıya gösterilecek Türkçe metin ne."""

    ok: bool
    message: str


Runner = Callable[..., ProcessResult]


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


def ollama_pull_argv(model: str, search_path: str) -> list[str]:
    """`ollama pull <model>` için sabit argv (`[mutlak yol, "pull", model]`); F10.

    Model adı `^[A-Za-z0-9._:/-]+$` dışındaysa ya da `ollama` `search_path` (PATH) içindeki
    mutlak dizinlerde yoksa `OllamaPullError` yükseltir. Kabuk kullanılmaz; çalışma dizinine
    bakılmaz (Faz A2, Y1).
    """
    name = model.strip()
    if OLLAMA_MODEL_RE.fullmatch(name) is None:
        raise OllamaPullError(
            'Geçersiz model adı: yalnız harf, rakam ve " . _ : / - " kullanılabilir.'
        )
    found = find_on_path("ollama", search_path)
    if found is None:
        raise OllamaPullError(
            "Ollama bulunamadı; kurulu olduğundan ve PATH'te olduğundan emin olun."
        )
    return [str(found), "pull", name]


def run_ollama_pull(
    model: str,
    argv: list[str],
    runner: Runner | None = None,
    cancel: threading.Event | None = None,
) -> PullOutcome:
    """Doğrulanmış `argv`'yi çalıştırır ve sonucu Türkçe özetler (F10).

    Gerçek `ollama` süreci yalnız `runner` ile başlatılır; çağıran (denetleyici) bunu arka plan
    işine verir, testler sahte bir `runner` geçirir. Hata beklenen bir sonuçtur: istisna değil,
    `PullOutcome.ok = False` döner (köprünün genel hata metni kullanıcıya anlamsız gelirdi).
    `cancel` verilirse ve tetiklenirse süreç sonlandırılır ve sonuç iptal olarak döner.
    """
    call_runner = runner or run_process
    try:
        result = call_runner(argv, "", _PULL_LIMITS, cancel=cancel)
    except TypeError:
        # Eski test runner'ları veya ek parametre almayan sahte runner'lar için yedek
        result = call_runner(argv, "", _PULL_LIMITS)
    if result.cancelled:
        return PullOutcome(False, "İndirme iptal edildi.")
    if result.error:
        return PullOutcome(False, f"İndirme başlatılamadı: {result.error}")
    if result.timed_out:
        minutes = OLLAMA_PULL_TIMEOUT_S // 60
        return PullOutcome(False, f"İndirme zaman aşımına uğradı ({minutes} dk).")
    if result.returncode != 0:
        text = result.stderr or result.stdout
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        reason = lines[-1] if lines else f"çıkış kodu {result.returncode}"
        return PullOutcome(False, f"İndirme başarısız: {reason}")
    return PullOutcome(True, f"{model} indirildi.")


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
