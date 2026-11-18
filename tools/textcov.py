"""textcov.py: text coverage for this game (phase 8 gate), on top of the skill's textcover.py.

tools/lua/textlog.lua logs what a run reached (SCR <pc> for script messages / speakers, TAB <accessor> <id> for arm9
table records). This tool turns that into the generic form textcover.py reads and runs it:

    python -X utf8 tools/textcov.py report work/qa/en work/qa/gallery [--waive docs/text_unshown.tsv] [--list]
    (converted logs go to work/qa/_textcov; the message gallery: tools/debug/gallery_run.py)
    python -X utf8 tools/textcov.py strings [--out build/strings.tsv]

Keys (hex, the same in strings.tsv and in the converted TEXT lines):
- rom.XXXXX (field/script/rom.img message or speaker at original offset XXXXX): 0x10000000 + XXXXX. A logged SCR pc
  is mapped through the ORIGINAL rom.img: the opcode at pc (70 or 9E) and its u32 operand at pc+1. The inserter
  only rewrites operands and appends strings, so code offsets are the same in the build.
- a9.<table>.<n>.<field>: 0x30000000 + (accessor & 0xFFFF) << 12 + record index. An accessor call reaches the whole
  record, so every field of it (name, reading, desc) counts as reached: coverage is per record here.
- quest.XXXX (quest/quest.img title / description at original offset XXXX): 0x20000000 + XXXX, from QST <pc>
  lines (the quest interpreter's 20 / 1A / 2D handlers), mapped through the original quest.img like SCR.
- a9.<addr> pointer strings (script/arm9/ptr.json): 0x40000000 + (first pointer word & 0xFFFFFF), from PTR <word>
  lines (a read watch on every pointer word: they never move, the code loads one to reach the string).
- name.<m|w>NNN generic buster names: 0x60000000 (+0x100 for w) + NNN, from NAM <m|w> <index> lines (the random
  pick when a generic buster is made, 0x02019608).
- anything else: 0x50000000 + a running number, never logged: 0x50000000 + a running number, never
  logged, so it is reported as not shown until a probe or a waiver covers it.
A key proves the game fetched the string, not that it drew correctly; visual QA judges that.
"""
import argparse
import collections
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arm9text  # noqa: E402
from skill import SKILL  # noqa: E402

FS = ROOT / 'work' / 'fs' / 'fs'
ROM_IMG = FS / 'field' / 'script' / 'rom.img'
ARM9 = ROOT / 'work' / 'fs' / 'arm9.bin'
QUEST_IMG = FS / 'quest' / 'quest.img'
SCR_OPS = (0x70, 0x9E)
QUEST_OPS = (0x20, 0x1A, 0x2D)
ROM_KEY, QUEST_KEY, TAB_KEY, PTR_KEY, NONE_KEY = 0x10000000, 0x20000000, 0x30000000, 0x40000000, 0x50000000
NAME_KEY = 0x60000000


def ptr_words():
    """{pointer word address: key} for script/arm9/ptr.json (an entry's key is its first word's)."""
    out = {}
    for e in json.loads((ROOT / 'script' / 'arm9' / 'ptr.json').read_text(encoding='utf-8'))['entries']:
        for w in e['ptrs']:
            out[int(w, 16)] = PTR_KEY + (int(e['ptrs'][0], 16) & 0xFFFFFF)
    return out


def entries():
    out = []
    for f in sorted((ROOT / 'script').rglob('*.json')):
        out += json.loads(f.read_text(encoding='utf-8'))['entries']
    return out


def tables():
    """{key: (accessor, base, size)} from arm9text.TABLES."""
    return {t[0]: (t[1], t[2], t[3]) for t in arm9text.TABLES}


def first_id(arm9, acc):
    """The id the accessor's record 0 has: `sub r1, r0, #N` at acc+4, else 0."""
    w = struct.unpack_from('<I', arm9, acc + 4 - arm9text.BASE)[0]
    return w & 0xFF if (w & 0x0FFFF000) == 0x02401000 else 0


def key_of(e, tabs, n):
    i = e['id']
    if i.startswith('rom.'):
        return ROM_KEY + int(i[4:], 16)
    if i.startswith('quest.'):
        return QUEST_KEY + int(i[6:], 16)
    if i.startswith('name.'):
        return NAME_KEY + (0x100 if i[5] == 'w' else 0) + int(i[6:])
    if e.get('ptrs'):
        return PTR_KEY + (int(e['ptrs'][0], 16) & 0xFFFFFF)
    parts = i.split('.')
    if i.startswith('a9.') and len(parts) == 4 and parts[1] in tabs:
        acc, base, size = tabs[parts[1]]
        return TAB_KEY + ((acc & 0xFFFF) << 12) + (int(e['addr'], 16) - base) // size
    return NONE_KEY + n


