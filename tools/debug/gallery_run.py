"""gallery_run.py: run the message gallery (tools/debug/gallery.lua) over every dialogue span, in chunks.

    python -X utf8 tools/debug/gallery_run.py [ROM] [--chunks 8] [--jobs 2] [--out work/qa/gallery] [--only 3,4]

Writes the span list (tools/debug/gallery.py -> <out>/pcs.txt), then one cold-boot emu.py run per chunk into
<out>/c<k>/ (log.txt with GAL / GALSTUCK / SCR lines, g<NNNN>.png = first page of each span). Feed the logs to the
coverage report together with the tour: `python -X utf8 tools/textcov.py report work/qa/en work/qa/gallery`.
Prints per chunk: spans started, spans skipped as stuck, and whether GALDONE was reached. Exit 1 if a chunk did not
finish.
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tools'))
from skill import SKILL  # noqa: E402

FRAMES_PER_SPAN = 160   # ~95 measured (one page + A); slack for long messages
BOOT = 1500             # cold boot + the opening's first message (armed at ~f1360)


def run(k, lo, hi, rom, out, shots):
    d = out / ('c%d' % k)
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(rom), '--out', str(d),
           '--script', str(REPO / 'tools/debug/warp.lua'), '--var', "SCENE='newgame'", '--var', 'NOMASH=1',
           '--script', str(REPO / 'tools/debug/gallery.lua'), '--var', "GALLERY='%d-%d'" % (lo, hi),
           '--var', "GALLERY_PCS='%s'" % (out / 'pcs.txt').as_posix(),
           # no --debugger: every hook here is on a block start, and the JIT runs ~20x faster (same SCR lines)
           '--script', str(REPO / 'tools/lua/textlog.lua'),
           '--frames', str(BOOT + FRAMES_PER_SPAN * (hi - lo + 1)), '--timeout', '7200']
    if shots:
        cmd += ['--var', 'GALLERY_SHOTS=1']
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = (d / 'log.txt').read_text(encoding='utf-8', errors='replace') if (d / 'log.txt').exists() else ''
    lines = log.splitlines()
    started = sum(1 for ln in lines if ln.startswith('GAL '))
    stuck = [ln for ln in lines if ln.startswith('GALSTUCK')]
    done = any(ln.startswith('GALDONE') for ln in lines)
    return k, lo, hi, p.returncode, started, stuck, done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('rom', nargs='?', default=str(REPO / 'build' / 'beet_en.nds'))
    ap.add_argument('--chunks', type=int, default=8)
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--out', default=str(REPO / 'work' / 'qa' / 'gallery'))
    ap.add_argument('--only', help='chunk numbers, e.g. 3,4')
    ap.add_argument('--no-shots', action='store_true')
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, '-X', 'utf8', str(REPO / 'tools/debug/gallery.py'), '--out',
                    str(out / 'pcs.txt')], check=True)
    n = sum(1 for ln in (out / 'pcs.txt').read_text().splitlines() if ln.strip())
    size = -(-n // a.chunks)
    jobs = [(k, lo + 1, min(lo + size, n)) for k, lo in enumerate(range(0, n, size))]
    if a.only:
        keep = {int(x) for x in a.only.split(',')}
        jobs = [j for j in jobs if j[0] in keep]
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda j: run(*j, a.rom, out, not a.no_shots), jobs))
    bad = 0
    for k, lo, hi, rc, started, stuck, done in res:
        bad += not done
        print('c%d %d-%d exit %d started %d stuck %d %s' % (k, lo, hi, rc, started, len(stuck),
                                                           'done' if done else 'NOT DONE'))
        for s in stuck:
            print('   ', s)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
