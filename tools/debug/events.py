"""List field-script event entries: targets of `17 <u32>` (jump to event) in field/script/rom.img.

For each entry: who jumps there, the first map load (`64 <u16>`), map changes (`98 <u16> x y`), battles
(`14 <u16> ...`) and the first message, found by walking the bytecode with the game's opcode-length table until
`FF` (end) or the next `17`. Used to pick warp targets for tools/debug/scenes.tsv.

    python -X utf8 tools/debug/events.py [--rom-img work/fs/fs/field/script/rom.img] [--arm9 work/fs/arm9.bin]
"""
import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scrdis import lengths, load_tbl, decode_string  # noqa: E402


def walk(data, lens, pc, limit=4000):
    """Yield (pc, op, raw) from pc until FF/unknown opcode/limit."""
    end = min(len(data), pc + limit)
    while pc < end:
        op = data[pc]
        n = lens[op] if op < 0xC0 else 0
        if n == 0:
            yield pc, op, data[pc:pc + 1]
            return
        yield pc, op, data[pc:pc + n]
        pc += n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--rom-img', default='work/fs/fs/field/script/rom.img')
    ap.add_argument('--arm9', default='work/fs/arm9.bin')
    ap.add_argument('--tbl', default='tbl/jp.tbl')
    a = ap.parse_args()
    data = Path(a.rom_img).read_bytes()
    lens = lengths(Path(a.arm9).read_bytes())
    tbl = load_tbl(a.tbl)
    # Reachable instructions: walk from known roots following 17/54/12 targets.
    roots = [4]
    seen_ins = set()
    callers = {}
    entries = set()
    todo = list(roots)
    while todo:
        pc = todo.pop()
        for p, op, raw in walk(data, lens, pc):
            if p in seen_ins:
                break
            seen_ins.add(p)
            if op in (0x17, 0x54, 0x12) and len(raw) == 5:
                t = struct.unpack_from('<I', raw, 1)[0]
                if 4 <= t < len(data):
                    if op == 0x17:
                        entries.add(t)
                        callers.setdefault(t, []).append(p)
                    todo.append(t)
    for t in sorted(entries):
        maps, moves, battles, msg = [], [], [], ''
        for p, op, raw in walk(data, lens, t):
            if op == 0x64 and len(raw) == 3:
                maps.append('%X' % struct.unpack_from('<H', raw, 1)[0])
            elif op == 0x98:
                moves.append('%X' % struct.unpack_from('<H', raw, 1)[0])
            elif op == 0x14:
                battles.append('%X' % struct.unpack_from('<H', raw, 1)[0])
            elif op == 0x70 and not msg:
                v = struct.unpack_from('<I', raw, 1)[0]
                if 2 <= v < len(data):
                    msg = decode_string(data, v, tbl)[:40]
            elif op == 0x17 and p != t:
                break
        print('%05X\tfrom=%s\tmap=%s\tmove=%s\tbattle=%s\t%s' % (
            t, ','.join('%X' % c for c in callers[t][:3]), ','.join(maps[:3]), ','.join(moves[:3]),
            ','.join(battles[:3]), msg))
    print('entries %d, instructions reached %d' % (len(entries), len(seen_ins)), file=sys.stderr)


if __name__ == '__main__':
    main()
