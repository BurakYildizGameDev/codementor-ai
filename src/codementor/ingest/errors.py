"""K0 giriş hataları.

Mesajlar kullanıcıya gösterilir (Türkçe); `status_code` API eşlemesi içindir.
"""

from __future__ import annotations

from typing import ClassVar, Literal

from codementor.models.enums import Language

SizeUnit = Literal["satır", "bayt", "karakter"]


class IngestError(ValueError):
    """Kod analiz için kabul edilemedi."""

    status_code: ClassVar[int] = 422


class CodeTooLargeError(IngestError):
    """Kod satır veya bayt sınırını aşıyor (mimari §5.1; API'de 413)."""

    status_code: ClassVar[int] = 413

    def __init__(self, kind: SizeUnit, actual: int, limit: int) -> None:
        super().__init__(
            f"Kod çok büyük: {actual} {kind} (en fazla {limit} {kind}). "
            "Lütfen yalnızca incelenmesini istediğiniz bölümü gönderin."
        )
        self.kind = kind
        self.actual = actual
        self.limit = limit


class EmptyCodeError(IngestError):
    """Kod boş veya yalnızca boşluk içeriyor."""

    def __init__(self) -> None:
        super().__init__("Kod boş; analiz edilecek bir şey yok.")


class InvalidEncodingError(IngestError):
    """Kod UTF-8 olarak çözülemedi ya da ikili veri içeriyor."""


class LanguageDetectionError(IngestError):
    """Dil belirlenemedi; kullanıcıdan dil/motor belirtmesi istenir (API'de 422)."""

    def __init__(self, reason: str) -> None:
        super().__init__(
            f"Kodun dili belirlenemedi ({reason}). "
            f"Lütfen dili ({', '.join(lang.value for lang in Language)}) ve varsa motoru "
            "(unity, unreal) belirtin."
        )
