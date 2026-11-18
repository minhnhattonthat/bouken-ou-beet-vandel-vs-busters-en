"""List every ARM BL/BLX and Thumb BL into one or more addresses in arm9.bin (direct calls only).

    python -X utf8 tools/debug/blscan.py 0x020146E0 [0x020146CC ..] [--arm9 work/fs/arm9.bin]
Prints `caller -> target` (Thumb callers marked t). Recon helper: who fetches a table record.
"""
import argparse
import struct
from pathlib import Path

BASE = 0x02000000


def scan(d, targets):
    out = []
    n = len(d) // 4
    for i in range(n):
        w = struct.unpack_from('<I', d, i * 4)[0]
        pc = BASE + i * 4
        if (w >> 24) & 0xF == 0xB and (w >> 28) != 0xF:  # BL (any cond)
            off = w & 0xFFFFFF
            if off & 0x800000:
                off -= 0x1000000
            t = pc + 8 + off * 4
            if t in targets:
                out.append((pc, t, 'a'))
        elif (w >> 25) == 0x7D:  # BLX imm (to Thumb)
            off = w & 0xFFFFFF
            if off & 0x800000:
                off -= 0x1000000
            t = pc + 8 + off * 4 + ((w >> 24) & 1) * 2
            if t in targets:
                out.append((pc, t, 'ax'))
    for i in range(len(d) // 2 - 1):
        h1, h2 = struct.unpack_from('<HH', d, i * 2)
        if (h1 & 0xF800) == 0xF000 and (h2 & 0xE800) in (0xE800, 0xF800):
            off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
            if off & 0x400000:
                off -= 0x800000
            pc = BASE + i * 2
            t = pc + 4 + off
            if (h2 & 0xF800) == 0xE800:
                t &= ~3
            if t in targets:
                out.append((pc, t, 't'))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('addrs', nargs='+', type=lambda s: int(s, 16))
    ap.add_argument('--arm9', default='work/fs/arm9.bin')
    a = ap.parse_args()
    d = Path(a.arm9).read_bytes()
    for pc, t, k in scan(d, set(a.addrs)):
        print(f'{pc:08X} -> {t:08X} {k}')


if __name__ == '__main__':
    main()
