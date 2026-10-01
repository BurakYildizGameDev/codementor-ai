"""Python için Tier 1 (ADR-0015): CPython ayrıştırıcısıyla süreç içi derleme denetimi.

Kod **çalıştırılmaz** (ADR-0005): yalnızca `compile(..., PyCF_ONLY_AST)` ile sözdizimi ağacı
kurulur; bu, `import` ya da ifade değerlendirmesi yapmaz. Girdi boyutu ingest sınırlarıyla
(`limits.max_lines`, `max_bytes`) zaten küçüktür. Aşırı iç içe girdinin yol açabileceği
`RecursionError` / `MemoryError` yakalanır ve denetim atlanır.
"""

from __future__ import annotations

import ast
import warnings
from typing import Literal

from codementor.models.enums import CompilationStatus
from codementor.models.findings import Diagnostic
from codementor.models.request import NormalizedCode
from codementor.models.validation import SkipReason, Tier1Result

TOOL: Literal["python"] = "python"
_FILENAME = "<ogrenci>"


def check_python(code: NormalizedCode) -> Tier1Result:
    """Sözdizimi hatası → FAILED, yalnız uyarı (ör. geçersiz kaçış dizisi) → WARNING."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            compile(code.text, _FILENAME, "exec", flags=ast.PyCF_ONLY_AST, dont_inherit=True)
        except SyntaxError as exc:  # IndentationError/TabError dahil
            return Tier1Result(
                status=CompilationStatus.FAILED, tool=TOOL, diagnostics=[_from_error(exc)]
            )
        except (RecursionError, MemoryError, ValueError) as exc:
            return Tier1Result(
                status=CompilationStatus.SKIPPED,
                tool=TOOL,
                skip_reason=SkipReason.TOOL_ERROR,
                warnings=[f"Python derleme denetimi yapılamadı ({type(exc).__name__})."],
            )
    found = [
        Diagnostic(
            tool=TOOL,
            severity="warning",
            line=max(1, int(getattr(w, "lineno", 1) or 1)),
            column=None,
            message=f"{w.category.__name__}: {w.message}",
        )
        for w in caught
        if issubclass(w.category, SyntaxWarning | DeprecationWarning)
    ]
    status = CompilationStatus.WARNING if found else CompilationStatus.PASSED
    return Tier1Result(status=status, tool=TOOL, diagnostics=found)


def _from_error(exc: SyntaxError) -> Diagnostic:
    return Diagnostic(
        tool=TOOL,
        severity="error",
        line=max(1, exc.lineno or 1),
        column=exc.offset,
        message=f"{type(exc).__name__}: {exc.msg}",
    )
