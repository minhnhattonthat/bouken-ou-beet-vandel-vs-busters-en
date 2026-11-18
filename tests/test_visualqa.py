"""visualqa.parse reads codex's verdict lines in the shapes it actually writes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import visualqa  # noqa: E402


def test_parse_tab_pipe_and_markdown():
    text = ('Here are the verdicts:\n'
            'title/sheet\tok\tEnglish title, no Japanese\n'
            '- `shop/sheet | issue | row 1 col 2: 武器購入 header still Japanese`\n'
            'other/sheet\tmaybe\tnot a verdict\n'
            'stray/sheet\tok\tnot in the chunk\n')
    got = visualqa.parse(text, {'title/sheet', 'shop/sheet', 'other/sheet'})
    assert got == {'title/sheet': ('ok', 'English title, no Japanese'),
                   'shop/sheet': ('issue', 'row 1 col 2: 武器購入 header still Japanese')}
