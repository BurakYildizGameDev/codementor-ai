"""Tier 0'ı süre sınırlı alt süreçte koşma (Faz 59, ADR-0025; ADR-0024'ü günceller).

tree-sitter 0.25.2'de ayrıştırma süreç içinde iptal edilemez (ADR-0024); 40 KB'lık kasıtlı C#
girdisi bir iş parçacığını ~12 sn meşgul eder. `validation.tier0_isolation` açıksa ayrıştırma
`runner.run_process` ile alt süreçte koşar: zaman aşımında süreç ağacı öldürülür, bellek
sınırlıdır, kod yalnız stdin ile gider.

Süre aşımı ya da işçi hatası **error** tanısına çevrilir: politika analizi erken bitirir
(§5.2.4), statik aşama aynı girdiyi süreç içinde yeniden ayrıştırmaz. Exe'de (`sys.frozen`)
`python -m` olmadığından yalıtım yapılmaz; uyarı loglanıp süreç içinde koşulur.
"""

from __future__ import annotations

import atexit
import sys
import threading
from typing import TYPE_CHECKING

from pydantic import ValidationError

from codementor.config import ValidationSettings
from codementor.log import get_logger
from codementor.models.findings import Diagnostic
from codementor.models.request import NormalizedCode
from codementor.models.validation import Tier0Result
from codementor.validation.runner import ProcessLimits, ProcessResult, run_process
from codementor.validation.tier0 import run_tier0

if TYPE_CHECKING:  # tier0_pool bu modülün mesajlarını içe aktarır: çalışma anında döngü olmasın
    from codementor.validation.tier0_pool import Tier0WorkerPool

WORKER_MODULE = "codementor.validation.tier0_worker"
TIMEOUT_MESSAGE = (
    "Kodun sözdizimi denetimi {seconds} saniyelik süre sınırını aştı; analiz durduruldu. "
    "Kod olağandışı derecede karmaşık görünüyor; daha küçük bir parçayla yeniden dene."
)
# Alt süreç hiç başlatılamadı (çalıştırılabilir yok, Job Object kurulamadı): kod suçlanmaz
INFRA_MESSAGE = (
    "Sözdizimi denetimi bu sunucuda başlatılamadı; bu senin kodunla ilgili değil, bir "
    "yapılandırma sorunu. Analiz durduruldu; daha sonra yeniden dene."
)
STOP_WARNING = "Kodun sözdizimi denetimi güvenlik sınırında durduruldu; bu rapor eksik."
# Bellek sınırı aşımı Windows'ta erişim ihlali olarak görünür, ayırt edilemez: ortak mesaj
FAILURE_MESSAGE = (
    "Kodun sözdizimi denetimi tamamlanamadı (bellek sınırı ya da beklenmeyen bir hata); "
    "analiz güvenlik için durduruldu. Kod olağandışı derecede karmaşık olabilir; daha küçük "
    "bir parçayla yeniden dene."
)

log = get_logger("codementor.tier0")
_frozen_warned = False  # exe uyarısı her analizde değil, bir kez
_global_pool: Tier0WorkerPool | None = None
_pool_lock = threading.Lock()
_atexit_registered = False


def get_tier0_pool(settings: ValidationSettings) -> Tier0WorkerPool:
    """Süreç geneli sıcak havuz (ADR-0032); ayarlar değiştiyse eskisi kapatılıp yeniden kurulur."""
    global _global_pool, _atexit_registered
    from codementor.validation.tier0_pool import Tier0WorkerPool

    key = (settings.tier0_warm_workers, settings.tier0_memory_mb, settings.tier0_timeout_s)
    stale: Tier0WorkerPool | None = None
    with _pool_lock:
        if _global_pool is not None and _global_pool.key != key:
            stale, _global_pool = _global_pool, None
        if _global_pool is None:
            _global_pool = Tier0WorkerPool(
                settings.tier0_warm_workers,
                memory_mb=settings.tier0_memory_mb,
                timeout_s=settings.tier0_timeout_s,
            )
            if not _atexit_registered:
                atexit.register(close_tier0_pool)
                _atexit_registered = True
        pool = _global_pool
    # Kilit dışında: boştaki işçilerin kapanmasını (işçi başına ≤2 sn) diğer analizler beklemesin.
    # Eskinin meşgul işçileri bırakılınca kapanır; geçiş sırasında canlı işçi en çok 2× sınır.
    if stale is not None:
        stale.close()
    return pool


