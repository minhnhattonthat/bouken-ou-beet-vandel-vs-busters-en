"""Generic buster types 0x11-0x33 (party records 16-50) must keep the name 0x003D (－): 0x02019564 rolls a random name
from busterman/busterwoman.bin only while the copied party name equals the literal at 0x021A94D4 (one u16 0x003D).
A translated "-" left every generic buster named "-" (phase 8 session 13)."""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generic_party_names_keep_placeholder():
    entries = {e['id']: e for e in json.loads((ROOT / 'script/arm9/party.json').read_text(encoding='utf-8'))['entries']}
    for n in range(16, 51):
        e = entries['a9.party.%03d.name' % n]
        assert e['jp'] == '－' and e['en'] == '', e['id']


def test_placeholder_literal_is_3d():
    arm9 = ROOT / 'work/fs/arm9.bin'
    if not arm9.exists():
        return
    data = arm9.read_bytes()
    assert struct.unpack_from('<I', data, 0x020198C8 - 0x02000000)[0] == 0x021A94D4
    assert struct.unpack_from('<2H', data, 0x021A94D4 - 0x02000000) == (0x003D, 0)
