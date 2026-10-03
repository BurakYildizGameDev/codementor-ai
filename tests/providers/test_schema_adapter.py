"""SchemaAdapter: tek Pydantic modelinden sağlayıcı şema varyantları (mimari §5.5.2)."""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any, Literal

import pytest
from pydantic import BaseModel, Field, ValidationError

from codementor.models.desktop import ConnectionPing
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSinglePassOutput,
    LLMSocraticOutput,
    LLMVerifyOutput,
)
from codementor.providers import ProviderConfigError
from codementor.providers.schema_adapter import SchemaAdapter


class Inner(BaseModel):
    label: str = Field(max_length=10, title="Etiket")
    score: int | None = Field(default=None, ge=0, le=5)


class Nested(BaseModel):
    kind: Literal["a", "b"]
    items: list[Inner] = Field(min_length=1, max_length=3)
    extra: Inner | None = None
    note: str = "varsayılan"


class Node(BaseModel):
    value: int
    children: list[Node] = []


MODELS = [LLMAnalysisOutput, LLMSocraticOutput, Nested]
UNSUPPORTED = {"minLength", "maxLength", "pattern", "minimum", "maximum", "maxItems", "title"}


def _objects(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        if node.get("type") == "object" or "properties" in node:
            yield node
        for value in node.values():
            yield from _objects(value)
    elif isinstance(node, list):
        for item in node:
            yield from _objects(item)


def _keys(node: Any) -> set[str]:
    """Şemadaki anahtar sözcükler; `properties` altındaki alan adları sayılmaz."""
    found: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            found.add(key)
            children = (
                value.values() if key == "properties" and isinstance(value, dict) else [value]
            )
            for child in children:
                found |= _keys(child)
    elif isinstance(node, list):
        for item in node:
            found |= _keys(item)
    return found


@pytest.mark.parametrize("model", MODELS, ids=lambda m: m.__name__)
def test_openai_strict_all_required_and_closed(model: type[BaseModel]) -> None:
    schema = SchemaAdapter(model).openai_strict()
    objects = list(_objects(schema))
    assert objects
    for obj in objects:
        assert obj["additionalProperties"] is False
        assert set(obj["required"]) == set(obj["properties"])


@pytest.mark.parametrize("variant", ["ollama", "anthropic", "openai_strict"])
@pytest.mark.parametrize("model", MODELS, ids=lambda m: m.__name__)
def test_every_variant_closed_and_ref_free(model: type[BaseModel], variant: str) -> None:
    schema = getattr(SchemaAdapter(model), variant)()
    text = repr(schema)
    assert "$ref" not in text
    assert "$defs" not in text
    for obj in _objects(schema):
        assert obj["additionalProperties"] is False


def test_optional_becomes_null_union() -> None:
    schema = SchemaAdapter(Nested).openai_strict()
    extra = schema["properties"]["extra"]
    assert {"type": "null"} in extra["anyOf"]
    note = schema["properties"]["note"]  # varsayılanlı alan: katı modda null da kabul
    assert note["anyOf"] == [{"type": "string"}, {"type": "null"}]
    kind = schema["properties"]["kind"]  # zaten zorunlu: değişmez
    assert kind["enum"] == ["a", "b"]


def test_non_strict_variants_keep_required_as_model() -> None:
    schema = SchemaAdapter(Nested).anthropic()
    assert set(schema["required"]) == {"kind", "items"}


def test_refs_inlined() -> None:
    schema = SchemaAdapter(Nested).anthropic()
    items = schema["properties"]["items"]["items"]
    assert items["properties"]["label"] == {
        "type": "string",
        "description": "(en fazla 10 karakter)",
    }
    assert "$defs" not in schema


def test_recursive_schema_rejected() -> None:
    with pytest.raises(ProviderConfigError, match="özyinelemeli"):
        SchemaAdapter(Node)


@pytest.mark.parametrize("variant", ["anthropic", "openai_strict"])
def test_unsupported_keywords_removed(variant: str) -> None:
    schema = getattr(SchemaAdapter(Nested), variant)()
    assert not (UNSUPPORTED & _keys(schema))
    assert "default" not in repr(schema)
    items = schema["properties"]["items"]
    if variant == "anthropic":
        assert items.get("minItems") == 1  # Anthropic 0/1'i destekler, korunur


def test_openai_strict_drops_min_items_into_description() -> None:
    """Faz 28: OpenAI katı modu (ve Gemini uyumlu uç) `minItems`'ı garanti etmiyor; şemada
    bırakmak 400 riski. Kısıt açıklamaya not olur, K5 Pydantic ile yine doğrular."""
    schema = SchemaAdapter(Nested).openai_strict()
    assert "minItems" not in _keys(schema)
    assert "en az 1 öğe" in schema["properties"]["items"]["description"]
    socratic = SchemaAdapter(LLMSocraticOutput).openai_strict()
    assert "minItems" not in _keys(socratic)


def test_property_named_like_keyword_is_kept() -> None:
    class Weird(BaseModel):
        title: str
        default: int

    schema = SchemaAdapter(Weird).openai_strict()
    assert set(schema["properties"]) == {"title", "default"}


def test_pydantic_still_validates_constraints() -> None:
    # kısıtlar şemadan çıksa da doğrulama modelde kalır (K5 bu modeli kullanır)
    with pytest.raises(ValidationError):
        LLMSocraticOutput.model_validate(
            {"key_flaw_concept": "x" * 81, "guiding_questions": ["?"], "next_step_hint": None}
        )


def test_base_returns_copies() -> None:
    adapter = SchemaAdapter(Nested)
    first = adapter.base()
    first["properties"].clear()
    assert adapter.base()["properties"]


def test_ollama_keeps_constraints() -> None:
    # Ollama şemayı dilbilgisine çevirip sınırları zorlar; çıkarılınca deepseek-r1 sınırı aştı
    schema = SchemaAdapter(LLMSocraticOutput).ollama()
    assert schema["properties"]["key_flaw_concept"]["maxLength"] == 80
    assert schema["properties"]["guiding_questions"]["maxItems"] == 4
    assert "title" not in repr(schema)


def test_dropped_constraints_become_description_notes() -> None:
    # API'nin zorlamadığı sınırlar modele açıklamada iletilir (Claude CLI canlı denemesi)
    props = SchemaAdapter(LLMSocraticOutput).anthropic()["properties"]
    assert props["key_flaw_concept"]["description"] == "(en fazla 80 karakter)"
    assert "en fazla 4 öğe" in props["guiding_questions"]["description"]
    hint = props["next_step_hint"]["anyOf"][0]
    assert hint["description"] == "(en fazla 300 karakter)"


# Faz 28: OpenAI katı modunda (Gemini uyumlu uç da aynı biçimi alır) belgelenen anahtar sözcükler
_STRICT_ALLOWED = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "enum",
    "anyOf",
    "description",
    "const",
}
LLM_MODELS = [
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSocraticOutput,
    LLMSinglePassOutput,
    LLMVerifyOutput,
    ConnectionPing,
]


