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
    assert job["env"]["PYTHONIOENCODING"] == "utf-8"
    runs = " ".join(str(step.get("run", "")) for step in job["steps"])
    assert "build_exe.py --both" in runs
    uploads = [
        s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact")
    ]
    assert uploads
    assert "dist/" in str(uploads[0]["with"]["path"])


def test_ci_builds_roslyn_for_tests_and_exe() -> None:
    """Faz 27: Linux'ta C# derleyici testleri koşar. Faz 29: zig kurulur ve zorunludur; exe
    self-contained Roslyn'i (dotnet gerektirmeyen) paketlemeden önce yayımlar."""
    workflow = yaml.safe_load((REPO / ".github" / "workflows" / "ci.yml").read_text("utf-8"))
    check = workflow["jobs"]["check"]["steps"]
    check_runs = [str(step.get("run", "")) for step in check]
    assert any("dotnet build tools/roslyn-check" in r for r in check_runs)
    linux_pytest = next(r for r in check_runs if r.startswith("uv run pytest"))
    pytest_index = check_runs.index(linux_pytest)
    install_index = check_runs.index("uv run codementor toolchain install zig")
    assert install_index < pytest_index
    env = check[pytest_index]["env"]
    assert env["CODEMENTOR_REQUIRE_ROSLYN"] == "1"
    assert env["CODEMENTOR_REQUIRE_ZIG"] == "1"
    exe = workflow["jobs"]["exe"]["steps"]
    runs = [str(step.get("run", "")) for step in exe]
    publish = next(r for r in runs if "dotnet publish tools/roslyn-check" in r)
    assert "--self-contained true" in publish
    assert "-o tools/roslyn-check/sc" in publish
    assert runs.index(publish) < runs.index(next(r for r in runs if "build_exe.py" in r))


def test_ci_runs_pip_audit_and_npm_audit() -> None:
    """Kabul (Faz 50): CI bağımlılık açığı denetimi yapar (mimari §12 "Bağımlılık riski")."""
    workflow = yaml.safe_load((REPO / ".github" / "workflows" / "ci.yml").read_text("utf-8"))
    check = [str(step.get("run", "")) for step in workflow["jobs"]["check"]["steps"]]
    export = next(r for r in check if "uv export" in r)
    audit = next(r for r in check if "pip-audit" in r)
    assert "--no-dev" in export
    assert check.index(export) < check.index(audit)
    web = [str(step.get("run", "")) for step in workflow["jobs"]["web"]["steps"]]
    assert any("npm audit --omit=dev" in r for r in web)


def test_ci_reports_coverage() -> None:
    """Kabul (Faz 53): CI Linux pytest adımı kapsama raporu üretir (mimari §15)."""
    workflow = yaml.safe_load((REPO / ".github" / "workflows" / "ci.yml").read_text("utf-8"))
    check = [str(step.get("run", "")) for step in workflow["jobs"]["check"]["steps"]]
    linux_pytest = next(r for r in check if "pytest" in r and "--cov=codementor" in r)
    assert '-m "not live"' in linux_pytest
    assert "--cov-report=term-missing:skip-covered" in linux_pytest
