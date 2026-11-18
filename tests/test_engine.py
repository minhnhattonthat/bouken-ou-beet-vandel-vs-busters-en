"""English engine (tools/engine.py, docs/re/vwf.md): encoder rules and the arm9 patch."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402
import engine  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.is_file(), reason="no ROM dump in rom/")


@pytest.fixture(scope="module")
def rom():
    import ndspy.rom
    return ndspy.rom.NintendoDSRom(build.ROM.read_bytes())


@pytest.fixture(scope="module")
def eng(rom):
    return engine.Engine.from_rom(rom)


def test_every_letter_has_a_glyph(eng):
    for ch, slot in engine.SLOT.items():
        assert 0 < eng.w12[slot] <= 12, ch
        assert 0 < eng.w8[slot] <= 12, ch


def test_pairs_fit_the_glyph_buffer(eng):
    text = ''.join(ch for ch in engine.SLOT) * 2
    for c in eng.codes(text):
        assert engine.EBASE <= c < engine.EEND
        assert eng.code_width(c, 12) <= engine.PAIR_MAX
        assert eng.code_width(c, 8) <= engine.PAIR_MAX


def test_controls_pass_through(eng):
    codes = eng.codes('Hi{br}there{page}[FF00]!{close}')
    assert 0xFF70 in codes and 0xFF72 in codes and 0xFF00 in codes and 0xFF71 in codes
    assert eng.width('Hi') == eng.letter_width('H') + eng.letter_width('i')


def test_unknown_letter_rejected(eng):
    with pytest.raises(ValueError):
        eng.codes('café')


def test_arm9_patch(rom, eng):
    import copy
    r = copy.copy(rom)
    log = []
    labels = eng.patch_arm9(r, log)
    a = bytes(r.arm9)
    p = struct.unpack_from('<9I', a, engine.MODPARAMS - engine.A9)
    assert p[1] - engine.A9 == len(a)
    blocks = [struct.unpack_from('<3I', a, p[0] - engine.A9 + i * 12) for i in range((p[1] - p[0]) // 12)]
    assert blocks[-1][0] == engine.BLOCK
    arena = struct.unpack_from('<I', a, engine.ARENA_LIT - engine.A9)[0]
    assert arena == engine.BLOCK + blocks[-1][1]
    assert len(log) == len(engine.SITES)
    assert all(v < engine.BLOCK + 0x400 for v in labels.values())