@pytest.mark.parametrize("model", LLM_MODELS, ids=lambda m: m.__name__)
def test_every_llm_schema_is_valid_strict_schema(model: type[BaseModel]) -> None:
    """Sağlayıcıya giden her gerçek şema: kök nesne, yalnız izinli anahtar sözcükler, her
    nesne kapalı ve tüm alanları zorunlu, `anyOf` yalnız `[T, null]`, şema adı geçerli."""
    schema = SchemaAdapter(model).openai_strict()
    assert schema["type"] == "object"
    assert "anyOf" not in schema
    assert _keys(schema) <= _STRICT_ALLOWED, _keys(schema) - _STRICT_ALLOWED
    for obj in _objects(schema):
        assert obj["additionalProperties"] is False
        assert obj["required"] == list(obj["properties"])
    for union in _unions(schema):
        assert len(union) == 2
        assert {"type": "null"} in union
    assert re.fullmatch(r"[A-Za-z0-9_-]{1,64}", model.__name__)


def _unions(node: Any) -> Iterator[list[Any]]:
    if isinstance(node, dict):
        if isinstance(node.get("anyOf"), list):
            yield node["anyOf"]
        for value in node.values():
            yield from _unions(value)
    elif isinstance(node, list):
        for item in node:
            yield from _unions(item)
