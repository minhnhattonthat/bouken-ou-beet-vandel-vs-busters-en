"""markerscan.py: read the glyph logs of a marker tour (tools/lua/glyphlog.lua under warp_all.py --script) and report

  1. Japanese still drawn (text the extractor missed, or graphics-free UI text from somewhere else), per caller;
  2. marker ids seen, with font, caller (lr), start x, end x (start + pixel widths) and y: the budgets per draw site;
  3. ids never seen (to reach with more scenes or waive).

    python -X utf8 tools/markerscan.py work/qa/marker [--out work/qa/marker/scan]

Writes <out>_jp.tsv, <out>_ids.tsv, <out>_sites.tsv and prints a summary.
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from engine import Engine, EBASE, EEND  # noqa: E402
from text16 import Codec  # noqa: E402

LINE = re.compile(r'f(\d+) (G\d+) lr=(\w+) x=(-?\d+) y=(-?\d+) n=\d+ (.*)')
ID = re.compile(r'\[?([rq][0-9A-F]{5}|n[mw]\d{3}|p[0-9A-F]{5}|[a-z0-9]{2}\d+[a-z0-9]{1,2})\]?')


def runs(log):
    """Merge per-frame pieces: consecutive draws by one caller on one y whose x continues the previous end."""
    out = []
    for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
        m = LINE.match(line)
        if not m:
            continue
        font = 12 if m[2] == 'G12' else 8
        codes = [int(h, 16) for h in m[6].split()]
        x, y = int(m[4]), int(m[5])
        prev = out[-1] if out else None
        if prev and prev['font'] == font and prev['lr'] == m[3] and prev['y'] == y and prev['end'] == x:
            prev['codes'] += codes
        else:
            prev = {'f': int(m[1]), 'font': font, 'lr': m[3], 'x': x, 'y': y, 'codes': list(codes), 'end': x}
            out.append(prev)
        prev['end'] = None   # recomputed below
        prev['end'] = prev['x'] + sum(ENG.code_width(c, font) for c in prev['codes'])
    return out


def main():
    global ENG
    ap = argparse.ArgumentParser()
    ap.add_argument('tour')
    ap.add_argument('--out')
    a = ap.parse_args()
    import ndspy.rom
    import build
    ENG = Engine.from_rom(ndspy.rom.NintendoDSRom(build.ROM.read_bytes()))
    jpc = Codec.load(ROOT / 'tbl' / 'jp.tbl')
    tour = Path(a.tour)
    out = Path(a.out) if a.out else tour / 'scan'
    jp, ids, sites = defaultdict(set), {}, defaultdict(lambda: [999, 0, set(), set()])
    for log in sorted(tour.glob('*/log.txt')):
        scene = log.parent.name
        for r in runs(log):
            text = ''.join(Engine.decode_code(c) if EBASE <= c < EEND else jpc.decode_code(c) for c in r['codes'])
            key = (r['font'], r['lr'])
            s = sites[key]
            s[0], s[1] = min(s[0], r['x']), max(s[1], r['end'])
            s[2].add(r['y'])
            s[3].add(scene)
            # Japanese = any code that is not English, the full-width space or a full-width digit (0x00CC-0x00D5,
            # generated numbers)
            if any(not EBASE <= c < EEND and c != 0x0001 and not 0x00CC <= c <= 0x00D5 for c in r['codes']):
                jp[(r['font'], r['lr'], text)].add(scene)
            for m in ID.finditer(text):
                ids.setdefault(m[1], (scene, r['font'], r['lr'], r['x'], r['end'], r['y']))
    with open(str(out) + '_jp.tsv', 'w', encoding='utf-8') as f:
        f.write('font\tlr\ttext\tscenes\n')
        for (font, lr, text), sc in sorted(jp.items()):
            f.write('%d\t%s\t%s\t%s\n' % (font, lr, text, ' '.join(sorted(sc))))
    with open(str(out) + '_ids.tsv', 'w', encoding='utf-8') as f:
        f.write('id\tscene\tfont\tlr\tx\tend\ty\n')
        for k, v in sorted(ids.items()):
            f.write('%s\t%s\n' % (k, '\t'.join(map(str, v))))
    with open(str(out) + '_sites.tsv', 'w', encoding='utf-8') as f:
        f.write('font\tlr\tmin_x\tmax_end\tys\tscenes\n')
        for (font, lr), (x0, x1, ys, sc) in sorted(sites.items()):
            f.write('%d\t%s\t%d\t%d\t%s\t%s\n' % (font, lr, x0, x1, ' '.join(map(str, sorted(ys))),
                                                  ' '.join(sorted(sc)[:6])))
    print('%d Japanese runs, %d ids seen, %d draw sites -> %s_*.tsv' % (len(jp), len(ids), len(sites), out))


if __name__ == '__main__':
    main()
