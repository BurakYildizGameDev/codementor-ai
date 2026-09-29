"""Derleyici çıktısını `Diagnostic` nesnelerine çevirir (mimari §5.2.3).

gcc ve clang ortak `file:line[:col]: severity: message` biçimini kullanır. Kod stdin ile
verildiği için yalnızca `<stdin>` kaynaklı satırlar alınır; stub başlığı, sistem
başlıkları, `In file included from` ve imleç (`^~~`) satırları atlanır.

Roslyn aracı (`tools/roslyn-check`) stdout'a JSON dizisi basar:
`[{"line": 1, "column": 5, "severity": "error", "id": "CS1002", "message": "..."}]`.
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal, cast

from codementor.models.findings import Diagnostic
from codementor.models.validation import DiagnosticTool

MAX_DIAGNOSTICS = 20
MAX_MESSAGE_CHARS = 500  # static_assert/#error metni kullanıcı kontrolünde

_LINE = re.compile(
    r"^<stdin>:(?P<line>\d+):(?:(?P<col>\d+):)?[ \t]*"
    r"(?P<sev>fatal error|error|warning|note):[ \t]*(?P<msg>[^\n]*)",
    re.MULTILINE,
)
_MISSING_HEADER = re.compile(r"file not found|No such file or directory")
_SEVERITY: dict[str, Literal["error", "warning", "note"]] = {
    "fatal error": "error",
    "error": "error",
    "warning": "warning",
    "note": "note",
}


def _message(raw: str) -> str:
    # Sondaki boşluk Python'da kırpılır: regex'te `.*?` + `[ \t]*$` karesel geri izler
    text = raw.rstrip(" \t\r")
    return text if len(text) <= MAX_MESSAGE_CHARS else text[:MAX_MESSAGE_CHARS] + "…"


def _capped(diags: list[Diagnostic]) -> tuple[list[Diagnostic], bool]:
    return diags[:MAX_DIAGNOSTICS], len(diags) > MAX_DIAGNOSTICS


def parse_compiler_output(
    text: str, tool: Literal["gcc", "clang"]
) -> tuple[list[Diagnostic], bool]:
    """gcc/clang stderr'ini ayrıştırır; (tanılar, üst sınıra takıldı mı)."""
    found = [
        Diagnostic(
            tool=tool,
            severity=_SEVERITY[m["sev"]],
            line=int(m["line"]),
            column=int(m["col"]) if m["col"] else None,
            message=_message(m["msg"]),
        )
        for m in _LINE.finditer(text)
    ]
    return _capped(found)


def is_missing_header(message: str) -> bool:
    """Tanı, bulunamayan bir başlık dosyasına mı ait (gcc ve clang biçimleri)."""
    return _MISSING_HEADER.search(message) is not None


def _roslyn_entry(raw: Any) -> Diagnostic:
    if not isinstance(raw, dict):
        raise ValueError("Roslyn çıktısı: öğe nesne değil")
    entry = cast(dict[str, Any], raw)
    line, column = entry.get("line"), entry.get("column")
    severity, code, message = entry.get("severity"), entry.get("id"), entry.get("message")
    if not (isinstance(line, int) and isinstance(column, int) and line >= 1 and column >= 1):
        raise ValueError("Roslyn çıktısı: geçersiz konum")
    if severity not in ("error", "warning"):
        raise ValueError("Roslyn çıktısı: geçersiz önem düzeyi")
    if not (isinstance(code, str) and isinstance(message, str)):
        raise ValueError("Roslyn çıktısı: eksik kimlik/mesaj")
    tool: DiagnosticTool = "roslyn"
    return Diagnostic(
        tool=tool,
        severity=cast(Literal["error", "warning"], severity),
        line=line,
        column=column,
        message=_message(f"{code}: {message}"),
    )


def parse_roslyn_output(text: str) -> tuple[list[Diagnostic], bool]:
    """Roslyn aracının JSON çıktısını ayrıştırır; bozuksa `ValueError`."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Roslyn çıktısı JSON değil") from exc
    if not isinstance(data, list):
        raise ValueError("Roslyn çıktısı: dizi bekleniyordu")
    return _capped([_roslyn_entry(item) for item in data])
