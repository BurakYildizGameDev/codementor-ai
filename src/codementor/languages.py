"""Dil ↔ dosya uzantısı tablosu (Faz 50): API SARIF artefaktı, CLI, masaüstü ve eval veri seti
aynı yerden okur. Şema değil, sabit tablodur (modeller `models/` altında kalır)."""

from __future__ import annotations

from pathlib import Path

from codementor.models.enums import Language

# Dışa aktarımda (SARIF artefakt adı, eval kod dosyası) kullanılan tek uzantı
CANONICAL_SUFFIX: dict[Language, str] = {
    Language.C: ".c",
    Language.CPP: ".cpp",
    Language.CSHARP: ".cs",
    Language.PYTHON: ".py",
    Language.HTML: ".html",
    Language.CSS: ".css",
}

# Dosya açarken tanınan uzantılar (küçük harf)
SUFFIXES: dict[str, Language] = {
    ".c": Language.C,
    ".h": Language.C,
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".hpp": Language.CPP,
    ".hh": Language.CPP,
    ".cs": Language.CSHARP,
    ".py": Language.PYTHON,
    ".pyw": Language.PYTHON,
    ".html": Language.HTML,
    ".htm": Language.HTML,
    ".css": Language.CSS,
}


def language_for_suffix(suffix: str) -> Language | None:
    """Uzantıdan dil (büyük/küçük harf duyarsız); bilinmiyorsa None."""
    return SUFFIXES.get(suffix.lower())


def language_for_file(path: str | Path) -> Language | None:
    """Dosya yolunun uzantısından dil; bilinmiyorsa None."""
    return language_for_suffix(Path(path).suffix)
