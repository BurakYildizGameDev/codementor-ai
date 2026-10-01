"""CodeMentor AI masaüstü uygulamasını Windows .exe olarak derler (PyInstaller, ADR-0013).

Kullanım:
    uv run python build_exe.py             # --onefile (varsayılan): dist/CodeMentor.exe
    uv run python build_exe.py --onedir    # dist/CodeMentor/ klasörü + zip (hızlı açılış)
    uv run python build_exe.py --both      # ikisi birden
    uv run python build_exe.py --console   # hata ayıklama için konsollu

İki profil aynı koddan:
  --onefile  tek dosya; açılışta arşiv %TEMP% altına çözülür (açılış görseli bu sırada görünür).
  --onedir   klasör; hiçbir şey çözülmez, açılış yalnızca import süresi kadardır.

Pakete girenler: `data/` (soru bankası, kontrol listeleri, şablonlar), `prompts/`, varsayılan
`codementor.toml` ve masaüstü görselleri. Kullanıcı exe'nin yanına kendi `codementor.toml`'unu
koyarsa o kullanılır (bkz. `codementor.desktop.runtime`). Veritabanı `~/.codementor` altındadır.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_NAME = "CodeMentor"
ENTRY = ROOT / "src" / "codementor" / "desktop" / "__main__.py"
ASSETS = ROOT / "src" / "codementor" / "desktop" / "assets"

# Çalışma anında okunan, kod olmayan dosyalar: (kaynak, paket içindeki hedef)
DATA = [
    (ROOT / "data", "data"),
    (ROOT / "prompts", "prompts"),
    (ROOT / "codementor.toml", "."),
    (ASSETS, "codementor/desktop/assets"),
]
# Roslyn denetleyicisi derlenmişse (make roslyn-check) C# Tier 1 de pakete girer
ROSLYN_OUT = ROOT / "tools" / "roslyn-check" / "out"

# Veri dosyaları ya da dinamik yüklenen uzantılar içeren paketler
COLLECT_ALL = [
    "customtkinter",
    "tree_sitter_c",
    "tree_sitter_cpp",
    "tree_sitter_c_sharp",
    "tree_sitter_python",
    "tree_sitter_html",
    "tree_sitter_css",
]
HIDDEN_IMPORTS = [
    "sqlalchemy.dialects.sqlite",
    "codementor.providers.ollama",
    "codementor.providers.openai_compat",
    "codementor.providers.anthropic",
    "codementor.providers.cli_agent",
    "keyring.backends.Windows",  # API anahtarları Kimlik Bilgisi Yöneticisi'nde (ADR-0014)
]
EXCLUDES = ["pytest", "hypothesis", "respx", "mypy", "ruff", "IPython", "matplotlib", "numpy"]

ZIP_EXCLUDE_DIRS = {"__pycache__", ".pytest_cache"}
ZIP_EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".log", ".zip")


def project_version() -> str:
    """pyproject.toml'daki sürüm (paketi import etmeden)."""
    try:
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    except OSError:
        return "0.0.0"
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    return match.group(1) if match else "0.0.0"


def version_tuple(version: str) -> tuple[int, int, int, int]:
    """`0.1.0` → (0, 1, 0, 0); sayı olmayan ekler yok sayılır."""
    numbers = [int(n) for n in re.findall(r"\d+", version)[:4]]
    a, b, c, d = [*numbers, 0, 0, 0, 0][:4]
    return (a, b, c, d)


