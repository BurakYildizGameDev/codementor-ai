"""`codementor questions list|show` komutları (mimari §10).

CLI yalnızca `QuestionPublic` görür: ipucu merdiveni, soruya özgü kontrol maddeleri,
kavram etiketleri ve referans çözüm yolu bu modelde hiç bulunmaz.

Çıkış kodları: 0 başarı · 1 soru bulunamadı · 2 geçersiz komut satırı (Typer) ·
3 sistem hatası (bozuk yapılandırma veya veri dosyası; mimari §10).
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Annotated, NoReturn

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.config import load_settings
from codementor.models.bigo import parse_cost
from codementor.models.enums import Difficulty, Engine, Language
from codementor.questions._loader import DataFileError
from codementor.questions.bank import QuestionBank, QuestionNotFoundError

EXIT_NOT_FOUND = 1
EXIT_SYSTEM_ERROR = 3

questions_app = typer.Typer(name="questions", no_args_is_help=True, help="Soru bankası.")

DirOption = Annotated[
    Path | None,
    typer.Option("--dir", help="Soru dizini (varsayılan: yapılandırmadaki data.questions_dir)."),
]


def _fail(message: str) -> NoReturn:
    typer.echo(f"Hata: {message}", err=True)
    raise typer.Exit(EXIT_SYSTEM_ERROR)


def _load_bank(directory: Path | None) -> QuestionBank:
    if directory is None:
        try:
            directory = load_settings().data.questions_dir
        except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
            _fail(f"yapılandırma okunamadı ({type(exc).__name__}): {exc}")
    try:
        return QuestionBank.load(directory)
    except DataFileError as exc:
        _fail(str(exc))


def _reflow(text: str) -> str:
    """YAML'daki sabit satır sonlarını kaldırır; boş satırla ayrılmış paragrafları korur."""
    paragraphs = [" ".join(p.split()) for p in text.strip().split("\n\n")]
    return "\n\n".join(p for p in paragraphs if p)


def _display_bigo(text: str) -> str:
    """`1*` → `O(1) amortize`, `n^2` → `O(n²)`."""
    value, amortized = parse_cost(text)
    return f"{value.display} amortize" if amortized else value.display


@questions_app.command("list")
def questions_list(
    language: Annotated[Language | None, typer.Option("--language", help="Dil.")] = None,
    engine: Annotated[Engine | None, typer.Option("--engine", help="Motor.")] = None,
    difficulty: Annotated[Difficulty | None, typer.Option("--difficulty", help="Zorluk.")] = None,
    directory: DirOption = None,
) -> None:
    """Soruları listeler; seçenekler birlikte (VE) uygulanır."""
    questions = _load_bank(directory).filter(language, engine, difficulty)
    console = Console()
    if not questions:
        console.print("Eşleşen soru yok.")
        return
    table = Table(title=f"Sorular ({len(questions)})")
    table.add_column("ID", no_wrap=True, style="cyan")
    table.add_column("Dil", no_wrap=True)
    table.add_column("Motor", no_wrap=True)
    table.add_column("Zorluk", no_wrap=True)
    table.add_column("Başlık", overflow="fold")
    for q in questions:
        table.add_row(q.id, q.language, q.engine, q.difficulty, escape(q.title))
    console.print(table)


@questions_app.command("show")
def questions_show(
    question_id: Annotated[str, typer.Argument(help="Soru kimliği, ör. c-hard-stack.")],
    directory: DirOption = None,
) -> None:
    """Sorunun metnini, kısıtlarını ve beklenen karmaşıklığını gösterir."""
    try:
        q = _load_bank(directory).public(question_id)
    except QuestionNotFoundError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(EXIT_NOT_FOUND) from exc

    console = Console()
    console.print(f"[bold]{escape(q.title)}[/bold]  [dim]({q.id})[/dim]")
    console.print(f"Dil: {q.language} · Motor: {q.engine} · Zorluk: {q.difficulty}\n")
    console.print(escape(_reflow(q.prompt)) + "\n")
    console.print("[bold]Kısıtlar[/bold]")
    for constraint in q.constraints:
        console.print(f"  • {escape(constraint)}")
    if q.expected is not None:
        console.print("\n[bold]Beklenen karmaşıklık[/bold]")
        for operation, complexity in q.expected.time.items():
            console.print(f"  {escape(operation)}: {_display_bigo(complexity)}")
        console.print(f"  bellek: {_display_bigo(q.expected.space)}")
