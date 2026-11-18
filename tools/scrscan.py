"""scrscan.py: survey strings in a `scr\\x1a` script file and the u32 operands that point at them.

    python -X utf8 tools/scrscan.py FILE [--list]

A string = a run of 16-bit glyph/control codes ending in 0x0000, starting on an even offset. For each one, every u32 in
the file equal to its start offset is reported with the 1-3 bytes before it (the opcode). Prints a histogram of
opcode prefixes, the strings with no reference, and the text range.
"""
import argparse
import collections
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mktbl import code_char  # noqa: E402

CTRL = {0xFF70: "\\n", 0xFF71: "{end}", 0xFF72: "{page}"}


def strings(data, start=4):
    """Yield (offset, codes) for even-aligned zero-terminated runs of text codes (>= 2 codes)."""
    i, n = start + (start & 1), len(data) - 1
    while i < n:
        j, codes = i, []
        while j < n:
            c = struct.unpack_from("<H", data, j)[0]
            if c == 0:
                break
            if not (code_char(c) or c in CTRL or 0xFF00 <= c <= 0xFFFF):
                codes = None
                break
            codes.append(c)
            j += 2
        if codes and len(codes) >= 1 and j < n and any(code_char(c) for c in codes):
            yield i, codes, j + 2
            i = j + 2
        else:
            i += 2


def text(codes):
    return "".join(code_char(c) or CTRL.get(c, f"[{c:04X}]") for c in codes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    data = Path(a.file).read_bytes()
    refs = collections.defaultdict(list)
    for k in range(4, len(data) - 3):
        v = struct.unpack_from("<I", data, k)[0]
        if 4 <= v < len(data):
            refs[v].append(k)
    hist, unref, total, lo, hi = collections.Counter(), [], 0, None, 0
    for off, codes, end in strings(data):
        r = refs.get(off, [])
        total += 1
        lo = off if lo is None else lo
        hi = end
        if not r:
            unref.append((off, text(codes)))
        for k in r:
            hist[data[max(0, k - 2):k].hex()] += 1
        if a.list:
            print(f"0x{off:05X} refs={','.join(hex(k) for k in r) or '-'}\t{text(codes)[:70]}")
    print(f"{a.file}: {total} strings, {len(unref)} unreferenced, text 0x{lo or 0:X}-0x{hi:X} of 0x{len(data):X}")
    print("2 bytes before each pointer:", hist.most_common(15))
    for off, t in unref[:15]:
        print(f"  unref 0x{off:05X} {t[:60]}")


if __name__ == "__main__":
    main()
