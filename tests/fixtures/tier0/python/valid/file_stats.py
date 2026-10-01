import sys
from pathlib import Path


def line_count(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def main() -> None:
    for arg in sys.argv[1:]:
        try:
            print(arg, line_count(Path(arg)))
        except OSError as exc:
            print(f"{arg}: {exc}")


main()
