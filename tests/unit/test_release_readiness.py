"""Faz D: tek kaynaklı sürüm (O18), exe duman testi (`--self-check`, O17).

Ayrıca public belge iddiaları (README sayıları ve faz listesi) teste bağlanır.
"""

from __future__ import annotations

import functools
import importlib.metadata
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

import codementor
from codementor.desktop import self_check

REPO = Path(__file__).resolve().parents[2]


def _build_exe() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_exe", REPO / "build_exe.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_version_single_source() -> None:
    version = codementor.__version__
    assert importlib.metadata.version("codementor") == version
    assert _build_exe().project_version() == version
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r"^version\s*=", pyproject, re.MULTILINE) is None  # ikinci kaynak yok
    assert 'dynamic = ["version"]' in pyproject


def test_changelog_top_entry_is_current_version() -> None:
    text = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    top = re.search(r"^## \[([^\]]+)\]", text, re.MULTILINE)
    assert top is not None
    assert top.group(1) == codementor.__version__


def test_self_check_passes_from_source(tmp_path: Path) -> None:
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["ok"] is True
    assert data["version"] == codementor.__version__
    names = {c["name"] for c in data["checks"]}
    assert {"soru bankası", "tree-sitter sorguları", "olgu çıkarımı (C)"} <= names


def test_self_check_fails_without_queries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Exe'de `.scm` eksikse (Faz 50 hatası) duman testi düşer."""
    empty = tmp_path / "queries"
    empty.mkdir()
    monkeypatch.setattr(self_check.queries_package, "__file__", str(empty / "__init__.py"))
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 1
    checks = {c["name"]: c for c in json.loads(out.read_text(encoding="utf-8"))["checks"]}
    assert checks["tree-sitter sorguları"]["ok"] is False


def test_optional_check_does_not_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEMENTOR_VALIDATION__ROSLYN_CHECK_EXE", str(tmp_path / "yok.exe"))
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 0
    checks = {c["name"]: c for c in json.loads(out.read_text(encoding="utf-8"))["checks"]}
    assert checks["Roslyn denetleyicisi"]["ok"] is False
    assert checks["Roslyn denetleyicisi"]["required"] is False


def test_launch_flag_runs_without_window(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # launch tkinter'a bağlı; tkinter'sız Linux CI'da atlanır (release Windows'ta exe ile sınar)
    launch = pytest.importorskip("codementor.desktop.launch", exc_type=ImportError)
    monkeypatch.setattr(launch.runtime, "prepare_environment", lambda: tmp_path)
    monkeypatch.setattr(launch, "App", None)  # pencere açılmaya kalkarsa test düşer
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["CodeMentor.exe", "--self-check", "rapor/sonuc.json"])
    with pytest.raises(SystemExit) as exit_info:
        launch.main()
    assert exit_info.value.code == 0
    assert json.loads((tmp_path / "rapor" / "sonuc.json").read_text(encoding="utf-8"))["ok"]


# ---------------------------------------------------------------------------
# Public belge iddiaları (KALAN_ISLER.md iş 3): sayılar, badge ve faz listesi
# ---------------------------------------------------------------------------

ADR_DIR = REPO / "docs" / "adr"
ARCHIVE_DIR = REPO / "docs" / "gelistirme-gunlugu"


def _flat(relative: str) -> str:
    """Belgeyi okur; satır kaydırmalarını gizlemek için boşlukları tekler."""
    return re.sub(r"\s+", " ", (REPO / relative).read_text(encoding="utf-8"))


def _number(text: str, pattern: str) -> int:
    """Kalıbın ilk grubunu tam sayı olarak döndürür (binlik ayraçlar atılır)."""
    match = re.search(pattern, text)
    assert match is not None, f"kalıp bulunamadı: {pattern}"
    return int(re.sub(r"\D", "", match.group(1)))


def _count_lines(data: bytes) -> int:
    """Ham içerikte boş olmayan (`\\n` ile ayrılan) satır sayısı."""
    return sum(1 for row in data.decode("utf-8", "replace").split("\n") if row.strip())


def _is_binary(data: bytes) -> bool:
    """Git'in sezgisi: ilk 8 KB'da NUL baytı varsa binary sayılır."""
    return b"\x00" in data[:8192]


def _tracked_files(prefix: str) -> list[str]:
    """`git ls-files <prefix>` çıktısı (git yoksa test atlanır)."""
    if shutil.which("git") is None:
        pytest.skip("git bulunamadı")
    listing = subprocess.run(
        ["git", "ls-files", prefix],
        cwd=REPO,
        capture_output=True,
        check=True,
        text=True,
        encoding="utf-8",
    )
    return [name for name in listing.stdout.splitlines() if name.strip()]


def _tracked_nonblank_lines(prefix: str) -> int:
    """İzlenen **metin** dosyalarında boş olmayan satır sayısı (README `~N bin satır` ölçümü).

    Binary dosyalar sayılmaz: ham baytlar utf-8'e çözülünce `\\x0b`/`\\x1c` gibi ayraçlar yüzünden
    yüzlerce sahte satır üretiyorlar (ör. `src/codementor/desktop/assets/icon.ico`).
    """
    total = 0
    for name in _tracked_files(prefix):
        data = (REPO / name).read_bytes()
        if not _is_binary(data):
            total += _count_lines(data)
    return total


