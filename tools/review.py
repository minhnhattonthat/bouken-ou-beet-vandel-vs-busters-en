"""review.py: phase-6 review pass through codex (no subagents in Orca workers), and applying its fixes.

    python -X utf8 tools/review.py run b018 b019 ... [--jobs 6]   # -> work/tr/review/bNNN.md (+ verdict summary)
    python -X utf8 tools/review.py apply b018 ...                  # Critical/Important suggested EN -> out file, merge
    python -X utf8 tools/review.py summary                         # per batch: counts and assessment

`run` writes the pairs file work/tr/review/bNNN.pairs.txt from the batch rows and the merged English in script/.
`apply` takes each Critical/Important line `id - gist - problem - suggested EN`, puts the suggested EN into
work/tr/out/bNNN.md (the translator output) and re-merges that batch with tools/batches.py (all checks apply); lines
that fail are reported, not merged. Minor findings go to docs/polish.md (appended once per batch).
"""
import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import codex_run  # noqa: E402

REV = batches.TR / 'review'
BRIEF = ROOT / 'docs' / 'reviewer-brief.md'
SYN = ROOT / 'docs' / 'synopsis.md'
POLISH = ROOT / 'docs' / 'polish.md'


def pairs(name):
    files = batches.load_files()
    byid = {e['id']: e for f, e in batches.all_entries(files)}
    out = []
    for r in batches.read_batch(name):
        e = byid[r['id']]
        out.append('>> %s | %s | %s\nJP: %s\nEN: %s\n' % (r['id'], r['speaker'], r['kind'], r['jp'],
                                                         batches.show_jp(e.get('en', ''))))
    return '\n'.join(out), [r['jp'] for r in batches.read_batch(name)]


def run_one(name):
    REV.mkdir(parents=True, exist_ok=True)
    text, jps = pairs(name)
    (REV / ('%s.pairs.txt' % name)).write_text(text, encoding='utf-8')
    terms = batches.terms_in(jps, batches.glossary())
    t = '\n'.join('| %s | %s |' % (j, e) for j, e, _ in terms)
    prompt = (BRIEF.read_text(encoding='utf-8') + '\n## Synopsis\n\n' + SYN.read_text(encoding='utf-8') +
              '\n## Glossary terms in this batch\n\n| JP | EN |\n|---|---|\n' + t + '\n\n## Pairs (batch %s)\n\n'
              % name + text)
    out = REV / ('%s.md' % name)
    rc = codex_run.codex(prompt, out, codex_run.LOGS / ('%s.review.log' % name))
    return name, rc


SECTION = re.compile(r'^#+\s*(Critical|Important|Minor|Assessment)', re.I)
FIND = re.compile(r'^\s*[-*]?\s*`?((?:rom|quest|a9|name)\.[\w.]+)`?\s+-\s+(.*)$')


def findings(name):
    """{'Critical': [(id, text)], ...}, assessment line."""
    p = REV / ('%s.md' % name)
    res, sec, assess = {'Critical': [], 'Important': [], 'Minor': []}, None, ''
    if not p.exists():
        return None, ''
    for line in p.read_text(encoding='utf-8').splitlines():
        m = SECTION.match(line)
        if m:
            sec = m.group(1).capitalize()
            continue
        if sec == 'Assessment' and line.strip():
            assess = assess or line.strip()
            continue
        m = FIND.match(line)
        if m and sec in res:
            res[sec].append((m.group(1), m.group(2)))
    return res, assess


def suggested(text):
    """Last ` - ` separated field = suggested EN (strip quotes)."""
    parts = re.split(r'\s+-\s+', text)
    en = parts[-1].strip() if len(parts) >= 3 else ''
    en = re.sub(r'^(?:\*\*)?suggested(?: EN)?:(?:\*\*)?\s*', '', en, flags=re.I)
    if len(en) >= 2 and en[0] in '"`' and en[-1] == en[0]:
        en = en[1:-1]
    return en


def cmd_apply(a):
    bad = 0
    only = set(a.only.split(',')) if getattr(a, 'only', None) else None
    for name in a.batches:
        res, assess = findings(name)
        if res is None:
            print(name, 'no review')
            continue
        outp = batches.OUT / ('%s.md' % name)
        lines = outp.read_text(encoding='utf-8').splitlines()
        idx = {}
        for i, l in enumerate(lines):
            m = batches.LINE.match(l)
            if m:
                idx[m.group(1)] = i
        n, kept = 0, []
        byid ={e['id']: e for f, e in batches.all_entries(batches.load_files())}
        for sev in ('Critical', 'Important'):
            for i, text in res[sev]:
                if only and i not in only:
                    continue
                en = suggested(text)
                for k, v in batches.NORMALISE.items():
                    en = en.replace(k, v)
                if i in idx and i in byid and en and not batches.lint.JP.search(en):
                    errs = batches.lint.lint_entry(dict(byid[i], en=batches.finish(en, byid[i])), batches.eng())
                    if errs:
                        print('  %s: %s kept (suggestion fails: %s)' % (name, i, errs[0][:80]))
                        kept.append((i, 'review suggestion blocked by width: %s' % errs[0][:100]))
                        continue
                    lines[idx[i]] = '%s\t%s' % (i, en)
                    n += 1
                else:
                    print('  %s: no usable suggestion for %s: %s' % (name, i, text[:120]))
        if n:
            backup = batches.OUT / ('%s.pre-review.md' % name)
            if not backup.exists():
                backup.write_text(outp.read_text(encoding='utf-8'), encoding='utf-8')
            outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        rc = batches.cmd_check(argparse.Namespace(batches=[name], verbose=False), write=True)
        bad += rc
        polish_minors(name, res['Minor'] + kept)
        print('%s: %d fixes applied, merge rc %d' % (name, n, rc))
    return 1 if bad else 0


def polish_minors(name, minors):
    text = POLISH.read_text(encoding='utf-8')
    tag = '## Review minors %s' % name
    if tag in text or not minors:
        return
    add = '\n%s\n' % tag + ''.join('- [ ] %s - %s\n' % (i, t) for i, t in minors)
    POLISH.write_text(text.rstrip('\n') + '\n' + add, encoding='utf-8', newline='\n')


def cmd_summary(a):
    for p in sorted(REV.glob('b*.md')):
        res, assess = findings(p.stem)
        print('%s C%d I%d M%d  %s' % (p.stem, len(res['Critical']), len(res['Important']), len(res['Minor']),
                                      assess[:100]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('run')
    p.add_argument('batches', nargs='+')
    p.add_argument('--jobs', type=int, default=6)
    p = sp.add_parser('apply')
    p.add_argument('batches', nargs='+')
    p.add_argument('--only', help='comma-separated ids: apply just these suggestions (others may carry hand fixes)')
    sp.add_parser('summary')
    a = ap.parse_args()
    if a.cmd == 'run':
        with ThreadPoolExecutor(a.jobs) as ex:
            for name, rc in ex.map(run_one, a.batches):
                print(name, 'review rc', rc)
        return cmd_summary(a)
    if a.cmd == 'apply':
        return cmd_apply(a)
    return cmd_summary(a)


if __name__ == '__main__':
    sys.exit(main())
