"""batches.py: phase-6 translation batches: split untranslated text into batch files, build translator prompts,
check translator output and merge it into script/*.json.

    python -X utf8 tools/batches.py split --wave tables|dialogue [--size 120 --chars 3500]
    python -X utf8 tools/batches.py prompt b001 [--brief docs/translator-brief.md]   # -> work/tr/prompts/b001.md
    python -X utf8 tools/batches.py check b001 [b002 ...]   # validate work/tr/out/bNNN.md, no writes
    python -X utf8 tools/batches.py merge b001 [b002 ...]   # check, then write passing batches into script/
    python -X utf8 tools/batches.py wrap "text // text" [--kind msg]   # dry-run the wrapper
    python -X utf8 tools/batches.py status

Batch rows (work/tr/batches/bNNN.tsv): id, speaker, kind, limit, jp. One row per distinct (kind, jp): the merge
writes the English to every entry with that kind and jp. JP `{br}` shows as ` / `, `{page}` as ` // `, a final
`{close}` is dropped and re-added. Translator output (work/tr/out/bNNN.md): lines `id<TAB>English`; other lines
(NEW TERM:, UNSURE:, CUT:) are kept as the report. In English, ` // ` forces a new page, ` / ` a new line; the
wrapper (`wrap()`) flows everything else into the box from tools/budgets.json (multi-line kinds only).
Readings (sort keys) are filled from their table's name; 説明 placeholders and KEEP_KINDS are skipped.
"""
import argparse
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402
import lint  # noqa: E402

SCRIPT = ROOT / 'script'
TR = ROOT / 'work' / 'tr'
BATCH, OUT, PROMPT = TR / 'batches', TR / 'out', TR / 'prompts'
GLOSSARY = ROOT / 'glossary.md'
CTRL = insert.CTRL
DIALOGUE = ('msg', 'desc', 'ptr.msg', 'quest', 'title')   # 'dialogue' wave; everything else is 'tables'
SKIP_JP = ('説明',)
DEFER_KINDS = ('elem.name',)   # 18 px canvas: translate after the draw code is widened (phase 7)
_ENG = None


def eng():
    global _ENG
    if _ENG is None:
        import textwidth
        _ENG = textwidth.load()
    return _ENG


# ---------------------------------------------------------------- script files

def load_files():
    """OrderedDict {path: data} of every script JSON, in sorted path order."""
    out = OrderedDict()
    for f in sorted(SCRIPT.rglob('*.json')):
        out[f] = json.loads(f.read_text(encoding='utf-8'))
    return out


def all_entries(files):
    for f, d in files.items():
        for e in d['entries']:
            yield f, e


def save(f, d):
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')


def is_reading(e):
    return e['kind'].endswith('.reading')


def skipped(e):
    return (not e.get('jp') or e['kind'] in insert.KEEP_KINDS or e['kind'] in DEFER_KINDS or is_reading(e)
            or e['jp'] in SKIP_JP)


def wave_of(kind):
    return 'dialogue' if kind in DIALOGUE else 'tables'


# ---------------------------------------------------------------- layout

def show_jp(jp):
    if jp.endswith('{close}') and jp.count('{close}') == 1:
        jp = jp[:-7]
    return jp.replace('{page}', ' // ').replace('{br}', ' / ')


def limit_of(e):
    b = lint.budget(e['kind'])
    parts = []
    if b and 'px' in b:
        per = b['px'] / (6.5 if b['font'] == 12 else 5.0)
        if b.get('lines', 1) > 1:
            parts.append('auto-wrap, %d lines x ~%d chars per page' % (b['lines'], per))
        else:
            parts.append('%dpx ~%dch' % (b['px'], per))
    if 'max' in e:
        parts.append('max %d bytes' % insert.text_cap(e))
    return ' '.join(parts) or 'free'


def measure(s):
    for k, v in lint.VARS.items():
        s = s.replace(k, v)
    return eng().width(CTRL.sub('', s), 12)


