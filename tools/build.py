"""build.py: build build/beet_en.nds from the pinned Japanese dump.

    python -X utf8 tools/build.py [--out build/beet_en.nds]

Steps: check the dump against rom.sha1, load it with ndspy, apply the edits (none yet: phase 3 identity build),
rebuild the NitroFS image and restore what ndspy does not keep byte-exact:
  - the word at 0x1000 (ndspy writes a size there; the original keeps its own bytes);
  - padding between regions (ndspy pads with 0xFF, the original with 0x00): every gap of the rebuilt layout takes the
    original's byte where the original also has a gap there, else 0x00; past the used size it stays 0xFF;
  - the cartridge size: padded with 0xFF back to the original length.
With no edits the output is byte-identical to the dump (tests/test_build.py)."""
import argparse
import struct
import sys
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_rom  # noqa: E402

ROM = ROOT / "rom" / "Bouken-ou Beet - Vandel vs. Busters (Japan).nds"
OUT = ROOT / "build" / "beet_en.nds"
ICON_SIZE = 0x840  # banner v1
NITRO_FOOTER = 12  # 0xDEC00621 + module params offset + 0, kept after arm9 by ndspy


def used_ranges(b):
    """(start, end) of every region the header and FAT point at."""
    r = [(0, 0x4000)]
    a9o, _, _, a9s = struct.unpack_from("<4I", b, 0x20)
    a7o, _, _, a7s = struct.unpack_from("<4I", b, 0x30)
    fnto, fnts, fato, fats = struct.unpack_from("<4I", b, 0x40)
    icon = struct.unpack_from("<I", b, 0x68)[0]
    r += [(a9o, a9o + a9s + NITRO_FOOTER), (a7o, a7o + a7s), (fnto, fnto + fnts), (fato, fato + fats)]
    if icon:
        r.append((icon, icon + ICON_SIZE))
    for i in range(fats // 8):
        s, e = struct.unpack_from("<II", b, fato + 8 * i)
        if e > s:
            r.append((s, e))
    return sorted(r)


def gaps(b, end):
    out, pos = [], 0
    for s, e in used_ranges(b):
        if s > pos:
            out.append((pos, s))
        pos = max(pos, e)
    if pos < end:
        out.append((pos, end))
    return out


def in_gap_mask(b, size):
    m = bytearray(size)
    for s, e in gaps(b, len(b)):
        m[s:min(e, size)] = b"\x01" * (min(e, size) - s)
    return m


def finish(orig, new):
    """Make ndspy's output match the original wherever the build did not change anything."""
    new = bytearray(new)
    new[0x1000:0x1004] = orig[0x1000:0x1004]
    used_end = struct.unpack_from("<I", new, 0x80)[0]
    if len(new) < len(orig):
        new += b"\xff" * (len(orig) - len(new))
    orig_gap = in_gap_mask(orig, len(new))
    for s, e in gaps(bytes(new), len(new)):
        new[s:e] = bytes(orig[i] if i < len(orig) and orig_gap[i] else (0 if i < used_end else 0xFF)
                         for i in range(s, e))
    return bytes(new)


def build(out=OUT):
    check_rom.check()
    orig = ROM.read_bytes()
    rom = ndspy.rom.NintendoDSRom(orig)
    # Edits go here (phase 7: insert text, fonts, graphics, code hooks).
    data = finish(orig, rom.save())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()
    import hashlib
    data = build(a.out)
    same = data == ROM.read_bytes()
    print(f"{a.out}  {len(data)} bytes  sha1 {hashlib.sha1(data).hexdigest()}  identical to dump: {same}")


if __name__ == "__main__":
    main()
