"""CLI sistem hataları (Faz C, Y9/O12; mimari §10).

`analyze` çıkış kodları: 0 tamam · 1 yüksek önemli bulgu · 2 derleme başarısız (erken çıkış) ·
3 sistem hatası. Sistem hatası (okunamayan yapılandırma ya da dosya, açılamayan veritabanı,
bozuk veri) traceback yerine Türkçe tek satırla ve 3 koduyla biter; CI onu bulgu sanmaz.
"""

from __future__ import annotations

import tomllib
from collections.abc import Iterator
from contextlib import contextmanager

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from sqlalchemy.exc import SQLAlchemyError

from codementor.questions._loader import DataFileError

EXIT_SYSTEM_ERROR = 3

# `typer.Exit` / click istisnaları bu listede yok: bilinçli çıkışlar olduğu gibi geçer
SYSTEM_ERRORS: tuple[type[BaseException], ...] = (
    OSError,
    SQLAlchemyError,
    ValidationError,
    tomllib.TOMLDecodeError,
    DataFileError,
)


def describe(exc: BaseException) -> str:
    """Kullanıcıya gösterilecek kısa açıklama (traceback yok)."""
    if isinstance(exc, tomllib.TOMLDecodeError):
        return f"codementor.toml okunamadı: {exc}"
    if isinstance(exc, ValidationError):
        return f"geçersiz değer ({exc.error_count()} hata): {exc.errors()[0]['msg']}"
    if isinstance(exc, SQLAlchemyError):
        return f"veritabanı açılamadı: {type(exc).__name__}"
    if isinstance(exc, OSError):
        target = f" ({exc.filename})" if exc.filename else ""
        return f"dosya işlemi başarısız{target}: {exc.strerror or exc}"
    return str(exc)


@contextmanager
def system_errors(console: Console | None = None, context: str = "") -> Iterator[None]:
    """İçindeki sistem hatalarını `Hata: …` + çıkış 3'e çevirir."""
    try:
        yield
    except SYSTEM_ERRORS as exc:
        prefix = f"{context}: " if context else ""
        (console or Console(stderr=True)).print(
            f"[red]Hata:[/red] {escape(prefix + describe(exc))}"
        )
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
