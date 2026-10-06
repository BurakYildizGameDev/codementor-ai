"""`build_exe.py` saf yardımcıları (derlemenin kendisi manuel: `uv run python build_exe.py`)."""

from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

import build_exe
import pytest


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


def test_self_contained_roslyn_preferred(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Faz 29: tek dosyalık Roslyn varsa yalnız o gömülür (dotnet gerekmez, ~15 MB)."""
    sc = tmp_path / "sc" / "RoslynCheck.exe"
    sc.parent.mkdir()
    sc.write_bytes(b"MZ")
    out = tmp_path / "out"
    out.mkdir()
    monkeypatch.setattr(build_exe, "ROSLYN_SC", sc)
    monkeypatch.setattr(build_exe, "ROSLYN_OUT", out)
    args = " ".join(build_exe.pyinstaller_args(onefile=True, console=False, work=tmp_path))
    assert f"{sc}{os.pathsep}tools/roslyn-check/sc" in args
    assert "tools/roslyn-check/out" not in args

    sc.unlink()
    args = " ".join(build_exe.pyinstaller_args(onefile=True, console=False, work=tmp_path))
    assert f"{out}{os.pathsep}tools/roslyn-check/out" in args


def test_queries_bundled(tmp_path: Path) -> None:
    """Faz 50 (Faz 49 denetimi K1): sorgular pakette; yoksa exe'de olgu çıkarımı boş."""
    args = build_exe.pyinstaller_args(onefile=False, console=False, work=tmp_path)
    data = [args[i + 1] for i, arg in enumerate(args) if arg == "--add-data"]
    queries = [d for d in data if d.endswith("codementor/analysis/queries")]
    assert len(queries) == 1
    source = Path(queries[0].rsplit(";" if ";" in queries[0] else ":", 1)[0])
    assert any(source.rglob("*.scm"))


def test_source_digest_written_and_bundled(tmp_path: Path) -> None:
    """Exe'de `.py` kaynağı yok: `rules_version` derleme anındaki kaynak özetini kullanır."""
    from codementor.pipeline.versions import DIGEST_FILE, source_digest

    args = build_exe.pyinstaller_args(onefile=True, console=False, work=tmp_path)
    written = tmp_path / DIGEST_FILE
    assert written.read_text(encoding="utf-8") == source_digest()
    data = [args[i + 1] for i, arg in enumerate(args) if arg == "--add-data"]
    assert any(d.startswith(str(written)) and d.endswith("codementor/pipeline") for d in data)


def test_build_info_written_and_bundled(tmp_path: Path) -> None:
    """Faz 60: build_info.json derleme anında yazılır ve pakette data altına eklenir."""
    args = build_exe.pyinstaller_args(onefile=True, console=False, work=tmp_path)
    written = tmp_path / "build_info.json"
    assert written.is_file()
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert payload["version"] == build_exe.project_version()
    assert payload["source"] == "exe"
    assert "built_at" in payload
    data = [args[i + 1] for i, arg in enumerate(args) if arg == "--add-data"]
    assert any(
        d.startswith(str(written)) and (d.endswith(";data") or d.endswith(":data")) for d in data
    )


def test_build_info_git_failure_sets_commit_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 60: git hatası olduğunda commit=None olur ve derleme durmaz."""

    def fake_run(*_a: object, **_k: object) -> None:
        raise build_exe.subprocess.SubprocessError("git bulunamadı")

    monkeypatch.setattr(build_exe.subprocess, "run", fake_run)
    written = build_exe.build_info_file(tmp_path)
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert payload["commit"] is None
    assert payload["source"] == "exe"
