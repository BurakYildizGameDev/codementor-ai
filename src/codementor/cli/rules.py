"""`codementor rules list|doc` komutları (mimari §10)."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.config import load_settings
from codementor.models.enums import Engine, Language
from codementor.rules.catalog import kind_label, render_catalog, rule_catalog

rules_app = typer.Typer(name="rules", no_args_is_help=True, help="Statik kural kataloğu.")


def _disabled_rules() -> set[str] | None:
    """Yapılandırmada kapatılan kurallar; yapılandırma okunamazsa None (liste yine basılır)."""
    try:
        return set(load_settings().rules.disabled)
    except (ValidationError, tomllib.TOMLDecodeError, OSError):
        return None


@rules_app.command("list")
def rules_list(
    language: Annotated[Language | None, typer.Option("--language", help="Dil.")] = None,
    engine: Annotated[Engine | None, typer.Option("--engine", help="Motor.")] = None,
) -> None:
    """O dil/motordaki kodda çalışacak kuralları listeler; `[rules] disabled`'dakiler "kapalı"."""
    rules = rule_catalog(language, engine)
    console = Console()
    disabled = _disabled_rules()
    if not rules:
        console.print("Eşleşen kural yok.")
        return
    table = Table(title=f"Kurallar ({len(rules)})")
    table.add_column("ID", no_wrap=True, style="cyan")
    table.add_column("Dil", no_wrap=True)
    table.add_column("Motor", no_wrap=True)
    table.add_column("Önem", no_wrap=True)
    table.add_column("Tür", no_wrap=True)  # Faz 52: hata / öneri
    table.add_column("Durum", no_wrap=True)  # Faz C (D20)
    table.add_column("Başlık", overflow="fold")
    for r in rules:
        engines = ", ".join(r.engines) if r.engines else "—"
        state = "—" if disabled is None else "[red]kapalı[/red]" if r.id in disabled else "açık"
        table.add_row(
            r.id,
            ", ".join(r.languages),
            engines,
            r.severity,
            kind_label(r),
            state,
            escape(r.title),
        )
    console.print(table)


@rules_app.command("doc")
def rules_doc(
    out: Annotated[Path, typer.Option("--out", help="Yazılacak Markdown dosyası.")] = Path(
        "docs/rules-catalog.md"
    ),
) -> None:
    """Kural kataloğunu Markdown olarak üretir."""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_catalog(), encoding="utf-8", newline="\n")
    typer.echo(f"Yazıldı: {out}")