def wrap(text, kind):
    """English with ` // ` pages and ` / ` forced lines -> `{br}`/`{page}` text fitted to the kind's box."""
    b = lint.budget(kind) or {}
    nlines = b.get('lines', 1)
    text = text.strip()
    if nlines == 1 or 'px' not in b:
        return text.replace(' // ', ' ').replace(' / ', ' ')
    px, last = b['px'], b.get('last_px', b['px'])
    pages = []
    for page in re.split(r'\s*//\s*', text):
        lines = []
        for forced in re.split(r'\s+/\s+', page):
            cur = ''
            for w in forced.split():
                cand = (cur + ' ' + w) if cur else w
                lim = last if len(lines) % nlines == nlines - 1 else px
                if cur and measure(cand) > lim:
                    lines.append(cur)
                    cur = w
                else:
                    cur = cand
            lines.append(cur)
        for i in range(0, len(lines), nlines):
            pages.append('{br}'.join(lines[i:i + nlines]))
    return '{page}'.join(pages)


def finish(en, e):
    en = wrap(en, e['kind'])
    jp = e['jp']
    if jp.endswith('{close}') and jp.count('{close}') == 1 and not en.endswith('{close}'):
        en += '{close}'
    return en


# ---------------------------------------------------------------- glossary

def glossary():
    """[(jp, en, avoid)] from the tables in glossary.md (rows | JP | EN | max | notes | Avoid |)."""
    return glossary_rows(GLOSSARY.read_text(encoding='utf-8'))


def glossary_rows(text):
    rows = []
    for line in text.splitlines():
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if len(c) >= 2 and line.startswith('|') and lint.JP.search(c[0]) and c[1] and not c[1].startswith('-'):
            avoid = [a.strip() for a in c[4].split(',')] if len(c) > 4 and c[4] else []
            for jp in c[0].split('/'):
                rows.append((jp.strip(), c[1], avoid))
    return rows


RUN = re.compile(r'[ァ-ヴー]+|[぀-ゟ]+|[一-鿿々]+|[Ａ-Ｚａ-ｚ０-９]+')


def terms_in(jps, rows):
    """Glossary rows whose JP occurs in the texts; katakana terms only on whole katakana runs."""
    hits = []
    for jp, en, avoid in rows:
        for t in jps:
            if jp not in t:
                continue
            if re.fullmatch(r'[ァ-ヴー・]+', jp) and not any(r == jp or r.startswith(jp) and jp + 'ー' != r
                                                              for r in RUN.findall(t)):
                continue
            hits.append((jp, en, avoid))
            break
    return hits


# ---------------------------------------------------------------- split / prompt

def pending(files, wave):
    """[(key, first entry)] of untranslated distinct (kind, jp) in file order."""
    seen, out = set(), []
    for f, e in all_entries(files):
        if skipped(e) or wave_of(e['kind']) != wave:
            continue
        key = (e['kind'], e['jp'])
        if key in seen:
            continue
        seen.add(key)
        if not e.get('en'):
            out.append((key, e))
    return out


def cmd_split(a):
    files = load_files()
    BATCH.mkdir(parents=True, exist_ok=True)
    rows = pending(files, a.wave)
    if not rows:
        print('nothing pending')
        return 0
    existing = sorted(BATCH.glob('b*.tsv'))
    n = int(existing[-1].stem[1:]) + 1 if existing else 1
    queued = set()
    for f in existing:
        for line in f.read_text(encoding='utf-8').splitlines()[1:]:
            queued.add(line.split('\t')[0])
    rows = [r for r in rows if r[1]['id'] not in queued]
    batches, cur, chars = [], [], 0
    for key, e in rows:
        cur.append(e)
        chars += len(e['jp'])
        if len(cur) >= a.size or chars >= a.chars:
            batches.append(cur)
            cur, chars = [], 0
    if cur:
        batches.append(cur)
    for b in batches:
        name = 'b%03d' % n
        path = BATCH / ('%s.tsv' % name)
        assert not path.exists()
        lines = ['id\tspeaker\tkind\tlimit\tjp']
        for e in b:
            lines.append('\t'.join([e['id'], e.get('speaker', '-').replace('\t', ' '), e['kind'], limit_of(e),
                                    show_jp(e['jp'])]))
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
        print('%s: %d rows, %d jp chars' % (name, len(b), sum(len(e['jp']) for e in b)))
        n += 1
    return 0


