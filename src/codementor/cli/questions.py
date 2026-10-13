"""`codementor questions list|show|validate|add|remove` komutları (mimari §10; Faz K).

CLI yalnızca `QuestionPublic` görür: ipucu merdiveni, soruya özgü kontrol maddeleri,
kavram etiketleri ve referans çözüm yolu bu modelde hiç bulunmaz.

Çıkış kodları: 0 başarı · 1 soru bulunamadı ya da bütünlük hatası (validate) · 2 geçersiz komut
satırı (Typer) ·
3 sistem hatası (bozuk yapılandırma veya veri dosyası; mimari §10).

`add`/`remove` kullanıcı sorularını `data.user_questions_dir` altında yönetir (ADR-0028);
`list`/`show` yerleşik bankayla birleşik görür, `validate` yalnız yerleşik bankayı denetler.
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

from codementor.config import DataSettings, load_settings
from codementor.models.bigo import parse_cost
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import UserQuestionDraft
from codementor.paths import resource_root
from codementor.questions._loader import DataFileError, load_model
from codementor.questions.bank import QuestionBank, QuestionNotFoundError
from codementor.questions.checklists import Checklists
from codementor.questions.user_store import UserQuestionError, delete_question, save_question
from codementor.questions.validate import DEFAULT_MIN_PER_GROUP, validate_bank

EXIT_NOT_FOUND = 1
EXIT_INVALID = 1
EXIT_SYSTEM_ERROR = 3

questions_app = typer.Typer(name="questions", no_args_is_help=True, help="Soru bankası.")

DirOption = Annotated[
    Path | None,
    typer.Option("--dir", help="Soru dizini (varsayılan: yapılandırmadaki data.questions_dir)."),
]


def _fail(message: str) -> NoReturn:
    typer.echo(f"Hata: {message}", err=True)
    raise typer.Exit(EXIT_SYSTEM_ERROR)


def _data_settings() -> DataSettings:
    try:
        return load_settings().data
    except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        _fail(f"yapılandırma okunamadı ({type(exc).__name__}): {exc}")


def _load_bank(directory: Path | None, *, include_user: bool = True) -> QuestionBank:
    """`--dir` verilirse yalnız o dizin; yoksa yerleşik banka (+ kullanıcı soruları)."""
    try:
        if directory is not None:
            return QuestionBank.load(directory)
        data = _data_settings()
        if not include_user:
            return QuestionBank.load(data.questions_dir)
        bank = QuestionBank.load_all(data)
    except DataFileError as exc:
        _fail(str(exc))
    for warning in bank.warnings:
        typer.echo(f"Uyarı: {warning}", err=True)
    return bank


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
        title = escape(q.title) + (" [dim](kendi)[/dim]" if q.origin == "user" else "")
        table.add_row(q.id, q.language, q.engine, q.difficulty, title)
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


@questions_app.command("validate")
def questions_validate(
    directory: DirOption = None,
    min_per_group: Annotated[
        int, typer.Option("--min-per-group", min=1, help="Dil/motor başına asgari soru.")
    ] = DEFAULT_MIN_PER_GROUP,
    solutions: Annotated[
        Path | None,
        typer.Option(
            "--solutions-root",
            help="Referans çözüm yollarının (private/...) çözüldüğü kök (varsayılan: kaynak kökü).",
        ),
    ] = None,
) -> None:
    """Soru bankasını denetler: şema, dil/zorluk dağılımı, kontrol listesi kapsamı, çözümler."""
    bank = _load_bank(directory, include_user=False)
    try:
        checklists = Checklists.load(load_settings().data.checklists_dir)
    except (DataFileError, ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        _fail(f"kontrol listeleri okunamadı: {exc}")
    report = validate_bank(
        bank,
        checklists,
        min_per_group=min_per_group,
        solutions_root=solutions if solutions is not None else resource_root(),
    )
    console = Console()
    for warning in report.warnings:
        console.print(f"[yellow]uyarı[/yellow] {escape(warning)}")
    for error in report.errors:
        console.print(f"[red]hata[/red] {escape(error)}")
    if report.errors:
        console.print(f"{report.question_count} soru denetlendi: {len(report.errors)} hata.")
        raise typer.Exit(EXIT_INVALID)
    console.print(f"{report.question_count} soru geçerli ({len(report.warnings)} uyarı).")


@questions_app.command("add")
def questions_add(
    file: Annotated[
        Path,
        typer.Argument(
            help="Soru YAML'ı: title, prompt, language, difficulty zorunlu; engine, constraints, "
            "expected_time, expected_space, concept_tags, hints isteğe bağlı."
        ),
    ],
) -> None:
    """Kendi sorunu ekler (kullanıcı soru dizinine kaydedilir); kimliğini yazdırır."""
    data = _data_settings()
    try:
        draft = load_model(file, UserQuestionDraft, UserQuestionError)
        taken = {q.id for q in QuestionBank.load(data.questions_dir)}
        question = save_question(draft, data.user_questions_dir, taken=taken)
    except UserQuestionError as exc:
        typer.echo(f"Hata: {exc}", err=True)
        raise typer.Exit(EXIT_INVALID) from exc
    except DataFileError as exc:
        _fail(str(exc))
    typer.echo(f"Soru eklendi: {question.id}")


@questions_app.command("remove")
def questions_remove(
    question_id: Annotated[str, typer.Argument(help="Kendi sorunun kimliği (kullanici-…).")],
) -> None:
    """Kendi eklediğin bir soruyu siler; yerleşik sorular silinemez."""
    try:
        delete_question(question_id, _data_settings().user_questions_dir)
    except UserQuestionError as exc:
        typer.echo(f"Hata: {exc}", err=True)
        raise typer.Exit(EXIT_NOT_FOUND) from exc
    typer.echo(f"Soru silindi: {question_id}")
