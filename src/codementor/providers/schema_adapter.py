"""Tek Pydantic modelinden sağlayıcıya özel JSON şema varyantları (mimari §5.5.2).

Ortak dönüşümler: `$ref`/`$defs` açılır (özyinelemeli şema reddedilir), `title`/`default`
atılır, her nesnede `additionalProperties: false`, sağlayıcıların zorlamadığı kısıtlar
(`minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `maxItems` ...) çıkarılır. Bu
kısıtlar kaybolmaz: K5 (Faz 9) yanıtı aynı Pydantic modeliyle doğrular.
"""

from __future__ import annotations

import copy
import json
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
_MAX_DEPTH = 64


class SchemaAdapter:
    """Bir çıktı modelinin sağlayıcı şemaları."""

    def __init__(self, model: type[BaseModel]) -> None:
        self.model = model
        raw = model.model_json_schema()
        definitions = raw.pop("$defs", {})
        inlined = _inline(raw, definitions, ())
        self._base = _clean(inlined, depth=0, drop=_UNSUPPORTED)
        self._annotated = _clean(inlined, depth=0, drop=_DOCUMENTATION_ONLY)

    def base(self) -> Schema:
        """Satır içi, kapalı (`additionalProperties: false`) ve temizlenmiş şema."""
        schema: Schema = copy.deepcopy(self._base)
        return schema

    def ollama(self) -> Schema:
        """Ollama `format` parametresi."""
        return self.base()

    def anthropic(self) -> Schema:
        """Anthropic `output_config.format.schema`."""
        return self.base()

    def openai_strict(self) -> Schema:
        """OpenAI katı mod: her nesnede tüm alanlar `required`; opsiyonel alan `anyOf[T, null]`."""
        schema: Schema = _strict(self.base())
        return schema

    def prompt_text(self) -> str:
        """Şemayı API'de zorlayamayan sağlayıcı (DeepSeek) için prompt'a gömülecek metin."""
        # API şemayı zorlamadığı için kısıtlar (maxLength, maxItems, minimum) korunur:
        # model sınırları görsün, K5 yine de aynı Pydantic modeliyle doğrular.
        schema = json.dumps(_strict(copy.deepcopy(self._annotated)), ensure_ascii=False, indent=2)
        return (
            "Yanıtını yalnızca aşağıdaki JSON şemasına uyan tek bir JSON nesnesi olarak ver; "
            "JSON dışında metin yazma. Tüm alanlar zorunludur; değer yoksa null kullan.\n"
            f"JSON şeması:\n{schema}"
        )


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
    for key, value in node.items():
        if key in drop:
            continue
        if key == "minItems" and value not in (0, 1) and drop is _UNSUPPORTED:
            continue  # yalnızca 0/1 destekleniyor (Anthropic); gerisi K5'te doğrulanır
        if key == "properties" and isinstance(value, dict):
            cleaned[key] = {name: _clean(sub, depth + 1, drop) for name, sub in value.items()}
        else:
            cleaned[key] = _clean(value, depth + 1, drop)
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
