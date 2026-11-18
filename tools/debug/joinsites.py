"""List rom.img party-join instructions (`58` / `5A` / `5B`, first operand u16 = party type) with their pc, so a
member that joins only late in the story can be reached by queuing that pc in a warp (`q<pc>`).

    python -X utf8 tools/debug/joinsites.py [--types 6-14]
"""
import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scr import parse_rom_img  # noqa: E402
from debug.idsweep import ids_of  # noqa: E402
import ndspy.rom  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ROM = ROOT / 'rom' / 'Bouken-ou Beet - Vandel vs. Busters (Japan).nds'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--types', default='0-0x33')
    a = ap.parse_args()
    want = set(ids_of(a.types))
    rom = ndspy.rom.NintendoDSRom.fromFile(str(ROM))
    data = rom.getFileByName('field/script/rom.img')
    s = parse_rom_img(data, rom.arm9)
    for pc in sorted(s.ins):
        op = data[pc]
        if op in (0x58, 0x5A, 0x5B) and s.ins[pc] >= 3:
            t = struct.unpack_from('<H', data, pc + 1)[0]
            if t in want:
                print('%05X  %02X  type %02X  %s' % (pc, op, t, data[pc:pc + s.ins[pc]].hex(' ')))


if __name__ == '__main__':
    main()
