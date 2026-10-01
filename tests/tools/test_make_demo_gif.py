"""README GIF aracı (Faz 26): kareler sırayla, küçültülmüş ve döngülü GIF olur."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest
from PIL import Image

TOOL = Path(__file__).resolve().parents[2] / "tools" / "make_demo_gif.py"


def _tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("make_demo_gif", TOOL)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["make_demo_gif"] = module
    spec.loader.exec_module(module)
    return module


def test_frames_sorted_numerically_and_gif_written(tmp_path: Path) -> None:
    tool = _tool()
    colors = {1: "red", 2: "green", 10: "blue"}
    for number, color in colors.items():
        Image.new("RGB", (400, 250), color).save(tmp_path / f"{number}.png")
    (tmp_path / "not.png").write_bytes(b"")  # sayı olmayan ad atlanır
    frames = tool.frame_paths(tmp_path)
    assert [p.stem for p in frames] == ["1", "2", "10"]

    out = tool.make_gif(frames, tmp_path / "out" / "demo.gif", width=200)
    with Image.open(out) as gif:
        assert gif.format == "GIF"
        assert gif.n_frames == 3
        assert gif.size == (200, 125)
        assert gif.info["loop"] == 0


def test_no_frames_is_clear_error(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="Kare bulunamadı"):
        _tool().make_gif([], tmp_path / "x.gif")
