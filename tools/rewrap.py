"""rewrap.py: re-fit the English of one kind to its box after a budget change.

    python -X utf8 tools/rewrap.py KIND [--write]

For every entry of KIND (in script/**/*.json) whose `en` has a line wider than the kind's budget (tools/budgets.json)
or more lines than it allows, joins its `{br}` lines and wraps the text again with batches.wrap(). Prints each change
(old -> new); `--write` saves the files (batches.save, the same format as extract/merge). An entry whose re-wrap
still does not fit (more lines than the box, or a {page}) is printed as LEFT and not changed: fix it by hand.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import lint  # noqa: E402


def fits(en, kind):
    b = lint.budget(kind) or {}
    lines = en.split('{br}')
    if '{page}' in en or len(lines) > b.get('lines', 1):
        return False
    return all(batches.measure(line) <= b['px'] for line in lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kind')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    if 'px' not in (lint.budget(a.kind) or {}):
        sys.exit(f'no px budget for kind {a.kind}')
    changed = left = 0
    for f in sorted((ROOT / 'script').rglob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        entries = d.get('entries') if isinstance(d, dict) else None
        if not entries:
            continue
        dirty = False
        for e in entries:
            if e.get('kind') != a.kind or not e.get('en') or fits(e['en'], a.kind):
                continue
            new = batches.wrap(e['en'].replace('{br}', ' '), a.kind)
            if not fits(new, a.kind):
                print(f"LEFT {e['id']}: {e['en']!r} -> {new!r}")
                left += 1
                continue
            print(f"{e['id']}: {e['en']!r} -> {new!r}")
            e['en'] = new
            dirty = True
            changed += 1
        if dirty and a.write:
            batches.save(f, d)
    print(f'rewrap {a.kind}: {changed} re-wrapped, {left} left{"" if a.write else " (dry run)"}')
    return 1 if left else 0


if __name__ == '__main__':
    sys.exit(main())
