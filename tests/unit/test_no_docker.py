"""ADR-0009: kodda ve yapılandırmada Docker'a bağımlılık yok."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_DOCKER = re.compile(r"docker", re.IGNORECASE)
# Python kaynağında açıklama serbest; çağrı/bağımlılık kalıpları yasak
_DOCKER_USE = re.compile(
    r"""["']docker|import docker|from docker|docker[ 	]+(run|exec|build|compose)|docker\.sock""",
    re.IGNORECASE,
)


def _files() -> list[Path]:
    files = [*sorted((ROOT / "src").rglob("*.py"))]
    files += [ROOT / "Makefile", ROOT / "pyproject.toml", ROOT / "codementor.toml"]
    files += sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    files += sorted((ROOT / "tools").rglob("*.cs")) + sorted((ROOT / "tools").rglob("*.csproj"))
    return files


def test_no_docker_reference_in_code_or_config() -> None:
    offenders = [
        str(path.relative_to(ROOT))
        for path in _files()
        if (_DOCKER_USE if path.suffix == ".py" else _DOCKER).search(
            path.read_text(encoding="utf-8")
        )
    ]
    assert offenders == []


def test_pattern_catches_invocations() -> None:
    for snippet in ('subprocess.run(["docker", "run"])', "import docker", "/var/run/docker.sock"):
        assert _DOCKER_USE.search(snippet), snippet
    assert not _DOCKER_USE.search("Docker yalıtımı yoktur (ADR-0009)")


def test_scan_covers_tier1_modules() -> None:
    names = {p.name for p in _files()}
    assert {"runner.py", "tier1.py", "toolchain.py", "Makefile"} <= names


def test_agents_docs_state_docker_not_required() -> None:
    """Belgelerde Docker yalnızca 'gerekmez/opsiyonel' bağlamında geçer."""
    for doc in ("AGENTS.md", "README.md"):
        text = (ROOT / doc).read_text(encoding="utf-8")
        for line in text.splitlines():
            if _DOCKER.search(line):
                assert re.search(r"gerekmez|opsiyonel|kaldır|ADR-0009", line), line
