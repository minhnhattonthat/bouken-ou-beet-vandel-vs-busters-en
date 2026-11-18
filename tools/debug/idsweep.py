"""One warp run per record id, for records the game fetches once (e.g. a party member's name, copied into the member
struct when they join, then drawn from RAM): idloop.lua forces the first call(s) of ACC to that id, textlog.lua logs
the TAB line, and the final shot shows the screen. Runs land in OUT/<id hex>/ (point textcov.py report at OUT).

    python -X utf8 tools/debug/idsweep.py --scene menu_status --acc 0x020140DC --ids 1-53 --out work/qa/cover/party
      [--calls 1] [--frames N] [--jobs 3] [--var NAME=VALUE ..] [--rom build/beet_en.nds]
"""
import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def ids_of(spec):
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a, 0), int(b or a, 0) + 1))
    return out


def frames_of(scene):
    for ln in (ROOT / 'tools' / 'debug' / 'scenes.tsv').read_text(encoding='utf-8').splitlines():
        f = ln.split('\t')
        if f[0] == scene:
            return int(f[4])
    raise SystemExit('no scene ' + scene)


def run(a, i):
    out = Path(a.out) / ('%03X' % i)
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'emu.py'), a.rom, '--debugger', '--out', str(out),
           '--script', 'tools/debug/warp.lua', '--script', 'tools/lua/idloop.lua', '--script', 'tools/lua/textlog.lua',
           '--var', "SCENE='%s'" % a.scene, '--var', 'IDLOOP_ACC=%s' % a.acc, '--var', 'IDLOOP_FROM=%d' % i,
           '--var', 'IDLOOP_N=%d' % a.calls, '--frames', str(a.frames or frames_of(a.scene))]
    for v in a.var:
        cmd += ['--var', v]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return i, r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scene', required=True)
    ap.add_argument('--acc', required=True)
    ap.add_argument('--ids', required=True, help='e.g. 1-53 or 1,4,0x10-0x12')
    ap.add_argument('--out', required=True)
    ap.add_argument('--calls', type=int, default=1, help='IDLOOP_N: calls forced, getting id, id+1, ... (default 1)')
    ap.add_argument('--frames', type=int)
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--var', action='append', default=[])
    ap.add_argument('--rom', default='build/beet_en.nds')
    a = ap.parse_args()
    bad = 0
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for i, rc in ex.map(lambda i: run(a, i), ids_of(a.ids)):
            print('%03X exit %d' % (i, rc), flush=True)
            bad += rc != 0
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
