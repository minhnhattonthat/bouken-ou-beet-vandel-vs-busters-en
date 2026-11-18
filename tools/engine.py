"""English text engine for Beet (docs/re/vwf.md): proportional letters as pair codes, drawn by an arm9 hook.

Codes 0x2000-0x5FFF are English: code = 0x2000 + a*128 + b, where a and b are letter slots (LETTERS; slot 0 = no
letter, so a single letter is `a*128`). The hook renders letter a, then letter b right after a's width, into the
game's glyph buffer, for both fonts the game uses (12x12 for dialogue/names, 8x8 for small menu text). The letters
are the game's own full-width Latin glyphs cropped to their ink plus a 1 px gap (lc12x12.bin / lc8x8.bin), so the
style matches. The advance after each glyph is the pair's width instead of the fixed 12/8 (six string loops and the
dialogue typewriter are patched), so text is proportional.

    from engine import Engine
    eng = Engine.from_rom(rom)            # ndspy rom (original): fonts + arm9
    eng.encode('Hello{br}world{close}')   # -> bytes (u16 LE codes + nothing else; caller adds 0000)
    eng.width('Hello', font=12)           # pixels
    eng.patch_arm9(rom)                   # adds the hook block (autoload) and patches the call sites
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from text16 import Codec  # noqa: E402

EBASE, EEND = 0x2000, 0x6000
PAIR_MAX = 16            # px: the glyph buffer is 24 px wide and the game shifts a glyph by up to 7 px
SPACE = {12: 4, 8: 3}
ROWS = {12: 12, 8: 8}
EXTRA = '…×♪★☆○●◎→←↑↓「」『』・※〜―'
LETTERS = [None] + [chr(c) for c in range(0x20, 0x7F)] + list(EXTRA)
assert len(LETTERS) <= 128
SLOT = {ch: i for i, ch in enumerate(LETTERS) if ch}
JIS_OVERRIDE = {'"': '”', "'": '’', '-': '‐', '`': '‘', '~': '〜', '\\': '＼'}

BLOCK = 0x021C7EC0       # new autoload block: the old main-arena start (arena-lo literal at ARENA_LIT)
ARENA_LIT = 0x020F97D8
MODPARAMS = 0x02000B48
A9 = 0x02000000
TOKEN = re.compile(r'\{(\w+)\}|\[([0-9A-F]{4})\]')


def glyph_index(ch):
    """Font glyph index of the full-width JIS form of ch (font rows 0-7 = JIS ku 1-8)."""
    fw = JIS_OVERRIDE.get(ch) or (chr(ord(ch) + 0xFEE0) if 0x21 <= ord(ch) <= 0x7E else ch)
    b = fw.encode('euc_jp')
    assert len(b) == 2 and b[0] < 0xA9, ch
    return (b[0] - 0xA1) * 94 + (b[1] - 0xA1)


def crop_font(font, size):
    """(widths[128], rows: 128 letters x ROWS[size] u16, MSB = leftmost px) cropped from a game font."""
    widths, rows = bytearray(128), bytearray(128 * ROWS[size] * 2)
    for slot, ch in enumerate(LETTERS):
        if ch is None:
            continue
        if ch == ' ':
            widths[slot] = SPACE[size]
            continue
        i = glyph_index(ch)
        if size == 12:
            g = [int.from_bytes(font[i * 24 + r * 2:i * 24 + r * 2 + 2], 'big') for r in range(12)]
        else:
            g = [font[i * 8 + r] << 8 for r in range(8)]
        cols = [c for c in range(16) if any(r >> (15 - c) & 1 for r in g)]
        left, right = min(cols), max(cols)
        widths[slot] = right - left + 2
        for r, bits in enumerate(g):
            struct.pack_into('<H', rows, (slot * ROWS[size] + r) * 2, (bits << left) & 0xFFFF)
    return bytes(widths), bytes(rows)


# ARM hook source. {NAME} fields are filled in by Engine.asm(). Sites are listed in SITES.
ASM = r"""
hook12:
    sub ip, r1, #{FW_UP}
    cmp ip, #26
    movlo r1, ip, lsl #7
    addlo r1, r1, #{PC_UP}
    sub ip, r1, #{FW_LO}
    cmp ip, #26
    movlo r1, ip, lsl #7
    addlo r1, r1, #{PC_LO}
    cmp r1, #0x2000
    blo orig12
    cmp r1, #0x6000
    bhs orig12
    mov r3, #12
    b render
