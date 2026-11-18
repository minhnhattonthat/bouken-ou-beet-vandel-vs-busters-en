"""romleft.py: why the rom.msg strings left in a textcov --list were never shown (phase 8 coverage).

    python -X utf8 tools/debug/romleft.py work/qa/missing.txt [-v]

For every `NEVER SHOWN  rom.XXXXX` line: the ops that point at the string (opcode, pc), whether the string has any
70/9E reference (gallery site), and counts per referencing opcode. -v prints one line per string.
"""
import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from scr import parse_rom_img  # noqa: E402

FS = ROOT / 'work' / 'fs'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('missing')
    ap.add_argument('-v', action='store_true')
    a = ap.parse_args()
    data = (FS / 'fs' / 'field' / 'script' / 'rom.img').read_bytes()
    s = parse_rom_img(data, (FS / 'arm9.bin').read_bytes())
    ids = [ln.split()[2] for ln in open(a.missing, encoding='utf8') if ln.startswith('NEVER SHOWN  rom.')]
    by = collections.Counter()
    for sid in ids:
        start = int(sid.split('.')[1], 16)
        refs = s.refs.get(start, [])
        ops = sorted({'%02X' % data[pc] for pc, k in refs})
        key = ','.join(ops) or 'none'
        by[key] += 1
        if a.v:
            print(sid, key, ' '.join('%X:%d' % (pc, k) for pc, k in refs[:4]), s.strs.get(start, (0, '?'))[1])
    for k, n in by.most_common():
        print('%5d  %s' % (n, k))


if __name__ == '__main__':
    main()