def write_strings(out):
    tabs = tables()
    lines = ['%s\t%X' % (e['id'], key_of(e, tabs, n)) for n, e in enumerate(entries())]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(lines)


def convert(logdir, outdir, tag=''):
    """Every log.txt under logdir -> outdir/<tag><run>/log.txt with TEXT lines; returns (runs, bad SCR pcs)."""
    img = ROM_IMG.read_bytes()
    qimg = QUEST_IMG.read_bytes()
    words = ptr_words()
    arm9 = ARM9.read_bytes()
    first = {acc: first_id(arm9, acc) for acc, _, _ in tables().values()}
    runs, bad = 0, collections.Counter()
    for log in sorted(Path(logdir).rglob('log.txt')):
        if outdir in log.parents or log.parent.name == '_textcov':
            continue
        keys = set()
        for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
            f = line.split()
            if len(f) == 2 and f[0] == 'SCR':
                pc = int(f[1], 16)
                if pc + 5 <= len(img) and img[pc] in SCR_OPS:
                    keys.add(ROM_KEY + struct.unpack_from('<I', img, pc + 1)[0])
                else:
                    bad[pc] += 1
            elif len(f) == 3 and f[0] == 'NAM' and f[1] in ('m', 'w'):
                keys.add(NAME_KEY + (0x100 if f[1] == 'w' else 0) + int(f[2]))
            elif len(f) == 2 and f[0] == 'PTR':
                k = words.get(int(f[1], 16))
                if k:
                    keys.add(k)
            elif len(f) == 2 and f[0] == 'QST':
                pc = int(f[1], 16)
                if pc + 5 <= len(qimg) and qimg[pc] in QUEST_OPS:
                    keys.add(QUEST_KEY + struct.unpack_from('<I', qimg, pc + 1)[0])
                else:
                    bad[pc] += 1
            elif len(f) == 3 and f[0] == 'TAB':
                acc, i = int(f[1], 16), int(f[2], 16)
                if acc in first:
                    keys.add(TAB_KEY + ((acc & 0xFFFF) << 12) + i - first[acc])
        if not keys:
            continue
        d = outdir / (tag + str(log.parent.relative_to(logdir)).replace('\\', '/').replace('/', '__'))
        d.mkdir(parents=True, exist_ok=True)
        (d / 'log.txt').write_text(''.join('TEXT %X\n' % k for k in sorted(keys)), encoding='utf-8')
        runs += 1
    return runs, bad


def cmd_report(a):
    out = ROOT / 'work' / 'qa' / '_textcov'
    if out.exists():
        shutil.rmtree(out)
    strings = ROOT / 'build' / 'strings.tsv'
    n = write_strings(strings)
    runs, bad = 0, collections.Counter()
    for k, logdir in enumerate(a.logdir):
        r, b = convert(Path(logdir).resolve(), out, '%d_' % k)
        runs += r
        bad += b
    print('strings %d, runs with text %d, SCR pcs not at a 70/9E opcode %d' % (n, runs, len(bad)))
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'textcover.py'), str(out), str(strings)]
    if a.waive:
        cmd += ['--waive', a.waive]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    missing = [ln.split()[2] for ln in r.stdout.splitlines() if ln.startswith('NEVER SHOWN')]
    kind = {e['id']: e.get('kind', '?') for e in entries()}
    by = collections.Counter(kind.get(m, '?').split('.')[0] if not m.startswith('rom.') else 'rom.msg' for m in missing)
    total = collections.Counter(k.split('.')[0] if not i.startswith('rom.') else 'rom.msg' for i, k in kind.items())
    for k in sorted(total):
        print('  %-10s %5d not shown of %5d' % (k, by.get(k, 0), total[k]))
    if a.list:
        print(r.stdout)
    print(r.stdout.splitlines()[-1] if r.stdout.strip() else r.stderr.strip())
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('report')
    s.add_argument('logdir', nargs='+', help='run directories (tour, gallery, ...), each searched for log.txt')
    s.add_argument('--waive')
    s.add_argument('--list', action='store_true')
    s = sub.add_parser('strings')
    s.add_argument('--out', default=str(ROOT / 'build' / 'strings.tsv'))
    a = ap.parse_args()
    if a.cmd == 'strings':
        print(write_strings(Path(a.out)))
        return 0
    return cmd_report(a)


if __name__ == '__main__':
    sys.exit(main())
