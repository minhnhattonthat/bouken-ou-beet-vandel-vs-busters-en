"""Phase 4 extraction: roundtrip (script/*.json `jp` re-encodes to the original bytes) and coverage (the script
containers are fully explained as code, strings, padding and known data; every string is in script/)."""
import json
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

import build  # noqa: E402
import extract  # noqa: E402
import scr  # noqa: E402
from text16 import Codec  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.is_file(), reason='no ROM dump in rom/')


@pytest.fixture(scope='module')
def rom():
    import ndspy.rom
    return ndspy.rom.NintendoDSRom(build.ROM.read_bytes())


@pytest.fixture(scope='module')
def codec():
    return Codec.load(extract.TBL)


def script_entries(prefix):
    out = {}
    for f in sorted((extract.SCRIPT / prefix).glob('*.json')) if prefix else []:
        for e in json.loads(f.read_text(encoding='utf-8'))['entries']:
            out[e['id']] = e
    return out


def check_container(s, string_ops, code_ops):
    data = s.data
    assert s.bad_ops == [], 'opcodes with no length inside code: %s' % ['%X' % p for p in s.bad_ops[:10]]
    miss = [(pc, k, v) for pc, k, v in scr._operands(s, string_ops) if 4 <= v < s.data_start and v not in s.strs]
    assert miss == [], 'string operands not on a string start: %s' % ['%X->%X' % (p, v) for p, k, v in miss[:10]]
    out = [(pc, v) for pc, k, v in scr._operands(s, string_ops) if not 4 <= v < s.data_start]
    assert out == [], 'string operands outside the code area: %s' % ['%X->%X' % x for x in out[:10]]
    jm = [(pc, v) for pc, k, v in scr._operands(s, code_ops) if 4 <= v < s.data_start and v not in s.ins]
    assert jm == [], 'jump targets not on an instruction: %s' % ['%X->%X' % x for x in jm[:10]]
    assert s.unref == [], 'strings nothing points at: %s' % ['%X' % x for x in s.unref]
    for p, b in s.pads.items():
        assert set(b) <= {0, 0x53}, 'pad at %X holds %s' % (p, b.hex())
    pieces = sorted([(p, p + n) for p, n in s.ins.items()] + [(p, e) for p, (e, _) in s.strs.items()]
                    + [(p, p + len(b)) for p, b in s.pads.items()] + list(s.data_blocks.items()))
    pos = 4
    for a, b in pieces:
        assert a == pos, 'gap or overlap at %X (next piece %X)' % (pos, a)
        pos = b
    assert pos == s.data_start
    for off, (end, form) in s.strs.items():
        if form == 'text':
            assert off % 4 == 0 and data[end - 2:end] == b'\0\0'


def check_json(prefix, data, s, codec):
    ents = script_entries(prefix)
    want = {'%s.%05X' % (prefix, off) for off, (e, form) in s.strs.items() if form == 'text'}
    assert set(ents) == want, 'script/%s ids differ from the parsed strings: missing %s, extra %s' % (
        prefix, sorted(want - set(ents))[:5], sorted(set(ents) - want)[:5])
    for id_, e in ents.items():
        off = int(id_.split('.')[1], 16)
        assert codec.encode(e['jp']) + b'\0\0' == data[off:s.strs[off][0]], id_


def test_rom_img(rom, codec):
    data = bytes(rom.getFileByName('field/script/rom.img'))
    s = scr.parse_rom_img(data, bytes(rom.arm9))
    check_container(s, scr.ROM_IMG_STRING_OPS, scr.ROM_IMG_CODE_OPS)
    check_json('rom', data, s, codec)
    assert len(s.strs) > 4000


def test_rom_img_tail_is_data(rom):
    """Nothing in the code area points into the data tail with a string operand, and the tail holds no SS pool."""
    data = bytes(rom.getFileByName('field/script/rom.img'))
    s = scr.parse_rom_img(data, bytes(rom.arm9))
    assert data[s.data_start:s.data_start + 4] == b'\0SSS'   # pool end `00`, S-fill to the aligned tables
    assert all(v < s.data_start for pc, k, v in scr._operands(s, scr.ROM_IMG_STRING_OPS))
    arm9 = bytes(rom.arm9)
    assert struct.pack('<II', 0x51BB8, 0x54A14) in arm9   # the arm9 record that points at the tables


def test_quest_img(rom, codec):
    data = bytes(rom.getFileByName('quest/quest.img'))
    s = scr.parse_quest_img(data, bytes(rom.arm9))
    check_container(s, scr.QUEST_STRING_OPS, scr.QUEST_CODE_OPS)
    check_json('quest', data, s, codec)
    tbl = struct.unpack_from('<8I', data, 0x11D4)
    assert all(v == 0 or v in s.ins for v in tbl)   # the 4F quest table holds quest.img code offsets


