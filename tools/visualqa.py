"""visualqa.py: visual-QA verdicts through `codex exec` (Orca workers may not start reviewer subagents).

    python -X utf8 tools/visualqa.py work/qa/chunks/chunk_1_001.txt [...] [--verdicts work/qa/verdicts]
                                    [--jp work/qa/tour_jp] [--en work/qa/en] [--jobs 3]

Each chunk file (from `qa_gate.py todo ... --out-dir work/qa/chunks`) is one read-only codex run: the prompt is
docs/visual-qa-brief.md plus the id list, every sheet is attached with `-i` (the original ROM's sheet of the same
id right after it, when --jp has one), and codex's final message (`id<TAB>verdict<TAB>note` lines) is parsed into
<verdicts>/<chunk stem>.tsv. Ids codex left out are reported and get no line, so `qa_gate.py todo` lists them again.
Logs: work/qa/vqa_logs/<chunk>.log. Exit 1 if any chunk failed or missed ids.
"""
import argparse
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / 'docs' / 'visual-qa-brief.md'
LOGS = ROOT / 'work' / 'qa' / 'vqa_logs'
VERDICTS = ('ok', 'issue', 'fixed')


def read_chunk(path):
    rows = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if line.strip():
            i, _, p = line.partition('\t')
            rows.append((i.strip(), Path(p.strip())))
    return rows


def jp_twin(path, en_dir, jp_dir):
    """The original ROM's sheet for the same scene: same path relative to the English tour dir."""
    if not jp_dir:
        return None
    try:
        rel = Path(path).resolve().relative_to(Path(en_dir).resolve())
    except ValueError:
        return None
    twin = Path(jp_dir) / rel
    return twin if twin.exists() else None


def parse(text, ids):
    """{id: (verdict, note)} from codex's lines; accepts tab or ' | ' separators and stray markdown."""
    out = {}
    for line in text.splitlines():
        line = line.strip().lstrip('-* ').strip().strip('`').strip()
        parts = [p.strip() for p in (line.split('\t') if '\t' in line else re.split(r'\s+\|\s+', line))]
        if len(parts) >= 2 and parts[0] in ids and parts[1].lower() in VERDICTS:
            out[parts[0]] = (parts[1].lower(), ' '.join(' '.join(parts[2:]).split()))
    return out


def run_chunk(chunk, verdict_dir, en_dir, jp_dir):
    rows = read_chunk(chunk)
    ids = [i for i, _ in rows]
    images, listing = [], []
    for i, p in rows:
        images.append(p)
        listing.append('%s\t%s' % (i, p.as_posix()))
        twin = jp_twin(p, en_dir, jp_dir)
        if twin:
            images.append(twin)
            listing.append('(JP original of %s)\t%s' % (i, twin.as_posix()))
    prompt = (BRIEF.read_text(encoding='utf-8') + '\n## Sheets (attached in this order)\n' + '\n'.join(listing)
              + '\n\nGive exactly one verdict line for each of these ids: ' + ', '.join(ids) + '\n')
    stem = Path(chunk).stem
    out = LOGS / ('%s.out.txt' % stem)
    LOGS.mkdir(parents=True, exist_ok=True)
    cmd = [shutil.which('codex'), 'exec', '-s', 'read-only', '--skip-git-repo-check', '-o', str(out)]
    for im in images:
        cmd += ['-i', str(im)]
    cmd.append('-')
    with open(LOGS / ('%s.log' % stem), 'w', encoding='utf-8') as lf:
        rc = subprocess.run(cmd, input=prompt.encode('utf-8'), stdout=lf, stderr=subprocess.STDOUT, cwd=str(ROOT),
                            timeout=3600).returncode
    got = parse(out.read_text(encoding='utf-8'), set(ids)) if out.exists() else {}
    if got:
        Path(verdict_dir).mkdir(parents=True, exist_ok=True)
        (Path(verdict_dir) / ('%s.tsv' % stem)).write_text(
            ''.join('%s\t%s\t%s\n' % (i, *got[i]) for i in ids if i in got), encoding='utf-8')
    missing = [i for i in ids if i not in got]
    issues = [(i, got[i][1]) for i in ids if i in got and got[i][0] == 'issue']
    return stem, rc, len(got), missing, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('chunks', nargs='+')
    ap.add_argument('--verdicts', default=str(ROOT / 'work' / 'qa' / 'verdicts'))
    ap.add_argument('--en', default=str(ROOT / 'work' / 'qa' / 'en'), help='English tour dir (to find JP twins)')
    ap.add_argument('--jp', default=str(ROOT / 'work' / 'qa' / 'tour_jp'), help='original ROM tour dir')
    ap.add_argument('--jobs', type=int, default=3)
    a = ap.parse_args()
    bad = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for stem, rc, n, missing, issues in ex.map(lambda c: run_chunk(c, a.verdicts, a.en, a.jp), a.chunks):
            print('%s: rc %d, %d verdicts, %d issues%s' % (stem, rc, n, len(issues),
                                                          ', MISSING ' + ' '.join(missing) if missing else ''))
            for i, note in issues:
                print('  ISSUE %s: %s' % (i, note))
            bad += bool(rc or missing)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
