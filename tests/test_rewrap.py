"""rewrap.py re-fits text to a kind's budget, and every quest board preview (kind brief) fits its 180 px box."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import rewrap  # noqa: E402


def test_fits_and_rewrap():
    long = 'Gather Medicinal Flowers in the{br}Nash Plains.'
    assert not rewrap.fits(long, 'brief')          # first line ~194 px > 180 (seen clipped in work/qa/p12_gc3)
    new = batches.wrap(long.replace('{br}', ' '), 'brief')
    assert rewrap.fits(new, 'brief')
    assert new.replace('{br}', ' ') == long.replace('{br}', ' ')
    assert not rewrap.fits('a{br}b{br}c{br}d{br}e', 'brief')   # 5 lines > 4


def test_every_brief_fits():
    bad = []
    for f in (ROOT / 'script' / 'quest').glob('*.json'):
        for e in json.loads(f.read_text(encoding='utf-8'))['entries']:
            if e['kind'] == 'brief' and e.get('en') and not rewrap.fits(e['en'], 'brief'):
                bad.append(e['id'])
    assert not bad
