"""Linear disassembler for the `scr\\x1a` script bytecode (field/script/rom.img, quest/quest.img).

Opcode lengths come from the game's own table in arm9 (0x021953D0, 0xC0 bytes, total length incl. opcode byte;
handlers at 0x02195490). Length 0 = no fixed length (00 = end, BF = unused).

    python -X utf8 tools/scrdis.py FILE START [END] [--arm9 work/fs/arm9.bin]

Prints `offset: op bytes` one instruction per line; a u32 operand that points at a `53 53`-prefixed string is
decoded with tbl/jp.tbl. Analysis only (phase 2 recon; phase 4 builds the real walker from entry points).
"""
import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
LEN_TABLE = 0x021953D0
ARM9_BASE = 0x02000000


def lengths(arm9):
    o = LEN_TABLE - ARM9_BASE
    return arm9[o:o + 0xC0]


def decode_string(data, off, tbl):
    out = []
    while off + 1 < len(data):
        c = struct.unpack_from('<H', data, off)[0]
        if c == 0:
            break
        out.append(tbl.get(c, '[%04X]' % c))
        off += 2
        if len(out) > 60:
            out.append('…')
            break
    return ''.join(out)


def load_tbl(path):
    t = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            try:
                t[struct.unpack('<H', bytes.fromhex(k))[0]] = v  # key = LE byte pair
            except ValueError:
                pass
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('start', type=lambda s: int(s, 16))
    ap.add_argument('end', nargs='?', type=lambda s: int(s, 16))
    ap.add_argument('--arm9', default='work/fs/arm9.bin')
    ap.add_argument('--tbl', default='tbl/jp.tbl')
    a = ap.parse_args()
    data = Path(a.file).read_bytes()
    lens = lengths(Path(a.arm9).read_bytes())
    tbl = load_tbl(a.tbl)
    pc, end = a.start, a.end or len(data)
    while pc < end:
        op = data[pc]
        n = lens[op] if op < 0xC0 else 0
        if n == 0:
            print('%05X: %02X  ; len 0 (end/unknown)' % (pc, op))
            n = 1
        raw = data[pc:pc + n]
        note = ''
        if n >= 5:
            v = struct.unpack_from('<I', raw, 1)[0]
            if 4 <= v < len(data) - 2 and data[v - 2:v] == b'SS':
                note = '  ; "%s"' % decode_string(data, v, tbl)
        print('%05X: %s%s' % (pc, raw.hex(' '), note))
        pc += n


if __name__ == '__main__':
    main()
