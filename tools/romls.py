"""romls.py: list the NDS header, ARM9/overlays and every NitroFS file (size, magic, compression guess).

    python -X utf8 tools/romls.py [--unpack work/fs]   # --unpack writes every file (and arm9/overlays) to disk
"""
import argparse
import collections
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Bouken-ou Beet - Vandel vs. Busters (Japan).nds"


def magic(b):
    m = b[:4]
    if m and all(32 <= c < 127 for c in m):
        return m.decode()
    if b[:1] in (b"\x10", b"\x11", b"\x30", b"\x24", b"\x28") and len(b) >= 4:
        return f"cmp{b[0]:02X}(dec {int.from_bytes(b[1:4], 'little')})"
    return b[:4].hex()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unpack")
    a = ap.parse_args()
    rom = ndspy.rom.NintendoDSRom.fromFile(str(ROM))
    print("title", rom.name, "code", rom.idCode, "arm9", hex(len(rom.arm9)), "ram", hex(rom.arm9RamAddress),
          "arm7", hex(len(rom.arm7)), "overlays9", len(rom.arm9OverlayTable))
    out = Path(a.unpack) if a.unpack else None
    if out:
        out.mkdir(parents=True, exist_ok=True)
        (out / "arm9.bin").write_bytes(rom.arm9)
        (out / "arm7.bin").write_bytes(rom.arm7)
        for i, ov in rom.loadArm9Overlays().items():
            (out / f"overlay9_{i:03d}.bin").write_bytes(ov.data)
    stats = collections.Counter()
    for i, data in enumerate(rom.files):
        name = rom.filenames.filenameOf(i) or f"#{i}"
        m = magic(data)
        stats[m.split("(")[0]] += 1
        print(f"{i:5d} {len(data):8d} {m:24s} {name}")
        if out and rom.filenames.filenameOf(i):
            p = out / "fs" / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    print("magic counts:", dict(stats.most_common()))


if __name__ == "__main__":
    main()
