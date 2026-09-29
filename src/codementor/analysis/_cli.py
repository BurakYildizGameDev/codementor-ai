"""Hata ayıklama CLI'ı: `uv run python -m codementor.analysis.extractor dosya.cs`.

Olguları, dosya ipucunu ve fonksiyon ipuçlarını JSON olarak basar. Dil uzantıdan
(`.c`, `.cpp`, `.cs` ...), motor içerikten tespit edilir. Çıktı her zaman UTF-8'dir
(Windows konsolunun cp1254 kod sayfası `→` gibi karakterleri basamaz).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from codementor.analysis.complexity_hint import compute_hint, function_hints
from codementor.ingest.errors import IngestError
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.request import LanguageHint

_BY_SUFFIX = {".c": Language.C, ".cs": Language.CSHARP} | dict.fromkeys(
    (".cpp", ".cc", ".cxx", ".hpp", ".hh"), Language.CPP
)


def _write_utf8(data: str) -> None:
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is None:
        sys.stdout.write(data)
        return
    sys.stdout.flush()
    buffer.write(data.encode("utf-8"))
    buffer.flush()


def run(argv: list[str] | None = None) -> int:
    """CLI gövdesi; çıkış kodu döner (0 başarı, 2 girdi hatası)."""
    from codementor.analysis.extractor import extract_facts

    parser = argparse.ArgumentParser(prog="python -m codementor.analysis.extractor")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        hint = LanguageHint(language=_BY_SUFFIX.get(args.path.suffix.lower()))
        code = normalize(args.path.read_bytes(), hint)
    except OSError as exc:
        print(f"Dosya okunamadı: {exc}", file=sys.stderr)
        return 2
    except IngestError as exc:
        print(f"Kod işlenemedi: {exc}", file=sys.stderr)
        return 2
    facts = extract_facts(code)
    output = {
        "language": code.language.value,
        "engine": code.engine.value,
        "facts": facts.model_dump(mode="json"),
        "hint": compute_hint(facts).model_dump(mode="json"),
        "function_hints": {
            name: hint.model_dump(mode="json") for name, hint in function_hints(facts).items()
        },
    }
    _write_utf8(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    return 0
