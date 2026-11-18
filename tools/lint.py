"""lint.py: text lint over script/ (every entry with an `en`). Run by tools/check.py, so it gates commits.

    python -X utf8 tools/lint.py [--quiet]

Errors (exit 1): Japanese left in `en`; text the engine cannot encode; control codes differing from the JP (line
and page breaks may differ in `msg`); an arm9 / name slot over its byte cap (insert.text_cap); a dialogue message over
255 codes; a line wider than its kind's budget, or more lines per page than the box has (tools/budgets.json, measured
in phase 5, evidence in docs/windows.md). Kinds with English but no budget yet are counted in one warning line.
Runtime variables are measured with stand-ins (VARS): `{hero}` as the longest default the name entry allows.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402

BUDGETS = json.loads((ROOT / 'tools' / 'budgets.json').read_text(encoding='utf-8'))
JP = re.compile(r'[぀-ヿ㐀-鿿ｦ-ﾟ]')
CTRL = insert.CTRL
BREAKS = ('{br}', '{page}')
# stand-ins for text the game inserts at runtime (guesses until the Latin name entry exists; docs/status.md)
VARS = {'{hero}': 'Beetmm', '{vandel}': 'Beelzebub', '{name93}': 'Mmmmmmmm', '{monster}': 'Sand Owl Mmmm',
        '{count}': '9999'}


def budget(kind):
    return BUDGETS.get(kind) or BUDGETS.get(kind.split('.')[0])


def pages(text):
    """[[line, ...], ...] split on {page} then {br}; other controls replaced by VARS or dropped."""
    out = []
    for page in text.split('{page}'):
        lines = []
        for line in page.split('{br}'):
            for k, v in VARS.items():
                line = line.replace(k, v)
            lines.append(CTRL.sub('', line))
        out.append(lines)
    return out


def lint_entry(e, eng):
    """List of error strings for one entry (empty if fine or untranslated)."""
    en = e.get('en')
    if not en:
        return []
    errs = []
    if JP.search(en):
        errs.append('Japanese in en')
    try:
        eng.codes(en)
    except Exception as x:  # noqa: BLE001 - report any encoder failure as a lint error
        return errs + ['not encodable: %s' % x]
    cj, ce = Counter(CTRL.findall(e['jp'])), Counter(CTRL.findall(en))
    if e['kind'] == 'msg':
        for b in BREAKS:
            cj.pop(b, None)
            ce.pop(b, None)
    if cj != ce:
        errs.append('controls differ: jp %s en %s' % (dict(cj), dict(ce)))
    if 'max' in e:
        n = len(eng.encode(en))
        cap = insert.text_cap(e)
        if n > cap:
            errs.append('%d bytes > slot cap %d' % (n, cap))
    if e['kind'] == 'msg':
        full = en
        for k, v in VARS.items():
            full = full.replace(k, v)
        if len(eng.codes(full)) > 255:
            errs.append('message over 255 codes')
    b = budget(e['kind'])
    if b:
        checks = [c for c in [b] + b.get('also', []) if 'px' in c]   # no px: not drawn (sort keys, placeholders)
        for pg in pages(en):
            if len(pg) > b.get('lines', 1):
                errs.append('%d lines > %d per page' % (len(pg), b.get('lines', 1)))
            for i, line in enumerate(pg):
                for c in checks:
                    lim = c['px']
                    if i == b.get('lines', 1) - 1 and 'last_px' in b and c is b:
                        lim = b['last_px']
                    w = eng.width(line, c['font'])
                    if w > lim:
                        errs.append('line %d: %d px > %d (%d px font) %r' % (i + 1, w, lim, c['font'], line))
    return errs


def run(entries, eng):
    """(errors [(id, msg)], kinds with English but no budget {kind: count})."""
    errors, nobudget = [], Counter()
    for e in entries:
        for m in lint_entry(e, eng):
            errors.append((e['id'], m))
        if e.get('en') and not budget(e['kind']):
            nobudget[e['kind']] += 1
    return errors, nobudget


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    import textwidth
    eng = textwidth.load()
    entries = [e for es in insert.load_entries().values() for e in es]
    errors, nobudget = run(entries, eng)
    for i, m in errors[:200]:
        print('%s: %s' % (i, m))
    done = sum(1 for e in entries if e.get('en'))
    print('lint: %d entries, %d translated, %d errors' % (len(entries), done, len(errors)))
    if nobudget:
        print('warning: no measured budget for %s' % ', '.join('%s (%d)' % kv for kv in sorted(nobudget.items())))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
