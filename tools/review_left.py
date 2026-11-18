"""review_left.py: Critical/Important review findings that are neither applied (the batch output line equals the
suggested EN) nor listed in docs/polish.md. Phase 6 is done when this prints nothing for every reviewed batch.

    python -X utf8 tools/review_left.py [b018 ...]     # default: every work/tr/review/bNNN.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import batches  # noqa: E402
import review  # noqa: E402


def main(argv):
    names = argv or sorted(p.stem for p in review.REV.glob('b*.md'))
    polish = review.POLISH.read_text(encoding='utf-8')
    left = 0
    for name in names:
        res, _ = review.findings(name)
        if res is None:
            print(name, 'no review')
            left += 1
            continue
        got, _, _ = batches.read_out(name)
        for sev in ('Critical', 'Important'):
            for i, text in res[sev]:
                en = review.suggested(text)
                for k, v in batches.NORMALISE.items():
                    en = en.replace(k, v)
                if en and got.get(i, '').strip().lower() == en.strip().lower():
                    continue
                if i in polish:
                    continue
                left += 1
                print('%s %s %s: %s' % (name, sev, i, text[:160]))
    print('left:', left)
    return 1 if left else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
