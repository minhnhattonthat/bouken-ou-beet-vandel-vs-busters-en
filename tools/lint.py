"""lint.py: text lint over script/ (every entry with an `en`). Run by tools/check.py, so it gates commits.

    python -X utf8 tools/lint.py [--quiet]

Errors (exit 1): Japanese left in `en`; text the engine cannot encode; control codes differing from the JP (line
and page breaks may differ in `msg`); an arm9 / name slot over its byte cap (insert.text_cap); a dialogue message over
engine.MSG_CODES (511) codes or a speaker over engine.SPEAKER_CODES (11), the expansion buffers; a line wider than its kind's budget, or more lines per page than the box has (tools/budgets.json, measured
in phase 5, evidence in docs/windows.md). Kinds with English but no budget yet are counted in one warning line.
Runtime variables are measured with stand-ins (VARS): `{hero}` as the widest name the name entry allows.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402
import insert  # noqa: E402

BUDGETS = json.loads((ROOT / 'tools' / 'budgets.json').read_text(encoding='utf-8'))
JP = re.compile(r'[぀-ヿ㐀-鿿ｦ-ﾟ]')
CTRL = insert.CTRL
BREAKS = ('{br}', '{page}')
# stand-ins for text the game inserts at runtime. Player names: the name entry takes 8 letters (obj+0x364 = 8 for
# entry types 0/1/3, 10 for 2/4; docs/re/vwf.md §Name entry), drawn proportionally: 8 x M or W = 80 px, the widest.
# {name93} is unidentified, so it gets the 10-letter limit.
VARS = {'{hero}': 'Mmmmmmmm', '{vandel}': 'Mmmmmmmm', '{name93}': 'Mmmmmmmmmm', '{monster}': 'Sand Owl Mmmm',
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
    if e['kind'] in insert.KEEP_KINDS:
        return ['%s is never inserted: leave en empty' % e['kind']]
    errs = []
    if JP.search(en):
        errs.append('Japanese in en')
    try:
        eng.codes(en)
    except Exception as x:  # noqa: BLE001 - report any encoder failure as a lint error
        return errs + ['not encodable: %s' % x]
    cj, ce = Counter(CTRL.findall(e['jp'])), Counter(CTRL.findall(en))
    if (budget(e['kind']) or {}).get('lines', 1) > 1:   # multi-line boxes: breaks are layout, re-wrapped in English
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
    lim = {'msg': engine.MSG_CODES, 'speaker': engine.SPEAKER_CODES}.get(e['kind'])
    if lim:
        full = en
        for k, v in VARS.items():
            full = full.replace(k, v)
        if len(eng.codes(full)) > lim:
            errs.append('message over %d codes' % lim)
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
    if e['kind'] == 'elem.name':   # Vandel status grid: 16 px cells drawn in the 8 px font (engine.ESHORT_SLOT)
        short = e.get('short', '')
        if not short or JP.search(short):
            errs.append('elem.name needs an English `short` form (16 px cell, 8 px font)')
        elif eng.width(short, 8) > 16 or len(eng.encode(short)) > engine.ESHORT_SLOT - 2:
            errs.append('short %r: %d px > 16 (8 px font) or over %d bytes' % (
                short, eng.width(short, 8), engine.ESHORT_SLOT - 2))
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


KEEP_JP = ROOT / 'script' / 'keep_jp.txt'


def keep_list(path=KEEP_JP):
    """{id: reason} from script/keep_jp.txt (`id<TAB>reason` per line, # comments)."""
    out = {}
    for line in path.read_text(encoding='utf-8').splitlines() if path.exists() else []:
        if line.strip() and not line.startswith('#'):
            i, _, why = line.partition('\t')
            out[i.strip()] = why.strip()
    return out


def untranslated(entries, keep):
    """Errors for entries with Japanese and no English that the keep-list does not name, and stale keep lines."""
    errs = [(e['id'], 'Japanese with no English (translate it or add it to script/keep_jp.txt with a reason)')
            for e in entries if e['jp'] and not e.get('en') and e['id'] not in keep]
    have = {e['id']: e for e in entries}
    errs += [(i, 'in script/keep_jp.txt but %s' % ('translated' if i in have else 'no such id'))
             for i in keep if i not in have or have[i].get('en')]
    return errs


def flat(en):
    """English with line/page breaks as spaces, for phrase searches across wrapped lines."""
    return re.sub(r'\s+', ' ', re.sub(r'\{(br|page)\}', ' ', en))


def glossary_check(entries, rows=None):
    """(errors, misses): an Avoid spelling of a glossary term the entry's Japanese uses is an error (any case,
    across line breaks), so re-applied review suggestions cannot undo a terminology fix; a term whose English is
    missing is only listed (paraphrase, plural, a longer term containing it)."""
    import batches
    rows = batches.glossary() if rows is None else rows
    errs, misses = [], []
    for e in entries:
        if not e.get('en'):
            continue
        en = flat(e['en'])
        for jp, ten, avoid in batches.terms_in([e['jp']], rows):
            if ten.lower() not in en.lower():
                misses.append((e['id'], jp, ten))
            for v in avoid:
                if v and re.search(r'(?i)(?<![A-Za-z])%s' % re.escape(v), en):
                    errs.append((e['id'], 'glossary: %s is %r, not %r' % (jp, ten, v)))
    return errs, misses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--terms', action='store_true', help='list entries whose glossary term English is missing')
    a = ap.parse_args()
    import textwidth
    eng = textwidth.load()
    entries = [e for es in insert.load_entries().values() for e in es]
    errors, nobudget = run(entries, eng)
    keep = keep_list()
    errors += untranslated(entries, keep)
    gerrs, misses = glossary_check(entries)
    errors += gerrs
    if a.terms:
        for i, jp, ten in misses:
            print('%s: glossary %s -> %s not used' % (i, jp, ten))
    for i, m in errors[:200]:
        print('%s: %s' % (i, m))
    done = sum(1 for e in entries if e.get('en'))
    print('lint: %d entries, %d translated, %d kept Japanese (script/keep_jp.txt), %d errors'
          % (len(entries), done, len(keep), len(errors)))
    if misses:
        print('note: %d glossary terms not used in their entry (lint --terms lists them)' % len(misses))
    if nobudget:
        print('warning: no measured budget for %s' % ', '.join('%s (%d)' % kv for kv in sorted(nobudget.items())))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