def read_batch(name):
    lines = (BATCH / ('%s.tsv' % name)).read_text(encoding='utf-8').splitlines()
    head = lines[0].split('\t')
    return [dict(zip(head, ln.split('\t'))) for ln in lines[1:] if ln]


def cmd_prompt(a):
    PROMPT.mkdir(parents=True, exist_ok=True)
    brief = (ROOT / a.brief).read_text(encoding='utf-8')
    extra = [(ROOT / p).read_text(encoding='utf-8') for p in a.include]
    for name in a.batches:
        rows = read_batch(name)
        terms = terms_in([r['jp'] for r in rows], glossary())
        t = ['| JP | EN | Avoid |', '|---|---|---|'] + ['| %s | %s | %s |' % (j, e, ', '.join(v)) for j, e, v in terms]
        text = brief + '\n' + '\n'.join(extra) + '\n## Glossary terms in this batch (binding)\n\n' + '\n'.join(t)
        text += '\n\n## Batch %s (id, speaker, kind, limit, jp)\n\n' % name
        text += (BATCH / ('%s.tsv' % name)).read_text(encoding='utf-8')
        (PROMPT / ('%s.md' % name)).write_text(text, encoding='utf-8', newline='\n')
        print(name, len(rows), 'rows,', len(terms), 'terms ->', PROMPT / ('%s.md' % name))
    return 0


# ---------------------------------------------------------------- check / merge

NORMALISE = {'’': "'", '‘': "'", '“': '"', '”': '"', '—': '--', '–': '-',
             ' ': ' ', '　': ' '}
LINE = re.compile(r'^\s*`?((?:rom|quest|a9|name)\.[\w.]+)`?\s*(?:\t|\s\|\s)\s*(.*?)\s*$')


def read_out(name):
    """({id: en}, duplicates, report lines)."""
    p = OUT / ('%s.md' % name)
    got, dups, report = {}, [], []
    if not p.exists():
        return None, [], []
    for line in p.read_text(encoding='utf-8').splitlines():
        m = LINE.match(line)
        if m:
            en = m.group(2)
            for k, v in NORMALISE.items():
                en = en.replace(k, v)
            if m.group(1) in got:
                dups.append(m.group(1))
            got[m.group(1)] = en
        elif re.match(r'\s*(NEW TERM|UNSURE|CUT)', line):
            report.append(line.strip())
    return got, dups, report


def check_batch(name, byid, gl):
    """(errors, warnings, {id: final en})."""
    rows = read_batch(name)
    got, dups, _ = read_out(name)
    if got is None:
        return ['no output file'], [], {}
    errs, warns, final = [], [], {}
    want = [r['id'] for r in rows]
    missing = [i for i in want if i not in got]
    extra = [i for i in got if i not in set(want)]
    if missing:
        errs.append('missing ids: %s' % ' '.join(missing))
    if extra:
        errs.append('extra ids: %s' % ' '.join(extra))
    if dups:
        errs.append('duplicate ids: %s' % ' '.join(dups))
    for i in want:
        if i not in got:
            continue
        e = byid[i]
        raw = got[i]
        if not raw.strip():
            errs.append('%s: empty' % i)
            continue
        if '\t' in raw or '\\u' in raw or '\\n' in raw:
            errs.append('%s: tab or escape in text' % i)
        en = finish(raw, e)
        test = dict(e, en=en)
        for m in lint.lint_entry(test, eng()):
            errs.append('%s: %s' % (i, m))
        if re.search(r'\}(st|nd|rd|th)\b', en):
            errs.append('%s: ordinal suffix after a variable' % i)
        for jp, ten, avoid in terms_in([e['jp']], gl):
            if ten.lower() not in en.lower():
                warns.append('%s: glossary %s -> %s not used' % (i, jp, ten))
            for v in avoid:
                if v and re.search(r'\b%s\b' % re.escape(v), en):
                    errs.append('%s: avoided spelling %r' % (i, v))
        final[i] = en
    return errs, warns, final


