"""tagbox.py: is every speaker tag centred? Runs the skill's inkbox.py on each tour shot that shows the tag.

    python -X utf8 tools/tagbox.py work/qa/en [--tol 2]

The speaker tag (docs/windows.md, 80 px) is the only font-drawn centred text in the game: choices and menus are
graphics buttons (gfx.py centres those by construction). The tag box on the bottom screen has its border (colour
90,66,74, the same as the tag text) at x 176, y 119 and y 139; its inside is x 177..255, so the rect is
178,121,77,17 with --ink on that colour. A shot shows a tag when those border pixels are set. Writes the crops of
failures to <dir>/_tagbox/. Exit 1 if any shot fails.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402

INK = (90, 66, 74)
RECT = (178, 121, 77, 17)


def has_tag(bot):
    return (bot.getpixel((176, 121)) == INK and bot.getpixel((178, 119)) == INK
            and bot.getpixel((178, 139)) == INK and bot.getpixel((177, 121)) != INK)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('tour')
    ap.add_argument('--tol', default='2')
    a = ap.parse_args()
    tour = Path(a.tour)
    out = tour / '_tagbox'
    out.mkdir(exist_ok=True)
    shots = fails = empty = 0
    for png in sorted(tour.glob('*/f*.png')):
        im = Image.open(png).convert('RGB')
        if im.size != (256, 384):
            continue
        bot = im.crop((0, 192, 256, 384))
        if not has_tag(bot):
            continue
        shots += 1
        tmp = out / f'{png.parent.name}_{png.stem}.png'
        bot.save(tmp)
        r = subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'inkbox.py'), str(tmp),
                            ','.join(map(str, RECT)), '--ink', ','.join(map(str, INK)), '--diff', '12',
                            '--tol', a.tol], capture_output=True, text=True)
        if r.returncode == 0:
            tmp.unlink()
            continue
        if r.returncode == 2:
            empty += 1
        fails += 1
        print(f'{png.parent.name}/{png.name}: {r.stdout.strip()}')
    print(f'{shots} shots with a speaker tag, {fails} not centred ({empty} with no ink); crops of failures in {out}')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
