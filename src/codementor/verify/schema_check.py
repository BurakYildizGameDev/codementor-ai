"""Şema kontrolü (mimari §5.6, 1. satır): Pydantic doğrulaması + onarım için hata özeti."""

from __future__ import annotations

import json
import re
from itertools import islice
from typing import Any

from pydantic import BaseModel, ValidationError

from codementor.models.verification import SchemaCheck
from codementor.prompts.builder import repair_errors

MAX_CANDIDATES = 3  # denenecek aday blok sayısı (her json.loads doğrusal)
MAX_JSON_DEPTH_ERROR = "JSON çok derin iç içe; çözülemedi"
_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def _object_spans(text: str) -> list[tuple[int, int]]:
    """Dengeli `{...}` blokları, en dıştakiler önce; tek geçiş (§12: 4 MB yanıtta da doğrusal).
    Metin sabitlerindeki ayraçlar sayılmaz; eşsiz `}` yok sayılır."""
    spans: list[tuple[int, int]] = []
    stack: list[int] = []
    in_string = escaped = False
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif ch == '"':
            in_string = True
        elif ch == "{":
            stack.append(i)
        elif ch == "}" and stack:
            spans.append((stack.pop(), i + 1))
    return sorted(spans)[:MAX_CANDIDATES]


def extract_json(raw_text: str) -> dict[str, Any] | None:
    """Sağlayıcı ayrıştıramadıysa ham metinden JSON nesnesi çıkarır: ``` çiti ya da
    önünde/arkasında düz yazı olan ilk dengeli nesne. Bulunamazsa None."""
    candidates = [m.group(1) for m in islice(_FENCE.finditer(raw_text), MAX_CANDIDATES)]
    candidates += [raw_text[start:end] for start, end in _object_spans(raw_text)]
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except (ValueError, RecursionError):
            continue
        if isinstance(value, dict):
            return value
    return None


def check_schema[M: BaseModel](
    model: type[M], *, parsed: dict[str, Any] | None, raw_text: str
) -> tuple[M | None, SchemaCheck]:
    """`parsed` (yoksa `raw_text`'ten çıkarılan JSON) `model`'e uyuyor mu.

    Uymuyorsa `SchemaCheck.errors` onarım prompt'una hazır satırlardır; modelin yazdığı değer
    (`input_value`) bilinçli olarak yoktur (mimari §12: öğrenci metni talimat kanalına dönmesin).
    """
    extracted = False
    data = parsed
    if data is None:
        data = extract_json(raw_text)
        extracted = data is not None
    if data is None:
        return None, SchemaCheck(ok=False, errors=["(kök): yanıt bir JSON nesnesi değil"])
    try:
        value = model.model_validate(data)
    except ValidationError as exc:
        return None, SchemaCheck(ok=False, errors=repair_errors(exc), extracted=extracted)
    except RecursionError:
        return None, SchemaCheck(ok=False, errors=[MAX_JSON_DEPTH_ERROR], extracted=extracted)
    return value, SchemaCheck(ok=True, extracted=extracted)