def apply(files, final):
    """Write each id's English to every entry with the same (kind, jp); then refill readings."""
    keys = {}
    for f, e in all_entries(files):
        if e['id'] in final:
            keys[(e['kind'], e['jp'])] = final[e['id']]
    touched = set()
    for f, e in all_entries(files):
        k = (e['kind'], e['jp'])
        if k in keys and not skipped(e):
            e['en'] = keys[k]
            touched.add(f)
    touched |= fill_readings(files)
    for f in touched:
        save(f, files[f])
    return len(keys)


def fill_readings(files):
    """`<table>.<n>.reading` = the English of `<table>.<n>.name`, cut to the slot cap."""
    touched = set()
    for f, d in files.items():
        names = {e['id']: e for e in d['entries']}
        for e in d['entries']:
            if not is_reading(e) or not e.get('jp'):
                continue
            src = names.get(e['id'][:-len('reading')] + 'name')
            if not src or not src.get('en'):
                continue
            en = src['en']
            while len(eng().encode(en)) > insert.text_cap(e):
                en = en[:-1].rstrip()
            if e.get('en') != en:
                e['en'] = en
                touched.add(f)
    return touched


def cmd_check(a, write=False):
    files = load_files()
    byid = {e['id']: e for f, e in all_entries(files)}
    gl = glossary()
    bad, allfinal = [], {}
    for name in a.batches:
        errs, warns, final = check_batch(name, byid, gl)
        _, _, report = read_out(name)
        for w in warns if a.verbose else []:
            print('  warn', w)
        for x in errs[:40]:
            print('  ERR', x)
        print('%s: %s (%d errors, %d warnings, %d report lines)' % (name, 'FAIL' if errs else 'OK', len(errs),
                                                                    len(warns), len(report)))
        if errs:
            bad.append(name)
        else:
            allfinal.update(final)
    if write and allfinal:
        print('merged', apply(files, allfinal), 'distinct strings')
    return 1 if bad else 0


def cmd_wrap(a):
    e = {'kind': a.kind, 'jp': ''}
    for t in a.text:
        out = finish(t, e)
        print(out)
        for pg in lint.pages(out):
            for ln in pg:
                print('  %3d px  %s' % (measure(ln), ln))
            print('  --')
    return 0


def cmd_status(a):
    files = load_files()
    c, d = Counter(), Counter()
    for f, e in all_entries(files):
        if skipped(e):
            continue
        c[wave_of(e['kind'])] += 1
        d[wave_of(e['kind'])] += bool(e.get('en'))
    for w in c:
        print('%-9s %5d / %5d translated' % (w, d[w], c[w]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('split')
    p.add_argument('--wave', choices=('tables', 'dialogue'), required=True)
    p.add_argument('--size', type=int, default=120)
    p.add_argument('--chars', type=int, default=3500)
    p = sp.add_parser('prompt')
    p.add_argument('batches', nargs='+')
    p.add_argument('--brief', default='docs/translator-brief.md')
    p.add_argument('--include', nargs='*', default=[])
    for c in ('check', 'merge'):
        p = sp.add_parser(c)
        p.add_argument('batches', nargs='+')
        p.add_argument('-v', '--verbose', action='store_true')
    p = sp.add_parser('wrap')
    p.add_argument('text', nargs='+')
    p.add_argument('--kind', default='msg')
    sp.add_parser('status')
    a = ap.parse_args()
    if a.cmd == 'split':
        return cmd_split(a)
    if a.cmd == 'prompt':
        return cmd_prompt(a)
    if a.cmd == 'check':
        return cmd_check(a)
    if a.cmd == 'merge':
        return cmd_check(a, write=True)
    if a.cmd == 'wrap':
        return cmd_wrap(a)
    return cmd_status(a)


if __name__ == '__main__':
    sys.exit(main())
