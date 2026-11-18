"""The text lint (tools/lint.py) catches each error class, passes good lines, and passes the current script."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402
import lint  # noqa: E402
import textwidth  # noqa: E402


@pytest.fixture(scope='module')
def eng():
    return textwidth.load()


def msg(en, jp='あ{br}い{page}う'):
    return {'id': 'rom.T', 'kind': 'msg', 'jp': jp, 'en': en}


def test_good_msg(eng):
    assert lint.lint_entry(msg('Hello there.{br}How are you?{page}Fine.'), eng) == []


def test_untranslated_is_skipped(eng):
    assert lint.lint_entry(msg(''), eng) == []


def test_japanese_left(eng):
    assert any('Japanese' in m for m in lint.lint_entry(msg('Hello あ'), eng))


def test_not_encodable(eng):
    assert any('encodable' in m for m in lint.lint_entry(msg('Café Ж'), eng))


def test_controls_differ(eng):
    errs = lint.lint_entry(msg('Hi.', jp='{hero}は'), eng)
    assert any('controls' in m for m in errs)
    assert lint.lint_entry(msg('Hi, {hero}.', jp='{hero}は'), eng) == []


def test_too_wide_and_too_many_lines(eng):
    wide = 'mmmm ' * 20
    assert any('px' in m for m in lint.lint_entry(msg(wide), eng))
    assert any('lines' in m for m in lint.lint_entry(msg('a{br}b{br}c{br}d'), eng))


def test_last_line_leaves_room_for_page_arrow(eng):
    s = ''
    while eng.width(s + 'e') <= 230:
        s += 'e'
    assert lint.lint_entry(msg(s), eng) == []                      # line 1 may be 240 px
    assert any('222' in m for m in lint.lint_entry(msg('a{br}b{br}' + s), eng))


def test_slot_cap(eng):
    e = {'id': 'a9.item.000.name', 'kind': 'item.name', 'jp': 'あ', 'max': 8, 'en': 'Silver Charm'}
    assert any('slot cap' in m for m in lint.lint_entry(e, eng))
    e['en'] = 'Herb'
    assert lint.lint_entry(e, eng) == []


def test_every_budget_kind_names_its_evidence():
    for k, b in lint.BUDGETS.items():
        if not k.startswith('_'):
            assert b['status'] in ('measured', 'guess') and b.get('shot'), k


def test_current_script_is_clean(eng):
    entries = [e for es in insert.load_entries().values() for e in es]
    errors, _ = lint.run(entries, eng)
    assert errors == []
