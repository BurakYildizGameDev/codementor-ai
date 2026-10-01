from pathlib import Path


def first_line(path):
    return Path(path).read_text(encoding="utf-8").splitlines()[0]
