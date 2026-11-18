"""Identity build: with no edits, tools/build.py must rebuild the dump byte for byte (keep this green forever)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402


@pytest.mark.skipif(not build.ROM.is_file(), reason="no ROM dump in rom/")
def test_identity_rebuild(tmp_path):
    import ndspy.rom
    orig = build.ROM.read_bytes()
    data = build.finish(orig, ndspy.rom.NintendoDSRom(orig).save())
    assert len(data) == len(orig)
    if data != orig:
        first = next(i for i in range(len(orig)) if data[i] != orig[i])
        pytest.fail(f"rebuilt ROM differs from the dump, first at 0x{first:X}")


@pytest.mark.skipif(not build.ROM.is_file(), reason="no ROM dump in rom/")
def test_file_replace_roundtrip():
    """Replacing every file with its own bytes (the path edits will take) still rebuilds identically."""
    import ndspy.rom
    orig = build.ROM.read_bytes()
    rom = ndspy.rom.NintendoDSRom(orig)
    rom.files = [bytes(f) for f in rom.files]
    rom.arm9 = bytes(rom.arm9)
    assert build.finish(orig, rom.save()) == orig
