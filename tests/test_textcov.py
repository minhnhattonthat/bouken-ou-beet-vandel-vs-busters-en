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


@pytest.mark.skipif(not textcov.QUEST_IMG.exists(), reason='needs work/fs (tools/romls.py --unpack)')
def test_quest_and_ptr_lines_map(tmp_path):
    q = textcov.QUEST_IMG.read_bytes()
    pc = q.index(b'\x20' + struct.pack('<I', 0x59C))        # quest.0059C title
    run = tmp_path / 'logs' / 'scene'
    run.mkdir(parents=True)
    (run / 'log.txt').write_text('QST %X\nPTR 200B0B8\nPTR 1234\n' % pc, encoding='utf-8')
    runs, bad = textcov.convert(tmp_path / 'logs', tmp_path / 'out')
    assert runs == 1 and not bad
    got = (tmp_path / 'out' / 'scene' / 'log.txt').read_text().split()
    assert got == ['TEXT', '%X' % (textcov.QUEST_KEY + 0x59C), 'TEXT', '%X' % (textcov.PTR_KEY + 0x00B0B8)]
    tabs = textcov.tables()
    keys = {e['id']: textcov.key_of(e, tabs, n) for n, e in enumerate(textcov.entries())}
    assert keys['quest.0059C'] == textcov.QUEST_KEY + 0x59C and keys['a9.0219AD0C'] == textcov.PTR_KEY + 0xB0B8


@pytest.mark.skipif(not textcov.ARM9.exists(), reason='needs work/fs (tools/romls.py --unpack)')
def test_tab_ids_map_to_records(tmp_path):
    # weapon ids are 0x100 + inventory byte (accessor masks & 0xFF, then - 1); vandel/buster ids start 0x13F / 0x15E
    run = tmp_path / 'logs' / 'scene'
    run.mkdir(parents=True)
    (run / 'log.txt').write_text('TAB 2014684 11A\nTAB 2014608 13F\nTAB 2014628 15F\n', encoding='utf-8')
    textcov.convert(tmp_path / 'logs', tmp_path / 'out')
    got = set((tmp_path / 'out' / 'scene' / 'log.txt').read_text().split()[1::2])
    assert got == {'%X' % (textcov.TAB_KEY + (acc << 12) + i) for acc, i in ((0x4684, 0x19), (0x4608, 0), (0x4628, 1))}


def test_gallery_spans_cover_dialogue():
    sys.path.insert(0, str(ROOT / 'tools' / 'debug'))
    import gallery
    if not (gallery.FS / 'arm9.bin').exists():
        pytest.skip('needs work/fs')
    data, s, pcs = gallery.sites()
    spans = gallery.spans(data, s, pcs)
    assert all(any(a <= p < b for a, b in spans) for p in pcs)       # every site inside a span
    assert all(data[a] in (0x2A, 0x9E, 0x70) for a, _ in spans)
    assert len(pcs) >= 4100


def test_waiver_prefix_expands_and_needs_reason(tmp_path):
    src = tmp_path / 'w.tsv'
    src.write_text('# comment\na9.title.*\tdev label\na9.area.000.name\tone id\n', encoding='utf-8')
    rows = textcov.expand_waivers(src, tmp_path / 'out.tsv').read_text(encoding='utf-8').split('\n')
    ids = [r.split('\t')[0] for r in rows if r]
    assert 'a9.title.000.name' in ids and 'a9.area.000.name' in ids
    assert sum(i.startswith('a9.title.') for i in ids) == 130
    for bad in ('a9.title.*\n', 'a9.title.*\t \n', 'no.such.id\twhy\n', 'no.such.*\twhy\n'):
        src.write_text(bad, encoding='utf-8')
        with pytest.raises(SystemExit):
            textcov.expand_waivers(src, tmp_path / 'out.tsv')
    # the real waiver file parses
    textcov.expand_waivers(ROOT / 'docs' / 'text_unshown.tsv', tmp_path / 'real.tsv')
