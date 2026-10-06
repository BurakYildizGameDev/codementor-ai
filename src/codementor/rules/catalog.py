"""Kural kataloğu: filtreleme ve `docs/rules-catalog.md` üretimi (mimari §8.2, §10)."""

from __future__ import annotations

from codementor.models.enums import Engine, FindingKind, Language, required_language
from codementor.models.rules import RuleInfo
from codementor.rules.registry import all_rules

_HEADER = """# Kural Kataloğu

> Bu dosya otomatik üretilir: `make rules-doc`
> (`uv run codementor rules doc --out docs/rules-catalog.md`). Elle düzenlemeyin.

Statik kurallar (mimari §5.3.3, §8.2). "LLM" tespitli maddeler burada değil,
`data/checklists/` altındaki kontrol listelerindedir. Bir kural `codementor.toml`
içinde `[rules] disabled = ["KURAL-ID"]` ile kapatılabilir.
"""


def rule_catalog(language: Language | None = None, engine: Engine | None = None) -> list[RuleInfo]:
    """Kurallar; filtre verilirse o dil/motordaki kodda çalışacak olanlar.

    Yalnızca motor verilirse dil motordan çıkarılır (Unity → C#, Unreal → C++);
    `none` motoru motordan bağımsız kuralları seçer.
    """
    if language is None and engine is not None:
        language = required_language(engine)
    result: list[RuleInfo] = []
    for rule in all_rules():
        if language is not None and language not in rule.languages:
            continue
        if engine is not None and rule.engines and engine not in rule.engines:
            continue
        result.append(rule.info())
    return result


def _engines(info: RuleInfo) -> str:
    return ", ".join(info.engines) if info.engines else "—"


def kind_label(info: RuleInfo) -> str:
    """Katalog ve CLI tür etiketi (Faz 52): `hata` ya da `öneri`."""
    return "öneri" if info.kind is FindingKind.SUGGESTION else "hata"


def render_catalog() -> str:
    """Katalog Markdown metni (kimliğe göre sıralı; belirleyici)."""
    rules = rule_catalog()
    lines = [
        _HEADER,
        f"Toplam: {len(rules)} kural.",
        "",
        "| ID | Başlık | Dil | Motor | Kategori | Önem | Tür |",
        "|---|---|---|---|---|---|---|",
    ]
    lines += [
        f"| {r.id} | {r.title} | {', '.join(r.languages)} | {_engines(r)} "
        f"| {r.category} | {r.severity} | {kind_label(r)} |"
        for r in rules
    ]
    notes = {rule.id: rule.catalog_note for rule in all_rules()}
    lines += ["", "## Açıklamalar", ""]
    for r in rules:
        lines += [f"### {r.id} — {r.title}", "", r.description, ""]
        if notes.get(r.id):
            lines += [f"*Kapsam ve sınırlar:* {notes[r.id]}", ""]
    return "\n".join(lines).rstrip() + "\n"
