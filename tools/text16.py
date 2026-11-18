"""16-bit text codec for this game (docs/re/text.md): u16 little-endian codes, 0x0000 ends a string.

Reads tbl/jp.tbl (keys are the LE byte pairs). A code with a table entry decodes to its character or `{control}`;
any other code decodes to `[XXXX]` (the u16 value in hex), so decode -> encode is byte-exact and a stray code never
shifts the alignment (tbl.py would fall back to single bytes).

    from text16 import Codec
    c = Codec.load('tbl/jp.tbl')
    text, end = c.decode(data, pos)          # through the 0000 terminator; text excludes it
    c.encode(text) + b'\\0\\0' == data[pos:end]
"""
import re
import struct
from pathlib import Path

TOKEN = re.compile(r'\{(\w+)\}|\[([0-9A-F]{4})\]')


class Codec:
    def __init__(self, lines):
        self.dec, self.enc = {}, {}
        for line in lines:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            key, _, val = line.partition('=')
            code = struct.unpack('<H', bytes.fromhex(key))[0]
            if code == 0:
                continue   # the terminator is implicit
            m = re.fullmatch(r'\{(\w+)\}', val)
            text = '{%s}' % m[1] if m else (' ' if val == r'\s' else val)
            self.dec[code] = text
            self.enc.setdefault(text, code)

    @classmethod
    def load(cls, path):
        return cls(Path(path).read_text(encoding='utf-8-sig').splitlines())

    def decode_code(self, c):
        t = self.dec.get(c)
        return t if t is not None and self.enc[t] == c else '[%04X]' % c   # duplicate glyphs stay as codes

    def decode(self, data, pos, end=None, limit=0x4000):
        """Decode u16 codes from pos up to the 0000 terminator (or to `end`, exclusive, when given).
        Returns (text, position after the terminator / end)."""
        out = []
        stop = len(data) - 1 if end is None else end
        p = pos
        while p < stop:
            c = data[p] | data[p + 1] << 8
            p += 2
            if c == 0 and end is None:
                return ''.join(out), p
            out.append(self.decode_code(c))
            if p - pos > limit:
                raise ValueError('no terminator within %#x bytes of %#x' % (limit, pos))
        if end is None:
            raise ValueError('ran off the data decoding from %#x' % pos)
        return ''.join(out), p

    def encode(self, text):
        """Codes for text, without a terminator."""
        out = bytearray()
        i = 0
        while i < len(text):
            m = TOKEN.match(text, i)
            if m and (m[2] or ('{%s}' % m[1]) in self.enc):
                code = int(m[2], 16) if m[2] else self.enc['{%s}' % m[1]]
                i = m.end()
            else:
                ch = text[i]
                if ch not in self.enc:
                    raise ValueError('unencodable %r at %d in %r' % (ch, i, text))
                code = self.enc[ch]
                i += 1
            out += struct.pack('<H', code)
        return bytes(out)
