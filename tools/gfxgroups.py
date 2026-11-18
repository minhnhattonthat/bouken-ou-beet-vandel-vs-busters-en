"""gfxgroups.py: write docs/gfx-groups.tsv, the graphics-survey rows not yet in gfx/*.tsv, split into redraw groups
that share no file (references/graphics.md §Parallel redraws).

    python -X utf8 tools/gfxgroups.py        # prints the count per group
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gfx  # noqa: E402

JP = re.compile(r'[぀-ヿ一-鿿]')
RULES = [
    ('credits', r'^bg/credit'), ('cutins', r'^battle/cutin'), ('obj', r'\.ob$|^(?!screen/)'),
    ('shopbuttons', r'^screen/button_'),
    ('title', r'^screen/(title|mode_|copyright|start|debug_bg|signature|gba_link)'),
    ('radio', r'^screen/radio'), ('shops', r'^screen/(shop_|v_shop|monster_confidental|v_uptake)'),
    ('info', r'^screen/(info_base|quest_|monster_book|buster_book|vandel_book)'),
    ('windows', r'^screen/(save|trap_win|party_.*_str|confirmation|monster_exchange|party_yn|party_breakup)'),
    ('nameopt', r'^screen/(name_|option_)'),
    ('obj', r'^screen/(skill_range|skill_type|hit|exp|mg|saiga_timing|waiting)'),
    ('menus', r''),
]
# text the survey left as '?' (read in game)
EXTRA = {'screen/mode_begin.nbfc': 'はじめから'}
# survey rows that need no redraw, with the reason (checked by rendering each file through its map / sprite layout)
SKIP = {
    'battle/cutin/': 'portraits and speed lines only, no lettering (rendered through their .nbfs maps, 2026-11-19)',
    'screen/main_v_parts.nbfc': 'Latin "BL", not 星',
    'screen/tengeki_D.nbfc': 'arrow button, no text', 'screen/tengeki_U.nbfc': 'arrow button, no text',
    'screen/tengeki_v_parts2.nbfc': 'diamond marker, no text',
    'screen/title.nbfc': 'title logo: kept, no official English logo (decision D5)',
    'screen/debug_bg.nbfc': 'debug-menu backdrop with the logo (D5); not in the release build',
    'screen/monster_exchange_take_sub1_1.nbfc': 'survey misspelling of monster_exchange_take_sub_1 (gfx/windows.tsv)',
}


def skipped(f):
    return next((why for k, why in SKIP.items() if f.startswith(k)), None)


def group(f):
    return next(g for g, rx in RULES if re.search(rx, f))


def main():
    done = {gfx.split_name(r['file'])[0] for r in gfx.load_rows()}
    rows = [line.split('\t') for line in
            (ROOT / 'docs' / 're' / 'graphics-survey.tsv').read_text(encoding='utf-8').splitlines()[1:]]
    rows = [(r[1], EXTRA.get(r[1], r[2]), r[3]) for r in rows if len(r) >= 4]
    out, c = ['group\tfile\tjp\twhat'], Counter()
    for f, jp, what in rows:
        if f in done or skipped(f) or not (JP.search(jp) or jp == '?'):
            continue
        g = group(f)
        c[g] += 1
        out.append('\t'.join([g, f, jp, what]))
    (ROOT / 'docs' / 'gfx-groups.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
    print(dict(c), sum(c.values()))


if __name__ == '__main__':
    main()
