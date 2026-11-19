"""qaruler.py: width-gate build for jp-bound kinds (phase 9 polish): every entry of the given kinds gets a ruler string
of distinct characters, cut to its byte cap, so a shot shows how far a box really draws. The last visible character
names the prefix; --width prints that prefix's px.

    python -X utf8 tools/qaruler.py build area.name area2.name skill.name ... [--out build/beet_ruler.nds]
    python -X utf8 tools/qaruler.py width 0123456789abcd        # px of a visible ruler prefix (12 px font)
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import insert  # noqa: E402

RULER = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def ruler_for(e):
    cap = insert.text_cap(e) if 'max' in e else 60
    s = RULER
    while len(batches.eng().encode(s)) > cap:
        s = s[:-1]
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build')
    b.add_argument('kinds', nargs='+')
    b.add_argument('--out', default=str(ROOT / 'build/beet_ruler.nds'))
    w = sub.add_parser('width')
    w.add_argument('text', nargs='+')
    w.add_argument('--font', type=int, default=12)
    a = ap.parse_args()
    if a.cmd == 'width':
        for t in a.text:
            print('%4d px  %s' % (batches.eng().width(t, a.font), t))
        return 0
    files = batches.load_files()
    qa = {}
    for f, e in batches.all_entries(files):
        if e['kind'] in a.kinds and e.get('en') and not batches.skipped(e):
            qa[e['id']] = ruler_for(e)
    print(len(qa), 'entries ruled', flush=True)
    import build   # build.build(out, mode, qa, identity); a command line of --qa pairs is too long for Windows
    data = build.build(Path(a.out), 'en', qa, False)
    print(a.out, len(data), 'bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
