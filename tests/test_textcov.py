"""textcov.py: the Lua probe hooks every arm9 table accessor; keys are unique; a logged SCR pc maps to its string."""
import re
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arm9text  # noqa: E402
import textcov  # noqa: E402


def test_lua_accessors_match_tables():
    lua = (ROOT / 'tools' / 'lua' / 'textlog.lua').read_text(encoding='utf-8')
    block = lua.split('TEXT_ACCESSORS = {')[1].split('}')[0]
    got = {int(x, 16) for x in re.findall(r'0x([0-9A-Fa-f]+)', block)}
    assert got == {t[1] for t in arm9text.TABLES}


def test_keys_unique_per_record():
    tabs = textcov.tables()
    seen = {}
    for n, e in enumerate(textcov.entries()):
        k = textcov.key_of(e, tabs, n)
        if k in seen:   # only fields of one table record share a key
            a, b = seen[k].split('.'), e['id'].split('.')
            assert a[:3] == b[:3] and a[0] == 'a9', (seen[k], e['id'])
        seen.setdefault(k, e['id'])


@pytest.mark.skipif(not textcov.ROM_IMG.exists(), reason='needs work/fs (tools/romls.py --unpack)')
def test_scr_pc_maps_to_message(tmp_path):
    img = textcov.ROM_IMG.read_bytes()
    pc = img.index(b'\x70' + struct.pack('<I', 0x30CF8))
    run = tmp_path / 'logs' / 'scene'
    run.mkdir(parents=True)
    (run / 'log.txt').write_text('SCR %X\nSCR 0\n' % pc, encoding='utf-8')
    out = tmp_path / 'logs' / '_textcov'
    runs, bad = textcov.convert(tmp_path / 'logs', out)
    assert runs == 1 and list(bad) == [0]
    assert (out / 'scene' / 'log.txt').read_text() == 'TEXT %X\n' % (textcov.ROM_KEY + 0x30CF8)
