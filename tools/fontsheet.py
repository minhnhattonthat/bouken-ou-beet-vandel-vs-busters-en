"""fontsheet.py: render one of the game's raw fonts (font/lc*.bin) to a labelled PNG sheet.

    python -X utf8 tools/fontsheet.py work/fs/fs/font/lc12x12.bin 12 12 2 OUT.png [--first 0] [--count 512] [--cols 32]

Glyphs are fixed-size records, W*H pixels at BPP bits, packed LSB-first per byte (NDS order). The label above each
cell is the glyph index in hex; read zoomed sheets to map codes to characters.
"""
import argparse

from PIL import Image, ImageDraw


def glyph_pixels(data, idx, w, h, bpp, msb=False):
    size = (w * h * bpp + 7) // 8
    rec = data[idx * size:(idx + 1) * size]
    px = []
    for i in range(w * h):
        bit = i * bpp
        b = rec[bit // 8] if bit // 8 < len(rec) else 0
        sh = (8 - bpp - bit % 8) if msb else bit % 8
        px.append((b >> sh) & ((1 << bpp) - 1))
    return px


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("font")
    ap.add_argument("w", type=int)
    ap.add_argument("h", type=int)
    ap.add_argument("bpp", type=int)
    ap.add_argument("out")
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--count", type=int, default=512)
    ap.add_argument("--cols", type=int, default=32)
    ap.add_argument("--msb", action="store_true", help="pixels MSB-first within each byte")
    ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()
    data = open(a.font, "rb").read()
    rows = (a.count + a.cols - 1) // a.cols
    cw, ch = a.w * a.scale + 4, a.h * a.scale + 12
    img = Image.new("RGB", (a.cols * cw, rows * ch), "white")
    d = ImageDraw.Draw(img)
    shades = [255 - 255 * v // ((1 << a.bpp) - 1) for v in range(1 << a.bpp)]
    for n in range(a.count):
        idx = a.first + n
        x0, y0 = (n % a.cols) * cw, (n // a.cols) * ch
        d.text((x0 + 1, y0), f"{idx:X}", fill=(200, 0, 0))
        for i, v in enumerate(glyph_pixels(data, idx, a.w, a.h, a.bpp, a.msb)):
            if v:
                g = shades[v]
                x, y = x0 + 2 + (i % a.w) * a.scale, y0 + 11 + (i // a.w) * a.scale
                d.rectangle([x, y, x + a.scale - 1, y + a.scale - 1], fill=(g, g, g))
    img.save(a.out)
    print(a.out, img.size)


if __name__ == "__main__":
    main()