@functools.lru_cache(maxsize=1)
def _collected_test_count() -> int:
    """Test toplama sayısı (alt süreç; ağa çıkmaz, ~7 sn sürer)."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "--collect-only",
            "-q",
            "-m",
            "not live",
            "-p",
            "no:cacheprovider",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    match = re.search(r"(\d+)(?:/\d+)? tests collected", result.stdout)
    assert match is not None, result.stdout[-500:]
    return int(match.group(1))


def _expand_phases(claim: str) -> set[str]:
    """`A-H, J ve K` gibi bir ifadeyi harf kümesine açar."""
    letters: set[str] = set()
    for part in re.split(r",|\bve\b", claim):
        part = part.strip()
        if not part:
            continue
        assert re.fullmatch(r"[A-K](?:-[A-K])?", part), f"beklenmeyen faz ifadesi: {part!r}"
        if "-" in part:
            first, last = part.split("-")
            letters.update(chr(code) for code in range(ord(first), ord(last) + 1))
        else:
            letters.add(part)
    return letters


def test_readme_adr_claims_match_adr_directory() -> None:
    """ADR sayısı iddiaları (TR + EN) `docs/adr/` içeriğiyle aynı olmalı."""
    adr_files = [path for path in ADR_DIR.glob("*.md") if path.name[:4].isdigit()]
    assert adr_files
    readme = _flat("README.md")
    assert _number(readme, r"(\d+) ADR\b") == len(adr_files)
    assert _number(readme, r"(\d+) kayıt\)") == len(adr_files)
    assert _number(_flat("README.en.md"), r"(\d+) ADRs") == len(adr_files)


def test_readme_test_count_claims_are_lower_bounds() -> None:
    """`3700+` badge'i ve `N+ test` iddiaları gerçek toplama sayısının alt sınırı olmalı."""
    collected = _collected_test_count()
    readme = _flat("README.md")
    claims = {
        "badge": _number(readme, r"badge/testler-(\d+)%2B"),
        "kalite tablosu": _number(readme, r"([\d.]+)\+ test"),
        "README.en.md": _number(_flat("README.en.md"), r"([\d,]+)\+ tests"),
    }
    for name, value in claims.items():
        assert 0 < value <= collected, f"{name}: {value} > toplama sayısı {collected}"


# KALAN_ISLER iş 23: "~N bin" yaklaşık bir iddiadır; birebir yuvarlama her değişiklikte kırılıyordu
# (tam taramada 3 kez). Ölçüm iddianın ±1 bin içinde olmalı; ters yazılmış ya da çok bayat sayılar
# (iş 1'deki "~28 bin test / ~29 bin kaynak" gibi) yine yakalanır. Dosya satırı iddiaları ±15 satır.
THOUSAND_TOLERANCE = 1
FILE_LINE_TOLERANCE = 15


def _approx_thousand(lines: int, claimed_thousand: int) -> bool:
    """Ölçülen satır sayısı "~N bin" iddiasının toleransı içinde mi."""
    return abs(lines / 1000 - claimed_thousand) <= THOUSAND_TOLERANCE


def _assert_thousand(prefix: str, claimed_thousand: int) -> None:
    lines = _tracked_nonblank_lines(prefix)
    assert _approx_thousand(lines, claimed_thousand), (
        f"{prefix}: belge ~{claimed_thousand} bin, ölçüm {lines} (±{THOUSAND_TOLERANCE} bin)"
    )


@pytest.mark.parametrize(
    ("lines", "claimed", "ok"),
    [
        (39_662, 40, True),
        (39_662, 39, True),
        (40_990, 40, True),
        (41_100, 40, False),
        (38_000, 40, False),
    ],
)
def test_thousand_tolerance_bounds(lines: int, claimed: int, ok: bool) -> None:
    """Tolerans yaklaşık iddiayı kabul eder, bayat ya da ters iddiayı reddeder."""
    assert _approx_thousand(lines, claimed) is ok


def test_readme_line_count_claims_match_measurement() -> None:
    """`~40 bin satır test (~29 bin satır kaynak)` iddiası ölçümün ±1 bin içinde olmalı."""
    readme = _flat("README.md")
    _assert_thousand("tests/", _number(readme, r"~(\d+) bin satır test"))
    _assert_thousand("src/", _number(readme, r"\(~(\d+) bin satır kaynak"))


def test_line_count_measurement_skips_binary_assets() -> None:
    """Binary varlıklar (`desktop/assets/*.png|ico`) ölçüme girmemeli: sahte satır üretiyorlar."""
    assets = sorted((REPO / "src/codementor/desktop/assets").glob("*"))
    binaries = [path for path in assets if path.is_file() and _is_binary(path.read_bytes())]
    assert binaries, "beklenen binary varlık bulunamadı"
    polluted = sum(_count_lines((REPO / name).read_bytes()) for name in _tracked_files("src/"))
    clean = _tracked_nonblank_lines("src/")
    assert clean < polluted, "binary varlıklar hâlâ metin gibi sayılıyor"
    assert polluted - clean > 100, "binary dosyalar ölçüme girmiyor gibi"


