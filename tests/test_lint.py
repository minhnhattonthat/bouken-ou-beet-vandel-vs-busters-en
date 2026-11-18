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


def test_untranslated_needs_keep_line():
    ents = [msg(''), dict(msg('Hi.'), id='rom.U')]
    assert [i for i, _ in lint.untranslated(ents, {})] == ['rom.T']
    assert lint.untranslated(ents, {'rom.T': 'why'}) == []
    assert [i for i, _ in lint.untranslated(ents, {'rom.T': 'why', 'rom.U': 'stale', 'rom.X': 'gone'})] == \
        ['rom.U', 'rom.X']


def test_glossary_avoid_any_case_across_breaks():
    """A re-applied review suggestion that lower-cases or line-breaks an Avoid spelling still fails."""
    rows = [('封印のリング', 'Sealing Ring', ['Seal Ring']), ('昇格値', 'Rank Points', ['promotion points'])]
    bad = [msg('the seal{br}rings!', jp='封印のリング'), dict(msg('the bounty and promotion{br}points', jp='昇格値'),
                                                             id='rom.U')]
    errs, _ = lint.glossary_check(bad, rows)
    assert [i for i, _ in errs] == ['rom.T', 'rom.U']
    good = [msg('broken Sealing Rings!', jp='封印のリング'), msg('Rank{br}Points', jp='昇格値')]
    assert lint.glossary_check(good, rows) == ([], [])


def test_script_has_no_avoided_glossary_spellings():
    entries = [e for es in insert.load_entries().values() for e in es]
    errs, _ = lint.glossary_check(entries)
    assert errs == [], errs[:5]


def test_message_code_limits(eng):
    long = ' '.join(['Mmmm'] * 130) + '{close}'     # > 511 codes (M never pairs)
    assert any('over 511 codes' in m for m in lint.lint_entry(msg(long, jp='あ{close}'), eng))
    spk = {'id': 'rom.S', 'kind': 'speaker', 'jp': 'あ', 'en': 'M' * 12}
    assert any('over 11 codes' in m for m in lint.lint_entry(spk, eng))


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
            assert b['status'] in ('measured', 'jp-bound', 'not-drawn') and b.get('shot'), k
            assert ('px' in b) == (b['status'] != 'not-drawn'), k


def test_not_drawn_kind_has_no_width_check(eng):
    e = {'id': 'a9.item.000.reading', 'kind': 'item.reading', 'jp': 'あ', 'max': 40,
         'en': 'Return Scorpio Remedy'}
    assert lint.lint_entry(e, eng) == []


def test_relocated_slot_uses_the_new_cap(eng):
    e = {'id': 'a9.elem.000.name', 'kind': 'elem.name', 'jp': '沼', 'max': 4, 'addr': '021233D8', 'en': 'Marsh',
         'short': 'Ma'}
    assert insert.text_cap(e) == 14
    assert lint.lint_entry(e, eng) == []
    e['en'] = 'Ma Ma Ma Ma Ma'   # fits the 14-byte slot, not the 72 px canvas (engine.ELEM_WIN)
    assert any('px' in m for m in lint.lint_entry(e, eng))


def test_elem_needs_a_short_form(eng):
    e = {'id': 'a9.elem.000.name', 'kind': 'elem.name', 'jp': '沼', 'max': 4, 'addr': '021233D8', 'en': 'Marsh'}
    assert any('short' in m for m in lint.lint_entry(e, eng))
    e['short'] = 'Marsh'   # wider than the 16 px status cell
    assert any('short' in m for m in lint.lint_entry(e, eng))


def test_current_script_is_clean(eng):
    entries = [e for es in insert.load_entries().values() for e in es]
    errors, _ = lint.run(entries, eng)
    assert errors == []
