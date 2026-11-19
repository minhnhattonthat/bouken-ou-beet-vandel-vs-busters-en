"""polishbatch.py: phase-9 polish pass over docs/polish.md through the phase-6 batch machinery (tools/batches.py:
every check and the merge apply). One polish batch = a range of unticked polish lines.

    python -X utf8 tools/polishbatch.py make p001 --from 14 --to 120 [--kind area.name]
        -> work/tr/batches/p001.tsv (rows) + work/tr/prompts/p001.md (codex prompt)
    python -X utf8 tools/codex_run.py raw work/tr/prompts/p001.md work/tr/out/p001.raw.md
    python -X utf8 tools/polishbatch.py fit p001
        checks each proposal alone (batches.finish + lint); keeps the passing changes in work/tr/out/p001.md and the
        batch rows for them, and writes work/tr/out/p001.res.tsv (line, id, fixed|waived, note)
    python -X utf8 tools/batches.py merge p001
    python -X utf8 tools/polishbatch.py tick p001      # ticks docs/polish.md lines from p001.res.tsv

A polish line is ticked `fixed` when at least one of its ids got new English, else `waived: <reason>` (the
reviewer's KEEP reason, or why the proposal failed the checks). docs/polish.md is Markdown, written here by line.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import lint  # noqa: E402

POLISH = ROOT / 'docs/polish.md'
ID = re.compile(r'\b((?:a9|rom|quest|name)\.[0-9A-Za-z_.]+?)(?=[\s,:;)]|$| -)')
OUTL = re.compile(r'^\s*`?((?:rom|quest|a9|name)\.[\w.]+)`?\t(.*?)\s*$')
KEEPL = re.compile(r'^\s*KEEP\t`?((?:rom|quest|a9|name)\.[\w.]+)`?\t(.*?)\s*$')

BRIEF = """# Polish pass - Bouken-ou Beet: Vandel vs. Busters (NDS), JP -> English

You fix deferred review findings and flagged cuts of a finished fan translation. Read-only: no edits, no git, no
tools. Return your answer as your final message.

