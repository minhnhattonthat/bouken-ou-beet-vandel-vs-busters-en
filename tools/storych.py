"""storych.py: story-pass chapter files (`>> id | speaker | JP` / `EN`, story order = file order) for the phase-9
story reviewers, one file per script file (docs/synopsis.md "Reading order and file grouping"). Files larger than
--max chars are split into parts at entry boundaries, so one reviewer reads one part.

    python -X utf8 tools/storych.py [--out work/qa/story/chapters] [--max 60000]

Then: qa_gate.py init work/qa/story/manifest.tsv work/qa/story/chapters --glob "*.txt"
Regenerate after every script edit and before the release gate.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def flat(t):
    if t.endswith('{close}'):
        t = t[:-7]
    return t.replace('{br}', ' / ').replace('{page}', ' // ').replace('{close}', ' {close} ')


def blocks(path):
    """One text block per shown entry of a script file."""
    for e in json.loads(path.read_text(encoding='utf-8'))['entries']:
        if e.get('kind') == 'speaker' or not e.get('jp'):
            continue
        spk = e.get('speaker') or '-'
        yield '>> %s | %s | %s\n   EN: %s\n' % (e['id'], spk, flat(e['jp']), flat(e.get('en') or '(untranslated)'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(ROOT / 'work/qa/story/chapters'))
    ap.add_argument('--max', type=int, default=60000)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    want = set()
    for g in ('rom', 'quest'):
        for f in sorted((ROOT / 'script' / g).glob('*.json')):
            parts, cur = [], ''
            for b in blocks(f):
                if cur and len(cur) + len(b) > a.max:
                    parts.append(cur)
                    cur = ''
                cur += b
            if cur:
                parts.append(cur)
            for i, p in enumerate(parts):
                name = '%s_%s%s.txt' % (g, f.stem, '' if len(parts) == 1 else '_p%d' % (i + 1))
                head = '# Chapter file %s (script/%s/%s, part %d of %d)\n\n' % (
                    name[:-4], g, f.name, i + 1, len(parts))
                want.add(name)
                dst = out / name
                text = head + p
                if not dst.exists() or dst.read_text(encoding='utf-8') != text:
                    dst.write_text(text, encoding='utf-8')
    for old in out.glob('*.txt'):
        if old.name not in want:
            old.unlink()
    print(len(want), 'chapter files ->', out)


if __name__ == '__main__':
    main()
