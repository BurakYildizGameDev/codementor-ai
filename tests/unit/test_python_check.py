"""Python Tier 1 uyarı yakalamasının yalıtımı (tam tarama #9, KALAN_ISLER iş 18)."""

from __future__ import annotations

import builtins
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from codementor.ingest.normalize import normalize
from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.validation import python_check
from codementor.validation.python_check import check_python


def _code(text: str) -> NormalizedCode:
    return normalize(text, LanguageHint(language=Language.PYTHON, engine=Engine.NONE))


CLEAN = _code("x = 1\n")
WARNED = _code('path = "C:\\d"\n')  # geçersiz kaçış dizisi → SyntaxWarning


def test_foreign_warnings_do_not_leak_into_report(monkeypatch: pytest.MonkeyPatch) -> None:
    """Derleme sırasında başka koddan (ör. başka iş parçacığı) gelen uyarı rapora girmez."""
    real_compile = builtins.compile

    def noisy(*args: Any, **kwargs: Any) -> Any:
        warnings.warn("başka bir yerin uyarısı", DeprecationWarning, stacklevel=1)
        return real_compile(*args, **kwargs)

    monkeypatch.setattr(python_check, "compile", noisy, raising=False)
    result = check_python(CLEAN)
    assert result.status is CompilationStatus.PASSED
    assert result.diagnostics == []


def test_concurrent_checks_are_isolated() -> None:
    """8 iş parçacığında 400 eşzamanlı çağrı: her sonuç kendi girdisine ait, filtreler sızmaz."""
    filters_before = list(warnings.filters)

    def run(i: int) -> tuple[bool, CompilationStatus, int]:
        warned = i % 2 == 1
        result = check_python(WARNED if warned else CLEAN)
        return warned, result.status, len(result.diagnostics)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, range(400)))

    for warned, status, count in results:
        expected = (CompilationStatus.WARNING, 1) if warned else (CompilationStatus.PASSED, 0)
        assert (status, count) == expected
    assert warnings.filters == filters_before
