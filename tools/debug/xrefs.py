"""xrefs.py: every u32 operand in rom.img / quest.img / arm9 that points into a rom.img range (phase 8 waivers).

    python -X utf8 tools/debug/xrefs.py FROM TO

Lists script instructions (rom.img, by the opcode length table) whose operand bytes hold a u32 in [FROM, TO), plus
raw aligned and unaligned u32 hits in quest.img and arm9.bin (rom.img offsets are absolute u32 operands). Used to show a
block is unreachable: no jump, call or table word points into it.
"""
import argparse
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from scr import parse_rom_img  # noqa: E402

FS = ROOT / 'work' / 'fs'


def raw_hits(buf, lo, hi):
    return [i for i in range(len(buf) - 3) if lo <= struct.unpack_from('<I', buf, i)[0] < hi]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lo', type=lambda x: int(x, 16))
    ap.add_argument('hi', type=lambda x: int(x, 16))
    a = ap.parse_args()
    rom = (FS / 'fs' / 'field' / 'script' / 'rom.img').read_bytes()
    s = parse_rom_img(rom, (FS / 'arm9.bin').read_bytes())
    n = 0
    for pc in sorted(s.ins):
        ln = s.ins[pc]
        for k in range(1, ln - 3):
            v = struct.unpack_from('<I', rom, pc + k)[0]
            if a.lo <= v < a.hi and not (a.lo <= pc < a.hi and rom[pc] in (0x70, 0x9E)):
                print('rom.img ins %X op %02X +%d -> %X' % (pc, rom[pc], k, v))
                n += 1
    for name, path in (('quest.img', FS / 'fs' / 'quest' / 'quest.img'), ('arm9', FS / 'arm9.bin')):
        if not path.exists():
            print('missing', path)
            continue
        hits = raw_hits(path.read_bytes(), a.lo, a.hi)
        print('%s: %d raw u32 hits%s' % (name, len(hits), ' ' + ' '.join('%X' % h for h in hits[:20]) if hits else ''))
    print('rom.img instruction refs:', n)


if __name__ == '__main__':
    main()
