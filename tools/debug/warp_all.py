"""Run every scene in tools/debug/scenes.tsv from a cold boot, save a state per scene, and report.

    python -X utf8 tools/debug/warp_all.py [ROM] [--only a,b] [--jobs 3] [--out work/qa/warps] [--states work/states]

Per scene: work/qa/warps/<scene>/ (shots every 300 frames, sheet.png, final.png, log.txt) and
work/states/<scene>.dst. A scene passes when emu.py exits 0, warp.lua logged WARP (or the scene is `title`),
and the final frame is not a flat colour. Summary: <out>/summary.tsv. Exit 1 if any scene fails.
Regenerate the whole state library with this after engine, font or graphics changes (cold boot every time).
"""
import argparse
import csv
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tools'))
from skill import SKILL  # noqa: E402

DEFAULT_ROM = REPO / 'rom' / 'Bouken-ou Beet - Vandel vs. Busters (Japan).nds'


def scenes():
    with open(REPO / 'tools/debug/scenes.tsv', encoding='utf-8', newline='') as f:
        rows = [r for r in csv.reader(f, delimiter='\t') if r and not r[0].startswith('#')]
    head = rows[0]
    for r in rows[1:]:
        assert len(r) == len(head), 'scenes.tsv row has %d columns, want %d: %r' % (len(r), len(head), r)
        yield dict(zip(head, r))


def flat(png):
    from PIL import Image
    im = Image.open(png).convert('RGB')
    lo, hi = zip(*im.getextrema())
    return max(h - l for l, h in zip(lo, hi)) < 8


def run(sc, rom, out, states):
    d = out / sc['name']
    state = states / (sc['name'] + '.dst')
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(rom), '--out', str(d),
           '--script', str(REPO / 'tools/debug/warp.lua'), '--var', "SCENE='%s'" % sc['name'],
           '--frames', sc['frames'], '--shot-every', '300', '--sheet', '--state-out', str(state),
           '--timeout', '900']
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = (d / 'log.txt').read_text(encoding='utf-8', errors='replace') if (d / 'log.txt').exists() else ''
    warped = 'WARP' in log or sc['kind'] == 'title'
    final = d / 'final.png'
    ok_img = final.exists() and not flat(final)
    ok = p.returncode == 0 and warped and ok_img
    end = next((l for l in log.splitlines() if l.startswith('END')), '')
    why = '' if ok else 'exit %d warped=%s image=%s %s' % (p.returncode, warped, ok_img, p.stdout[-200:].strip())
    return sc['name'], ok, end, why


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('rom', nargs='?', default=str(DEFAULT_ROM))
    ap.add_argument('--only')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--out', default=str(REPO / 'work/qa/warps'))
    ap.add_argument('--states', default=str(REPO / 'work/states'))
    a = ap.parse_args()
    out, states = Path(a.out), Path(a.states)
    out.mkdir(parents=True, exist_ok=True)
    states.mkdir(parents=True, exist_ok=True)
    todo = [s for s in scenes() if not a.only or s['name'] in a.only.split(',')]
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda s: run(s, a.rom, out, states), todo))
    bad = 0
    with open(out / 'summary.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('scene\tok\tend\twhy\n')
        for name, ok, end, why in res:
            bad += not ok
            f.write('%s\t%s\t%s\t%s\n' % (name, 'ok' if ok else 'FAIL', end, why.replace('\n', ' ')))
            print('%-24s %s %s' % (name, 'ok  ' if ok else 'FAIL', why or end))
    print('%d/%d scenes ok; summary %s' % (len(res) - bad, len(res), out / 'summary.tsv'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
