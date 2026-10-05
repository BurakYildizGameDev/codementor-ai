"""K0 — giriş ve normalizasyon (mimari §5.1).

- Boyut sınırları (satır/bayt; config `limits`) → `CodeTooLargeError` (413).
- UTF-8'e çözme, BOM atma; çözülemeyen bayt veya NUL → `InvalidEncodingError`.
- CRLF ve tek CR → LF; sekmeler korunur (satır/kolon doğruluğu için).
- Satırlar yalnızca `\\n` ile bölünür (tree-sitter ile aynı satır numaraları).
- LLM'e giden numaralı görünüm ve önbellek anahtarı için SHA-256.
"""

from __future__ import annotations

import hashlib

from codementor.config import LimitsSettings, get_settings
from codementor.ingest.detect import detect
from codementor.ingest.errors import (
    CodeTooLargeError,
    EmptyCodeError,
    InvalidEncodingError,
    SizeUnit,
)
from codementor.models.request import LanguageHint, NormalizedCode

_BOM = chr(0xFEFF)
_RAW_SLACK = 4  # ham girdi bu kat sınırı aşarsa çözmeden reddedilir (DoS koruması)

# Satır sonu gibi görünen ama satır bölmeyen karakterler (U+0085, U+2028, U+2029, \v, \f).
# LLM'e giden numaralı görünümde görünür kaçışa çevrilir: sahte satır numarası üretilemesin.
_INVISIBLE_BREAKS = str.maketrans(
    {chr(cp): f"\\u{cp:04x}" for cp in (0x0B, 0x0C, 0x85, 0x2028, 0x2029)}
)


_UTF16_BOMS = {b"\xff\xfe": "utf-16-le", b"\xfe\xff": "utf-16-be"}


def decode_source(raw: bytes) -> str:
    """Dosya baytlarını metne çevirir (Faz 50): UTF-8 (BOM'lu/BOM'suz) ve BOM'lu UTF-16.
    Başka kodlama sessizce U+FFFD'ye dönüşmez; Türkçe `InvalidEncodingError`."""
    codec = _UTF16_BOMS.get(raw[:2])
    try:
        if codec is not None:
            return raw[2:].decode(codec)
        return raw.decode("utf-8").removeprefix(_BOM)
    except UnicodeDecodeError as exc:
        raise InvalidEncodingError(
            f"Dosya UTF-8 değil (bayt {exc.start}); Windows-1254 gibi bir kod sayfasıyla "
            "kaydedilmiş olabilir. Dosyayı UTF-8 olarak kaydedin."
        ) from None


def _decode(raw: str | bytes) -> str:
    return raw if isinstance(raw, str) else decode_source(raw)


def split_lines(text: str) -> list[str]:
    """Metni yalnızca `\\n` ile böler; sondaki tek satır sonu ek satır sayılmaz."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def escape_invisible_breaks(line: str) -> str:
    """Satır sonu gibi görünen ama satır bölmeyen karakterleri `\\uXXXX` kaçışına çevirir."""
    return line.translate(_INVISIBLE_BREAKS)


def numbered_view(lines: list[str]) -> str:
    """`  9 | kod` biçimi; numaralar en uzun numaraya göre sağa hizalı.

    Görünmez satır ayırıcılar kaçışlanır (mimari §12: kullanıcı kodu güvenilmez).
    """
    width = len(str(len(lines)))
    return "\n".join(
        f"{i:>{width}} |" + (f" {escape_invisible_breaks(line)}" if line else "")
        for i, line in enumerate(lines, start=1)
    )


def normalize(
    raw: str | bytes,
    hint: LanguageHint | None = None,
    *,
    limits: LimitsSettings | None = None,
) -> NormalizedCode:
    """Ham kodu doğrular ve normalize eder; dil/motor `hint` yoksa sezgisel tespit edilir."""
    limits = limits or get_settings().limits
    if len(raw) > limits.max_bytes * _RAW_SLACK:  # çözmeden önce ucuz kısayol
        kind: SizeUnit = "karakter" if isinstance(raw, str) else "bayt"
        raise CodeTooLargeError(kind, len(raw), limits.max_bytes * _RAW_SLACK)

    text = _decode(raw).removeprefix(_BOM)
    if "\x00" in text:
        raise InvalidEncodingError(
            "Kod NUL karakteri içeriyor; ikili bir dosya gönderilmiş olabilir."
        )
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        raise EmptyCodeError()

    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as exc:  # ör. JSON'dan gelen tek başına surrogate (\ud800)
        raise InvalidEncodingError(
            f"Kod geçersiz bir Unicode karakteri içeriyor (konum {exc.start})."
        ) from None
    size = len(encoded)
    if size > limits.max_bytes:
        raise CodeTooLargeError("bayt", size, limits.max_bytes)
    lines = split_lines(text)
    if len(lines) > limits.max_lines:
        raise CodeTooLargeError("satır", len(lines), limits.max_lines)

    detection = detect(text, hint)
    return NormalizedCode(
        text=text,
        lines=lines,
        numbered_view=numbered_view(lines),
        language=detection.language,
        engine=detection.engine,
        sha256=hashlib.sha256(encoded).hexdigest(),
    )
