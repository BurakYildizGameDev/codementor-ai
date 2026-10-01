"""README demo GIF'i (Faz 26): Playwright karelerinden Pillow ile (ffmpeg gerekmez).

    cd web && npx playwright test -g "GIF"     # kareler: web/test-results/demo-frames/*.png
    uv run python tools/make_demo_gif.py       # → docs/img/web-demo.gif

Kareler sayı sırasıyla alınır, genişlik küçültülür ve ortak bir palete indirgenir (boyut).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "web" / "test-results" / "demo-frames"
OUT = ROOT / "docs" / "img" / "web-demo.gif"
WIDTH = 960
FRAME_MS = 1600
LAST_FRAME_MS = 3200


def frame_paths(folder: Path) -> list[Path]:
    """`1.png`, `2.png`, ... sayı sırasıyla (10 > 9)."""
    paths = [p for p in folder.glob("*.png") if p.stem.isdigit()]
    return sorted(paths, key=lambda p: int(p.stem))


def make_gif(frames: list[Path], out: Path, width: int = WIDTH) -> Path:
    """Kareleri GIF'e çevirir; son kare daha uzun durur, döngü sonsuz."""
    if not frames:
        raise SystemExit("Kare bulunamadı; önce `npx playwright test -g GIF` çalıştırın.")
    images: list[Image.Image] = []
    for path in frames:
        with Image.open(path) as source:
            rgb = source.convert("RGB")
        height = round(rgb.height * width / rgb.width)
        images.append(rgb.resize((width, height), Image.Resampling.LANCZOS))
    # Ortak palet tüm karelerden: yalnız ilk kareden çıkarılırsa sonraki karelerin renkleri
    # kaybolur (ör. sonuç paneli), kareler aynılaşıp birleşir
    montage = Image.new("RGB", (width, sum(im.height for im in images)))
    top = 0
    for im in images:
        montage.paste(im, (0, top))
        top += im.height
    palette = montage.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    quantized = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images]
    durations = [FRAME_MS] * (len(quantized) - 1) + [LAST_FRAME_MS]
    out.parent.mkdir(parents=True, exist_ok=True)
    quantized[0].save(
        out,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Playwright karelerinden README GIF'i")
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--width", type=int, default=WIDTH)
    args = parser.parse_args()
    out = make_gif(frame_paths(args.frames), args.out, args.width)
    print(f"yazıldı: {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
