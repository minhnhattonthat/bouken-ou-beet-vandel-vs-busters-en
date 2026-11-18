"""techsweep.py: text coverage runs for the Tengeki (Divine Attack) and Meigeki (Dark Attack) lists.

The Saiga screen's Divine/Dark Attack list draws the ids of the learned list in the member struct, u32 words at
save+0x16E8 (member at save+0x1660, list at +0x88; row routine 0x020CC5EC: [[obj+0xD8] + 0x88 + 4*row], tengeki
accessor 0x020145D8 in Buster mode, meigeki 0x020145F0 when save+0 = 1 (Vandel mode)). Each run writes up to 25 ids
there at warp time (warp.lua wOFF token; the list draws only the first 20), opens the list from the Saiga screen (scene menu_skills, button t14,180)
and taps the scroll arrow (t16,138) so every row is fetched and drawn. Saiga skills (accessor 0x020142E0, Vandel
mode only) are listed at save+0x174C; their rows are fetched but draw blank here, see docs/status.md session 14.

    python -X utf8 tools/debug/techsweep.py [--rom build/beet_en.nds] [--only tengeki_a,...] [--jobs 2]

Runs go to work/qa/cover/<name> (they count for tools/textcov.py report).
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VANDEL = ['--script', 'tools/lua/memset.lua', '--var', 'MEMSET_PTR=0x021BA3A0', '--var', 'MEMSET_OFF=0',
          '--var', 'MEMSET_VAL=1', '--var', 'MEMSET_FROM=3500']
# name: (first id, count, list offset in save, open-button touch, vandel mode)
RUNS = {
    # the list draws 20 entries (a 25-id write showed ids 1-20 only)
    'tengeki_a': (1, 25, 0x16E8, 't14,180', False),
    'tengeki_b': (26, 18, 0x16E8, 't14,180', False),
    'tengeki_c': (21, 5, 0x16E8, 't14,180', False),
    'meigeki_a': (1, 25, 0x16E8, 't14,180', True),
    'meigeki_b': (26, 18, 0x16E8, 't14,180', True),
    'meigeki_c': (21, 5, 0x16E8, 't14,180', True),
    'skill_a': (1, 25, 0x174C, None, True),
    'skill_b': (26, 25, 0x174C, None, True),
    'skill_c': (51, 17, 0x174C, None, True),
}


def words(first, n):
    return ''.join((first + i).to_bytes(4, 'little').hex().upper() for i in range(n))


def run(rom, name):
    first, n, off, button, vandel = RUNS[name]
    taps = ' '.join(['t16,138 w30'] * (n + 2))
    extra = f'w{off:X}={words(first, n)}'
    if button:
        extra += f' @4300 {button} w200 {taps}'
    frames = 4600 + (130 * (n + 2) if button else 0)  # a tX,Y token is 6 + 90 frames, then w30
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'emu.py'), rom, '--debugger',
           '--out', f'work/qa/cover/{name}', '--script', 'tools/debug/warp.lua', *(VANDEL if vandel else []),
           '--script', 'tools/lua/textlog.lua', '--var', "SCENE='menu_skills'", '--var', f"EXTRA='{extra}'",
           '--frames', str(frames), '--shot-every', '126']
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return name, r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--rom', default='build/beet_en.nds')
    ap.add_argument('--only', default=','.join(RUNS))
    ap.add_argument('--jobs', type=int, default=2)
    a = ap.parse_args()
    names = a.only.split(',')
    with ThreadPoolExecutor(a.jobs) as ex:
        bad = 0
        for name, code in ex.map(lambda k: run(a.rom, k), names):
            print(name, 'ok' if code == 0 else f'exit {code}')
            bad += code != 0
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
