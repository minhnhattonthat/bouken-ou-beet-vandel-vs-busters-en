"""English engine (tools/engine.py, docs/re/vwf.md): encoder rules and the arm9 patch."""
import re
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


def test_fullwidth_latin_maps_to_single_letters(eng):
    # name entry writes full-width Latin (code = glyph index + 1); the hooks draw them as single English letters
    for ch in 'AZaz':
        fw = engine.glyph_index(ch) + 1
        assert engine.fullwidth_code(fw) == engine.EBASE + engine.SLOT[ch] * 128, ch
        assert eng.code_width(fw) == eng.letter_width(ch)
    for c in (engine.FW['FW_UP'] - 1, engine.FW['FW_UP'] + 26, engine.FW['FW_LO'] + 26, 0x0001, 0xFF70):
        assert engine.fullwidth_code(c) == c


def test_relocated_pointer_string(rom):
    # a pointer string that outgrew its room moves into the block; every pointer word then points at the copy
    import copy
    r = copy.copy(rom)
    e = engine.Engine.from_rom(rom)
    old, ptrs = 0x021B6C78, [0x02000000 + o for o in range(0, len(rom.arm9) - 3, 4)
                             if struct.unpack_from('<I', rom.arm9, o)[0] == 0x021B6C78]
    assert ptrs
    data = e.encode('A line much longer than the Japanese it replaces, to force a move')
    e.relocate_string(old, ptrs, data)
    labels = e.patch_arm9(r)
    a = bytes(r.arm9)
    p = struct.unpack_from('<9I', a, engine.MODPARAMS - engine.A9)
    size = struct.unpack_from('<3I', a, p[1] - engine.A9 - 12)[1]
    blk = p[0] - engine.A9 - size
    for w in ptrs:
        to = struct.unpack_from('<I', a, w - engine.A9)[0]
        assert to == labels['R_STRINGS']
        o = blk + to - engine.BLOCK
        assert a[o:o + len(data) + 2] == data + b'\0\0'


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
    # append + module params + arena literal + one per site + two per relocated table (literal, scale insn)
    assert len(log) == 3 + len(engine.SITES) + 2 * len(engine.RELOC)
    assert all(re.match(r'arm9 (append [0-9A-F]+ |[0-9A-F]+ [0-9a-f]+ [0-9a-f]+ )', line) for line in log)
    assert all(v < engine.BLOCK + 0x400 for k, v in labels.items() if not k.startswith('R_'))
    # relocated tables: the accessor literal points at the copy in the block (block = autoload at BLOCK, stored
    # at file offset p[0] - size), which holds the original records at the new stride
    size = blocks[-1][1]
    blk = p[0] - engine.A9 - size
    for key, rl in engine.RELOC.items():
        new_base = struct.unpack_from('<I', a, rl['lit'] - engine.A9)[0]
        assert new_base == labels['R_' + key]
        o = blk + new_base - engine.BLOCK
        assert a[o:o + rl['count'] * rl['new']] == eng.reloc_default(rom.arm9, key)
        assert a[rl['insn'] - engine.A9:rl['insn'] - engine.A9 + 4].hex() != rl['orig']
