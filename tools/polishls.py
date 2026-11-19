"""polishls.py: the unticked lines of docs/polish.md with each entry's current English, width against its kind's
budget and its byte cap, for the phase-9 polish pass.

    python -X utf8 tools/polishls.py [--section TEXT] [--kind KIND] [--from LINE --to LINE] [--ticked]

One block per line: `L<line> id kind w/budget px (status) bytes/cap` then `  en: ...` and `  note: ...`.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402
import textwidth  # noqa: E402

BUDGETS = json.loads((ROOT / 'tools/budgets.json').read_text(encoding='utf-8'))
ID = re.compile(r'\b((?:a9|rom|quest|names|ptr)\.[0-9A-Za-z_.]+?)(?=[\s,:;)]|$| -)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--section')
    ap.add_argument('--kind')
    ap.add_argument('--from', dest='lo', type=int, default=0)
    ap.add_argument('--to', dest='hi', type=int, default=1 << 30)
    ap.add_argument('--ticked', action='store_true', help='list ticked lines too')
    a = ap.parse_args()
    eng = textwidth.load()
    byid = {e['id']: e for es in insert.load_entries().values() for e in es}
    sec = ''
    n = 0
    for i, line in enumerate((ROOT / 'docs/polish.md').read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('## '):
            sec = line[3:]
        if not (line.startswith('- [ ]') or (a.ticked and line.startswith('- [x]'))):
            continue
        if not (a.lo <= i <= a.hi) or (a.section and a.section not in sec):
            continue
        ids = [m.group(1).rstrip('.') for m in ID.finditer(line)]
        es = [byid[x] for x in ids if x in byid]
        if a.kind and not any(e['kind'] == a.kind for e in es):
            continue
        n += 1
        print('L%d %s' % (i, line[6:].split(' - ')[0][:60] if not es else ''), end='')
        for e in es[:3]:
            b = BUDGETS.get(e['kind'], {})
            en = e.get('en') or ''
            w = max((eng.width(x, b.get('font', 12)) for x in re.split(r'\{br\}|\{page\}', en) if x), default=0)
            cap = insert.text_cap(e) if e['id'].startswith('a9.') and 'max' in e else '-'
            try:
                nb = len(eng.encode(en))
            except Exception:  # noqa: BLE001
                nb = -1
            print('\n  %s %s %d/%s px (%s) %s/%s B\n  en: %s' % (e['id'], e['kind'], w, b.get('px', '-'),
                                                                 b.get('status', '-'), nb, cap, en), end='')
        print('\n  note: %s' % line[6:][:220])
    print('%d lines' % n)


if __name__ == '__main__':
    main()
