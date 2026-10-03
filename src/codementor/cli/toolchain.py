"""`codementor toolchain status|install` (Faz 29, ADR-0018).

Derleyicisi olmayan kullanıcı (ve CI) için zig'i indirir; masaüstündeki "Derleyiciyi indir"
düğmesiyle aynı kurulum kodunu kullanır.
"""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console
from rich.markup import escape
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn
from rich.table import Table

from codementor.config import load_settings
from codementor.models.validation import DownloadProgress
from codementor.validation.toolchain import clear_toolchain_cache, compiler_statuses, get_toolchain
from codementor.validation.toolchain_install import (
    ToolchainInstallError,
    install_zig,
    installed_zig,
    platform_key,
    zig_root,
)

toolchain_app = typer.Typer(
    name="toolchain", no_args_is_help=True, help="Tier 1 derleyicileri (indirilebilir zig)."
)

_ORIGINS = {"system": "PATH", "downloaded": "indirilen", "bundled": "gömülü"}
_STAGES = {"download": "İndiriliyor", "extract": "Açılıyor", "check": "Denetleniyor"}


@toolchain_app.command("status")
def status() -> None:
    """Hedef başına kullanılacak derleyiciyi ve indirilen zig'in durumunu gösterir."""
    settings = load_settings().validation
    console = Console()
    table = Table(title="Tier 1 derleyicileri")
    table.add_column("Hedef", no_wrap=True)
    table.add_column("Araç", no_wrap=True)
    table.add_column("Kaynak", no_wrap=True)
    for item in compiler_statuses(get_toolchain(settings)):
        origin = _ORIGINS.get(item.origin, "—") if item.origin else "—"
        table.add_row(item.target, item.tool or "[dim]bulunamadı[/dim]", origin)
    console.print(table)
    exe = installed_zig(zig_root(settings.toolchain_dir))
    key = platform_key()
    if exe is not None:
        console.print(f"İndirilen zig: {escape(str(exe))}")
    elif key in settings.zig.sources:
        console.print("İndirilen zig yok. Kurmak için: codementor toolchain install zig")
    else:
        console.print(f"Bu platform ({key}) için indirilebilir derleyici tanımlı değil.")


@toolchain_app.command("install")
def install(
    tool: Annotated[str, typer.Argument(help="Kurulacak araç (şimdilik yalnızca zig).")] = "zig",
) -> None:
    """Zig'i yapılandırmadaki adresten indirir, sha256 ile doğrular ve kurar."""
    console = Console()
    if tool != "zig":
        console.print(f"[red]Bilinmeyen araç: {escape(tool)}. Yalnızca 'zig' kurulabilir.[/red]")
        raise typer.Exit(2)
    settings = load_settings().validation
    with Progress(
        TextColumn("{task.description}"), BarColumn(), DownloadColumn(), console=console
    ) as bar:
        task = bar.add_task("Hazırlanıyor", total=None)

        def on_progress(event: DownloadProgress) -> None:
            description = _STAGES[event.stage]
            if event.stage == "download":
                bar.update(task, description=description, completed=event.done, total=event.total)
            else:
                bar.update(task, description=description)

        try:  # Ctrl+C: install_zig yarım dosyaları `finally` ile siler
            exe = install_zig(settings, progress=on_progress)
        except ToolchainInstallError as exc:
            bar.stop()
            console.print(f"[red]{escape(str(exc))}[/red]")
            raise typer.Exit(1) from exc
    clear_toolchain_cache()
    console.print(f"Zig kuruldu: {escape(str(exe))}")
