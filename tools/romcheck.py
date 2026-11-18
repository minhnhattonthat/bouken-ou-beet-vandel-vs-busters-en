"""romcheck.py: ROM-level checks of a build against the pinned dump, per NitroFS file (phase 7).

    python -X utf8 tools/romcheck.py [build/beet_en.nds] [--writes build/beet_en.writes.txt]

ndspy re-lays the files out, so a whole-image byte diff says nothing; this compares file by file instead and fails
(exit 1) when
  - a ROM header byte outside the regenerated words (offsets, sizes, used size, CRC) differs from the dump (entry
    and RAM addresses, autoload hooks, game code, secure area, logo, ...), the header CRC is wrong, a section runs
    past the image, or a size word disagrees with the parsed file;
  - a file outside CHANGEABLE differs (arm7, overlays, banner, graphics, fonts, ...), or the file count changes;
  - a write in the build log (`FILE OFFSET ORIG_HEX NEW_HEX [what]`) does not find ORIG_HEX in the clean dump's
    file (stale address, wrong revision, write planned on a patched buffer) or its NEW_HEX is not in the built file
    (a later write overwrote it), or two writes overlap;
  - a changed byte inside the original file length is covered by no write, unless it lies past the file's logged
    `FILE append OFFSET` (appended strings; for arm9 the hook block + autoload list replacing the old list);
  - a file grew with no `append` line, or a script file's append starts inside the original data;
  - a relocated arm9 pointer string leaves a word holding its old address that the build did not repoint (every
    4-aligned word of the original arm9 equal to the old address must be in the entry's `ptrs`).
Writes into in-memory tables (`reloc.<key> ...`) and `arm9 relocate` notes are not file writes and are skipped.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402

A9 = 0x02000000
# files the build may change; anything else must stay byte-identical
CHANGEABLE = {'arm9', 'field/script/rom.img', 'quest/quest.img', 'status/bustername/busterman.bin',
              'status/bustername/busterwoman.bin'}
SCRIPT_FILES = {'field/script/rom.img', 'quest/quest.img'}


def files_of(rom):
    """{name: bytes} for arm9, arm7, banner and every NitroFS file (overlays by id)."""
    out = {'arm9': bytes(rom.arm9), 'arm7': bytes(rom.arm7), 'banner': bytes(rom.iconBanner),
           'arm9ovt': bytes(rom.arm9OverlayTable), 'arm7ovt': bytes(rom.arm7OverlayTable)}
    for i, data in enumerate(rom.files):
        out[rom.filenames.filenameOf(i) or 'file#%d' % i] = bytes(data)
    return out


def parse_log(path):
    """({file: [(off, orig, new, what)]}, {file: append offset})."""
    writes, appends = {}, {}
    for n, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        p = line.split(None, 4)
        if not p or p[0].startswith('reloc.') or p[1] == 'relocate':
            continue
        if p[1] == 'append':
            off = int(p[2], 16)
            appends[p[0]] = min(off, appends.get(p[0], off))
            continue
        writes.setdefault(p[0], []).append((int(p[1], 16), bytes.fromhex(p[2]), bytes.fromhex(p[3]),
                                            '%s:%d %s' % (Path(path).name, n, p[4] if len(p) > 4 else '')))
    return writes, appends


def check_file(name, orig, new, writes, append):
    errs = []
    covered = bytearray(len(orig))
    spans = sorted(writes)
    for (o1, a, _, w1), (o2, _, _, w2) in zip(spans, spans[1:]):
        if o2 < o1 + len(a):
            errs.append('%s: writes overlap at %X (%s) and %X (%s)' % (name, o1, w1, o2, w2))
    for off, want, data, what in spans:
        if orig[off:off + len(want)] != want:
            errs.append('%s %X: original holds %s, write expected %s (%s)'
                        % (name, off, orig[off:off + len(want)].hex(), want.hex(), what))
        if new[off:off + len(data)] != data:
            errs.append('%s %X: built holds %s, write put %s: overwritten later (%s)'
                        % (name, off, new[off:off + len(data)].hex(), data.hex(), what))
        covered[off:off + len(data)] = b'\1' * len(data[:max(0, len(orig) - off)])
    if len(new) > len(orig) and append is None:
        errs.append('%s grew %d -> %d bytes with no append logged' % (name, len(orig), len(new)))
    if len(new) < len(orig):
        errs.append('%s shrank %d -> %d bytes' % (name, len(orig), len(new)))
    if name in SCRIPT_FILES and append is not None and append < len(orig):
        errs.append('%s: append at %X is inside the original data (ends %X)' % (name, append, len(orig)))
    end = min(len(orig), len(new), append if append is not None else len(orig))
    bad = [i for i in range(end) if orig[i] != new[i] and not covered[i]]
    if bad:
        errs.append('%s: %d changed bytes with no write behind them, first at %X' % (name, len(bad), bad[0]))
    return errs


def check_relocated(orig_arm9, log_path):
    """Every word of the original arm9 holding a relocated string's old address must be in its `ptrs`."""
    ids = [line.split()[2] for line in Path(log_path).read_text(encoding='utf-8').splitlines()
           if line.startswith('arm9 relocate ')]
    ents = {e['id']: e for e in json.loads((ROOT / 'script' / 'arm9' / 'ptr.json').read_text(encoding='utf-8'))
            ['entries']}
    words = {}
    for o in range(0, len(orig_arm9) - 3, 4):
        words.setdefault(struct.unpack_from('<I', orig_arm9, o)[0], []).append(A9 + o)
    errs = []
    for i in ids:
        old = int(i.split('.')[1], 16)
        left = set(words.get(old, [])) - {int(w, 16) for w in ents[i]['ptrs']}
        if left:
            errs.append('%s relocated, but words %s still hold %08X' % (i, ' '.join('%08X' % w for w in sorted(left)),
                                                                     old))
    return errs, len(ids)


