"""`codementor eval ...` (mimari §10, §14).

`run`: bir bölümü (dev/test) çalıştırır, `eval/results/`'a yazar. `test` bölümü yalnızca
`--final` ile çalışır (prompt ayarı yalnızca dev ile; test en sonda bir kez).
`compare`: sonuç dosyalarından Markdown tablo. `breakdown` / `analyze`: kayıtlı sonucun
grup dökümü ve precision analizi (Faz 18/22). `check-drafts`: taslak etiketleri statik analizle
karşılaştırır. `promote`: incelenen taslağı bir bölüme taşır.
"""

from __future__ import annotations

import asyncio
import tomllib
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.cli.errors import system_errors
from codementor.config import Settings, load_settings
from codementor.eval.analysis import analysis_markdown, analyze
from codementor.eval.breakdown import breakdown, breakdown_table
from codementor.eval.compare import compare_table, load_results
from codementor.eval.dataset import (
    DATASET_DIR,
    DRAFT,
    DatasetError,
    check_disjoint,
    dataset_version,
    load_split,
    promote,
)
from codementor.eval.parts import parse_part, select_part
from codementor.eval.review import DraftCheck, check_draft
from codementor.eval.runner import ABLATIONS, run_eval, save_result
from codementor.models.enums import Language, PipelineMode
from codementor.models.eval import Label, RunResult, SampleResult, Split

EXIT_PROBLEMS = 1
EXIT_USAGE = 2
EXIT_SYSTEM_ERROR = 3
RESULTS_DIR = Path("eval/results")

eval_app = typer.Typer(name="eval", no_args_is_help=True, help="Değerlendirme (eval).")


def _settings(console: Console) -> Settings:
    try:
        return load_settings()
    except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        console.print(f"[red]Hata:[/red] Yapılandırma okunamadı: {escape(str(exc))}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc


@eval_app.command("run")
def run(
    split: Annotated[str, typer.Option(help="dev | test")],
    provider: Annotated[
        str | None, typer.Option(help="Sağlayıcı (varsayılan: yapılandırma).")
    ] = None,
    mode: Annotated[
        PipelineMode, typer.Option(help="two_pass | single_pass")
    ] = PipelineMode.TWO_PASS,
    static_only: Annotated[
        bool, typer.Option("--static-only", help="LLM'siz taban çizgisi.")
    ] = False,
    ablate: Annotated[
        list[str] | None, typer.Option(help=f"Ablasyon: {', '.join(ABLATIONS)}")
    ] = None,
    limit: Annotated[int | None, typer.Option(help="İlk N örnek (deneme için).")] = None,
    language: Annotated[
        list[Language] | None,
        typer.Option(
            help="Yalnızca bu dil(ler): c, cpp, csharp, python, html, css "
            "(csharp Unity'yi, cpp Unreal'ı da kapsar)."
        ),
    ] = None,
    part: Annotated[
        str | None,
        typer.Option(
            help="Dengeli parça, ör. 1/4: bölüm dil/motor ve örnek türüne göre orantılı "
            "n parçaya ayrılır, yalnız k. parça koşulur (canlı koşu bütçesi)."
        ),
    ] = None,
    final: Annotated[
        bool, typer.Option("--final", help="test bölümünü çalıştırmaya izin ver.")
    ] = False,
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
    out_dir: Annotated[Path, typer.Option(help="Sonuç dizini.")] = RESULTS_DIR,
) -> None:
    """Bir bölümü çalıştırır; önbellek kapalı, sonuç tüm metrikler ve sürümlerle yazılır."""
    if part is not None and limit:
        Console(stderr=True).print("[red]Hata:[/red] --part ile --limit birlikte kullanılamaz.")
        raise typer.Exit(EXIT_USAGE)
    try:
        part_spec = parse_part(part) if part is not None else None
    except ValueError as exc:
        Console(stderr=True).print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_USAGE) from exc
    console = Console(stderr=True)
    if split not in ("dev", "test"):
        console.print("[red]Hata:[/red] --split dev ya da test olmalı.")
        raise typer.Exit(EXIT_USAGE)
    if split == "test" and not final:
        console.print(
            "[red]Hata:[/red] test bölümü yalnızca en sonda bir kez çalıştırılır (--final). "
            "Prompt ayarı için dev kullanın."
        )
        raise typer.Exit(EXIT_USAGE)
    target: Split = "dev" if split == "dev" else "test"
    settings = _settings(console)
    try:
        samples = load_split(dataset, target)
    except DatasetError as exc:
        console.print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    selected = set(language or [])  # G5-3: Typer `Language` enum doğrular; burada yalnız filtre
    if selected:
        samples = [s for s in samples if s.label.language in selected]
    samples = samples[:limit] if limit else samples
    if part_spec is not None:
        samples = select_part(samples, *part_spec)
    if selected and not samples:
        console.print("[red]Hata:[/red] Seçilen dillerde bu bölümde örnek yok.")
        raise typer.Exit(EXIT_USAGE)
    unreviewed = [s.label.id for s in samples if not s.label.reviewed]
    if unreviewed:
        console.print(f"[yellow]Uyarı:[/yellow] incelenmemiş örnekler: {', '.join(unreviewed)}")

    def progress(index: int, total: int, result: SampleResult) -> None:
        status = "hata" if result.error else f"{result.latency_ms / 1000:.1f} sn"
        console.print(f"[{index}/{total}] {result.id}: {status}")

    try:
        result = asyncio.run(
            run_eval(
                samples,
                settings,
                split=target,
                provider=provider,
                mode=mode,
                static_only=static_only,
                ablations=list(ablate or []),
                progress=progress,
                languages=[lang.value for lang in language or []],
                part=part,
            )
        )
    except ValueError as exc:
        console.print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_USAGE) from exc
    path = save_result(result, out_dir)
    console.print(f"yazıldı: {path}")
    typer.echo(compare_table([result]))


