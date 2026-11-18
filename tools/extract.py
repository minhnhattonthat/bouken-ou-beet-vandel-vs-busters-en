"""extract.py: dump every text source of the original ROM to script/*.json (phase 4).

    python -X utf8 tools/extract.py [--force] [--only rom,quest,names,arm9]

Sources (docs/re/text.md, docs/re/scripts.md, docs/re/arm9.md):
  rom    field/script/rom.img   -> script/rom/NN.json     (one file per 0x4000 bytes of the container)
  quest  quest/quest.img        -> script/quest/NN.json
  names  status/bustername/*.bin -> script/names.json     (generic buster names, fixed 22-byte records)
  arm9   arm9.bin tables + pointer-referenced messages -> script/arm9/*.json (arm9text.py)

Each file: {"src": ..., "entries": [{"id", "jp", "en", "kind", ...}]}. `id` is address-based and stable; `jp` is the
decoded original (text16.Codec: `{br}` `{page}` `{close}` controls, `[XXXX]` for codes with no table entry).
Never clobbers English: a file that exists is left alone unless --force, and --force keeps `en`, `status` and `notes`
of every id it already had.
Not text (checked by tests/test_extract.py, not dumped): file-name strings in rom.img (`credit17.nbfc`...), the rom.img
data tail from 0x51BB4, the quest.img offset table at 0x11D4, kanakan.img (name-entry kana->kanji dictionary).
"""
import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import scr  # noqa: E402
from text16 import Codec  # noqa: E402

SCRIPT = ROOT / 'script'
TBL = ROOT / 'tbl' / 'jp.tbl'
ROM_KINDS = {0x70: 'msg', 0x9E: 'speaker', 0x4F: 'quest', 0x99: 'quest', 0x60: 'file', 0x6B: 'file'}
QUEST_KINDS = {0x20: 'title', 0x1A: 'desc', 0x2D: 'desc'}
NAME_FILES = ('status/bustername/busterman.bin', 'status/bustername/busterwoman.bin')
NAME_REC, NAME_SLOT = 22, 16          # record size; name field = up to 7 full-width chars + 0000 (then 6 bytes)
KEEP = ('en', 'status', 'notes', 'short')   # short: elem.name card-icon form (insert.py, engine.ESHORT_SLOT)


def load_rom():
    import ndspy.rom
    import build
    import check_rom
    check_rom.check()
    return ndspy.rom.NintendoDSRom(build.ROM.read_bytes())


def rom_file(rom, name):
    return bytes(rom.getFileByName(name))


def entry(id_, jp, kind, **extra):
    e = {'id': id_, 'jp': jp, 'en': '', 'kind': kind}
    e.update({k: v for k, v in extra.items() if v not in (None, '', [])})
    return e


def script_entries(data, s, codec, prefix, kinds):
    """Entries for every non-file string of a parsed scr container, in file order."""
    speaker_of = {}
    cur = None
    for pc in sorted(s.ins):
        op = data[pc]
        if op == 0xFF:
            cur = None
        elif op == 0x9E and prefix == 'rom':
            t = struct.unpack_from('<I', data, pc + 1)[0]
            cur = t if t in s.strs else None
        elif op == 0x70 and prefix == 'rom' and cur is not None:
            speaker_of.setdefault(struct.unpack_from('<I', data, pc + 1)[0], cur)
    out = []
    for off in sorted(s.strs):
        end, form = s.strs[off]
        if form == 'file':
            continue
        jp, _ = codec.decode(data, off)
        ops = sorted({data[pc] for pc, _ in s.refs.get(off, [])})
        kind = '/'.join(dict.fromkeys(kinds.get(op, '%02X' % op) for op in ops)) or 'unref'
        spk = speaker_of.get(off)
        out.append(entry('%s.%05X' % (prefix, off), jp, kind,
                         speaker=codec.decode(data, spk)[0] if spk is not None else None,
                         refs=len(s.refs.get(off, []))))
    return out


def chunk(entries, size):
    """{NN: [entries]} by file offset // size (offset parsed back from the id)."""
    files = {}
    for e in entries:
        off = int(e['id'].split('.')[1], 16)
        files.setdefault('%02X' % (off // size), []).append(e)
    return files


def extract_rom(rom, codec):
    data = rom_file(rom, 'field/script/rom.img')
    s = scr.parse_rom_img(data, bytes(rom.arm9))
    return {'rom/%s.json' % k: ('field/script/rom.img', v)
            for k, v in chunk(script_entries(data, s, codec, 'rom', ROM_KINDS), 0x4000).items()}


def extract_quest(rom, codec):
    data = rom_file(rom, 'quest/quest.img')
    s = scr.parse_quest_img(data, bytes(rom.arm9))
    return {'quest/%s.json' % k: ('quest/quest.img', v)
            for k, v in chunk(script_entries(data, s, codec, 'quest', QUEST_KINDS), 0x2000).items()}


def name_entries(data, codec, tag):
    out = []
    for i in range(len(data) // NAME_REC):
        off = i * NAME_REC
        jp, _ = codec.decode(data, off)
        out.append(entry('name.%s%03d' % (tag, i), jp, 'name', max=NAME_SLOT - 2))
    return out


def extract_names(rom, codec):
    ents = []
    for f in NAME_FILES:
        ents += name_entries(rom_file(rom, f), codec, 'w' if 'woman' in f else 'm')
    return {'names.json': (', '.join(NAME_FILES), ents)}


def extract_arm9(rom, codec):
    import arm9text
    return arm9text.extract(bytes(rom.arm9), codec)


SOURCES = {'rom': extract_rom, 'quest': extract_quest, 'names': extract_names, 'arm9': extract_arm9}


def write(rel, src, entries, force):
    path = SCRIPT / rel
    if path.exists():
        if not force:
            return 'kept'
        old = {e['id']: e for e in json.loads(path.read_text(encoding='utf-8'))['entries']}
        for e in entries:
            for k in KEEP:
                if old.get(e['id'], {}).get(k):
                    e[k] = old[e['id']][k]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'src': src, 'entries': entries}, ensure_ascii=False, indent=1) + '\n',
                    encoding='utf-8', newline='\n')
    return 'written'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--force', action='store_true', help='rewrite existing files (keeps en/status/notes)')
    ap.add_argument('--only', default=','.join(SOURCES))
    a = ap.parse_args()
    rom = load_rom()
    codec = Codec.load(TBL)
    for name in a.only.split(','):
        files = SOURCES[name](rom, codec)
        n = sum(len(v[1]) for v in files.values())
        res = [write(rel, src, ents, a.force) for rel, (src, ents) in sorted(files.items())]
        print('%-6s %5d strings in %3d files (%d written, %d kept)' % (
            name, n, len(files), res.count('written'), res.count('kept')))


if __name__ == '__main__':
    main()
