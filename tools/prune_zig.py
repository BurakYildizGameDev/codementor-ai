"""Zig libc başlıklarını budama CLI betiği (Faz J, J2).

Kullanım:
    uv run python tools/prune_zig.py [HEDEF_DIZIN] [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from codementor.validation.toolchain_prune import prune_zig_directory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zig gereksiz libc başlıklarını budar.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(Path.home() / ".codementor" / "toolchain" / "zig"),
        help="Zig kurulum kök dizini",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Gerçekte silmeden temizlenecek boyut ve dizinleri listeler",
    )
    parser.add_argument(
        "--platform",
        default=None,
        help="Hedef platform (örn. linux-x86_64, windows-x86_64)",
    )

    args = parser.parse_args(argv)
    target_dir = Path(args.path)

    if not target_dir.is_dir():
        print(f"Hata: Dizin bulunamadı: {target_dir}", file=sys.stderr)
        return 1

    report = prune_zig_directory(target_dir, platform=args.platform, dry_run=args.dry_run)

    mb = report.reclaimed_bytes / (1024 * 1024)
    mode = "[DRY-RUN] " if report.dry_run else ""
    print(f"{mode}Zig budama tamamlandı:")
    print(f"  Silinen dizin sayısı: {len(report.removed_dirs)}")
    print(f"  Silinen dosya sayısı: {report.removed_files_count}")
    print(f"  Kazanılan alan: {mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