orig12:
    push {{r4, r5, r6, r7, r8, sb, sl, fp, lr}}
    b #0x02007914
hook8:
    sub ip, r1, #{FW_UP}
    cmp ip, #26
    movlo r1, ip, lsl #7
    addlo r1, r1, #{PC_UP}
    sub ip, r1, #{FW_LO}
    cmp ip, #26
    movlo r1, ip, lsl #7
    addlo r1, r1, #{PC_LO}
    cmp r1, #0x2000
    blo orig8
    cmp r1, #0x6000
    bhs orig8
    mov r3, #8
    b render
orig8:
    push {{r4, r5, r6, r7, r8, sb, sl, fp, lr}}
    b #0x02007AA8

render:
    push {{r4, r5, r6, r7, r8, sb, sl, fp, lr}}
    add r4, r0, #0x14
    mov r5, #0
    mvn r6, #0
    mov r7, #0x48
clr:
    str r5, [r4]
    str r6, [r4, #0x120]
    add r4, r4, #4
    subs r7, r7, #1
    bne clr
    ldr ip, lit_ones
    and r2, r2, #0xF
    mul r2, ip, r2
    sub r1, r1, #0x2000
    mov r8, r1, lsr #7
    and sb, r1, #0x7F
    cmp r3, #12
    ldreq sl, lit_t12
    ldrne sl, lit_t8
    ldreq fp, lit_w12
    ldrne fp, lit_w8
    ldrb fp, [fp, r8]
    mov ip, r3, lsl #1
    mla r8, ip, r8, sl
    mla sb, ip, sb, sl
    mov r4, #0
rowlp:
    ldrh r5, [r8], #2
    ldrh r6, [sb], #2
    mov r5, r5, lsl #16
    mov r6, r6, lsl #16
    orr r5, r5, r6, lsr fp
    mov r6, r4, lsr #3
    add r6, r6, r6, lsl #1
    mov r6, r6, lsl #5
    and r7, r4, #7
    add r6, r6, r7, lsl #2
    add r6, r6, r0
    add r6, r6, #0x14
    mov r7, #3
tlp:
    mov sl, #0
    mov r1, #0
bitlp:
    mov lr, r5, lsl r1
    tst lr, #0x80000000
    mov lr, r1, lsl #2
    movne ip, #0xF
    orrne sl, sl, ip, lsl lr
    add r1, r1, #1
    cmp r1, #8
    blt bitlp
    and lr, sl, r2
    str lr, [r6]
    mvn lr, sl
    str lr, [r6, #0x120]
    add r6, r6, #32
    mov r5, r5, lsl #8
    subs r7, r7, #1
    bne tlp
    add r4, r4, #1
    cmp r4, r3
    blt rowlp
    pop {{r4, r5, r6, r7, r8, sb, sl, fp, lr}}
    bx lr

adv_r6m:
    ldrh r1, [r6, #-2]
    b adv
adv_r7m:
    ldrh r1, [r7, #-2]
    b adv
adv_r7:
    ldrh r1, [r7]
adv:
    push {{lr}}
    bl wcode
    ldr r1, lit_scr
    str r0, [r1]
    mov r0, r1
    pop {{lr}}
    bx lr

wcode:
    sub r3, r1, #{FW_UP}
    cmp r3, #26
    movlo r1, r3, lsl #7
    addlo r1, r1, #{PC_UP}
    sub r3, r1, #{FW_LO}
    cmp r3, #26
    movlo r1, r3, lsl #7
    addlo r1, r1, #{PC_LO}
    sub r3, r1, #0x2000
    cmp r3, #0x4000
    bhs wfix
    cmp r0, #0
    ldreq r2, lit_w8
    ldrne r2, lit_w12
    mov r1, r3, lsr #7
    and r3, r3, #0x7F
    ldrb r1, [r2, r1]
    ldrb r3, [r2, r3]
    add r0, r1, r3
    bx lr
wfix:
    ldr r2, lit_adv
    ldr r0, [r2, r0, lsl #2]
    bx lr

tw_x:
    push {{r0, r2, r3, r4, r5, ip, lr}}
    sub r4, r3, r1, lsl #1
    mov r5, r1
    mov ip, #8
twl:
    cmp r5, #0
    beq twd
    ldrh r1, [r4], #2
    mov r0, #2
    bl wcode
    add ip, ip, r0
    sub r5, r5, #1
    b twl
twd:
    mov r1, ip
    pop {{r0, r2, r3, r4, r5, ip, lr}}
    bx lr

name_half:
    push {{r1, r2, r3, r4, r5, r6, lr}}
    mov r4, r3
    mov r5, r1
    mov r6, #0
nhl:
    cmp r5, #0
    beq nhd
    ldrh r1, [r4], #2
    mov r0, #2
    bl wcode
    add r6, r6, r0
    sub r5, r5, #1
    b nhl
nhd:
    mov r0, r6, lsr #1
    pop {{r1, r2, r3, r4, r5, r6, lr}}
    bx lr

ne_init:
    push {{lr}}
    bl #0x02029A14
    mov r0, #1
    str r0, [r4, #0xdc]
    pop {{lr}}
    bx lr

lit_ones: .word 0x11111111
lit_t12: .word {T12}
lit_t8: .word {T8}
lit_w12: .word {W12}
lit_w8: .word {W8}
lit_scr: .word {SCR}
lit_adv: .word 0x0210D32C
"""

# site address -> (original bytes hex, replacement: label to branch to / 'bl:label' / raw asm)
SITES = {
    0x02007910: ('f04f2de9', 'b hook12'),     # 12x12 glyph fetch entry (push {r4-fp,lr})
    0x02007AA4: ('f04f2de9', 'b hook8'),      # 8x8 glyph fetch entry
    0x02020200: (None, 'bl adv_r6m'),        # string loops: bl 0x02020230 (advance table) -> pair width
    0x02020280: (None, 'bl adv_r6m'),
    0x020204F4: (None, 'bl adv_r6m'),
    0x02020574: (None, 'bl adv_r7m'),
    0x0202062C: (None, 'bl adv_r7'),
    0x020206A0: (None, 'bl adv_r6m'),
    0x02022828: ('081082e2', 'bl tw_x'),      # typewriter: add r1, r2, #8 (x = col*12 + 8) -> sum of widths
    0x02022884: ('130050e3', 'cmp r0, #0xFF'),   # typewriter auto-wrap after 19 codes -> off (explicit breaks)
    0x02095314: ('0600a0e3', 'bl name_half'),     # speaker tag centring: mov r0, #6; mul r0, r1, r0 (6 px x count)
    0x02095318: ('910000e0', 'mov r0, r0'),       #   -> half the pixel width
    0x0202B6F0: ('c7f8ffeb', 'bl ne_init'),       # name entry constructor: bl 0x02029A14 (keyboard rows), then
                                                  #   the keyboard opens on 英字 (mode obj+0xDC = 1; docs/re/vwf.md)
}

# Name entry writes full-width Latin codes (Ａ-Ｚ 0x00DD.., ａ-ｚ 0x00FD..); the hooks draw and measure them as
# the single proportional letter, so a typed name looks like the English around it (FW_* = first code, PC_* = the
# pair code of the single letter 'A' / 'a').
FW = {'FW_UP': 0xDD, 'FW_LO': 0xFD, 'PC_UP': 0x2000 + SLOT['A'] * 128, 'PC_LO': 0x2000 + SLOT['a'] * 128}


def fullwidth_code(code):
    """The English single-letter code a full-width Latin code is drawn as, else the code itself."""
    for fw, pc in ((FW['FW_UP'], FW['PC_UP']), (FW['FW_LO'], FW['PC_LO'])):
        if 0 <= code - fw < 26:
            return pc + (code - fw) * 128
    return code


# arm9 tables moved into the hook block because their slots cannot hold English (docs/re/arm9.md). Per table: the
# accessor's literal-pool word (= the old base), the old base, record count, old/new record size, and the accessor's
# scale instruction (orig hex -> replacement). The inserter fills Engine.reloc[key] (count * new bytes) before
# patch_arm9; untranslated records keep their Japanese.
RELOC = {
    # monster attribute (属性) kanji 沼 窟 渦 砂 地 鉱 樹 極 骨 絶: 4-byte slots = one code; accessor 0x020140F4
    'elem': {'lit': 0x02014104, 'base': 0x021233D8, 'count': 10, 'old': 4, 'new': 16,
             'insn': 0x020140FC, 'orig': '000181e0', 'repl': 'add r0, r1, r0, lsl #4'},
}


class Engine:
    def __init__(self, f12, f8, codec):
        self.w12, self.t12 = crop_font(f12, 12)
        self.w8, self.t8 = crop_font(f8, 8)
        self.codec = codec
        self.reloc = {}   # RELOC key -> new table bytes (set by insert.Inserter)
        self.strings = []   # pointer strings moved into the block: (old address, [pointer word addrs], bytes + 0000)

    def relocate_string(self, old, ptrs, data):
        """Put a pointer string that outgrew its old room into the block; patch_arm9 repoints its pointer words."""
        self.strings.append((old, list(ptrs), bytes(data) + b'\0\0'))

    def _pool(self):
        """(pool bytes, {old address: offset in the pool}) of the relocated pointer strings, each 4-aligned."""
        pool, offs = bytearray(), {}
        for old, _, data in self.strings:
            offs[old] = len(pool)
            pool += data.ljust((len(data) + 3) & ~3, b'\0')
        return bytes(pool), offs

    def reloc_default(self, arm9, key):
        """The table at its new record size, filled with the original records (zero-padded)."""
        r = RELOC[key]
        out = bytearray()
        for i in range(r['count']):
            o = r['base'] - A9 + i * r['old']
            out += arm9[o:o + r['old']].ljust(r['new'], b'\0')
        return out

    def _data(self):
        blobs = [('W12', self.w12), ('W8', self.w8), ('T12', self.t12), ('T8', self.t8), ('SCR', bytes(4))]
        for key, r in RELOC.items():
            blob = self.reloc.get(key) or bytes(r['count'] * r['new'])
            assert len(blob) == r['count'] * r['new'], key
            blobs.append(('R_' + key, bytes(blob)))
        blobs.append(('R_STRINGS', self._pool()[0]))
        return blobs

    @classmethod
    def from_rom(cls, rom):
        return cls(bytes(rom.getFileByName('font/lc12x12.bin')), bytes(rom.getFileByName('font/lc8x8.bin')),
                   Codec.load(ROOT / 'tbl' / 'jp.tbl'))

    # ---- text
    def letter_width(self, ch, font=12):
        return (self.w12 if font == 12 else self.w8)[SLOT[ch]]

    def code_width(self, code, font=12):
        code = fullwidth_code(code)
        if EBASE <= code < EEND:
            w = self.w12 if font == 12 else self.w8
            return w[(code - EBASE) >> 7] + w[(code - EBASE) & 0x7F]
        return 12 if font == 12 else 8

    def codes(self, text):
        """English text -> list of u16 codes. Letters pair greedily while the pair fits PAIR_MAX (12 px font)."""
        out, run = [], []

        def flush():
            i = 0
            while i < len(run):
                a = run[i]
                b = run[i + 1] if i + 1 < len(run) else None
                if b is not None and self.letter_width(a) + self.letter_width(b) <= PAIR_MAX:
                    out.append(EBASE + SLOT[a] * 128 + SLOT[b])
                    i += 2
                else:
                    out.append(EBASE + SLOT[a] * 128)
                    i += 1
            run.clear()

        pos = 0
        for m in TOKEN.finditer(text):
            run.extend(self._letters(text[pos:m.start()]))
            flush()
            if m[1]:
                out.append(self.codec.enc['{%s}' % m[1]])
            else:
                out.append(int(m[2], 16))
            pos = m.end()
        run.extend(self._letters(text[pos:]))
        flush()
        return out

    @staticmethod
    def _letters(s):
        for ch in s:
            if ch not in SLOT:
                raise ValueError('no English glyph for %r' % ch)
        return list(s)

    @staticmethod
    def decode_code(c):
        """English pair code -> its letters ('' for a non-English code)."""
        if not EBASE <= c < EEND:
            return ''
        return ''.join(LETTERS[i] or '' for i in ((c - EBASE) >> 7, (c - EBASE) & 0x7F))

    def encode(self, text):
        return b''.join(struct.pack('<H', c) for c in self.codes(text))

    def width(self, text, font=12):
        """Pixel width of one line of English text (no control codes)."""
        return sum(self.code_width(c, font) for c in self.codes(text))

    # ---- arm9
    def block(self):
        """(code+data bytes, labels) of the hook block at BLOCK."""
        from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
        data_off = 0x400
        lay = {}
        pos = data_off
        data = self._data()
        for name, blob in data:
            lay[name] = BLOCK + pos
            pos += (len(blob) + 3) & ~3
        fields = {k: '0x%08X' % v for k, v in lay.items() if not k.startswith('R_')}
        fields.update({k: '0x%X' % v for k, v in FW.items()})
        src = ASM.format(**fields)
        ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
        enc, _ = ks.asm(src, BLOCK)
        code = bytes(enc)
        assert len(code) <= data_off, hex(len(code))
        labels = self._labels(ks, src)
        labels.update({k: v for k, v in lay.items() if k.startswith('R_')})
        out = bytearray(code.ljust(data_off, b'\0'))
        for name, blob in data:
            out += blob.ljust((len(blob) + 3) & ~3, b'\0')
        return bytes(out), labels

    @staticmethod
    def _labels(ks, src):
        """Label addresses (keystone has no symbol API): ARM mode, every instruction and .word is 4 bytes."""
        labels, n = {}, 0
        for line in src.splitlines():
            m = re.match(r'(\w+):\s*(.*)', line.strip())
            if m:
                labels[m[1]] = BLOCK + 4 * n
                line = m[2]
            if line.strip():
                n += 1
        assert BLOCK + 4 * n == BLOCK + len(ks.asm(src, BLOCK)[0])
        return labels

    def patch_arm9(self, rom, log=None):
        """Append the hook block as a new autoload section, raise the arena start, patch the call sites."""
        from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
        a = bytearray(rom.arm9)
        for key in RELOC:
            self.reloc.setdefault(key, self.reloc_default(a, key))
        blob, labels = self.block()
        p = list(struct.unpack_from('<9I', a, MODPARAMS - A9))
        lst_start, lst_end = p[0] - A9, p[1] - A9
        assert lst_end == len(a), 'autoload list is not at the end of arm9'
        entries = a[lst_start:lst_end]
        assert BLOCK == p[4], 'block must start at the static BSS end'
        size = (len(blob) + 31) & ~31
        blob = blob.ljust(size, b'\0')
        new = a[:lst_start] + blob + entries + struct.pack('<3I', BLOCK, size, 0)
        p[0], p[1] = A9 + lst_start + size, A9 + len(new)
        struct.pack_into('<2I', new, MODPARAMS - A9, p[0], p[1])
        lit = ARENA_LIT - A9
        assert struct.unpack_from('<I', new, lit)[0] == BLOCK
        struct.pack_into('<I', new, lit, BLOCK + size)
        ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
        for site, (orig, repl) in SITES.items():
            o = site - A9
            m = re.match(r'(bl?) (\w+)$', repl)
            asm = '%s #0x%08X' % (m[1], labels[m[2]]) if m and m[2] in labels else repl
            enc = bytes(ks.asm(asm, site)[0])
            assert len(enc) == 4, repl
            want = bytes.fromhex(orig) if orig else bytes(ks.asm('bl #0x02020230', site)[0])
            assert a[o:o + 4] == want, 'site %08X holds %s, expected %s' % (site, a[o:o + 4].hex(), want.hex())
            if log is not None:
                log.append('arm9 %08X %s %s %s' % (site, want.hex(), enc.hex(), repl))
            new[o:o + 4] = enc
        for key, r in RELOC.items():
            lit, o = r['lit'] - A9, r['insn'] - A9
            assert struct.unpack_from('<I', a, lit)[0] == r['base'], key
            assert a[o:o + 4].hex() == r['orig'], key
            enc = bytes(ks.asm(r['repl'], r['insn'])[0])
            new[lit:lit + 4] = struct.pack('<I', labels['R_' + key])
            new[o:o + 4] = enc
            if log is not None:
                log.append('arm9 %08X reloc %s -> %08X (%s)' % (r['lit'], key, labels['R_' + key], r['repl']))
        offs = self._pool()[1]
        for old, ptrs, _ in self.strings:
            to = labels['R_STRINGS'] + offs[old]
            for w in ptrs:
                o = w - A9
                assert struct.unpack_from('<I', a, o)[0] == old, 'pointer word %08X does not hold %08X' % (w, old)
                struct.pack_into('<I', new, o, to)
                if log is not None:
                    log.append('arm9 %08X ptr %08X -> %08X' % (w, old, to))
        rom.arm9 = bytes(new)
        return labels
