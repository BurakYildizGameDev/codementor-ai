"""`codementor rules list|doc` komutları (mimari §10)."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.models.enums import Engine, Language
from codementor.rules.catalog import render_catalog, rule_catalog

rules_app = typer.Typer(name="rules", no_args_is_help=True, help="Statik kural kataloğu.")


@rules_app.command("list")
def rules_list(
    language: Annotated[Language | None, typer.Option("--language", help="Dil.")] = None,
    engine: Annotated[Engine | None, typer.Option("--engine", help="Motor.")] = None,
) -> None:
    """O dil/motordaki kodda çalışacak kuralları listeler."""
    rules = rule_catalog(language, engine)
    console = Console()
    if not rules:
        console.print("Eşleşen kural yok.")
        return
    table = Table(title=f"Kurallar ({len(rules)})")
    table.add_column("ID", no_wrap=True, style="cyan")
    table.add_column("Dil", no_wrap=True)
    table.add_column("Motor", no_wrap=True)
    table.add_column("Önem", no_wrap=True)
    table.add_column("Başlık", overflow="fold")
    for r in rules:
        engines = ", ".join(r.engines) if r.engines else "—"
        table.add_row(r.id, ", ".join(r.languages), engines, r.severity, escape(r.title))
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
