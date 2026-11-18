"""romcheck.check_file catches each bad-write class on synthetic files."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import romcheck  # noqa: E402

ORIG = bytes(range(32))


def run(new, writes, append=None, name='x'):
    return romcheck.check_file(name, ORIG, bytes(new), writes, append)


def edited(*pairs):
    b = bytearray(ORIG)
    for off, data in pairs:
        b[off:off + len(data)] = data
    return b


def test_clean_write_passes():
    assert run(edited((4, b'\xaa\xbb')), [(4, ORIG[4:6], b'\xaa\xbb', 'w')]) == []


def test_stale_original_bytes():
    errs = run(edited((4, b'\xaa\xbb')), [(4, b'\0\0', b'\xaa\xbb', 'w')])
    assert any('original holds' in e for e in errs)


def test_overwritten_write():
    errs = run(edited((4, b'\xaa\xcc')), [(4, ORIG[4:6], b'\xaa\xbb', 'w')])
    assert any('overwritten' in e for e in errs)


def test_overlap():
    errs = run(edited((4, b'\xaa\xbb\xcc')), [(4, ORIG[4:6], b'\xaa\xbb', 'a'), (5, ORIG[5:7], b'\xbb\xcc', 'b')])
    assert any('overlap' in e for e in errs)


def test_uncovered_change():
    errs = run(edited((4, b'\xaa'), (20, b'\xee')), [(4, ORIG[4:5], b'\xaa', 'w')])
    assert any('no write behind' in e for e in errs)


def test_growth_needs_append():
    assert any('no append' in e for e in run(ORIG + b'\1\2', []))
    assert run(ORIG + b'\1\2', [], append=32) == []


def test_english_build_passes(tmp_path):
    """The English build from script/ touches only allowed files, every change logged and checked."""
    import build
    out = tmp_path / 'en.nds'
    build.build(out)
    errs, summary = romcheck.run(out, tmp_path / 'en.writes.txt')
    assert errs == [], errs[:5]
    assert 'arm9' in summary


def test_script_append_inside_data():
    errs = run(ORIG + b'\1\2', [], append=16, name='field/script/rom.img')
    assert any('inside the original data' in e for e in errs)