def version_file(version: str, target: Path) -> Path:
    """Windows dosya özellikleri (Ayrıntılar sekmesi) için PyInstaller sürüm kaynağı."""
    v = version_tuple(version)
    fields = {
        "CompanyName": "CodeMentor AI",
        "FileDescription": "CodeMentor AI - Sokratik kod mentoru",
        "FileVersion": version,
        "InternalName": APP_NAME,
        "OriginalFilename": f"{APP_NAME}.exe",
        "ProductName": "CodeMentor AI",
        "ProductVersion": version,
    }
    strings = ",\n".join(f"          StringStruct('{k}', '{val}')" for k, val in fields.items())
    target.write_text(
        f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={v}, prodvers={v}, mask=0x3f, flags=0x0, OS=0x40004,
                    fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('041F04B0', [
{strings}
    ])]),
    VarFileInfo([VarStruct('Translation', [1055, 1200])])
  ]
)
""",
        encoding="utf-8",
    )
    return target


def pyinstaller_args(onefile: bool, console: bool, work: Path) -> list[str]:
    """PyInstaller komut satırı (test edilebilsin diye ayrı)."""
    sep = ";" if sys.platform == "win32" else ":"
    name = APP_NAME if onefile else f"{APP_NAME}-dir"
    args = [
        str(ENTRY),
        "--name",
        name,
        "--noconfirm",
        "--clean",
        "--paths",
        str(ROOT / "src"),
        "--distpath",
        str(ROOT / "dist"),
        "--workpath",
        str(work),
        "--specpath",
        str(work),
        "--icon",
        str(ASSETS / "icon.ico"),
        "--version-file",
        str(version_file(project_version(), work / "version.txt")),
        "--onefile" if onefile else "--onedir",
        "--console" if console else "--windowed",
    ]
    if onefile:
        args += ["--splash", str(ASSETS / "splash.png")]
    data = list(DATA)
    if ROSLYN_OUT.is_dir():
        data.append((ROSLYN_OUT, "tools/roslyn-check/out"))
    for source, target in data:
        args += ["--add-data", f"{source}{sep}{target}"]
    for package in COLLECT_ALL:
        args += ["--collect-all", package]
    for module in HIDDEN_IMPORTS:
        args += ["--hidden-import", module]
    for module in EXCLUDES:
        args += ["--exclude-module", module]
    return args


def should_zip(path: Path) -> bool:
    """Dağıtım arşivine girmemesi gereken artıklar."""
    if any(part in ZIP_EXCLUDE_DIRS for part in path.parts):
        return False
    return not path.name.endswith(ZIP_EXCLUDE_SUFFIXES)


def package_zip(folder: Path, version: str) -> Path:
    """onedir klasörünü `CodeMentor-<sürüm>-win64.zip` olarak arşivler."""
    archive = folder.parent / f"{APP_NAME}-{version}-win64.zip"
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(folder.rglob("*")):
            relative = path.relative_to(folder)
            if path.is_file() and should_zip(relative):
                zf.write(path, Path(APP_NAME) / relative)
    return archive


def build(onefile: bool, console: bool) -> Path:
    work = ROOT / "build" / ("onefile" if onefile else "onedir")
    work.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "PyInstaller", *pyinstaller_args(onefile, console, work)]
    print(f"\n==> PyInstaller ({'onefile' if onefile else 'onedir'})")
    subprocess.run(cmd, check=True, cwd=ROOT)
    if onefile:
        return ROOT / "dist" / f"{APP_NAME}.exe"
    built = ROOT / "dist" / f"{APP_NAME}-dir"
    final = ROOT / "dist" / APP_NAME
    shutil.rmtree(final, ignore_errors=True)
    built.rename(final)
    (final / f"{APP_NAME}-dir.exe").rename(final / f"{APP_NAME}.exe")
    return final


def main() -> None:
    parser = argparse.ArgumentParser(description="CodeMentor AI .exe derleyici")
    profile = parser.add_mutually_exclusive_group()
    profile.add_argument("--onefile", action="store_true", help="tek dosya (varsayılan)")
    profile.add_argument("--onedir", action="store_true", help="klasör + zip")
    profile.add_argument("--both", action="store_true", help="ikisi birden")
    parser.add_argument(
        "--console", action="store_true", help="konsol penceresiyle (hata ayıklama)"
    )
    args = parser.parse_args()

    version = project_version()
    outputs: list[Path] = []
    if args.onedir or args.both:
        folder = build(onefile=False, console=args.console)
        outputs += [folder, package_zip(folder, version)]
    if not args.onedir:
        outputs.append(build(onefile=True, console=args.console))
    print(f"\nCodeMentor AI {version} hazır:")
    for path in outputs:
        size = path.stat().st_size / 1_048_576 if path.is_file() else 0
        print(f"  {path}" + (f"  ({size:.1f} MB)" if size else ""))


if __name__ == "__main__":
    main()
