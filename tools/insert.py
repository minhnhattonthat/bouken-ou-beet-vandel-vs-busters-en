"""insert.py: put English (or marker) text from script/*.json into the ndspy ROM object (called by build.py).

Sources (same as extract.py):
  rom.img / quest.img  each string goes back in place when it fits (rest of the old string zeroed), else it is
                       appended to the file (4-aligned) and every operand that pointed at it (Script.refs) is repointed;
  names                16-byte slots in status/bustername/*.bin (max 14 bytes + 0000);
  arm9 tables          fixed slots at `addr`, `max` bytes (zero-filled);
  arm9 pointer strings in place when the new bytes fit the old string, else an error (relocation: phase 7).
Text is encoded by engine.Engine (English pair codes). An entry with empty `en` keeps its Japanese.

Marker mode (`text_for = marker`) replaces every entry by a short id plus filler of about the translated length, so a
tour shows which entry each box comes from (phase 5).
"""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import scr  # noqa: E402

SCRIPT = ROOT / 'script'
A9 = 0x02000000
NAME_FILES = {'m': 'status/bustername/busterman.bin', 'w': 'status/bustername/busterwoman.bin'}
NAME_REC, NAME_MAX = 22, 14
CTRL = re.compile(r'(\{\w+\}|\[[0-9A-F]{4}\])')
FILLER = 'the quick brown fox jumps over a lazy dog while five wizards box '


def load_entries():
    """{source key: [entries]} for rom, quest, names, arm9 (tables and ptr)."""
    out = {'rom': [], 'quest': [], 'names': [], 'arm9': []}
    for f in sorted(SCRIPT.rglob('*.json')):
        key = f.relative_to(SCRIPT).parts[0].removesuffix('.json')
        out[key] += json.loads(f.read_text(encoding='utf-8'))['entries']
    return out


def short_id(e):
    i = e['id']
    if i.startswith(('rom.', 'quest.')):
        return i[0] + i.split('.')[1]
    if i.startswith('name.'):
        return 'n' + i[5:]
    p = i.split('.')
    if len(p) == 2:                       # a9.0219AD0C pointer string
        return 'p' + p[1][-5:]
    return '%s%d%s' % (p[1][:2], int(p[2]), p[3][0] + p[3][-1:])


def marker(e, eng):
    """Marker text: the id, then filler of ~1.8x the Japanese length per text run, controls kept in place."""
    parts = CTRL.split(e['jp'])
    out, first, fpos = [], True, 0
    limit = 200
    for part in parts:
        if CTRL.fullmatch(part) or not part:
            out.append(part)
            continue
        n = max(1, int(len(part) * 1.8))
        s = ('[%s] ' % short_id(e)) if first else ''
        first = False
        while len(s) < n:
            s += FILLER[fpos % len(FILLER)]
            fpos += 1
        while eng.width(s) > limit:
            s = s[:-1]
        out.append(s.rstrip() or s)
    return ''.join(out)


def fit_bytes(text, eng, max_bytes):
    """Cut text (no controls) until it encodes in max_bytes."""
    while text and len(eng.encode(text)) > max_bytes:
        text = text[:-1]
    return text


class Inserter:
    def __init__(self, rom, eng, text_for, log, fit=False):
        self.rom, self.eng, self.text_for, self.log, self.fit = rom, eng, text_for, log, fit
        self.arm9_orig = bytes(rom.arm9)
        self.counts = {}

    def put(self, buf, off, data, by):
        self.log.append('%s %X %s %s' % (by, off, bytes(buf[off:off + len(data)]).hex(), data.hex()))
        buf[off:off + len(data)] = data

    def script_file(self, name, parse, entries, prefix):
        data = bytearray(self.rom.getFileByName(name))
        s = parse(bytes(data), self.arm9_orig)
        n = 0
        for e in entries:
            text = self.text_for(e)
            if not text:
                continue
            off = int(e['id'].split('.')[1], 16)
            end, form = s.strs[off]
            assert form == 'text'
            new = self.eng.encode(text) + b'\0\0'
            if len(new) <= end - off:
                self.put(data, off, new.ljust(end - off, b'\0'), name)
            else:
                at = (len(data) + 3) & ~3
                data += bytes(at - len(data)) + new
                self.log.append('%s append %X %s' % (name, at, e['id']))
                for pc, k in s.refs[off]:
                    assert struct.unpack_from('<I', data, pc + k)[0] == off, (e['id'], pc)
                    self.put(data, pc + k, struct.pack('<I', at), name)
            n += 1
        self.rom.setFileByName(name, bytes(data))
        self.counts[prefix] = n

    def names(self, entries):
        bufs = {t: bytearray(self.rom.getFileByName(f)) for t, f in NAME_FILES.items()}
        n = 0
        for e in entries:
            text = self.text_for(e)
            if not text:
                continue
            tag, idx = e['id'][5], int(e['id'][6:])
            new = self.eng.encode(text)
            assert len(new) <= NAME_MAX, (e['id'], text)
            self.put(bufs[tag], idx * NAME_REC, new.ljust(NAME_MAX + 2, b'\0'), NAME_FILES[tag])
            n += 1
        for t, f in NAME_FILES.items():
            self.rom.setFileByName(f, bytes(bufs[t]))
        self.counts['names'] = n

    def arm9(self, entries):
        a = bytearray(self.rom.arm9)
        n = 0
        for e in entries:
            text = self.text_for(e)
            if not text:
                continue
            new = self.eng.encode(text)
            if 'addr' in e:
                off, mx = int(e['addr'], 16) - A9, e['max']
                # always keep a 0000 inside the slot: readers run past a full slot into the next record
                assert len(new) <= mx - 2, (e['id'], text, len(new), mx)
                self.put(a, off, new.ljust(mx, b'\0'), 'arm9')
            else:
                off = int(e['id'].split('.')[1], 16) - A9
                p = off                   # end of the old string: first 0000 on a 2-byte boundary
                while a[p:p + 2] != b'\0\0':
                    p += 2
                room = p - off
                if self.fit and len(new) > room:
                    new = self.eng.encode(fit_bytes(text, self.eng, room))
                assert len(new) <= room, (e['id'], text, len(new), room)
                self.put(a, off, new.ljust(room, b'\0'), 'arm9')
            n += 1
        self.rom.arm9 = bytes(a)
        self.counts['arm9'] = n

    def run(self, ents):
        self.script_file('field/script/rom.img', scr.parse_rom_img, ents['rom'], 'rom')
        self.script_file('quest/quest.img', scr.parse_quest_img, ents['quest'], 'quest')
        self.names(ents['names'])
        self.arm9(ents['arm9'])
        return self.counts


def text_marker(eng):
    def f(e):
        if 'max' in e:
            return fit_bytes(short_id(e) + ' ' + FILLER, eng, e['max'] - 2)
        if e['id'].startswith('a9.0'):
            return short_id(e) + ' ' + FILLER   # cut to the old string's room (Inserter.fit)
        return marker(e, eng)
    return f


def text_en(e):
    return e.get('en') or None
