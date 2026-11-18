import re
from pathlib import Path
lines = []
FIXED = {'rom.063E0', 'rom.06AC8', 'rom.0D3EC', 'rom.19F6C', 'rom.30C54'}
for f in sorted(Path('work/tr/out').glob('b*.md')):
    for l in f.read_text(encoding='utf-8').splitlines():
        m = re.match(r'CUT:\s*(\S+)\s*-\s*(.*)', l)
        if m and m.group(1) in FIXED:
            lines.append('- [x] %s - CUT (%s): %s - fixed: full form fits the 80 px tag' % (m.group(1), f.stem,
                                                                                        m.group(2).strip()))
        elif m:
            lines.append('- [ ] %s - CUT (%s): %s' % (m.group(1), f.stem, m.group(2).strip()))
head = """# Polish

Minor findings and flagged cuts, fixed in one pass before release (`references/translation.md` §Review). Tick each
line `[x]` with `fixed` or `waived: reason`; the release script refuses to run while a line is unticked.

## General
- [ ] speaker tag: Resistance A-L show as "Resist. A" and 橋かけ名人 as "Master" (87/89 px > 80 px measured tag);
  widen the tag (90 px was not drawn: find the canvas width in the draw code) or keep, then waive.
- [ ] jp-bound budgets (area/area2 names, key items, tengeki/meigeki, skills, titles): measure each box in phase 8 and
  undo the cuts below that the real box allows (full area names: Mountains, Volcano, Snowfield ...).
- [ ] weapon descriptions "1H"/"2H": rephrase to full words within 194 px.

## Flagged cuts from translation batches
"""
Path('docs/polish.md').write_text(head + '\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
print(len(lines))
