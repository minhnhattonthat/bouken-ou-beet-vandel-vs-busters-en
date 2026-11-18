"""textwidth.py: pixel width of English strings in the game's engine (tools/engine.py), 12 px or 8 px font.

    python -X utf8 tools/textwidth.py "Shako the Elder" "Grand Elder Shako" [--font 8]
    python -X utf8 tools/textwidth.py --fill 70 [--char M]   # a string of exactly ~70 px, for --qa width tests
"""
import argparse
import sys
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402

ROM = next((ROOT / 'rom').glob('*.nds'))


def load():
    return engine.Engine.from_rom(ndspy.rom.NintendoDSRom.fromFile(str(ROM)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text', nargs='*')
    ap.add_argument('--font', type=int, default=12, choices=(8, 12))
    ap.add_argument('--fill', type=int, help='print the longest run of --char at most this many px wide')
    ap.add_argument('--char', default='m')
    a = ap.parse_args()
    eng = load()
    for s in a.text:
        print('%4d px  %3d bytes  %r' % (eng.width(s, a.font), len(eng.encode(s)), s))
    if a.fill:
        s = ''
        while eng.width(s + a.char, a.font) <= a.fill:
            s += a.char
        print('%4d px  %r' % (eng.width(s, a.font), s))


if __name__ == '__main__':
    main()
