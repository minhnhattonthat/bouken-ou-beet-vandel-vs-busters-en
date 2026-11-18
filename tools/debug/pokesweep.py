"""One warp run per id with a warp-time save poke built from the id (e.g. the first member's equipped weapon,
save+0x185C = id+1 | 1 << 8, read when a battle builds its units: the battle then fetches that weapon record,
its wpntype and its special). Runs land in OUT/<id hex>/ with textlog.lua; point textcov.py report at OUT.

    python -X utf8 tools/debug/pokesweep.py --scene b29_my_castle --poke "w185C={lo:02X}{hi:02X}" --add 1 --hi 1
      --ids 0,13-19,22-24 --out work/qa/cover/wbattle [--frames 4000] [--jobs 3] [--rom build/beet_en.nds]

{lo}/{hi} = low / high byte of (id + ADD) | HI << 8; {v} = that whole value; {id} = the id. Exit 1 if any run
failed (emu exit != 0).

--poke is optional; --script LUA (inserted before textlog.lua, repeatable) and --var NAME=VALUE (repeatable, same
{..} fields) add Lua probes that need the id, with --debugger. Session 20 examples:
  member 2's weapon (the event script rewrites save+0x1988 at f1626, so hold it after that) -> its wpntype:
    --scene b29_my_castle --add 1 --hi 1 --debugger --script tools/lua/memset.lua --var MEMSET_PTR=0x021BA3A0
    --var MEMSET_OFF=0x1988 --var MEMSET_VAL={v} --var MEMSET_SIZE=2 --var MEMSET_FROM=1640 --var MEMSET_ONCE=1
  the battle special cut-in (0x020AF570) with the acting unit's weapon id forced at 0x020AAD28 (r0 = weapon id+1):
    the memset above with --var MEMSET_VAL=0x110 (weapon 15, whose special member 2 uses at f1860), plus
    --script tools/lua/idloop.lua --var IDLOOP_ACC=0x020AAD28 --var IDLOOP_FROM={v} --add 1 --frames 2400
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def ids_of(spec):
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a, 0), int(b or a, 0) + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scene', required=True)
    ap.add_argument('--poke', default='')
    ap.add_argument('--add', type=lambda s: int(s, 0), default=0)
    ap.add_argument('--hi', type=lambda s: int(s, 0), default=0)
    ap.add_argument('--ids', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--frames', type=int, default=4000)
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--rom', default='build/beet_en.nds')
    ap.add_argument('--script', action='append', default=[], help='extra Lua probe, before textlog.lua')
    ap.add_argument('--var', action='append', default=[], help='NAME=VALUE for the probes ({id} {v} {lo} {hi})')
    ap.add_argument('--debugger', action='store_true', help='emu.py --debugger (exec hooks)')
    ap.add_argument('--shot-every', type=int, default=500)
    a = ap.parse_args()

    def run(i):
        v = ((i + a.add) & 0xFF) | a.hi << 8
        fields = dict(lo=v & 0xFF, hi=v >> 8, id=i, v=v)
        tok = a.poke.format(**fields)
        out = Path(a.out) / f'{i:X}'
        cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'emu.py'), a.rom, '--out', str(out),
               '--script', 'tools/debug/warp.lua', '--var', f"SCENE='{a.scene}'"]
        if tok:
            cmd += ['--var', f"EXTRA='{tok}'"]
        for s in a.script:
            cmd += ['--script', s]
        for kv in a.var:
            cmd += ['--var', kv.format(**fields)]
        if a.debugger:
            cmd += ['--debugger']
        cmd += ['--script', 'tools/lua/textlog.lua', '--frames', str(a.frames), '--shot-every', str(a.shot_every)]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        print(f'{i:X} {tok} exit {r.returncode}', flush=True)
        return r.returncode

    with ThreadPoolExecutor(a.jobs) as ex:
        codes = list(ex.map(run, ids_of(a.ids)))
    sys.exit(1 if any(codes) else 0)


if __name__ == '__main__':
    main()
