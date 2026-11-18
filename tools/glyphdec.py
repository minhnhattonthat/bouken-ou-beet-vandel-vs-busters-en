"""Decode a tools/lua/glyphlog.lua log: one line per (font, caller, x, y) run, codes -> text via tbl/jp.tbl.

    python -X utf8 tools/glyphdec.py work/qa/RUN/log.txt [--uniq]
"""
import argparse
import re
import sys

sys.path.insert(0, __file__.rsplit('tools', 1)[0] + 'tools')
from text16 import Codec  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('log')
    ap.add_argument('--uniq', action='store_true', help='one line per (font, caller, text)')
    a = ap.parse_args()
    c = Codec.load('tbl/jp.tbl')
    seen = set()
    for line in open(a.log, encoding='utf-8', errors='replace'):
        m = re.match(r'f(\d+) (G\d+) lr=(\w+) x=(-?\d+) y=(-?\d+) n=\d+ (.*)', line)
        if not m:
            continue
        text = ''.join(c.decode_code(int(h, 16)) for h in m[6].split())
        key = (m[2], m[3], text)
        if a.uniq and key in seen:
            continue
        seen.add(key)
        print('f%s %s %s x=%s y=%s %s' % (m[1], m[2], m[3], m[4], m[5], text))


if __name__ == '__main__':
    main()
