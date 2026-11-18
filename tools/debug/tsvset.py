"""Set cells in tools/debug/scenes.tsv without losing empty columns (hand edits of TSVs dropped tabs).

    python tools/debug/tsvset.py tools/debug/scenes.tsv NAME COL VALUE [NAME COL VALUE ...]
    python tools/debug/tsvset.py tools/debug/scenes.tsv --where-col COL=OLD --set COL=NEW   (event rows only)

Keeps comment lines, asserts every row's column count."""
import sys
path = sys.argv[1]
lines = open(path, encoding='utf-8', newline='').read().split('\n')
head = None
out = []
args = sys.argv[2:]
bulk = None
if args and args[0] == '--where-col':
    wc, wv = args[1].split('=', 1); sc, sv = args[3].split('=', 1); bulk = (wc, wv, sc, sv)
    args = []
sets = [(args[i], args[i + 1], args[i + 2]) for i in range(0, len(args), 3)]
for ln in lines:
    if ln == '' or ln.startswith('#'):
        out.append(ln); continue
    r = ln.split('\t')
    if head is None:
        head = r; out.append(ln); continue
    assert len(r) == len(head), r
    d = dict(zip(head, r))
    for n, c, v in sets:
        if d['name'] == n:
            d[c] = v
    if bulk and d[bulk[0]] == bulk[1] and d['kind'] == 'event':
        d[bulk[2]] = bulk[3]
    out.append('\t'.join(d[h] for h in head))
open(path, 'w', encoding='utf-8', newline='').write('\n'.join(out))
