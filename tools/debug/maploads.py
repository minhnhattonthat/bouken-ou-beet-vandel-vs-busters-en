"""List map-load scripts in field/script/rom.img: `66 77 xx 64 <map u16> 69 <u16> <x u16> <y u16> <u8> 17 <setup>`.

    python -X utf8 tools/debug/maploads.py [--map 70] [--setup 29DA1]

A warp to one of these offsets (scenes.tsv `event` kind) loads that map and its NPC setup with no event; with
`qXXXX` in the scene's `set` column, warp.lua then runs a talk event (one that loads no map) there.
Each row: offset, map, player x/y, NPC setup offset (the `17` target), and which NPC setups' `61` triggers point at
the given --setup's handlers is left to scrdis.py.
"""
import argparse
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--rom-img', default=str(REPO / 'work/fs/fs/field/script/rom.img'))
    ap.add_argument('--map', type=lambda s: int(s, 16))
    ap.add_argument('--setup', type=lambda s: int(s, 16))
    a = ap.parse_args()
    d = Path(a.rom_img).read_bytes()
    i = d.find(b'\x66\x77')
    while i >= 0:
        j = i + 3
        if d[j] == 0x64 and d[j + 3] == 0x69 and d[j + 11] == 0x17:
            m = struct.unpack_from('<H', d, j + 1)[0]
            _, x, y = struct.unpack_from('<HHH', d, j + 4)
            setup = struct.unpack_from('<I', d, j + 12)[0]
            if (a.map is None or m == a.map) and (a.setup is None or setup == a.setup):
                print('%05X\tmap=%X\tpos=%d,%d\tsetup=%05X' % (i, m, x, y, setup))
        i = d.find(b'\x66\x77', i + 1)


if __name__ == '__main__':
    main()
