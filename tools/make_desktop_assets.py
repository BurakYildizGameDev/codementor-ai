"""Masaüstü görsellerini üretir: logo.png, icon.ico, splash.png (src/codementor/desktop/assets/).

Monogram: altın kod parantezleri arasında bir soru işareti — "kodu düzeltmez, soru sorar".
Çalıştırma: `uv run python tools/make_desktop_assets.py` (çıktılar depoya eklenir).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "codementor" / "desktop" / "assets"

BG_TOP = (24, 32, 54)
BG_BOTTOM = (10, 14, 22)
GOLD = (232, 176, 75)
GOLD_LIGHT = (246, 210, 140)
VIOLET = (154, 140, 255)
TEXT = (232, 236, 244)
MUTED = (134, 145, 168)

_FONTS = ("seguisb.ttf", "segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf")
_FONTS_REGULAR = ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf")


def _font(
    size: int, names: tuple[str, ...] = _FONTS
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in names:
        for folder in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")):
            path = folder / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size)


def _gradient(
    size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]
) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(a + (b - a) * t) for a, b in zip(top, bottom, strict=True))
        draw.line([(0, y), (width, y)], fill=color)
    return image


def logo(size: int = 512) -> Image.Image:
    """Yuvarlatılmış kare zemin + altın parantezler + soru işareti."""
    scale = 4  # kenar yumuşatma için büyük çizip küçült
    s = size * scale
    base = _gradient((s, s), BG_TOP, BG_BOTTOM).convert("RGBA")
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.23), fill=255)

    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        [int(s * 0.18), int(s * 0.18), int(s * 0.82), int(s * 0.82)], fill=(*VIOLET, 70)
    )
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(s * 0.12)))

    draw = ImageDraw.Draw(base)
    stroke = int(s * 0.055)
    mid = s // 2
    reach, height = int(s * 0.13), int(s * 0.19)
    for side in (-1, 1):
        x_tip = mid + side * int(s * 0.33)
        x_back = x_tip - side * reach
        draw.line(
            [(x_back, mid - height), (x_tip, mid), (x_back, mid + height)],
            fill=GOLD,
            width=stroke,
            joint="curve",
        )
        for x, y in ((x_back, mid - height), (x_tip, mid), (x_back, mid + height)):
            r = stroke // 2
            draw.ellipse([x - r, y - r, x + r, y + r], fill=GOLD)
    font = _font(int(s * 0.44))
    draw.text((mid, mid + int(s * 0.01)), "?", font=font, fill=GOLD_LIGHT, anchor="mm")

    border = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle(
        [2, 2, s - 3, s - 3], radius=int(s * 0.23), outline=(*GOLD, 90), width=int(s * 0.008)
    )
    base.alpha_composite(border)
    base.putalpha(mask)
    return base.resize((size, size), Image.Resampling.LANCZOS)


def splash(width: int = 720, height: int = 400) -> Image.Image:
    """PyInstaller açılış görseli (exe açılırken arşiv çözülürken görünür)."""
    image = _gradient((width, height), (16, 22, 38), BG_BOTTOM).convert("RGBA")
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-120, -160, 380, 300], fill=(*VIOLET, 45))
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    mark = logo(132)
    image.alpha_composite(mark, (64, 96))
    draw = ImageDraw.Draw(image)
    draw.text((226, 112), "CodeMentor", font=_font(46), fill=TEXT)
    title_width = draw.textlength("CodeMentor", font=_font(46))
    draw.text((226 + title_width + 10, 112), "AI", font=_font(46), fill=GOLD)
    draw.text((228, 176), "Kodu düzeltmez, düşündürür.", font=_font(20, _FONTS_REGULAR), fill=MUTED)
    draw.rounded_rectangle([64, 300, width - 64, 303], radius=2, fill=(30, 42, 66))
    draw.rounded_rectangle([64, 300, 64 + (width - 128) // 3, 303], radius=2, fill=GOLD)
    draw.text((64, 324), "Yükleniyor…", font=_font(15, _FONTS_REGULAR), fill=MUTED)
    draw.rectangle([0, 0, width - 1, height - 1], outline=(46, 61, 92), width=1)
    return image.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mark = logo(512)
    mark.resize((256, 256), Image.Resampling.LANCZOS).save(OUT / "logo.png")
    mark.save(
        OUT / "icon.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    splash().save(OUT / "splash.png")
    print(f"Görseller üretildi: {OUT}")


if __name__ == "__main__":
    main()
