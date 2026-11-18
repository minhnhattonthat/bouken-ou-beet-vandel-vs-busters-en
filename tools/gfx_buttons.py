"""gfx_buttons.py: draft gfx rows for the OBJ buttons (screen/button_*.nbfc): finds each button's lettering and the
interior around it, and prints `gfx/*.tsv` rows for the English in LABELS. Review and hand-tune the rows it prints.

    python -X utf8 tools/gfx_buttons.py [NAME ...] > work/gfx_buttons.tsv

Button sprites are 64x32 (32 tiles, @8) or 128x32 (64 tiles, @16); lettering uses indices outside the button's
fill (8-11) and frame (7, 13-15). A button without a left frame is drawn cut by the screen edge: its visible part
starts at sprite x 23 (battle menu, measured in game: right frame at screen x 37 = sprite x 59; a T at sprite
x 22 lost its first column).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfx  # noqa: E402

FILL = {8, 9, 10, 11, 12}
FRAME = {7, 13, 14, 15}
CUT_LEFT_X = 23


def analyse(name, grid):
    img = gfx.Image4(name, gfx.fs_get(name), None, grid)
    spans = {}
    for y in range(img.H):
        xs = [x for x in range(img.W) if img.px[y][x] in FILL]
        if len(xs) > 8:
            spans[y] = (xs[0], xs[-1])
    ink = [(x, y) for y, (a, b) in spans.items() for x in range(a, b + 1) if img.px[y][x] not in FILL]
    if not ink:
        return None
    x0, x1 = min(x for x, _ in ink), max(x for x, _ in ink)
    y0, y1 = min(y for _, y in ink), max(y for _, y in ink)
    rows = [y for y in spans if y0 - 1 <= y <= y1 + 1] or list(spans)
    left = min(spans[y][0] for y in range(y0, y1 + 1) if y in spans)
    right = max(spans[y][1] for y in range(y0, y1 + 1) if y in spans) + 1
    top, bot = min(spans), max(spans) + 1
    cut = img.px[(y0 + y1) // 2][left - 1] == 0 if left > 0 else True
    cut_right = right >= img.W or img.px[(y0 + y1) // 2][right] == 0
    inks = sorted({img.px[y][x] for x, y in ink})
    del rows
    return dict(text=(x0, y0, x1, y1), left=left, right=right, top=top, bot=bot, inks=inks, cut=cut,
                cut_right=cut_right)


LABELS = {
    'array': 'Lineup', 'array2': 'Lineup', 'assign': 'Party|Orders', 'back': 'Back', 'busterbook': 'Buster|Book',
    'category': 'Type', 'decision2': 'OK', 'detail': 'Details', 'dispatch': 'Dispatch', 'equip': 'Equip',
    'equipitem': 'Equip', 'fast': 'Fast', 'finish': 'Report', 'giveup': 'Give Up', 'info': 'Info',
    'monster': 'Monsters', 'monsterbook': 'Monster|Book', 'name': 'Name', 'no': 'No', 'normal': 'Normal',
    'option': 'Options', 'order': 'Orders', 'party': 'Party', 'quest': 'Quests', 'quickcommand': 'Quick|Command',
    'saiga': 'Saiga', 'saiga2': 'Saiga', 'save': 'Save', 'shuffle': 'Swap', 'skill': 'Skills', 'skill2': 'Skills',
    'slow': 'Slow', 'sort_armor': 'Armor', 'sort_tool': 'Items', 'sort_treasure': 'Treasure',
    'sort_weapon': 'Weapons', 'status': 'Status', 'tactics': 'Tactics', 'tactics2': 'Tactics',
    'tengeki': 'Divine|Attack', 'tengeki2': 'Divine|Attack', 'tengeki3': 'Divine|Attack', 'tool': 'Items',
    'tool2': 'Items', 'undo2': 'Remove', 'uptake': 'Uptake', 'v_assign': 'Force|Orders',
    'v_meigeki': 'Dark|Attack', 'v_meigeki2': 'Dark|Attack', 'v_meigeki3': 'Dark|Attack', 'v_party': 'Force',
    'v_trap': 'Trap', 'v_uptake': 'Monster|Uptake', 'v_waza': 'Skills', 'v_waza2': 'Skills',
    'vandelbook': 'Vandel|Book', 'yes': 'Yes',
}


def main():
    names = sys.argv[1:] or list(LABELS)
    print('\t'.join(gfx.COLS))
    for n in names:
        name = 'screen/button_%s.nbfc' % n
        ntiles = len(gfx.fs_get(name)) // 32
        grid = {32: 8, 64: 16, 16: 4}[ntiles]
        a = analyse(name, grid)
        if a is None:
            print('# %s: no lettering found' % name)
            continue
        left = CUT_LEFT_X if a['cut'] else a['left']
        x, w = left, a['right'] - left
        y, h = a['top'], a['bot'] - a['top']
        en = LABELS[n]
        font = 's' if '|' in en else 'sb'
        align = 'c'
        if a['cut_right']:      # cut by the right screen edge: keep the English where the Japanese started
            x, w, align = a['text'][0], a['right'] - a['text'][0], 'l'
        print('# %s text %s inks %s%s%s' % (n, a['text'], a['inks'], ' cut-left' if a['cut'] else '',
                                            ' cut-right' if a['cut_right'] else ''))
        print('\t'.join(map(str, ['%s@%d' % (name, grid), x, y, w, h, font, 1, 2, align,
                                  ','.join(map(str, a['inks'])), en])))


if __name__ == '__main__':
    main()
