"""storyreview.py: phase-9 story pass through `codex exec` (read-only), one reviewer per chapter file, for sessions
without subagents. The prompt inlines docs/story-reviewer-brief.md, docs/synopsis.md, glossary.md and the chapter
(the codex sandbox can't run processes to read files itself).

    python -X utf8 tools/storyreview.py [CHAPTER ...] [--jobs 4] [--tag r1] [--fixed]

No CHAPTER = every chapter without a current verdict (qa_gate todo). Report -> work/qa/story/reports/<ch>.md, verdict
-> work/qa/story/verdicts/<ch>[_<tag>].tsv ("ch<TAB>ok|issue<TAB>note", from the report's Assessment). --fixed writes
"fixed" for an ok re-review of a chapter whose earlier verdict was issue.
Logs: work/qa/story/logs/.
"""
import argparse
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402

STORY = ROOT / 'work/qa/story'
MANIFEST = STORY / 'manifest.tsv'


def todo():
    p = subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/qa_gate.py'), 'todo', str(MANIFEST),
                        str(STORY / 'verdicts'), '--size', '1'], capture_output=True, text=True, encoding='utf-8')
    out = []
    for line in p.stdout.splitlines():
        m = re.match(r'^\s*([A-Za-z0-9_]+)\t', line)
        if m:
            out.append(m.group(1))
    return out


def prompt(ch):
    parts = [(ROOT / 'docs/story-reviewer-brief.md').read_text(encoding='utf-8'),
             '\n\n---\n# docs/synopsis.md\n\n' + (ROOT / 'docs/synopsis.md').read_text(encoding='utf-8'),
             '\n\n---\n# glossary.md\n\n' + (ROOT / 'glossary.md').read_text(encoding='utf-8'),
             '\n\n---\n# The chapter\n\n' + (STORY / 'chapters' / (ch + '.txt')).read_text(encoding='utf-8'),
             '\n\n---\nNow write the report described in the brief, as your final message.\n']
    return ''.join(parts)


def assessment(report):
    m = re.search(r'#+\s*Assessment\s*\n+(.*)', report)
    if not m:
        return None, ''
    line = m.group(1).strip().strip('`*').strip()
    w = re.match(r'`?\*?\s*(ok|issue)\b', line, re.I)
    if not w:
        return None, line
    note = re.sub(r'^`?\*?\s*(ok|issue)`?\*?\s*[-:–—]?\s*', '', line, flags=re.I)
    return w.group(1).lower(), note.replace('\t', ' ')[:300]


def run(ch, tag, fixed):
    exe = shutil.which('codex')
    rep = STORY / 'reports' / (ch + '.md')
    log = STORY / 'logs' / (ch + '.log')
    rep.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    if rep.exists():
        rep.unlink()
    with open(log, 'w', encoding='utf-8') as lf:
        p = subprocess.run([exe, 'exec', '-s', 'read-only', '--skip-git-repo-check', '-o', str(rep), '-'],
                           input=prompt(ch).encode('utf-8'), stdout=lf, stderr=subprocess.STDOUT,
                           cwd=str(STORY), timeout=3600)
    if p.returncode or not rep.exists():
        return ch, 'codex exit %d' % p.returncode
    word, note = assessment(rep.read_text(encoding='utf-8'))
    if word is None:
        return ch, 'no Assessment word: %s' % note[:80]
    if word == 'ok' and fixed:
        word = 'fixed'
    vd = STORY / 'verdicts'
    vd.mkdir(parents=True, exist_ok=True)
    (vd / ('%s%s.tsv' % (ch, '_' + tag if tag else ''))).write_text('%s\t%s\t%s\n' % (ch, word, note),
                                                                     encoding='utf-8')
    return ch, word + ' - ' + note[:100]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('chapters', nargs='*')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--tag', default='')
    ap.add_argument('--fixed', action='store_true')
    a = ap.parse_args()
    chs = a.chapters or todo()
    print(len(chs), 'chapters:', ' '.join(chs), flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        for ch, res in ex.map(lambda c: run(c, a.tag, a.fixed), chs):
            print(ch, res, flush=True)


if __name__ == '__main__':
    main()
