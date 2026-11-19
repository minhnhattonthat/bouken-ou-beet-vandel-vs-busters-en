"""codex_run.py: run translator / reviewer prompts through `codex exec` (read-only sandbox, prompt on stdin) in
parallel, for sessions without subagents (Orca workers). Translator mode checks each output with
tools/batches.py and sends failures back with the errors for up to --rounds fix rounds.

    python -X utf8 tools/codex_run.py translate b001 b002 ... [--jobs 6 --rounds 2]
    python -X utf8 tools/codex_run.py raw PROMPT.md OUT.md      # one prompt file -> final message

Outputs: work/tr/out/bNNN.md (final message), logs in work/tr/logs/. Existing outputs that pass are skipped.
"""
import argparse
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402

LOGS = batches.TR / 'logs'


def codex(prompt_text, out, log):
    """Run codex exec on prompt_text; final message -> out. Returns exit code."""
    exe = shutil.which('codex')
    out.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    with open(log, 'w', encoding='utf-8') as lf:
        p = subprocess.run([exe, 'exec', '-s', 'read-only', '--skip-git-repo-check', '-o', str(out), '-'],
                           input=prompt_text.encode('utf-8'), stdout=lf, stderr=subprocess.STDOUT,
                           cwd=str(batches.TR), timeout=3600)
    return p.returncode


def errors_of(name):
    files = batches.load_files()
    byid = {e['id']: e for f, e in batches.all_entries(files)}
    errs, warns, _ = batches.check_batch(name, byid, batches.glossary())
    return errs, warns


def translate_one(name, rounds, brief, include):
    out = batches.OUT / ('%s.md' % name)
    if out.exists() and not errors_of(name)[0]:
        return name, 'skip (passes)'
    a = argparse.Namespace(batches=[name], brief=brief, include=include)
    batches.cmd_prompt(a)
    prompt = (batches.PROMPT / ('%s.md' % name)).read_text(encoding='utf-8')
    rc = codex(prompt, out, LOGS / ('%s.log' % name))
    for r in range(rounds):
        errs, warns = errors_of(name)
        if not errs:
            return name, 'OK (rc %d, round %d, %d warnings)' % (rc, r, len(warns))
        prev = out.read_text(encoding='utf-8') if out.exists() else '(no output)'
        fix = (prompt + '\n\n## Your previous output\n\n' + prev + '\n\n## Check errors to fix\n\n' +
               '\n'.join(errs[:80]) +
               '\n\nWrite the complete corrected output again (every id, same format), fixing every error. '
               'Width errors: rephrase shorter while keeping the meaning; for multi-line kinds the wrapper adds '
               'pages, so only single-line kinds and byte caps need shortening.\n')
        rc = codex(fix, out, LOGS / ('%s.fix%d.log' % (name, r + 1)))
    errs, warns = errors_of(name)
    return name, ('OK after fixes' if not errs else 'FAIL %d errors' % len(errs))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('translate')
    p.add_argument('batches', nargs='+')
    p.add_argument('--jobs', type=int, default=6)
    p.add_argument('--rounds', type=int, default=2)
    p.add_argument('--brief', default='docs/translator-brief.md')
    p.add_argument('--include', nargs='*', default=['docs/synopsis.md'])
    p = sp.add_parser('raw')
    p.add_argument('prompt')
    p.add_argument('out')
    a = ap.parse_args()
    if a.cmd == 'raw':
        rc = codex(Path(a.prompt).read_text(encoding='utf-8'), Path(a.out).resolve(),LOGS / (Path(a.out).stem + '.log'))
        print('rc', rc, '->', a.out)
        return rc
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda n: translate_one(n, a.rounds, a.brief, a.include), a.batches))
    bad = 0
    for name, msg in res:
        print(name, msg)
        bad += msg.startswith('FAIL')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