def close_tier0_pool() -> None:
    """Sıcak havuzu kapatır (süreç çıkışında `atexit` ile de çağrılır)."""
    global _global_pool
    with _pool_lock:
        pool, _global_pool = _global_pool, None
    if pool is not None:
        pool.close()


def is_frozen() -> bool:
    """PyInstaller exe'si mi (alt süreçte `python -m` yok)."""
    return bool(getattr(sys, "frozen", False))


def worker_argv() -> list[str]:
    """İşçi komutu; `-I` kullanıcı ortamını (`PYTHONPATH`, kullanıcı site) yok sayar."""
    return [sys.executable, "-I", "-m", WORKER_MODULE]


def check_syntax(code: NormalizedCode, settings: ValidationSettings) -> Tier0Result:
    """Tier 0: yalıtım açıksa alt süreçte (veya sıcak havuzda), değilse süreç içinde `run_tier0`."""
    if not settings.tier0_isolation:
        return run_tier0(code)
    if is_frozen():
        global _frozen_warned
        if not _frozen_warned:
            log.warning("tier0_isolation_unsupported", reason="frozen")
            _frozen_warned = True
        return run_tier0(code)
    if settings.tier0_warm_workers > 0:
        warm = get_tier0_pool(settings).try_check_syntax(code)
        if warm is not None:
            return warm  # None: tüm sıcak işçiler meşgul → aynı sınırlarla soğuk yol
    limits = ProcessLimits(timeout_s=settings.tier0_timeout_s, memory_mb=settings.tier0_memory_mb)
    result = run_process(worker_argv(), code.model_dump_json(), limits)
    return _parse(result, settings.tier0_timeout_s)


def _parse(result: ProcessResult, timeout_s: float) -> Tier0Result:
    if result.timed_out:
        log.warning("tier0_timeout", timeout_s=timeout_s)
        return stopped_result(TIMEOUT_MESSAGE.format(seconds=f"{timeout_s:g}"))
    if result.error:
        log.error("tier0_worker_unavailable", error=result.error)
        return stopped_result(INFRA_MESSAGE)
    if result.cancelled or result.truncated or result.returncode != 0:
        # stderr kullanıcı kodundan parça taşıyabilir: yalnız son satırın başı loglanır
        tail = result.stderr.strip().splitlines()[-1][:120] if result.stderr.strip() else ""
        log.warning(
            "tier0_worker_failed",
            returncode=result.returncode,
            cancelled=result.cancelled,
            truncated=result.truncated,
            stderr_tail=tail,
        )
        return stopped_result(FAILURE_MESSAGE)
    try:
        return Tier0Result.model_validate_json(result.stdout)
    except ValidationError:
        log.warning("tier0_worker_bad_output", stdout_bytes=len(result.stdout))
        return stopped_result(FAILURE_MESSAGE)


def stopped(result: Tier0Result) -> bool:
    """Sonuç, yalıtımın durdurma tanısı mı (süre, bellek, çökme ya da altyapı).

    D18: karar `Tier0Result.stopped` bayrağına dayanır — durdurma tanısı üreten tek yer
    `stopped_result(...)`; çağıran tanı metnine bakmaz, metin değişince sessizce bozulmaz. Metin
    karşılaştırması yalnızca bayrağı taşımayan sonuçlar için yedek olarak kalır (eski bir işçi
    sürecinden gelen JSON ya da elle kurulmuş sonuç).
    """
    if result.stopped:
        return True
    return any(
        d.message in (FAILURE_MESSAGE, INFRA_MESSAGE) or d.message.startswith("Kodun sözdizimi")
        for d in result.diagnostics
    )


def stopped_result(message: str) -> Tier0Result:
    """Yalıtımın durdurma sonucu (`stopped=True`); soğuk yol ve sıcak havuz ortak kullanır."""
    diagnostic = Diagnostic(
        tool="tree-sitter", severity="error", line=1, column=None, message=message
    )
    return Tier0Result(diagnostics=[diagnostic], stopped=True)
