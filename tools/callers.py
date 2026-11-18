"""Walk ARM call chains upward from an address in arm9.bin: function start (nearest preceding push/stmdb ..lr),
then BL callers and pointer references, to DEPTH. Marks field-script opcode handlers (table 0x02195490).

    python -X utf8 tools/callers.py ADDR [--depth 4] [--arm9 work/fs/arm9.bin]
Recon helper (phase 2): e.g. which script opcode opens the shop UI.
"""
import argparse
import struct
from pathlib import Path

BASE = 0x02000000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('addr', type=lambda s: int(s, 16))
    ap.add_argument('--depth', type=int, default=4)
    ap.add_argument('--arm9', default='work/fs/arm9.bin')
    a = ap.parse_args()
    d = Path(a.arm9).read_bytes()
    words = struct.unpack_from('<%dI' % (len(d) // 4), d)
    handlers = {w: i for i, w in enumerate(struct.unpack_from('<192I', d, 0x02195490 - BASE))}

    def fstart(addr):
        i = (addr - BASE) // 4
        while i > 0:
            w = words[i]
            # push {.., lr} = stmdb sp!, {...lr}: 0xE92D4xxx ; also stmdb sp!,{lr} = E52DE004
            if (w & 0xFFFF4000) == 0xE92D4000 or w == 0xE52DE004:
                return BASE + i * 4
            i -= 1
        return None

    bl_callers = {}
    ptr_refs = {}
    for i, w in enumerate(words):
        pc = BASE + i * 4
        if (w & 0x0F000000) == 0x0B000000 and (w >> 28) != 0xF:  # BL (any cond)
            off = w & 0xFFFFFF
            if off & 0x800000:
                off -= 0x1000000
            bl_callers.setdefault(pc + 8 + off * 4, []).append(pc)
        if BASE <= w < BASE + len(d):
            ptr_refs.setdefault(w, []).append(pc)

    seen = set()

    def up(addr, depth, ind):
        f = fstart(addr)
        if f is None or f in seen:
            return
        seen.add(f)
        tag = ' <= script opcode %02X handler' % handlers[f] if f in handlers else ''
        print('%s%08X (func of %08X)%s' % ('  ' * ind, f, addr, tag))
        if depth == 0:
            return
        for c in bl_callers.get(f, [])[:12]:
            up(c, depth - 1, ind + 1)
        for p in ptr_refs.get(f, [])[:6]:
            print('%s  ptr @%08X' % ('  ' * ind, p))

    up(a.addr, a.depth, 0)


if __name__ == '__main__':
    main()
