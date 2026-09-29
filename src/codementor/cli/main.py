"""`codementor` komut satırı girişi."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from codementor import __version__
from codementor.cli.questions import questions_app
from codementor.cli.rules import rules_app
from codementor.models.schemas import export_schemas

app = typer.Typer(name="codementor", no_args_is_help=True, add_completion=False)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"codementor {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True, help="Sürümü göster."
    ),
) -> None:
    """CodeMentor AI — kodu düzeltmeyen, sorgulatan mentor."""


schema_app = typer.Typer(name="schema", no_args_is_help=True, help="JSON şema işlemleri.")
app.add_typer(schema_app)
app.add_typer(questions_app)
app.add_typer(rules_app)


@schema_app.command("export")
def schema_export(
    out: Annotated[Path, typer.Option("--out", help="Şemaların yazılacağı dizin.")] = Path(
        "schemas"
    ),
) -> None:
    """Rapor ve LLM çıktı modellerinin JSON şemalarını üretir."""
    for path in export_schemas(out):
        typer.echo(f"yazıldı: {path}")
