"""textscan.py: find the game's text in arm9 and every NitroFS file.

    python -X utf8 tools/textscan.py [--min 4] [--only PREFIX] [--show N]

Encoding (verified, docs/re/text.md): 16-bit little-endian codes, code = JIS X 0208 glyph index + 1
(index = (ku-1)*94 + ten-1, the order of font/lc*.bin); 0x0000 ends a string, 0x000A is a newline, 0xFF7x are control
codes. A hit is a run of such codes holding at least --min kana. Prints per file: run count, first offset, sample.
Also reports Shift-JIS runs, in case some text uses it.
"""
import argparse
from array import array
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Bouken-ou Beet - Vandel vs. Busters (Japan).nds"
NGLYPH = 7332


def code_char(c):
    """Character for a text code, or None if it is not a glyph code."""
    if not 1 <= c <= NGLYPH:
        return None
    i = c - 1
    ku, ten = i // 94 + 1, i % 94 + 1
    try:
        return bytes([0xA0 + ku, 0xA0 + ten]).decode("euc_jp")
    except UnicodeDecodeError:
        return "�"


KANA_LO, KANA_HI = 3 * 94 + 1, 5 * 94 + 86  # hiragana row 4 .. katakana row 5 (codes)


def is_ctrl(c):
    return c == 0x0A or 0xFF00 <= c <= 0xFFFF


def runs_idx(data, minc):
    """(byte offset, text) for every run of glyph/control codes with >= minc kana."""
    out = []
    for par in (0, 1):
        b = data[par:]
        b = b[:len(b) // 2 * 2]
        a = array("H")
        a.frombytes(b)
        n, i = len(a), 0
        while i < n:
            c = a[i]
            if not (1 <= c <= NGLYPH):
                i += 1
                continue
            j, kana = i, 0
            while j < n and (1 <= a[j] <= NGLYPH or is_ctrl(a[j])):
                if KANA_LO <= a[j] <= KANA_HI:
                    kana += 1
                j += 1
            if kana >= minc:
                txt = "".join(code_char(x) or ("\\n" if x == 0x0A else f"[{x:04X}]") for x in a[i:j])
                out.append((par + 2 * i, txt))
            i = j + 1
    return sorted(out)


def runs_sjis(data, minc):
    out, i, n = [], 0, len(data)
    while i < n - 1:
        j, kana = i, 0
        while j < n - 1 and (0x81 <= data[j] <= 0x9F or 0xE0 <= data[j] <= 0xEF):
            if data[j] == 0x82 and 0x9F <= data[j + 1] <= 0xF1 or data[j] == 0x83 and data[j + 1] <= 0x96:
                kana += 1
            j += 2
        if kana >= minc:
            out.append((i, data[i:j].decode("cp932", "replace")))
            i = j
        else:
            i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=4)
    ap.add_argument("--only")
    ap.add_argument("--show", type=int, default=1, help="samples per file")
    a = ap.parse_args()
    rom = ndspy.rom.NintendoDSRom.fromFile(str(ROM))
    items = [("arm9", bytes(rom.arm9))] + [(rom.filenames.filenameOf(i) or f"#{i}", bytes(d))
                                          for i, d in enumerate(rom.files)]
    for name, data in items:
        if a.only and not name.startswith(a.only):
            continue
        for enc, hits in (("idx16", runs_idx(data, a.min)), ("sjis", runs_sjis(data, a.min))):
            if hits:
                print(f"{name}\t{enc}\t{len(hits)} runs\t{sum(len(t) for _, t in hits)} chars")
                for off, t in hits[:a.show]:
                    print(f"    0x{off:X}\t{t[:60]}")


if __name__ == "__main__":
    main()