def test_readme_phase_claims_match_progress() -> None:
    """README'nin faz listesi, PROGRESS.md'de bölümü olan fazlarla birebir olmalı."""
    readme = _flat("README.md")
    match = re.search(r"\(Faz 0-(\d+), ardından public öncesi Faz ([^)]*)\)", readme)
    assert match is not None, "README'de faz anlatımı bulunamadı"
    last_archived = int(match.group(1))
    claimed = _expand_phases(match.group(2))
    progress = (REPO / "PROGRESS.md").read_text(encoding="utf-8")
    documented = set(re.findall(r"(?m)^#{2,4}\s+Faz\s+([A-K])", progress))
    assert documented, "PROGRESS.md'de faz bölümü bulunamadı"
    assert claimed == documented, f"README {sorted(claimed)} · PROGRESS {sorted(documented)}"
    archive = ARCHIVE_DIR / f"PROGRESS-faz-0-{last_archived}.md"
    assert archive.exists(), archive
    assert f"Faz 0-{last_archived}" in archive.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Zayıf yönler belgesi iddiaları (KALAN_ISLER.md iş 4c): sayılar ölçümle sabit
# ---------------------------------------------------------------------------

WEAK_DOC = "docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md"
SRC_PREFIX = "src/codementor"


def _open_sonraya_items() -> tuple[int, int]:
    """`PROGRESS.md` "Sonraya" bölümündeki (toplam, açık) madde sayısı.

    Madde = bölümdeki tek düzey `- ` satırı; kapalı olanlar üstü çizili başlar (`- ~~…~~`).
    """
    text = (REPO / "PROGRESS.md").read_text(encoding="utf-8")
    heading = re.search(r"(?m)^## .*Sonraya.*$", text)
    assert heading is not None, "PROGRESS.md'de Sonraya bölümü yok"
    rest = text[heading.end() :]
    following = re.search(r"(?m)^## ", rest)
    section = rest[: following.start()] if following else rest
    items = [line for line in section.splitlines() if line.startswith("- ")]
    assert items, "Sonraya bölümü boş"
    return len(items), sum(1 for line in items if not line.startswith("- ~~"))


def test_weak_doc_line_count_claims_match_measurement() -> None:
    """`~29 bin satır kaynak, ~40 bin satır test` iddiası ölçümün ±1 bin içinde olmalı."""
    doc = _flat(WEAK_DOC)
    _assert_thousand("tests/", _number(doc, r"~(\d+) bin satır test"))
    _assert_thousand("src/", _number(doc, r"~(\d+) bin satır kaynak"))


def test_weak_doc_test_count_and_adr_claims_match_reality() -> None:
    """`N+ test` iddiaları alt sınır, `N ADR` iddiaları `docs/adr/` sayısıyla eşleşmeli."""
    doc = _flat(WEAK_DOC)
    claims = [int(re.sub(r"\D", "", value)) for value in re.findall(r"([\d.]+)\+ test", doc)]
    assert len(claims) >= 2, f"belgede 'N+ test' iddiası beklenenden az: {claims}"
    collected = _collected_test_count()
    for claim in claims:
        assert 0 < claim <= collected, f"test iddiası {claim} > toplama sayısı {collected}"
    adr_claims = [int(value) for value in re.findall(r"(\d+) ADR\b", doc)]
    assert adr_claims, "belgede 'N ADR' iddiası yok"
    adr_files = [path for path in ADR_DIR.glob("*.md") if path.name[:4].isdigit()]
    assert set(adr_claims) == {len(adr_files)}, (
        f"ADR iddiaları {adr_claims} · dosya {len(adr_files)}"
    )


def test_weak_doc_file_line_counts_within_tolerance() -> None:
    """`path.py NNN` biçimindeki her satır sayısı gerçek dosyanın ±15 satırı içinde olmalı."""
    doc = _flat(WEAK_DOC)
    claims = re.findall(r"`([\w/]+\.py)` (\d+)", doc)
    assert len(claims) >= 6, f"beklenen dosya satır iddiası bulunamadı: {claims}"
    for relative, claimed in claims:
        actual = _count_lines((REPO / SRC_PREFIX / relative).read_bytes())
        assert abs(int(claimed) - actual) <= FILE_LINE_TOLERANCE, (
            f"{relative}: belge {claimed}, gerçek {actual} (tolerans ±{FILE_LINE_TOLERANCE})"
        )


def test_weak_doc_sonraya_count_matches_progress() -> None:
    """Belgedeki açık "Sonraya" madde sayısı `PROGRESS.md` ile aynı olmalı (tanım belgede)."""
    doc = _flat(WEAK_DOC)
    total, open_items = _open_sonraya_items()
    assert _number(doc, r"madde sayısı \(açık\) \| (\d+)") == open_items
    assert _number(doc, r"\((\d+) madde\)") == total
