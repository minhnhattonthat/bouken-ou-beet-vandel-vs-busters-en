"""mkpolish.py: append translators' `CUT:` report lines (work/tr/out/b*.md) to docs/polish.md as unticked lines,
skipping ids already listed there. Never rewrites existing lines (ticks and review sections stay).

    python -X utf8 tools/mkpolish.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLISH = ROOT / 'docs' / 'polish.md'


def main():
    text = POLISH.read_text(encoding='utf-8')
    have = set(re.findall(r'^- \[[ x]\] (\S+) - CUT', text, re.M))
    new = []
    for f in sorted((ROOT / 'work' / 'tr' / 'out').glob('b*.md')):
        if '.pre-review' in f.name:
            continue
        for line in f.read_text(encoding='utf-8').splitlines():
            m = re.match(r'CUT:\s*(\S+)\s*-\s*(.*)', line)
            if m and m.group(1) not in have:
                have.add(m.group(1))
                new.append('- [ ] %s - CUT (%s): %s' % (m.group(1), f.stem, m.group(2).strip()))
    if new:
        POLISH.write_text(text.rstrip('\n') + '\n\n## Flagged cuts (added)\n' + '\n'.join(new) + '\n',
                          encoding='utf-8', newline='\n')
    print(len(new), 'new CUT lines')


if __name__ == '__main__':
    main()
