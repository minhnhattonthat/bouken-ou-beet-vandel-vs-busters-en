"""storyminors.py: append the Minor findings of the story-pass reports (work/qa/story/reports/<ch>.md) to
docs/polish.md as unticked lines, one `## Story pass minors <ch>` section per chapter, added once (a chapter whose
section exists is skipped). Never rewrites existing lines.

    python -X utf8 tools/storyminors.py [CHAPTER ...]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLISH = ROOT / 'docs/polish.md'
REPORTS = ROOT / 'work/qa/story/reports'


def minors(text):
    m = re.search(r'#+\s*Minor[^\n]*\n(.*?)(?=\n#+\s|\Z)', text, re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith(('- ', '* ')) and len(line) > 4:
            out.append(re.sub(r'\s+', ' ', line[2:]).strip())
    return out


def main():
    chs = sys.argv[1:] or sorted(p.stem for p in REPORTS.glob('*.md'))
    pol = POLISH.read_text(encoding='utf-8')
    add, n = [], 0
    for ch in chs:
        head = '## Story pass minors %s' % ch
        if head in pol:
            continue
        ms = minors((REPORTS / (ch + '.md')).read_text(encoding='utf-8'))
        if not ms or ms == ['None.']:
            continue
        add.append('\n' + head + '\n' + '\n'.join('- [ ] ' + x for x in ms if x.lower() != 'none.'))
        n += len(ms)
    if add:
        POLISH.write_text(pol.rstrip('\n') + '\n' + '\n'.join(add) + '\n', encoding='utf-8', newline='\n')
    print('added', n, 'minor lines from', len(add), 'chapters')


if __name__ == '__main__':
    main()