Each row below: id, kind, limit (box width in px and byte cap), current width of the English in px, the JP, the
current English, and the polish note (a reviewer's minor finding, or a translator's CUT note saying what was shortened
to fit). For each row decide:
- a better English that fixes the note and FITS the limit: about 6.5 px per character on average in the 12 px font
  (i, l, ., ' are narrow ~3-4 px; m, w, M, W are wide ~10-11 px; capitals ~8 px). The current width is given, so
  compare: a fix must not be wider than the limit. Single-line kinds have no line breaks. For multi-line kinds
  (msg, brief, desc) write ` // ` for a new page; the box is re-wrapped automatically, so don't break lines yourself.
- or keep the current English, with a short reason (the full form can't fit, the note is wrong, it is fine as is).

Rules: names and terms exactly as in the glossary below (binding). Full words over abbreviations when they fit.
Keep every control code ({hero}, [FF00], {page} as ` // `, ...) the Japanese has. No suffix glued onto a variable.
Keep a character's voice. Don't widen anything past its limit.

Answer format, one line per row, nothing else:
`id<TAB>new English`   or   `KEEP<TAB>id<TAB>reason`
"""


def polish_lines():
    """[(line no, text, [ids])] of unticked lines."""
    out = []
    for i, line in enumerate(POLISH.read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('- [ ]'):
            out.append((i, line, [m.group(1).rstrip('.') for m in ID.finditer(line)]))
    return out


def flat_en(en, kind):
    b = lint.budget(kind) or {}
    if b.get('lines', 1) > 1:
        en = en.replace('{br}', ' ')
    return en.replace('{close}', '').replace('{page}', ' // ').replace('{br}', ' / ')


def cmd_make(a):
    files = batches.load_files()
    byid = {e['id']: e for f, e in batches.all_entries(files)}
    rows, seen, text = [], set(), []
    for n, line, ids in polish_lines():
        if not (a.lo <= n <= a.hi):
            continue
        for i in ids:
            e = byid.get(i)
            if not e or i in seen or not e.get('en') or batches.skipped(e):
                continue
            if a.kind and e['kind'] != a.kind:
                continue
            seen.add(i)
            rows.append(e)
            w = max((batches.measure(x) for x in re.split(r'\{br\}|\{page\}', e['en']) if x), default=0)
            text.append('- id: %s | kind: %s | limit: %s | current width: %d px\n  JP: %s\n  EN: %s\n  note: %s' % (
                i, e['kind'], batches.limit_of(e), w, batches.show_jp(e['jp']), flat_en(e['en'], e['kind']),
                line[6:].replace('\n', ' ')))
    batches.BATCH.mkdir(parents=True, exist_ok=True)
    head = 'id\tspeaker\tkind\tlimit\tjp'
    (batches.BATCH / ('%s.tsv' % a.name)).write_text(
        '\n'.join([head] + ['%s\t%s\t%s\t%s\t%s' % (e['id'], e.get('speaker', ''), e['kind'], batches.limit_of(e),
                                                    batches.show_jp(e['jp'])) for e in rows]) + '\n',
        encoding='utf-8', newline='\n')
    terms = batches.terms_in([e['jp'] for e in rows], batches.glossary())
    gl = '\n'.join('| %s | %s | %s |' % (j, en, ', '.join(v)) for j, en, v in terms)
    prompt = BRIEF + '\n## Glossary terms in these rows (JP | EN | avoid)\n\n' + gl + '\n\n## Rows\n\n' + \
        '\n'.join(text) + '\n'
    batches.PROMPT.mkdir(parents=True, exist_ok=True)
    (batches.PROMPT / ('%s.md' % a.name)).write_text(prompt, encoding='utf-8', newline='\n')
    print(a.name, len(rows), 'rows ->', batches.PROMPT / ('%s.md' % a.name))
    return 0


def cmd_fit(a):
    files = batches.load_files()
    byid = {e['id']: e for f, e in batches.all_entries(files)}
    rows = batches.read_batch(a.name) if (batches.BATCH / ('%s.tsv' % a.name)).exists() else []
    raw = (batches.OUT / ('%s.raw.md' % a.name)).read_text(encoding='utf-8').splitlines()
    want = {r['id'] for r in rows}
    props, keeps = {}, {}
    for line in raw:
        m = KEEPL.match(line)
        if m:
            keeps[m.group(1)] = m.group(2)
            continue
        m = OUTL.match(line)
        if m:
            en = m.group(2)
            for k, v in batches.NORMALISE.items():
                en = en.replace(k, v)
            props[m.group(1)] = en
    gl = batches.glossary()
    res, good = {}, {}
    for i in sorted(want):
        e = byid[i]
        if i in props:
            en = batches.finish(props[i], e)
            errs = lint.lint_entry(dict(e, en=en), batches.eng())
            if re.search(r'\}(st|nd|rd|th)\b', en):
                errs.append('ordinal suffix after a variable')
            for jp, ten, avoid in batches.terms_in([e['jp']], gl):
                for v in avoid:
                    if v and re.search(r'\b%s\b' % re.escape(v), en):
                        errs.append('avoided spelling %r' % v)
            if en == e['en']:
                res[i] = ('waived', 'kept as is after review')
            elif errs:
                res[i] = ('waived', 'fuller form %r fails the checks (%s); kept' % (props[i], errs[0]))
            else:
                good[i] = props[i]
                res[i] = ('fixed', props[i])
        elif i in keeps:
            res[i] = ('waived', keeps[i])
        else:
            res[i] = (None, 'no answer')
    batches.OUT.mkdir(parents=True, exist_ok=True)
    (batches.OUT / ('%s.md' % a.name)).write_text(''.join('%s\t%s\n' % kv for kv in sorted(good.items())),
                                                   encoding='utf-8', newline='\n')
    head = 'id\tspeaker\tkind\tlimit\tjp'
    (batches.BATCH / ('%s.tsv' % a.name)).write_text(
        '\n'.join([head] + ['\t'.join(r[k] for k in head.split('\t')) for r in rows if r['id'] in good]) + '\n',
        encoding='utf-8', newline='\n')
    (batches.OUT / ('%s.res.tsv' % a.name)).write_text(
        ''.join('%s\t%s\t%s\n' % (i, s, n.replace('\t', ' ')) for i, (s, n) in sorted(res.items()) if s),
        encoding='utf-8', newline='\n')
    c = {}
    for s, _ in res.values():
        c[s] = c.get(s, 0) + 1
    print(a.name, c, '-> merge with: python -X utf8 tools/batches.py merge', a.name)
    for i, (s, n) in sorted(res.items()):
        if s is None:
            print('  no answer:', i)
    return 0


def cmd_tick(a):
    res = {}
    for line in (batches.OUT / ('%s.res.tsv' % a.name)).read_text(encoding='utf-8').splitlines():
        i, s, n = line.split('\t', 2)
        res[i] = (s, n)
    files = batches.load_files()
    byid = {e['id']: e for f, e in batches.all_entries(files)}
    lines = POLISH.read_text(encoding='utf-8').split('\n')
    n = 0
    for k, line in enumerate(lines):
        if not line.startswith('- [ ]'):
            continue
        ids = [m.group(1).rstrip('.') for m in ID.finditer(line)]
        got = [res[i] for i in ids if i in res]
        if not got or len(got) < len([i for i in ids if i in byid]):
            continue
        fixed = [x for x in got if x[0] == 'fixed']
        if fixed:
            if any(byid[i].get('en') != batches.finish(res[i][1], byid[i]) for i in ids if res.get(i, ('',))[0] ==
                   'fixed'):
                continue   # not merged yet
            tag = 'fixed (%s): %s' % (a.name, '; '.join(x[1] for x in fixed))
        else:
            tag = 'waived (%s): %s' % (a.name, '; '.join(x[1] for x in got))
        lines[k] = '- [x]' + line[5:] + ' -- ' + tag
        n += 1
    POLISH.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print('ticked', n, 'lines')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('make')
    p.add_argument('name')
    p.add_argument('--from', dest='lo', type=int, default=0)
    p.add_argument('--to', dest='hi', type=int, default=1 << 30)
    p.add_argument('--kind')
    for c in ('fit', 'tick'):
        sub.add_parser(c).add_argument('name')
    a = ap.parse_args()
    return {'make': cmd_make, 'fit': cmd_fit, 'tick': cmd_tick}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