# header words ndspy regenerates when it re-lays the image (ROM offsets, sizes, used size); all other header bytes
# (title, game code, entry/RAM addresses, autoload hooks, port settings, secure area, logo, ...) must stay identical
HEADER_LEN = 0x200
REGEN_WORDS = {0x20: 'arm9 offset', 0x2C: 'arm9 size', 0x30: 'arm7 offset', 0x3C: 'arm7 size', 0x40: 'FNT offset',
               0x44: 'FNT size', 0x48: 'FAT offset', 0x4C: 'FAT size', 0x50: 'ovt9 offset', 0x54: 'ovt9 size',
               0x58: 'ovt7 offset', 0x5C: 'ovt7 size', 0x68: 'banner offset', 0x80: 'used ROM size'}
HEADER_CRC = 0x15E  # CRC-16 of header bytes 0..0x15D


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def check_header(orig, new, rom=None):
    """Invariant header bytes equal the dump; regenerated words are consistent with the built image."""
    errs = []
    regen = set()
    for o in REGEN_WORDS:
        regen.update(range(o, o + 4))
    regen.update((HEADER_CRC, HEADER_CRC + 1))
    for w in range(0, HEADER_LEN, 4):  # one error per changed word
        if any(o not in regen and orig[o] != new[o] for o in range(w, w + 4)):
            errs.append('header %X changed %s -> %s (invariant field)' % (w, orig[w:w + 4].hex(), new[w:w + 4].hex()))
    word = lambda o: struct.unpack_from('<I', new, o)[0]  # noqa: E731
    want = crc16(new[:HEADER_CRC])
    if struct.unpack_from('<H', new, HEADER_CRC)[0] != want:
        errs.append('header CRC %04X, computed %04X' % (struct.unpack_from('<H', new, HEADER_CRC)[0], want))
    for off_o, size_o in ((0x20, 0x2C), (0x30, 0x3C), (0x40, 0x44), (0x48, 0x4C), (0x50, 0x54), (0x58, 0x5C)):
        if word(off_o) + word(size_o) > len(new):
            errs.append('header %s %X + %X runs past the image (%X)'
                        % (REGEN_WORDS[off_o], word(off_o), word(size_o), len(new)))
    if word(0x80) > len(new):
        errs.append('header used ROM size %X > image %X' % (word(0x80), len(new)))
    if rom is not None:
        for size_o, data in ((0x2C, rom.arm9), (0x3C, rom.arm7), (0x54, rom.arm9OverlayTable),
                             (0x5C, rom.arm7OverlayTable)):
            if word(size_o) != len(data):
                errs.append('header %s %X, file is %X' % (REGEN_WORDS[size_o], word(size_o), len(data)))
    return errs


def run(built, log_path):
    orig_img, new_img = build.ROM.read_bytes(), Path(built).read_bytes()
    new_rom = ndspy.rom.NintendoDSRom(new_img)
    orig = files_of(ndspy.rom.NintendoDSRom(orig_img))
    new = files_of(new_rom)
    writes, appends = parse_log(log_path)
    errs = check_header(orig_img, new_img, new_rom)
    if set(orig) != set(new):
        errs.append('file set differs: only orig %s, only built %s'
                    % (sorted(set(orig) - set(new))[:5], sorted(set(new) - set(orig))[:5]))
    changed = sorted(k for k in orig if k in new and orig[k] != new[k])
    for k in changed:
        if k not in CHANGEABLE:
            errs.append('%s changed, but the build may not touch it' % k)
    for k in sorted(set(writes) | set(appends)):
        if k not in orig:
            errs.append('log writes to unknown file %s' % k)
            continue
        errs += check_file(k, orig[k], new[k], writes.get(k, []), appends.get(k))
    for k in changed:
        if k in CHANGEABLE and k not in writes and k not in appends:
            errs.append('%s changed with no write logged' % k)
    rel_errs, nrel = check_relocated(orig['arm9'], log_path)
    errs += rel_errs
    nw = sum(map(len, writes.values()))
    return errs, 'files changed: %s; %d writes checked; %d relocated strings' % (', '.join(changed), nw, nrel)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('built', nargs='?', default=str(build.OUT))
    ap.add_argument('--writes', default=None, help='write log (default: <built stem>.writes.txt)')
    a = ap.parse_args()
    log = a.writes or str(Path(a.built).with_name(Path(a.built).stem + '.writes.txt'))
    errs, summary = run(a.built, log)
    for e in errs[:40]:
        print('ERR', e)
    print('romcheck: %s; %d errors' % (summary, len(errs)))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
