"""Parser for the `scr\\x1a` script containers (field/script/rom.img, quest/quest.img).

Layout (docs/re/scripts.md §Container): magic, then code blocks and string pools interleaved, then (rom.img only) a
data-table tail. A code block is a run of instructions (lengths from the game's own opcode-length table in arm9)
ending in `FF`. A string pool may follow an `FF`:

    FF 00 [S..] str [S..] str ... 00.. <next code>

- every string starts 4-aligned; the gap before it is filled with `S` (0x53), except the single `00` right after `FF`;
- a text string is 16-bit codes ending in `0000`; a file-name string is ASCII ending in `00`;
- after the last string, `00` bytes pad up to the next code block (which need not be aligned).

Strings are told from code by evidence, never by looks alone: a pointer operand of a string opcode (STRING_OPS) or
`S` padding before it; a jump target (CODE_OPS) is always code. The parse runs twice so that pointers found in the
first pass decide pools the first pass got wrong. tests/test_extract.py checks the result for consistency (every
string pointer lands on a parsed string, every jump on an instruction, no unknown opcode in code).

    from scr import parse_rom_img, parse_quest_img
    s = parse_rom_img(rom_img_bytes, arm9_bytes)   # s.ins {pc: len}, s.strs {start: (end, kind)}, s.refs ...
"""
import re
import struct
from dataclasses import dataclass, field

ARM9_BASE = 0x02000000
ROM_IMG_LEN_TABLE = 0x021953D0   # 0xC0 entries, total length incl. opcode; 0 = variable (00, FF, BF)
QUEST_LEN_TABLE = 0x0210D338     # 0x31 entries
ROM_IMG_DATA_START = 0x51BB4     # data tables to the end of the file (arm9 0x02123434 points at 0x51BB8 / 0x54A14)

# Operand byte offsets (from the opcode byte) of u32 file offsets.
ROM_IMG_STRING_OPS = {0x70: (1,), 0x9E: (1,), 0x4F: (13, 17), 0x60: (1, 5, 9), 0x6B: (1, 5, 9),
                      0x99: (5, 9)}
# Not string ops although an operand sometimes equals a string offset: 28 (handler 0x02054668 reads its u32 with
# bytes 1/2 swapped and passes it to the sound object 0x021BA39C).
ROM_IMG_CODE_OPS = {0x17: (1,), 0x54: (1,), 0x12: (1,), 0x04: (9,), 0x61: (9,), 0x67: (6,), 0x68: (6,),
                    0x78: (5,), 0x07: (9,)}
QUEST_STRING_OPS = {0x20: (1,), 0x1A: (1,), 0x2D: (1,)}
QUEST_CODE_OPS = {}
# quest.img 0x11D1-0x11F4: `00 00 S` pad + 8 u32 quest.img code offsets (0x11F4, 0x135C, 0x14A4, 0, 0x1298, ...),
# the table rom.img's quest-offer opcode `4F` points at with its third operand (`4F .. .. D4110000 <place> <client>`).
QUEST_DATA = {0x11D1: 0x11F4}

FILENAME = re.compile(rb'[/A-Za-z0-9_]+\.[a-z]{3,4}')


@dataclass
class Script:
    data: bytes
    ins: dict = field(default_factory=dict)       # pc -> instruction length
    strs: dict = field(default_factory=dict)      # start -> (end incl. terminator, 'text' | 'file')
    pads: dict = field(default_factory=dict)      # start -> bytes (S / 00 fill)
    refs: dict = field(default_factory=dict)      # string start -> [(pc, operand offset)]
    jumps: dict = field(default_factory=dict)     # code target -> [(pc, operand offset)]
    bad_ops: list = field(default_factory=list)   # pcs of opcodes with no length in code
    unref: list = field(default_factory=list)     # string starts no operand points at
    data_start: int = 0                           # start of the non-code tail (== len(data) if none)
    data_blocks: dict = field(default_factory=dict)   # start -> end of known data inside the code area


