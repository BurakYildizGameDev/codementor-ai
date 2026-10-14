"""Tkinter'sız ortamda (Linux CI'daki uv Python'u) içe aktarılması gereken modüller.

Faz K'da `questions_controller` en üstte Tk formunu içe aktarınca Linux CI kırıldı; Windows'ta
tkinter olduğu için yerelde görünmüyordu. Burada tkinter engellenmiş bir alt süreçte denenir.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

MODULES = [
    "codementor.desktop.questions_controller",
    "codementor.desktop.history_controller",
    "codementor.desktop.config_controller",
    "codementor.desktop.self_check",
    "codementor.desktop.runtime",
    "codementor.desktop.config_writer",
    "codementor.desktop.viewmodel",
    "codementor.cli.main",
    "codementor.api.app",
]

BLOCK = (
    "import sys\n"
    "for name in ('tkinter', 'customtkinter', '_tkinter', 'tkinterdnd2'):\n"
    "    sys.modules[name] = None\n"
    "import importlib\n"
    "importlib.import_module(sys.argv[1])\n"
)


@pytest.mark.parametrize("module", MODULES)
def test_imports_without_tkinter(module: str) -> None:
    result = subprocess.run(
        [sys.executable, "-c", BLOCK, module],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr[-2000:]
