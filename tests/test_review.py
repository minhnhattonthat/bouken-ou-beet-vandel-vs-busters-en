import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import review  # noqa: E402


def test_suggested_plain():
    assert review.suggested('JP means X - too short - "Fixed line."') == 'Fixed line.'


def test_suggested_strips_label():
    assert review.suggested('JP means X - voice lost - suggested EN: Fixed line.') == 'Fixed line.'
    assert review.suggested('JP means X - voice lost - **Suggested EN:** "Fixed line."') == 'Fixed line.'


def test_suggested_needs_three_fields():
    assert review.suggested('only one - field') == ''