def _result_and_labels(
    path: Path, dataset: Path, console: Console
) -> tuple[RunResult, dict[str, Label]]:
    """Sonuç dosyası + tüm bölümlerin güncel etiketleri; hata → çıkış kodu 3."""
    try:
        (result,) = load_results([path])
        split_samples = [
            s
            for split in ("dev", "test")
            if (dataset / split).is_dir()
            for s in load_split(dataset, split)
        ]
        labels = {s.label.id: s.label for s in split_samples}
        if result.config.dataset_version is not None:
            matched_samples = [
                s for s in split_samples if s.label.id in set(result.config.sample_ids)
            ]
            current_version = dataset_version(matched_samples)
            if result.config.dataset_version != current_version:
                console.print(
                    f"[yellow]Uyarı:[/yellow] Kayıtlı veri seti ({result.config.dataset_version}) "
                    f"ile diskteki etiketler ({current_version}) uyuşmuyor; "
                    "metrikler yeniden puanlanırken farklı etiketler kullanılıyor olabilir."
                )
    except (DatasetError, ValidationError, OSError) as exc:
        console.print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    return result, labels


@eval_app.command("breakdown")
def breakdown_cmd(
    path: Annotated[Path, typer.Argument(help="Sonuç dosyası.")],
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
) -> None:
    """Sonucu dil/motor grubuna göre döker (LLM çağrısı yok; etiketler veri setinden)."""
    console = Console(stderr=True)
    result, labels = _result_and_labels(path, dataset, console)
    groups, missing = breakdown(result, labels)
    if missing:
        console.print(f"[yellow]Uyarı:[/yellow] etiketi bulunamayan örnekler: {', '.join(missing)}")
    typer.echo(breakdown_table(groups))


@eval_app.command("analyze")
def analyze_cmd(
    path: Annotated[Path, typer.Argument(help="Sonuç dosyası.")],
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
    out: Annotated[Path | None, typer.Option(help="Analizi dosyaya yaz.")] = None,
) -> None:
    """Denetim precision analizi: kategorisiz eşleşme, `low` hariç, karışıklık, FP/FN listesi
    (LLM çağrısı yok; etiketler veri setinden)."""
    console = Console(stderr=True)
    result, labels = _result_and_labels(path, dataset, console)
    text = analysis_markdown(analyze(result, labels))
    if out is not None:
        with system_errors(console, "çıktı yazılamadı"):
            out.write_text(text, encoding="utf-8", newline="\n")
    typer.echo(text)


@eval_app.command("compare")
def compare(
    paths: Annotated[list[Path], typer.Argument(help="Sonuç dosyaları.")],
    out: Annotated[Path | None, typer.Option(help="Tabloyu dosyaya yaz.")] = None,
) -> None:
    """Sonuç dosyalarından Markdown karşılaştırma tablosu (§14.3)."""
    with system_errors():  # Faz C (O12): olmayan/bozuk sonuç dosyası → 3
        table = compare_table(load_results(paths))
        if out is not None:
            out.write_text(table, encoding="utf-8", newline="\n")
    typer.echo(table)


