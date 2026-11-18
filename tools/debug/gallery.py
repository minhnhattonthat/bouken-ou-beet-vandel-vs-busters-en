"""gallery.py: the message-gallery site list for tools/debug/gallery.lua (text coverage, phase 8).

    python -X utf8 tools/debug/gallery.py [--out work/qa/gallery/pcs.txt] [--chunks N]

Writes one hex rom.img pc per line: for every text string a `70` (message) or `9E` (speaker) operand points at, the
first instruction that points at it, sorted by pc (so a speaker op runs before the message after it). gallery.lua
feeds these to the field-script interpreter one by one, so the game's own message code fetches and draws every
script message and speaker tag; tools/lua/textlog.lua logs them for tools/textcov.py. With --chunks N it also prints
N index ranges `FROM-TO` (1-based, inclusive) for the gallery_* rows of tools/debug/scenes.tsv.
Strings reached only by other opcodes (`4F`/`99` quest place/client) are not in the list.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from scr import parse_rom_img  # noqa: E402

FS = ROOT / 'work' / 'fs'
OPS = (0x70, 0x9E)


def sites():
    data = (FS / 'fs' / 'field' / 'script' / 'rom.img').read_bytes()
    s = parse_rom_img(data, (FS / 'arm9.bin').read_bytes())
    out = set()
    for start, (end, kind) in s.strs.items():
        if kind != 'text':
            continue
        pcs = sorted(pc for pc, k in s.refs.get(start, []) if data[pc] in OPS and k == 1)
        if pcs:
            out.add(pcs[0])
    return data, s, sorted(out)


def spans(data, s, pcs):
    """(start, end) per site: the dialogue group around it, `2A` (open window) [`9E` speaker] `70` message .. `34`
    (wait for A, close). Walk back over 2A/9E/70 and forward over 9E/70 to the 34; groups shared by a speaker site
    and its message site are listed once."""
    order = sorted(s.ins)
    at = {pc: n for n, pc in enumerate(order)}
    out = []
    for pc in pcs:
        n = at[pc]
        a = n
        while a > 0 and data[order[a - 1]] in (0x2A, 0x9E, 0x70) and data[order[a]] != 0x2A:
            a -= 1
        b = n
        while b + 1 < len(order) and data[order[b + 1]] in (0x9E, 0x70):
            b += 1
        if b + 1 < len(order) and data[order[b + 1]] == 0x34:
            b += 1
        span = (order[a], order[b] + s.ins[order[b]])
        if not out or out[-1] != span:
            out.append(span)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(ROOT / 'work' / 'qa' / 'gallery' / 'pcs.txt'))
    ap.add_argument('--chunks', type=int, default=0)
    a = ap.parse_args()
    data, s, pcs = sites()
    pcs = spans(data, s, pcs)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(''.join('%X %X\n' % p for p in pcs), encoding='ascii')
    print('%d spans -> %s' % (len(pcs), out))
    if a.chunks:
        n = -(-len(pcs) // a.chunks)
        for i in range(0, len(pcs), n):
            print('%d-%d' % (i + 1, min(i + n, len(pcs))))


if __name__ == '__main__':
    main()
