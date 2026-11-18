"""gfxsweep.py: static graphics-text sweep. Renders every tile graphic in NitroFS into labelled contact sheets.

    python -X utf8 tools/gfxsweep.py --fs work/fs/fs --out work/gfx [--per 20]

Formats (docs/re/graphics.md): .nbfc / .ob = 4bpp tiles (8bpp when the palette has 256 colours), optional u32 size
header (dropped when u32 == len-4); .nbfs = u16 width, u16 height (tiles), then 16-bit BG map entries
(tile | hflip<<10 | vflip<<11 | pal<<12); .nbfp / .pb = BGR555 palettes, same header rule. A .nbfc with a same-stem .nbfs is drawn through the map
(as the screen shows it); everything else as a tile grid (32 tiles wide for BG tiles, 4/8 for OBJ). Palette: same
stem, else a grey ramp. Prints every file it skipped and why; writes index.tsv.
"""
import argparse
import struct
from pathlib import Path

from PIL import Image, ImageDraw


def body(b):
    if len(b) >= 4 and struct.unpack_from("<I", b)[0] == len(b) - 4:
        return b[4:]
    return b


def palette(path):
    if path is None:
        return None
    p = body(path.read_bytes())
    cols = []
    for i in range(0, len(p) - 1, 2):
        v = struct.unpack_from("<H", p, i)[0]
        cols.append(((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31))
    return cols or None


def grey(n):
    return [(255 - i * 255 // (n - 1),) * 3 for i in range(n)]


def tiles(data, bpp):
    size = 8 * bpp
    out = []
    for t in range(len(data) // size):
        raw = data[t * size:(t + 1) * size]
        if bpp == 4:
            px = [raw[i // 2] >> (4 * (i & 1)) & 15 for i in range(64)]
        else:
            px = list(raw)
        out.append(px)
    return out


def draw_tile(img, px, x0, y0, pal, base=0, hf=False, vf=False):
    for i, v in enumerate(px):
        if v == 0:
            continue
        x, y = i % 8, i // 8
        if hf:
            x = 7 - x
        if vf:
            y = 7 - y
        c = pal[(base + v) % len(pal)] if pal else (0, 0, 0)
        img.putpixel((x0 + x, y0 + y), c)


def find_pal(f):
    for ext in (".nbfp", ".pb"):
        p = f.with_suffix(ext)
        if p.exists():
            return p
    return None  # a borrowed palette from the same folder often renders black; grey keeps text readable


def render(f):
    raw = body(f.read_bytes())
    pp = find_pal(f)
    pal = palette(pp)
    bpp = 8 if pal and len(pal) >= 256 else 4
    if not pal:
        pal = grey(16 if bpp == 4 else 256)
    ts = tiles(raw, bpp)
    if not ts:
        return None, "no tiles"
    m = f.with_suffix(".nbfs")
    bg = (0, 96, 96)
    if f.suffix == ".nbfc" and m.exists():
        mb = m.read_bytes()
        w, h = struct.unpack_from("<HH", mb)
        mp = mb[4:]
        n = min(len(mp) // 2, w * h)
        img = Image.new("RGB", (w * 8, h * 8), bg)
        for k in range(n):
            e = struct.unpack_from("<H", mp, 2 * k)[0]
            t = e & 0x3FF
            if t < len(ts):
                draw_tile(img, ts[t], (k % w) * 8, (k // w) * 8, pal, ((e >> 12) * 16) if bpp == 4 else 0,
                          bool(e & 0x400), bool(e & 0x800))
        return img, f"map {w}x{h} pal={pp.name if pp else 'grey'}"
    w = 32 if f.suffix == ".nbfc" else (8 if len(ts) >= 32 else 4)
    h = (len(ts) + w - 1) // w
    img = Image.new("RGB", (w * 8, h * 8), bg)
    for k, px in enumerate(ts):
        draw_tile(img, px, (k % w) * 8, (k // w) * 8, pal)
    return img, f"grid {w}x{h} pal={pp.name if pp else 'grey'}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fs", default="work/fs/fs")
    ap.add_argument("--out", default="work/gfx")
    ap.add_argument("--per", type=int, default=20)
    ap.add_argument("--maxh", type=int, default=256, help="crop each render to this height (rest -> next panel)")
    a = ap.parse_args()
    fs, out = Path(a.fs), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in fs.rglob("*") if p.suffix in (".nbfc", ".ob"))
    panels, index = [], []
    for f in files:
        rel = f.relative_to(fs).as_posix()
        try:
            img, how = render(f)
        except Exception as e:  # report, never drop silently
            print(f"SKIP {rel}: {e}")
            continue
        if img is None:
            print(f"SKIP {rel}: {how}")
            continue
        for part, y in enumerate(range(0, img.height, a.maxh)):
            crop = img.crop((0, y, img.width, min(img.height, y + a.maxh)))
            panels.append((f"{rel}" + (f" #{part}" if img.height > a.maxh else ""), crop, how))
    sheet_no = 0
    for s in range(0, len(panels), a.per):
        chunk = panels[s:s + a.per]
        cols = 4
        cw = 2 * max(p[1].width for p in chunk) + 8
        rowh = []
        for r in range(0, len(chunk), cols):
            rowh.append(2 * max(p[1].height for p in chunk[r:r + cols]) + 14)
        sheet = Image.new("RGB", (cols * cw, sum(rowh)), "white")
        d = ImageDraw.Draw(sheet)
        y = 0
        for r in range(0, len(chunk), cols):
            for c, (name, img, how) in enumerate(chunk[r:r + cols]):
                x = c * cw
                d.text((x + 2, y + 1), name[-40:], fill=(200, 0, 0))
                sheet.paste(img.resize((img.width * 2, img.height * 2), Image.NEAREST), (x + 2, y + 12))
                index.append(f"{sheet_no:03d}\t{name}\t{how}")
            y += rowh[r // cols]
        sheet.save(out / f"sheet_{sheet_no:03d}.png")
        sheet_no += 1
    (out / "index.tsv").write_text("sheet\tfile\trender\n" + "\n".join(index) + "\n", encoding="utf-8")
    print(f"{len(files)} files, {len(panels)} panels, {sheet_no} sheets -> {out}")


if __name__ == "__main__":
    main()
