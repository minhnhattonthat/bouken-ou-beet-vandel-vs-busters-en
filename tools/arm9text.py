"""arm9text.py: text in arm9.bin (docs/re/arm9.md): fixed-record tables and pointer-referenced strings.

Tables: the game reads them through `get(id) = base + (id - first) * size` leaf functions (tools/a9tables.py lists
them all; accessor address in the comments below). Text fields are fixed slots of 16-bit codes: the text ends at a
0000 or at the end of the slot (a full slot has no terminator). Each extracted slot records `max`: the bytes it may
hold, i.e. the original text plus the zero bytes after it up to the field limit (only zeros are ever overwritten).

Pointer strings: every 4-aligned word in arm9 whose value is the address of a clean text string (valid codes up to a
0000, at least one kana/kanji) outside the tables. `ptrs` lists the words that point at it (to repoint on insert).

    import arm9text; files = arm9text.extract(arm9_bytes, codec)   # {relpath: (src, entries)}
"""
import struct

BASE = 0x02000000
NGLYPH = 7332
KANA = range(3 * 94 + 1, 5 * 94 + 87)

# (key, accessor, base, size, count, fields{name: (offset, limit)}, kind)
TABLES = [
    ('armor', 0x02014040, 0x0210D430, 0xA0, 71, {'name': (4, 24), 'reading': (24, 44), 'desc': (44, 122)}),
    ('shout', 0x020140B0, 0x0211A6AC, 0x168, 81, {'s%02d' % i: (32 * i, 32 * i + 32) for i in range(11)}),
    ('party', 0x020140DC, 0x02121BD4, 0x74, 53, {'name': (0, 20)}),
    # monster attribute (属性, monster book top right): one kanji per 4-byte slot; relocated (engine.RELOC)
    ('elem', 0x020140F4, 0x021233D8, 0x4, 10, {'name': (0, 4)}),
    ('title', 0x0201419C, 0x02123400, 0x4C, 130, {'name': (0, 20)}),
    ('keyitem', 0x02014200, 0x0212AFE4, 0x88, 30, {'name': (4, 24), 'reading': (24, 44), 'desc': (44, 122)}),
    ('item', 0x0201421C, 0x0212BFD4, 0xA4, 34, {'name': (4, 24), 'reading': (24, 44), 'desc': (44, 122),
                                                'name2': (132, 152)}),
    ('monster', 0x02014234, 0x0212D59C, 0x10C, 319, {'name': (0, 22), 'reading': (22, 44), 'area': (44, 66)}),
    ('special', 0x020142C8, 0x02142390, 0x24, 36, {'name': (0, 24)}),
    ('skill', 0x020142E0, 0x021428A0, 0x48, 67, {'name': (0, 20), 'desc': (20, 48)}),
    ('tengeki', 0x020145D8, 0x02143B8C, 0xB0, 43, {'name': (0, 14), 'reading': (14, 40), 'desc': (40, 120)}),
    ('meigeki', 0x020145F0, 0x0214591C, 0xB0, 43, {'name': (0, 14), 'reading': (14, 40), 'desc': (40, 120)}),
    # ids 0x13F-0x15D and 0x15E-0x190 (bounds checks at 0x02014248..), same record shape; desc is the placeholder 説明
    ('vandel', 0x02014608, 0x021476AC, 0x1B4, 31, {'name': (0, 22), 'name2': (22, 44), 'desc': (44, 104)}),
    ('buster', 0x02014628, 0x0214AB78, 0x1B4, 51, {'name': (0, 22), 'name2': (22, 44), 'desc': (44, 104)}),
    # weapon categories (12) then special weapons (バーニングランス...); 79 records fill the gap to the weapon table
    ('wpntype', 0x0201466C, 0x02150254, 0x1C, 79, {'name': (0, 20)}),
    ('weapon', 0x02014684, 0x02150AF8, 0x438, None, {'name': (4, 24), 'reading': (24, 44), 'desc': (44, 122),
                                                       'name2': (132, 152)}),
    ('area', 0x020146CC, 0x02193E08, 0x30, 70, {'name': (0, 24)}),
    ('area2', 0x020146E0, 0x02194B28, 0x30, 25, {'name': (0, 24)}),
]


# Pointer targets that decode as text but are not text (checked by eye, 2026-11-18): table bases and numeric words
# (0210D328, 0210D338, 02194FD8, 021958B8), kana class lists used by the name-entry code (021AE0C8-021AE34C; not
# displayed), and numeric data near the end (021B6E9C-021B6FEC). 021233D8 was listed here until phase 5: it is the
# `elem` table (the monster book's 属性 kanji).
NOT_TEXT = {0x0210D328, 0x0210D338, 0x02194FD8, 0x021958B8, 0x021AE0C8, 0x021AE13C, 0x021AE15C,
            0x021AE1F0, 0x021AE2A4, 0x021AE2F0, 0x021AE34C, 0x021B6E9C, 0x021B6EA8, 0x021B6EE4, 0x021B6EF0,
            0x021B6FEC}
# Name-entry kana keyboard rows (021AA0F8-021AA2A8) stay in as text (kind ptr.keyboard, never written: the 英字 tab
# is the English keyboard; docs/re/vwf.md §Name entry).
NOTES = {0x021AA0F8: 'name-entry kana keyboard row: keep Japanese (ptr.keyboard is never inserted)',
         0x021AA2A8: 'name-entry kana list (keyboard logic): keep Japanese',
         0x021B1820: 'appended after a buster name: "<name> joined the party"',
         0x021B68B0: 'GBA-link news lines are built from these fragments (line by line)'}
