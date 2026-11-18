"""One warp run per inventory id: puts that one record into an inventory region (warp.lua `inv=REGION:CAT:ID:1`),
opens a list screen and keeps the final shot. A run whose bottom screen is flat (the list never drew: the game
hung) is reported as HANG; run the same ids on the original ROM (--rom rom/...) to tell an English bug from the
game's own behaviour. Runs land in OUT/<id hex>/ (point textcov.py report at OUT for the ones that drew).

    python -X utf8 tools/debug/invsweep.py --scene menu_equip --region 11E0 --cat 1 --ids 0-10 \
        --extra 't160,53 w200' --out work/qa/cover/wequip [--rom build/beet_en.nds] [--jobs 3] [--frames 4600]
"""
import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402
from debug.idsweep import ids_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def flat(png):
    """True when the bottom screen is one flat colour (stddev < 2 on every band)."""
    im = Image.open(png).convert('RGB')
    w, h = im.size
    return max(ImageStat.Stat(im.crop((0, h // 2, w, h))).stddev) < 2


def run(a, i):
    out = Path(a.out) / ('%03X' % i)
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'emu.py'), a.rom, '--debugger', '--out', str(out),
           '--script', 'tools/debug/warp.lua', '--script', 'tools/lua/textlog.lua', '--var', "SCENE='%s'" % a.scene,
           '--var', "EXTRA='inv=%s:%s:%d:1 %s'" % (a.region, a.cat, i, a.extra), '--frames', str(a.frames)]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    png = out / 'final.png'
    state = 'NOSHOT' if not png.exists() else 'HANG' if flat(png) else 'ok'
    return i, r.returncode, state


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scene', required=True)
    ap.add_argument('--region', required=True, help='inventory region offset in the save block, hex (11E0 weapons)')
    ap.add_argument('--cat', required=True, help='category byte (1 weapon, 2 armor, 4 item)')
    ap.add_argument('--ids', required=True, help='record ids (entry byte 0 = id+1), e.g. 0-10,13')
    ap.add_argument('--extra', default='', help='inputs after the scene route that open the list')
    ap.add_argument('--out', required=True)
    ap.add_argument('--frames', type=int, default=4600)
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--rom', default='build/beet_en.nds')
    ap.add_argument('--recheck', action='store_true',
                    help='no runs: judge the final shots already in OUT (the in-run verdict once read "ok" for a '
                         'flat shot; always recheck before using the result)')
    a = ap.parse_args()
    res = []
    if a.recheck:
        def judge(i):
            png = Path(a.out) / ('%03X' % i) / 'final.png'
            return i, 0, 'NOSHOT' if not png.exists() else 'HANG' if flat(png) else 'ok'
        work = map(judge, ids_of(a.ids))
    else:
        work = concurrent.futures.ThreadPoolExecutor(a.jobs).map(lambda i: run(a, i), ids_of(a.ids))
    for i, rc, state in work:
        print('%3d %03X exit %d %s' % (i, i, rc, state), flush=True)
        res.append(state)
    print('ok %d, hang %d, no shot %d' % (res.count('ok'), res.count('HANG'), res.count('NOSHOT')))


if __name__ == '__main__':
    main()
