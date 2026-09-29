"""`codementor` komut satırı girişi."""

from __future__ import annotations

import typer

from codementor import __version__

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