# Pointer strings by screen (kind ptr.<group>; budgets in tools/budgets.json): first address of each group, in order.
PTR_GROUPS = [
    (0x0219AD0C, 'label'),      # バスター / ハーデンの配下 (b14 caption), quest categories 護衛 討伐..
    (0x021A9D04, 'msg'),        # save / backup errors (message window)
    (0x021AA0F8, 'keyboard'),   # name-entry kana rows + kana list
    (0x021AAE9C, 'msg'),        # ring broken/repaired, appraiser lines
    (0x021AAECC, 'speaker'),    # 鑑定士
    (0x021AAED8, 'msg'),
    (0x021AB998, 'line'),       # one-line notices: equip, shop full, joined the party, skill confirm
    (0x021ADF44, 'label'),      # 無期限 (quest deadline)
    (0x021AE554, 'line'),
    (0x021B4EA8, 'comm'),       # wireless (通信) screens, 8 px font
    (0x021B68B0, 'gba'),        # GBA-link news and cartridge check, 12 px font, bottom screen
]


def ptr_kind(v):
    kind = 'ptr'
    for lo, g in PTR_GROUPS:
        if v >= lo:
            kind = 'ptr.' + g
    return kind


def u16(a, p):
    return a[p] | a[p + 1] << 8


def is_code(v):
    return 1 <= v <= NGLYPH or 0xFF00 <= v < 0xFFFF


def slot(a, p, limit):
    """(text_end, terminated, max) of the field at p..limit, or None if it holds a non-text code."""
    q = p
    while q < limit:
        v = u16(a, q)
        if v == 0:
            break
        if not is_code(v):
            return None
        q += 2
    end = q
    term = q < limit
    if term:
        q += 2
        while q < limit and u16(a, q) == 0:
            q += 2
    return end, term, q - p


def table_count(a, base, size, fields, limit_addr):
    """Records up to the first whose name field is not clean text."""
    off, lim = fields.get('name') or next(iter(fields.values()))
    n = 0
    while base + (n + 1) * size <= limit_addr:
        r = base - BASE + n * size
        s = slot(a, r + off, r + lim)
        if s is None:
            break
        n += 1
    return n


def table_entries(a, codec, key, base, size, count, fields):
    out = []
    for i in range(count):
        r = base - BASE + i * size
        for fname, (off, lim) in fields.items():
            s = slot(a, r + off, r + lim)
            if s is None:
                raise ValueError('%s %d %s: not text at %08X' % (key, i, fname, BASE + r + off))
            end, term, mx = s
            if end == r + off:
                continue   # empty slot
            jp = codec.decode(a, r + off, end)[0]
            out.append({'id': 'a9.%s.%03d.%s' % (key, i, fname), 'jp': jp, 'en': '', 'kind': '%s.%s' % (key, fname),
                        'addr': '%08X' % (BASE + r + off), 'max': mx})
    return out


def resolved_tables(a):
    """TABLES with counts filled in (None = scan until the name field stops being text)."""
    out = []
    bases = sorted(t[2] for t in TABLES) + [BASE + len(a)]
    for key, acc, base, size, count, fields in TABLES:
        nxt = bases[bases.index(base) + 1]
        if count is None:
            count = table_count(a, base, size, fields, nxt)
        out.append((key, acc, base, size, count, fields))
    return out


def table_spans(a):
    return [(t[2], t[2] + t[3] * t[4]) for t in resolved_tables(a)]


def clean_string(a, p, end_limit):
    """End (after 0000) of a clean string at p with >= 1 kana/kanji, else None."""
    q, jp = p, 0
    while q + 1 < end_limit:
        v = u16(a, q)
        q += 2
        if v == 0:
            return q if q - p > 2 and jp else None
        if not is_code(v):
            return None
        if v in KANA or v > 15 * 94:
            jp += 1
    return None


def pointer_strings(a, spans):
    """{address: (end_offset, [pointer word addresses])} for strings outside the tables."""
    n = len(a)
    found = {}
    for p in range(0, n - 3, 4):
        v = struct.unpack_from('<I', a, p)[0]
        if not BASE <= v < BASE + n or v & 1 or v in NOT_TEXT or any(s <= v < e for s, e in spans):
            continue
        if v in found:
            found[v][1].append(BASE + p)
            continue
        e = clean_string(a, v - BASE, n)
        if e:
            found[v] = (e, [BASE + p])
    return found


def extract(a, codec):
    files = {}
    for key, acc, base, size, count, fields in resolved_tables(a):
        files['arm9/%s.json' % key] = ('arm9.bin table %08X x%d (%#x bytes, accessor %08X)' % (base, count, size, acc),
                                       table_entries(a, codec, key, base, size, count, fields))
    ents = []
    for v, (end, ptrs) in sorted(pointer_strings(a, table_spans(a)).items()):
        e = {'id': 'a9.%08X' % v, 'jp': codec.decode(a, v - BASE)[0], 'en': '', 'kind': ptr_kind(v),
             'ptrs': ['%08X' % p for p in ptrs]}
        if v in NOTES:
            e['notes'] = NOTES[v]
        ents.append(e)
    files['arm9/ptr.json'] = ('arm9.bin strings reached by pointer words', ents)
    return files