def _string_end(data, p):
    """(end, kind) of a string at p, or (None, None)."""
    n = len(data)
    q = p
    while q < n and 0x20 <= data[q] < 0x7F:
        q += 1
    if q - p >= 4 and q < n and data[q] == 0 and FILENAME.fullmatch(data[p:q]):
        return q + 1, 'file'
    q = p
    while q + 1 < n:
        lo, hi = data[q], data[q + 1]
        q += 2
        if lo == 0 and hi == 0:
            return q, 'text'   # may be empty (a bare 0000 that pointers use as a blank message)
        if not (hi <= 0x1C or hi == 0xFF):   # glyph codes are < 0x1CA5; FFxx are control codes
            return None, None
    return None, None


def _sweep(data, lens, data_start, str_targets, code_targets, data_ranges):
    s = Script(data, data_start=data_start)
    n = data_start

    def next_string(p, after_ff):
        r = p
        if after_ff and r < n and data[r] == 0:
            r += 1
        filled = False
        while r < n and r % 4 and data[r] == 0x53:
            filled = True
            r += 1
        if r >= n or r % 4 or r in code_targets:
            return None
        end, kind = _string_end(data, r)
        if end is None or end > n:
            return None
        if r in str_targets or filled:
            return r
        if end - r == 2:   # an empty string only on evidence
            return None
        if after_ff:   # FF 00 then an aligned string nobody points at (copies of arm9 names, file names)
            return r if kind == 'file' or (r > p and end - r >= 6) else None
        if r == p and data[r] != 0:   # straight after a string: a pool ends with 00, so this is a string
            return r
        return None

    pc = 4
    while pc < n:
        if pc in data_ranges:   # non-code block inside the code area (pad included)
            s.data_blocks[pc] = data_ranges[pc]
            pc = data_ranges[pc]
            continue
        op = data[pc]
        ln = lens[op] if op < len(lens) else 0
        if op != 0xFF:
            if ln == 0:
                s.bad_ops.append(pc)
                ln = 1
            s.ins[pc] = ln
            pc += ln
            continue
        s.ins[pc] = 1
        pc += 1
        if pc in data_ranges:
            continue
        first = True
        while pc < n:
            r = next_string(pc, first)
            if r is None:
                break
            if r > pc:
                s.pads[pc] = data[pc:r]
            end, kind = _string_end(data, r)
            s.strs[r] = (end, kind)
            pc = end
            first = False
        q = pc
        while q < n and data[q] == 0 and q not in code_targets:
            q += 1
        if q > pc:
            s.pads[pc] = data[pc:q]
        pc = q
    return s


def _operands(s, table):
    for pc, ln in s.ins.items():
        for k in table.get(s.data[pc], ()):
            if k + 4 <= ln:
                yield pc, k, struct.unpack_from('<I', s.data, pc + k)[0]


def parse(data, lens, string_ops, code_ops, data_start=None, data_ranges=None):
    data_ranges = data_ranges or {}
    data = bytes(data)
    assert data[:4] == b'scr\x1a', 'not a scr container'
    data_start = len(data) if data_start is None else data_start
    str_targets, code_targets = set(), set()
    for _ in range(3):
        s = _sweep(data, lens, data_start, str_targets, code_targets, data_ranges)
        new_str = {v for pc, k, v in _operands(s, string_ops) if 4 <= v < data_start}
        new_code = {v for pc, k, v in _operands(s, code_ops) if 4 <= v < data_start}
        if new_str == str_targets and new_code == code_targets:
            break
        str_targets, code_targets = new_str, new_code
    for pc, k, v in _operands(s, string_ops):
        if v in s.strs:
            s.refs.setdefault(v, []).append((pc, k))
    for pc, k, v in _operands(s, code_ops):
        if 4 <= v < data_start:
            s.jumps.setdefault(v, []).append((pc, k))
    s.unref = sorted(set(s.strs) - set(s.refs))
    return s


def opcode_lengths(arm9, table, count):
    o = table - ARM9_BASE
    return bytes(arm9[o:o + count])


def parse_rom_img(data, arm9):
    return parse(data, opcode_lengths(arm9, ROM_IMG_LEN_TABLE, 0xC0), ROM_IMG_STRING_OPS, ROM_IMG_CODE_OPS,
                 ROM_IMG_DATA_START)


def parse_quest_img(data, arm9):
    return parse(data, opcode_lengths(arm9, QUEST_LEN_TABLE, 0x31), QUEST_STRING_OPS, QUEST_CODE_OPS,
                 data_ranges=QUEST_DATA)
