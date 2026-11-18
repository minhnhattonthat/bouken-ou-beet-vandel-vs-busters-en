"""Find the ARM function holding an address (walk back to the nearest `push {.., lr}` / `stmdb sp!, {.., lr}`),
then list its direct callers (blscan) and literal-pool words pointing at it (method tables).

    python -X utf8 tools/debug/funcstart.py 0x020CC070 [..] [--arm9 work/arm9_jp.bin]
"""
import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blscan  # noqa: E402

BASE = 0x02000000


def start_of(d, addr, limit=0x2000):
    o = addr - BASE
    while o > 0 and addr - BASE - o < limit:
        w = struct.unpack_from('<I', d, o)[0]
        # STMDB sp!, {...lr} = E92D4xxx (push with lr)
        if w & 0xFFFF4000 == 0xE92D4000:
            return BASE + o
        o -= 4
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('addrs', nargs='+')
    ap.add_argument('--arm9', default='work/arm9_jp.bin')
    a = ap.parse_args()
    d = Path(a.arm9).read_bytes()
    for s in a.addrs:
        f = start_of(d, int(s, 0))
        if f is None:
            print(f'{s}: no push found')
            continue
        words = [BASE + o for o in range(0, len(d) - 3, 4) if struct.unpack_from('<I', d, o)[0] == f]
        print(f'{s}: function {f:08X}; literal words at {" ".join(f"{w:08X}" for w in words) or "-"}')
        for site, tgt, mode in blscan.scan(d, [f]):
            print(f'  {site:08X} -> {tgt:08X} {mode}')


if __name__ == '__main__':
    main()
