"""Referans çözüm yolunun güvenli çözümü (mimari §7.1, §12; Faz 31).

Analiz (`pipeline.stages.load_reference`) ve `codementor questions validate` aynı kuralı
kullanır: yol kaynak köküne göre çözülür (çalışma dizinine göre değil), sembolik bağlantılar
çözüldükten sonra `private/` dışına çıkamaz, boyut sınırlıdır.
"""

from __future__ import annotations

from pathlib import Path

from codementor.models.questions import REFERENCE_ROOT

MAX_REFERENCE_BYTES = 256 * 1024


class ReferenceError(OSError):
    """Referans çözüm okunamıyor; `missing` dosya hiç yoksa (dağıtımda `private/` olmaz)."""

    def __init__(self, message: str, *, missing: bool = False) -> None:
        super().__init__(message)
        self.missing = missing


def resolve_reference(relative: str, root: Path) -> Path:
    """`root` altındaki referans çözüm dosyası; kurala uymuyorsa `ReferenceError`."""
    try:
        base = root.resolve()
        allowed = (base / REFERENCE_ROOT).resolve(strict=True)
        path = (base / relative).resolve(strict=True)
    except FileNotFoundError as exc:
        raise ReferenceError("dosya yok", missing=True) from exc
    # RuntimeError: Python 3.12'de döngülü sembolik bağlantı resolve(strict=True)'da
    except (OSError, RuntimeError) as exc:
        raise ReferenceError(f"yol çözülemedi ({type(exc).__name__})") from exc
    if not path.is_relative_to(allowed):
        raise ReferenceError("private/ dışını gösteriyor")
    if not path.is_file():
        raise ReferenceError("dosya değil")
    if path.stat().st_size > MAX_REFERENCE_BYTES:
        raise ReferenceError(f"çok büyük (> {MAX_REFERENCE_BYTES // 1024} KB)")
    return path
