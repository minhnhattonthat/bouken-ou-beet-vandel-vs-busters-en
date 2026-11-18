"""a9tables.py: find arm9's record accessors `get(id) = base + (id - 1) * size` and list their tables.

The game reads its fixed-record tables (items, monsters, weapons, shouts...) through tiny leaf functions:
    ldr rB, =base ; sub rI, r0, #1 ; mov rS, #size ; mla r0, rI, rS, rB ; bx lr      (size any immediate)
    ldr rB, =base ; sub r0, r0, #1 ; add r0, rB, r0, lsl #k ; bx lr                  (size 1 << k)
This scans arm9 for both shapes (any registers) with capstone and prints `accessor base size`.

    python -X utf8 tools/a9tables.py [--arm9 work/fs/arm9.bin]
"""
import argparse
import struct
from pathlib import Path

BASE = 0x02000000


def accessors(arm9):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    out = []
    for p in range(0, len(arm9) - 24, 4):
        w = struct.unpack_from('<I', arm9, p)[0]
        if w & 0xFFFF0000 != 0xE59F0000:       # ldr rX, [pc, #imm]
            continue
        ins = list(md.disasm(arm9[p:p + 20], BASE + p))
        if len(ins) < 3:
            continue
        one = 1
        if ins[1].mnemonic == 'sub' and ins[1].op_str.endswith('#1'):
            ins = ins[:1] + ins[2:]   # 1-based ids
        else:
            one = 0
        lit = p + 8 + (w & 0xFFF)
        if lit + 4 > len(arm9):
            continue
        base = struct.unpack_from('<I', arm9, lit)[0]
        if not BASE <= base < BASE + len(arm9):
            continue
        size = None
        mn = [i.mnemonic for i in ins]
        if mn[1:4] == ['mov', 'mla', 'bx'] and '#' in ins[1].op_str:
            size = int(ins[1].op_str.split('#')[1], 0)
        elif mn[1:3] == ['add', 'bx'] and 'lsl #' in ins[1].op_str:
            size = 1 << int(ins[1].op_str.split('lsl #')[1], 0)
        if size:
            out.append((BASE + p, base, size, one))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--arm9', default='work/fs/arm9.bin')
    a = ap.parse_args()
    for acc, base, size in sorted(accessors(Path(a.arm9).read_bytes()), key=lambda x: x[1]):
        print('%08X  base %08X  size %#x' % (acc, base, size))


if __name__ == '__main__':
    main()
