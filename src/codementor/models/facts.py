"""Statik olgu modelleri (mimari §5.3.1) ve karmaşıklık ipucu (§5.3.2).

Olgular tree-sitter çıkarıcısı (Faz 5) tarafından doldurulur; kurallar (Faz 6)
ve prompt oluşturucu (Faz 8) bunları okur.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from codementor.models._base import StrictModel
from codementor.models.bigo import parse_bigo, parse_cost
from codementor.models.enums import AllocationKind, DeallocationKind, LoopBound


class FunctionFact(StrictModel):
    name: str
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)
    parameters: list[str] = Field(default_factory=list)
    lifecycle: str | None = Field(
        default=None, description="Motor yaşam döngüsü adı (Update, Tick, OnEnable ...)"
    )
    is_hot_path: bool = Field(
        default=False, description="Update/FixedUpdate/LateUpdate/OnGUI/Tick gövdesi"
    )


class LoopFact(StrictModel):
    kind: Literal["for", "while", "do", "foreach"]
    line: int = Field(ge=1)
    depth: int = Field(ge=1, description="İç içe derinlik; en dış döngü 1")
    bound: LoopBound
    function: str | None = None
    parent_line: int | None = Field(default=None, description="Doğrudan dıştaki döngünün satırı")
    parent_index: int | None = Field(
        default=None, ge=0, description="Dıştaki döngünün `loops` listesindeki indeksi"
    )
    counter_outer: bool = Field(
        default=False,
        description="İç döngü sayacı dış döngüde sıfırlanmıyor (two-pointer/amortize şüphesi)",
    )


class RecursionFact(StrictModel):
    function: str
    self_call_count: int = Field(ge=1)
    branching_factor: int = Field(ge=1, description="Gövdedeki öz-çağrı sayısı")
    lines: list[int] = Field(default_factory=list)
    halving: bool = Field(
        default=False, description="Tüm öz-çağrı argümanları yarılama içeriyor (`/ 2`, `mid`)"
    )


class CallFact(StrictModel):
    name: str
    line: int = Field(ge=1)
    loop_depth: int = Field(ge=0)
    known_cost: str | None = Field(default=None, description="data/call_costs.yaml değeri")
    function: str | None = None
    loop_line: int | None = Field(default=None, description="En içteki döngünün satırı")
    loop_index: int | None = Field(
        default=None, ge=0, description="En içteki döngünün `loops` listesindeki indeksi"
    )


class AllocationFact(StrictModel):
    kind: AllocationKind
    line: int = Field(ge=1)
    loop_depth: int = Field(default=0, ge=0)
    in_hot_path: bool = False
    function: str | None = None


class DeallocationFact(StrictModel):
    kind: DeallocationKind
    line: int = Field(ge=1)
    function: str | None = None


class SymbolRef(StrictModel):
    name: str
    line: int = Field(ge=1)


class EngineSymbols(StrictModel):
    uproperty_fields: list[SymbolRef] = Field(default_factory=list)
    uobject_fields: list[SymbolRef] = Field(default_factory=list)
    event_subscriptions: list[SymbolRef] = Field(default_factory=list)
    has_on_enable: bool = False
    has_on_disable: bool = False


class CodeFacts(StrictModel):
    """Bir kaynak dosyadan çıkarılan tüm olgular."""

    functions: list[FunctionFact] = Field(default_factory=list)
    loops: list[LoopFact] = Field(default_factory=list)
    recursion: list[RecursionFact] = Field(default_factory=list)
    calls: list[CallFact] = Field(default_factory=list)
    allocations: list[AllocationFact] = Field(default_factory=list)
    deallocations: list[DeallocationFact] = Field(default_factory=list)
    engine_symbols: EngineSymbols = Field(default_factory=EngineSymbols)
    warnings: list[str] = Field(default_factory=list, description="Kullanıcıya dönük notlar")


class ComplexityHint(StrictModel):
    """Statik karmaşıklık ipucu. Gerçek değil ipucudur; K5'te LLM ile uzlaştırılır."""

    value: str = Field(description="Kanonik Big-O (parse_bigo ile normalize edilir)")
    confidence: Literal["low", "medium", "high"]
    basis: list[str] = Field(description="İpucunun dayandığı gözlemler")
    function: str | None = Field(default=None, description="Fonksiyon ipucuysa fonksiyon adı")
    exponential_suspect: bool = Field(
        default=False, description="Dallanma faktörü > 1 olan özyineleme (EXPONENTIAL_SUSPECT)"
    )

    @field_validator("value")
    @classmethod
    def _normalize_value(cls, v: str) -> str:
        return parse_bigo(v).canonical


class CallCostTable(StrictModel):
    """`data/call_costs.yaml` şeması (mimari §5.3.2): dil → çağrı adı → maliyet."""

    c: dict[str, str] = Field(default_factory=dict)
    cpp: dict[str, str] = Field(default_factory=dict)
    csharp: dict[str, str] = Field(default_factory=dict)
    python: dict[str, str] = Field(default_factory=dict)

    @field_validator("c", "cpp", "csharp", "python")
    @classmethod
    def _valid_costs(cls, table: dict[str, str]) -> dict[str, str]:
        for name, cost in table.items():
            if not name.strip():
                raise ValueError("boş çağrı adı")
            parse_cost(cost)  # geçersizse BigOParseError (ValueError)
        return table
