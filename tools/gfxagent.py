"""gfxagent.py: graphics redraw groups through `codex exec` (Orca workers may not start graphics subagents).

    python -X utf8 tools/gfxagent.py GROUP [GROUP ...] [--jobs 2]

Each group (docs/gfx-groups.tsv) is one codex run in a workspace-write sandbox with the prompt "read
docs/graphics-brief.md and follow it for group G"; it writes gfx/<group>.tsv and nothing else (the brief says so;
check `git status` after). Final reports: work/gfx_agents/<group>.md, logs next to them. Then the main thread
reviews the previews, builds, warps to each screen for a zoomed cold-boot shot, and runs visual QA.
"""
import argparse
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'work' / 'gfx_agents'


def run(group):
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = ('Read docs/graphics-brief.md and follow it for group %s (its rows: docs/gfx-groups.tsv, first column '
              '"%s"). Write gfx/%s.tsv only. The skill directory ($SKILL) is printed by `python tools/skill.py`.'
              % (group, group, group))
    cmd = [shutil.which('codex'), 'exec', '-s', 'workspace-write', '--skip-git-repo-check',
           '-o', str(OUT / ('%s.md' % group)), prompt]
    with open(OUT / ('%s.log' % group), 'w', encoding='utf-8') as log:
        r = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    ok = r.returncode == 0 and (ROOT / 'gfx' / ('%s.tsv' % group)).exists()
    print(group, 'ok' if ok else 'FAILED (exit %d)' % r.returncode, flush=True)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('groups', nargs='+')
    ap.add_argument('--jobs', type=int, default=2)
    a = ap.parse_args()
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(run, a.groups))
    sys.exit(0 if all(res) else 1)


if __name__ == '__main__':
    main()
