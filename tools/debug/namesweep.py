"""Generic buster name coverage: every name in status/bustername/busterman.bin / busterwoman.bin (128 each) is picked
once by the game's own name roll. Scene `buster_join` queues a join block from East Village (man: rom.img 0x2D14F,
`55 1A; 5A 1B 00 1A`; woman: 0x2E9A0, `5A 20 00 1F`); each queued join makes a new generic buster, 0x02019564 rolls
its name (bl 0x0201A938, returns at 0x02019608 with r0 = index) and idloop.lua forces that index, so textlog.lua
logs `NAM <m|w> <index>`. 16 joins per run (the roster has 25 slots), one run per 16 names, into OUT/name_<m|w><first>.

    python -X utf8 tools/debug/namesweep.py [--out work/qa/cover] [--jobs 4] [--rom build/beet_en.nds]
"""
import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
JOIN_PC = {'m': '2D14F', 'w': '2E9A0'}
PER_RUN = 16


def run(a, sex, first):
    out = Path(a.out) / ('name_%s%03d' % (sex, first))
    extra = ' '.join(['q' + JOIN_PC[sex]] * PER_RUN)
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'emu.py'), a.rom, '--debugger', '--out', str(out),
           '--script', 'tools/debug/warp.lua', '--script', 'tools/lua/idloop.lua', '--script', 'tools/lua/textlog.lua',
           '--var', "SCENE='buster_join'", '--var', "EXTRA='%s'" % extra, '--var', 'IDLOOP_ACC=0x02019608',
           '--var', 'IDLOOP_FROM=%d' % first, '--var', 'IDLOOP_N=%d' % PER_RUN, '--frames', str(a.frames)]
    if sex == 'w':   # the scene's own man join (f1147) comes first: leave its roll alone
        cmd += ['--var', 'IDLOOP_AFTER=1300']
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    log = out / 'log.txt'
    got = sum(1 for ln in log.read_text(encoding='utf-8').splitlines() if ln.startswith('NAM ')) if log.exists() else 0
    return '%s%03d exit %d NAM %d/%d' % (sex, first, r.returncode, got, PER_RUN)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='work/qa/cover')
    ap.add_argument('--rom', default='build/beet_en.nds')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--frames', type=int, default=8000)
    ap.add_argument('--sex', default='mw', help='m, w or mw (default)')
    a = ap.parse_args()
    jobs = [(s, f) for s in a.sex for f in range(0, 128, PER_RUN)]
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for line in ex.map(lambda j: run(a, *j), jobs):
            print(line, flush=True)


if __name__ == '__main__':
    main()
