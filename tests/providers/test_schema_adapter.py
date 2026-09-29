"""SchemaAdapter: tek Pydantic modelinden sağlayıcı şema varyantları (mimari §5.5.2)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Literal

import pytest
from pydantic import BaseModel, Field, ValidationError

from codementor.models.llm_output import LLMAnalysisOutput, LLMSocraticOutput
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
    assert items.get("minItems") == 1  # 0/1 desteklenir ve korunur


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


def test_prompt_text_contains_schema_and_json_word() -> None:
    text = SchemaAdapter(LLMSocraticOutput).prompt_text()
    assert "JSON" in text
    assert '"guiding_questions"' in text


def test_base_returns_copies() -> None:
    adapter = SchemaAdapter(Nested)
    first = adapter.base()
    first["properties"].clear()
    assert adapter.base()["properties"]


def test_prompt_text_keeps_constraints() -> None:
    # denetim O8: DeepSeek şemayı zorlamaz; kısıtlar prompt'ta kalmalı ki model sınırları görsün
    text = SchemaAdapter(LLMSocraticOutput).prompt_text()
    assert '"maxLength": 80' in text
    assert '"maxItems": 4' in text
    assert '"title"' not in text


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