def _draft_table(checks: list[DraftCheck]) -> Table:
    table = Table(title="Taslak etiket kontrolü", show_lines=True)
    table.add_column("Örnek")
    table.add_column("Durum")
    table.add_column("Ayrıntı")
    for check in checks:
        status = "[green]uyumlu[/green]" if check.ok else "[red]sorun[/red]"
        lines = [f"[red]✗[/red] {escape(p)}" for p in check.problems]
        lines += [f"[yellow]?[/yellow] {escape(n)}" for n in check.notes]
        table.add_row(check.id, status, "\n".join(lines) or "—")
    return table


@eval_app.command("check-drafts")
def check_drafts(
    ids: Annotated[list[str] | None, typer.Argument(help="Yalnızca bu taslaklar.")] = None,
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
) -> None:
    """Taslak etiketleri statik analizle karşılaştırır (etiketi değiştirmez)."""
    console = Console()
    settings = _settings(console)
    try:
        samples = load_split(dataset, DRAFT)
        overlaps = check_disjoint(dataset)
    except DatasetError as exc:
        console.print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    if ids:
        samples = [s for s in samples if s.label.id in set(ids)]

    async def all_checks() -> list[DraftCheck]:
        return [await check_draft(sample, settings) for sample in samples]

    checks = asyncio.run(all_checks())
    console.print(_draft_table(checks))
    for problem in overlaps:
        console.print(f"[red]✗[/red] {escape(problem)}")
    if overlaps or any(not c.ok for c in checks):
        raise typer.Exit(EXIT_PROBLEMS)


@eval_app.command("promote")
def promote_cmd(
    ids: Annotated[list[str], typer.Argument(help="İncelenen taslak kimlikleri.")],
    split: Annotated[str, typer.Option(help="dev | test")],
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
) -> None:
    """İncelenen taslakları `reviewed: true` ile bir bölüme taşır."""
    console = Console(stderr=True)
    if split not in ("dev", "test"):
        console.print("[red]Hata:[/red] --split dev ya da test olmalı.")
        raise typer.Exit(EXIT_USAGE)
    target: Split = "dev" if split == "dev" else "test"
    for sample_id in ids:
        try:
            path = promote(dataset, sample_id, target)
        except DatasetError as exc:
            console.print(f"[red]Hata:[/red] {escape(str(exc))}")
            raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
        console.print(f"taşındı: {path.as_posix()}")


@eval_app.command("judge")
def judge_cmd(
    path: Annotated[Path, typer.Argument(help="Sonuç dosyası.")],
    dataset: Annotated[Path, typer.Option(help="Veri seti kökü.")] = DATASET_DIR,
    provider: Annotated[str | None, typer.Option(help="Yargıç LLM sağlayıcısı.")] = None,
    out: Annotated[Path | None, typer.Option(help="Yargıç raporunu dosyaya yaz.")] = None,
) -> None:
    """LLM-as-judge ile Sokratik kalite puanı üretir (Faz I / İş 10)."""
    console = Console(stderr=True)
    settings = _settings(console)
    result, _ = _result_and_labels(path, dataset, console)
    samples = {
        s.label.id: s
        for split in ("dev", "test")
        if (dataset / split).is_dir()
        for s in load_split(dataset, split)
    }
    name = provider or settings.providers.default
    from codementor.eval.judge import judge_run_result, judge_summary_markdown
    from codementor.eval.runner import _default_factory
    from codementor.prompts.templates import PromptTemplateError

    factory = _default_factory(settings)
    llm = factory(name)
    failed: list[str] = []
    try:
        reports = asyncio.run(
            judge_run_result(result, samples, llm, prompts_dir=settings.prompts.dir, errors=failed)
        )
    except PromptTemplateError as exc:
        console.print(f"[red]Hata:[/red] {escape(str(exc))}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    if failed:
        console.print(
            f"[yellow]Uyarı:[/yellow] {len(failed)} örnek yargılanamadı (bozuk yanıt ya da "
            f"sağlayıcı hatası): {escape(', '.join(failed))}"
        )
        if not reports:  # hiçbiri yargılanamadı: betik/CI başarı saymasın
            console.print("[red]Hata:[/red] hiçbir örnek yargılanamadı.")
            raise typer.Exit(EXIT_PROBLEMS)
    text = judge_summary_markdown(reports)
    if out is not None:
        with system_errors(console, "çıktı yazılamadı"):
            out.write_text(text, encoding="utf-8", newline="\n")
    typer.echo(text)
