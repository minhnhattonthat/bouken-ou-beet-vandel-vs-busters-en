"""vqasheets.py: full-resolution visual-QA sheets (changed frames only) from a warp_all tour.

    python -X utf8 tools/vqasheets.py work/qa/en work/qa/vqa_en [--jobs 6]

warp_all's own sheets are at half scale, too small to judge 8-12 px text. This writes <out>/<scene>/sheet*.png with
`sheet.py --div 1 --changed 0.02 --max 8` for every scene directory. Use the same command on the original ROM's
tour (work/qa/tour_jp -> work/qa/vqa_jp) so `tools/visualqa.py --en work/qa/vqa_en --jp work/qa/vqa_jp` attaches
twins. Then `qa_gate.py init work/qa/manifest.tsv work/qa/vqa_en --build build/beet_en.nds`.
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill import SKILL  # noqa: E402


def one(scene, out):
    o = out / scene.name
    o.mkdir(parents=True, exist_ok=True)
    for old in o.glob('sheet*.png'):
        old.unlink()
    r = subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts' / 'sheet.py'), str(scene),
                        '--div', '1', '--changed', '0.02', '--max', '8', '--cols', '4', '--out', str(o / 'sheet.png')],
                       capture_output=True, text=True)
    return scene.name, r.returncode, r.stderr.strip()[-200:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('tour')
    ap.add_argument('out')
    ap.add_argument('--jobs', type=int, default=6)
    a = ap.parse_args()
    scenes = [d for d in sorted(Path(a.tour).iterdir()) if d.is_dir() and any(d.glob('f*.png'))]
    bad = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, rc, err in ex.map(lambda s: one(s, Path(a.out)), scenes):
            if rc:
                bad += 1
                print('FAIL', name, err)
    print('%d scenes, %d failed -> %s' % (len(scenes), bad, a.out))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
