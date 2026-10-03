"""Tek Pydantic modelinden sağlayıcıya özel JSON şema varyantları (mimari §5.5.2).

Ortak dönüşümler: `$ref`/`$defs` açılır (özyinelemeli şema reddedilir), `title`/`default`
atılır, her nesnede `additionalProperties: false`. Sağlayıcıların zorlamadığı kısıtlar
(`minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `maxItems` ...) API şemasından
çıkarılır ama kaybolmaz: alan açıklamasına Türkçe not olarak eklenir ("en fazla 80 karakter")
ve K5 (Faz 9) yanıtı aynı Pydantic modeliyle doğrular. Ollama varyantı kısıtları olduğu gibi
korur: Ollama şemayı llama.cpp dilbilgisine çevirip çözümlemede zorlar.
"""

from __future__ import annotations

import copy
from typing import Any

from pydantic import BaseModel

from codementor.providers.base import ProviderConfigError

Schema = dict[str, Any]

_UNSUPPORTED = frozenset(
    {
        "minLength",
        "maxLength",
        "pattern",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "multipleOf",
        "maxItems",
        "uniqueItems",
        "title",
        "default",
        "examples",
    }
)
_DOCUMENTATION_ONLY = frozenset({"title", "default", "examples"})
# OpenAI katı modu ve Gemini uyumlu uç `minItems`'ı garanti etmiyor (Faz 28): tamamen not olur
_STRICT_UNSUPPORTED = _UNSUPPORTED | {"minItems"}
_CONSTRAINT_NOTES = {
    "minLength": "en az {} karakter",
    "maxLength": "en fazla {} karakter",
    "pattern": "biçim: {}",
    "minimum": "en az {}",
    "maximum": "en fazla {}",
    "exclusiveMinimum": "{} değerinden büyük",
    "exclusiveMaximum": "{} değerinden küçük",
    "multipleOf": "{} katı",
    "minItems": "en az {} öğe",
    "maxItems": "en fazla {} öğe",
    "uniqueItems": "öğeler benzersiz",
}
_MAX_DEPTH = 64


class SchemaAdapter:
    """Bir çıktı modelinin sağlayıcı şemaları."""

    def __init__(self, model: type[BaseModel]) -> None:
        self.model = model
        raw = model.model_json_schema()
        definitions = raw.pop("$defs", {})
        inlined = _inline(raw, definitions, ())
        self._base = _clean(inlined, depth=0, drop=_UNSUPPORTED)
        self._strict_base = _clean(inlined, depth=0, drop=_STRICT_UNSUPPORTED)
        self._annotated = _clean(inlined, depth=0, drop=_DOCUMENTATION_ONLY)

    def base(self) -> Schema:
        """Satır içi, kapalı (`additionalProperties: false`) ve temizlenmiş şema."""
        schema: Schema = copy.deepcopy(self._base)
        return schema

    def ollama(self) -> Schema:
        """Ollama `format` parametresi. Kısıtlar korunur: Ollama şemayı llama.cpp dilbilgisine
        çevirip `maxLength`/`maxItems` gibi sınırları çözümlemede zorlar; çıkarılırsa model
        sınırı aşıyor (deepseek-r1:8b ile canlı gözlendi)."""
        schema: Schema = copy.deepcopy(self._annotated)
        return schema

    def anthropic(self) -> Schema:
        """Anthropic `output_config.format.schema`."""
        return self.base()

    def openai_strict(self) -> Schema:
        """OpenAI uyumlu katı mod (Gemini, ADR-0020): her nesnede tüm alanlar `required`; opsiyonel
        alan `anyOf[T, null]`; `minItems` dahil zorlanmayan kısıtlar açıklamaya not olur."""
        schema: Schema = _strict(copy.deepcopy(self._strict_base))
        return schema


def _inline(node: Any, definitions: dict[str, Any], stack: tuple[str, ...]) -> Any:
    if len(stack) > _MAX_DEPTH:
        raise ProviderConfigError("schema", "şema çok derin")
    if isinstance(node, list):
        return [_inline(item, definitions, stack) for item in node]
    if not isinstance(node, dict):
        return node
    ref = node.get("$ref")
    if isinstance(ref, str):
        name = ref.rsplit("/", 1)[-1]
        if not ref.startswith("#/$defs/") or name not in definitions:
            raise ProviderConfigError("schema", f"çözülemeyen şema referansı: {ref}")
        if name in stack:
            raise ProviderConfigError("schema", f"özyinelemeli şema desteklenmiyor: {name}")
        merged = {**definitions[name], **{k: v for k, v in node.items() if k != "$ref"}}
        return _inline(merged, definitions, (*stack, name))
    return {key: _inline(value, definitions, stack) for key, value in node.items()}


def _clean(node: Any, depth: int, drop: frozenset[str]) -> Any:
    if depth > _MAX_DEPTH:
        raise ProviderConfigError("schema", "şema çok derin")
    if isinstance(node, list):
        return [_clean(item, depth + 1, drop) for item in node]
    if not isinstance(node, dict):
        return node
    cleaned: Schema = {}
    notes: list[str] = []
    for key, value in node.items():
        if key in drop or (
            key == "minItems" and value not in (0, 1) and drop is not _DOCUMENTATION_ONLY
        ):
            # zorlanamayan kısıt kaybolmasın: modele açıklamada söylenir (K5 yine doğrular)
            if key in _CONSTRAINT_NOTES:
                notes.append(_CONSTRAINT_NOTES[key].format(value))
            continue
        if key == "properties" and isinstance(value, dict):
            cleaned[key] = {name: _clean(sub, depth + 1, drop) for name, sub in value.items()}
        else:
            cleaned[key] = _clean(value, depth + 1, drop)
    if notes:
        prefix = f"{cleaned['description']} " if cleaned.get("description") else ""
        cleaned["description"] = f"{prefix}({'; '.join(notes)})"
    if cleaned.get("type") == "object" or "properties" in cleaned:
        cleaned["additionalProperties"] = False
        cleaned.setdefault("properties", {})
    return cleaned


def _nullable(schema: Schema) -> Schema:
    """`T` → `anyOf[T, null]` (zaten null kabul ediyorsa aynen)."""
    options = schema.get("anyOf")
    if isinstance(options, list) and any(o.get("type") == "null" for o in options):
        return schema
    if schema.get("type") == "null":
        return schema
    description = schema.pop("description", None)
    result: Schema = {"anyOf": [schema, {"type": "null"}]}
    if description is not None:
        result["description"] = description
    return result


def _strict(node: Any) -> Any:
    if isinstance(node, list):
        return [_strict(item) for item in node]
    if not isinstance(node, dict):
        return node
    result = {
        key: ({n: _strict(s) for n, s in value.items()} if key == "properties" else _strict(value))
        for key, value in node.items()
    }
    properties = result.get("properties")
    if isinstance(properties, dict):
        required = set(result.get("required", []))
        for name in properties:
            if name not in required:
                properties[name] = _nullable(properties[name])
        result["required"] = list(properties)
    return result
