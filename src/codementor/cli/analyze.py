"""`codementor analyze` (mimari §10).

Çıkış kodları: 0 analiz tamam, yüksek önemli bulgu yok · 1 yüksek önemli bulgu var ·
2 derleme başarısız (erken çıkış) · 3 sistem hatası.
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
import tomllib
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape

from codementor.config import Settings, load_settings
from codementor.ingest.errors import InvalidEncodingError
from codementor.ingest.normalize import decode_source
from codementor.languages import language_for_file
from codementor.models.enums import Engine, Language, PipelineMode, Severity
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline.orchestrator import Orchestrator, PipelineError
from codementor.report.cli_render import print_report
from codementor.report.markdown import to_markdown
from codementor.report.progress import ProgressLine
from codementor.report.sarif import to_sarif
from codementor.storage.db import Database

EXIT_OK = 0
EXIT_HIGH_FINDINGS = 1
EXIT_COMPILE_FAILED = 2
EXIT_SYSTEM_ERROR = 3
MAX_FILE_BYTES = 1024 * 1024  # K0 sınırı (40 KB) ayrıca uygulanır; bu yalnızca okuma koruması
PROGRESS_TICK_S = 0.2  # canlı süre bu aralıkla yenilenir (Faz 33)


class OutputFormat(StrEnum):
    PRETTY = "pretty"
    JSON = "json"
    MD = "md"
    SARIF = "sarif"


def exit_code(report: AnalysisReport) -> int:
    """§10 çıkış kodu."""
    if report.meta.early_exit:
        return EXIT_COMPILE_FAILED
    if any(f.severity is Severity.HIGH for f in report.findings):
        return EXIT_HIGH_FINDINGS
    return EXIT_OK


def language_from_path(path: Path) -> Language | None:
    """`--language` verilmezse uzantıdan dil; `.h` C ile C++ arasında belirsiz olduğundan
    içerik tespitine bırakılır (bilinmeyen uzantı da)."""
    if path.suffix.lower() == ".h":
        return None
    return language_for_file(path)


def render(report: AnalysisReport, fmt: OutputFormat, artifact: str) -> str:
    """Metin biçimleri (`pretty` hariç)."""
    if fmt is OutputFormat.JSON:
        return report.model_dump_json(indent=2) + "\n"
    if fmt is OutputFormat.MD:
        return to_markdown(report)
    return json.dumps(to_sarif(report, artifact), ensure_ascii=False, indent=2) + "\n"


def _write_stdout(text: str) -> None:
    """Yönlendirmede (`> out.sarif`) konsol kod sayfasından bağımsız UTF-8."""
    sys.stdout.flush()
    sys.stdout.buffer.write(text.encode("utf-8"))
    sys.stdout.buffer.flush()


def _fail(console: Console, message: str) -> typer.Exit:
    console.print(f"[red]Hata:[/red] {escape(message)}")
    return typer.Exit(EXIT_SYSTEM_ERROR)


async def _run(
    settings: Settings, request: AnalysisRequest, console: Console, progress: bool
) -> AnalysisReport:
    db = Database.from_settings(settings)
    try:
        orchestrator = Orchestrator(settings, db)
        if progress:
            line = ProgressLine(started=time.perf_counter())
            orchestrator.bus.subscribe(line.on_event)
            with console.status(line.text(time.perf_counter())) as status:
                task = asyncio.ensure_future(orchestrator.analyze(request))
                while not task.done():
                    status.update(line.text(time.perf_counter()))
                    await asyncio.wait({task}, timeout=PROGRESS_TICK_S)
                return await task
        return await orchestrator.analyze(request)
    finally:
        db.close()


def analyze(
    path: Annotated[Path, typer.Argument(help="Analiz edilecek kaynak dosya.")],
    language: Annotated[Language | None, typer.Option(help="Dil (boşsa tespit edilir).")] = None,
    engine: Annotated[Engine | None, typer.Option(help="Motor (boşsa tespit edilir).")] = None,
    question: Annotated[str | None, typer.Option(help="Soru bankası kimliği.")] = None,
    session: Annotated[str | None, typer.Option(help="Oturum (ipucu merdiveni).")] = None,
    provider: Annotated[str | None, typer.Option(help="Birincil sağlayıcı.")] = None,
    mode: Annotated[PipelineMode | None, typer.Option(help="two_pass | single_pass")] = None,
    fmt: Annotated[OutputFormat, typer.Option("--format", help="Çıktı biçimi.")] = (
        OutputFormat.PRETTY
    ),
    out: Annotated[Path | None, typer.Option(help="Çıktıyı dosyaya yaz.")] = None,
    no_cache: Annotated[bool, typer.Option("--no-cache", help="Önbelleği kullanma.")] = False,
    tier1: Annotated[
        bool | None, typer.Option("--tier1/--no-tier1", help="Yerel derleyici denetimi.")
    ] = None,
) -> None:
    """Kodu denetler; kodu düzeltmez, Sokratik sorular üretir."""
    console = Console(stderr=True)
    try:
        settings = load_settings()
    except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        raise _fail(console, f"Yapılandırma okunamadı: {exc}") from exc
    if tier1:  # yerel kullanıcı kendi yapılandırmasını açabilir; istek yalnız kapatır (Faz 47)
        validation = settings.validation.model_copy(update={"tier1_enabled": True})
        settings = settings.model_copy(update={"validation": validation})
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            raise _fail(console, f"Dosya çok büyük: {path}")
        raw = path.read_bytes()
    except OSError as exc:
        raise _fail(console, f"Dosya okunamadı: {path}") from exc
    try:
        source = decode_source(raw) if raw else " "
    except InvalidEncodingError as exc:  # U+FFFD'li kodla sessizce sürmesin (Faz 50)
        raise _fail(console, f"{path.name}: {exc}") from exc
    try:
        request = AnalysisRequest(
            code=source,
            language=language or language_from_path(path),
            engine=engine,
            question_id=question,
            session_id=session,
            provider=provider,
            options=AnalysisOptions(mode=mode, tier1=tier1, use_cache=False if no_cache else None),
        )
        pretty = fmt is OutputFormat.PRETTY and out is None
        report = asyncio.run(_run(settings, request, console, progress=pretty))
    except PipelineError as exc:
        raise _fail(console, str(exc)) from exc
    except ValidationError as exc:
        raise _fail(console, f"Geçersiz istek: {exc.error_count()} hata") from exc

    if fmt is OutputFormat.PRETTY:
        target = Console(file=out.open("w", encoding="utf-8")) if out else Console()
        print_report(report, target, request.code)
    else:
        text = render(report, fmt, path.as_posix())
        if out is not None:
            out.write_text(text, encoding="utf-8", newline="\n")
        else:
            _write_stdout(text)
    raise typer.Exit(exit_code(report))
