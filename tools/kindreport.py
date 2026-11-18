"""kindreport.py: per entry kind, how many marker ids a tour saw and where (from markerscan.py's <scan>_ids.tsv).

    python -X utf8 tools/kindreport.py work/qa/marker/scan_ids.tsv
Columns: kind, entries, seen, sites (font/lr), x range, y values, example scenes.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import insert  # noqa: E402


def main():
    ents = insert.load_entries()
    kind_of, total = {}, defaultdict(int)
    for lst in ents.values():
        for e in lst:
            k = e['kind']
            kind_of[insert.short_id(e)] = k
            total[k] += 1
    seen = defaultdict(list)
    for row in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='\t'):
        k = kind_of.get(row['id'])
        if k:
            seen[k].append(row)
    for k in sorted(total):
        rows = seen.get(k, [])
        sites = sorted({'%s/%s' % (r['font'], r['lr'][-4:]) for r in rows})
        xs = [int(r['x']) for r in rows]
        print('%-16s %5d %5d  %-22s x %s  y %s  %s' % (
            k, total[k], len(rows), ','.join(sites), '%d-%d' % (min(xs), max(xs)) if xs else '-',
            ','.join(sorted({r['y'] for r in rows}))[:20], ' '.join(sorted({r['scene'] for r in rows}))[:40]))


if __name__ == '__main__':
    main()