def test_names(rom, codec):
    ents = json.loads((extract.SCRIPT / 'names.json').read_text(encoding='utf-8'))['entries']
    by_id = {e['id']: e for e in ents}
    for f in extract.NAME_FILES:
        data = bytes(rom.getFileByName(f))
        tag = 'w' if 'woman' in f else 'm'
        assert len(data) % extract.NAME_REC == 0
        for i in range(len(data) // extract.NAME_REC):
            e = by_id.pop('name.%s%03d' % (tag, i))
            raw = codec.encode(e['jp']) + b'\0\0'
            off = i * extract.NAME_REC
            assert len(raw) <= extract.NAME_SLOT and raw == data[off:off + len(raw)], e['id']
    assert by_id == {}


def arm9_entries():
    out = {}
    for f in sorted((extract.SCRIPT / 'arm9').glob('*.json')):
        for e in json.loads(f.read_text(encoding='utf-8'))['entries']:
            out[e['id']] = e
    return out


def test_arm9_json_matches_extractor(rom, codec):
    import arm9text
    want = {e['id']: e['jp'] for _, ents in arm9text.extract(bytes(rom.arm9), codec).values() for e in ents}
    have = {k: e['jp'] for k, e in arm9_entries().items()}
    assert have == want, 'script/arm9 is out of date: run tools/extract.py --only arm9 --force'


def test_arm9_roundtrip(rom, codec):
    a = bytes(rom.arm9)
    B = 0x02000000
    for id_, e in arm9_entries().items():
        raw = codec.encode(e['jp'])
        if 'addr' in e:   # fixed slot: text then 0000, or text filling the slot
            p = int(e['addr'], 16) - B
            assert a[p:p + len(raw)] == raw, id_
            assert len(raw) == e['max'] or (len(raw) + 2 <= e['max'] and a[p + len(raw):p + len(raw) + 2] == b'\0\0')
            assert a[p + len(raw):p + e['max']].strip(b'\0') == b'', id_   # max only spans zeros
        else:
            p = int(id_[3:], 16) - B
            assert a[p:p + len(raw) + 2] == raw + b'\0\0', id_
            for w in e['ptrs']:
                assert struct.unpack_from('<I', a, int(w, 16) - B)[0] == p + B, (id_, w)


# Kana runs in arm9 that are numeric fields of the vandel/buster tables, not text (checked by eye).
ARM9_WAIVED = {0x0204BEC8, 0x0214C05E, 0x0214FA46, 0x0214FBFA, 0x0214FDAE, 0x0214FF62, 0x02150116}


def test_arm9_coverage(rom, codec):
    """Every run of >= 2 kana codes (kana at least half the run, ending in 0000) lies in an extracted slot/string."""
    import bisect
    import re
    a = bytes(rom.arm9)
    B = 0x02000000
    spans = []
    for id_, e in arm9_entries().items():
        p = int(e['addr'], 16) if 'addr' in e else int(id_[3:], 16)
        spans.append((p, p + (e['max'] if 'addr' in e else len(codec.encode(e['jp'])) + 2)))
    spans.sort()
    starts = [s for s, _ in spans]

    def covered(x):
        i = bisect.bisect_right(starts, x) - 1
        return i >= 0 and spans[i][0] <= x < spans[i][1]

    kana = re.compile(r'[ぁ-んァ-ン]')
    import arm9text as T
    bad = []
    p = 0
    while p < len(a) - 1:
        if not T.is_code(T.u16(a, p)):
            p += 2
            continue
        q = p
        while q < len(a) - 1 and T.is_code(T.u16(a, q)):
            q += 2
        if q < len(a) - 1 and T.u16(a, q) == 0:
            text = codec.decode(a, p, q)[0]
            k = len(kana.findall(text))
            if k >= 2 and 2 * k >= (q - p) // 2 and not any(covered(B + x) for x in range(p, q, 2)) \
                    and B + p not in ARM9_WAIVED | T.NOT_TEXT:
                bad.append('%08X %s' % (B + p, text[:20]))
        p = q + 2
    assert bad == [], 'kana text outside script/arm9: %s' % bad[:10]


def test_kanakan_is_dictionary(rom, codec):
    """kanakan.img (name-entry kana -> kanji candidates) parses completely: u16 count, u32 offsets, then per kana
    `u16 nkana, u16 n, n codes, 0000`. It is input data, not displayed text: not in script/."""
    data = bytes(rom.getFileByName('kanakan.img'))
    n = struct.unpack_from('<H', data, 0)[0]
    offs = list(struct.unpack_from('<%dI' % n, data, 2)) + [len(data)]
    assert offs[0] == (2 + 4 * n + 3) & ~3 and data[2 + 4 * n:offs[0]] == b'\0\0'   # header padded to 4
    for a, b in zip(offs, offs[1:]):
        nk, cnt = struct.unpack_from('<HH', data, a)
        assert 4 + 2 * cnt + 2 == b - a and data[b - 2:b] == b'\0\0' and nk <= cnt
        codec.decode(data, a + 4)   # all codes decode
