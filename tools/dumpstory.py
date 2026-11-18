"""dumpstory.py: the dialogue script in file order as compact text (`id | speaker | JP`, `{br}` -> ` / `), for a
synopsis / story reader prompt. Optional EN column when translated.

    python -X utf8 tools/dumpstory.py OUT.txt [--en] [--files rom quest]
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entries(groups=('rom', 'quest')):
    for g in groups:
        for f in sorted((ROOT / 'script' / g).glob('*.json')):
            for e in json.loads(f.read_text(encoding='utf-8'))['entries']:
                e['_file'] = '%s/%s' % (g, f.stem)
                yield e


def flat(t):
    return t.replace('{br}', ' / ').replace('{page}', ' // ').replace('{close}', '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--en', action='store_true')
    ap.add_argument('--files', nargs='*', default=['rom', 'quest'])
    a = ap.parse_args()
    lines, cur = [], None
    for e in entries(a.files):
        if e['kind'] == 'speaker' or not e.get('jp'):
            continue
        if e['_file'] != cur:
            cur = e['_file']
            lines.append('=== %s' % cur)
        s = '%s | %s | %s' % (e['id'], e.get('speaker', '-'), flat(e['jp']))
        if a.en and e.get('en'):
            s += '\n    EN: ' + flat(e['en'])
        lines.append(s)
    Path(a.out).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(len(lines), 'lines ->', a.out)


if __name__ == '__main__':
    main()
