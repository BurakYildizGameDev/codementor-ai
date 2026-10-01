"""Dağıtım yapılandırması (Faz 23): wheel paket verisi, satır sonları, CI exe işi."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import yaml

from codementor import paths

REPO = Path(__file__).resolve().parents[2]


def _pyproject() -> dict[str, Any]:
    with (REPO / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)


def test_wheel_contains_data_and_prompts() -> None:
    """`data/` ve `prompts/` wheel'de `codementor/_resources/` altına girer."""
    wheel = _pyproject()["tool"]["hatch"]["build"]["targets"]["wheel"]
    include = wheel["force-include"]
    assert include["data"] == f"codementor/{paths.RESOURCES_DIR}/data"
    assert include["prompts"] == f"codementor/{paths.RESOURCES_DIR}/prompts"


def test_gitattributes_forces_lf() -> None:
    lines = (REPO / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "* text=auto eol=lf" in lines
    assert any(line.startswith("*.png") and "binary" in line for line in lines)


def test_exe_job_uploads_artifact() -> None:
    workflow = yaml.safe_load((REPO / ".github" / "workflows" / "ci.yml").read_text("utf-8"))
    job = workflow["jobs"]["exe"]
    assert job["runs-on"] == "windows-latest"
    assert job["needs"] == "check"
    runs = " ".join(str(step.get("run", "")) for step in job["steps"])
    assert "build_exe.py --both" in runs
    uploads = [
        s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact")
    ]
    assert uploads
    assert "dist/" in str(uploads[0]["with"]["path"])
