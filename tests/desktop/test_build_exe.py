"""`build_exe.py` saf yardımcıları (derlemenin kendisi manuel: `uv run python build_exe.py`)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import build_exe


def test_version_comes_from_pyproject() -> None:
    assert build_exe.project_version() == "0.1.0"
    assert build_exe.version_tuple("1.2.3rc4") == (1, 2, 3, 4)
    assert build_exe.version_tuple("2") == (2, 0, 0, 0)


def test_version_file_is_valid_python_expression(tmp_path: Path) -> None:
    path = build_exe.version_file("0.1.0", tmp_path / "v.txt")
    text = path.read_text(encoding="utf-8")
    assert "CodeMentor.exe" in text
    assert "filevers=(0, 1, 0, 0)" in text
    compile(text, "v.txt", "eval")  # PyInstaller dosyayı Python ifadesi olarak okur


def test_pyinstaller_args_bundle_runtime_data(tmp_path: Path) -> None:
    onefile = build_exe.pyinstaller_args(onefile=True, console=False, work=tmp_path)
    assert {"--onefile", "--windowed", "--splash"} <= set(onefile)
    data = [onefile[i + 1] for i, arg in enumerate(onefile) if arg == "--add-data"]
    for target in ("data", "prompts", "codementor/desktop/assets"):
        assert any(d.endswith(target) for d in data), target
    assert all(Path(d.rsplit(";" if ";" in d else ":", 1)[0]).exists() for d in data)
    collected = [onefile[i + 1] for i, arg in enumerate(onefile) if arg == "--collect-all"]
    assert "tkinterdnd2" in collected  # tkdnd ikilileri olmadan sürükle-bırak çalışmaz

    onedir = build_exe.pyinstaller_args(onefile=False, console=True, work=tmp_path)
    assert {"--onedir", "--console"} <= set(onedir)
    assert "--splash" not in onedir


def test_zip_skips_artifacts(tmp_path: Path) -> None:
    folder = tmp_path / "CodeMentor"
    (folder / "_internal" / "__pycache__").mkdir(parents=True)
    (folder / "CodeMentor.exe").write_bytes(b"MZ")
    (folder / "_internal" / "lib.dll").write_bytes(b"x")
    (folder / "_internal" / "__pycache__" / "a.pyc").write_bytes(b"x")
    (folder / "debug.log").write_text("x", encoding="utf-8")
    archive = build_exe.package_zip(folder, "0.1.0")
    assert archive.name == "CodeMentor-0.1.0-win64.zip"
    with zipfile.ZipFile(archive) as zf:
        names = sorted(zf.namelist())
    assert names == ["CodeMentor/CodeMentor.exe", "CodeMentor/_internal/lib.dll"]
