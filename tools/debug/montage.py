"""Side-by-side scene sheets for checking warps by eye: one column per scene, its shots stacked (every Nth).

    python -X utf8 tools/debug/montage.py work/qa/warps OUT.png scene1 scene2 ... [--every 2] [--scale 0.5]

Reads <dir>/<scene>/f*.png and final.png (warp_all.py output). Labels each column with the scene name.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dir')
    ap.add_argument('out')
    ap.add_argument('scenes', nargs='+')
    ap.add_argument('--every', type=int, default=2)
    ap.add_argument('--scale', type=float, default=0.5)
    ap.add_argument('--from-frame', type=int, default=900, help='skip shots before this frame (boot/title)')
    a = ap.parse_args()
    cols = []
    for s in a.scenes:
        d = Path(a.dir) / s
        shots = sorted(p for p in d.glob('f[0-9]*.png') if int(p.stem[1:]) >= a.from_frame)[::a.every]
        if (d / 'final.png').exists():
            shots.append(d / 'final.png')
        cols.append((s, [Image.open(p).convert('RGB') for p in shots]))
    w, h = int(256 * a.scale), int(384 * a.scale)
    rows = max(len(c[1]) for c in cols)
    im = Image.new('RGB', (w * len(cols) + 2 * len(cols), 14 + rows * (h + 2)), (40, 0, 40))
    dr = ImageDraw.Draw(im)
    for i, (s, shots) in enumerate(cols):
        x = i * (w + 2)
        dr.text((x + 2, 1), s[:22], fill=(255, 255, 0))
        for j, sh in enumerate(shots):
            im.paste(sh.resize((w, h)), (x, 14 + j * (h + 2)))
    im.save(a.out)
    print(a.out, im.size)


if __name__ == '__main__':
    main()
