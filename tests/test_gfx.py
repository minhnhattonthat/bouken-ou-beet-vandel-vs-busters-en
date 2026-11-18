"""gfx.py: re-tiling an unedited image gives the original bytes; every gfx/*.tsv row draws; edits stay in rects."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gfx  # noqa: E402

pytestmark = pytest.mark.skipif(not (gfx.FS / 'screen').exists(), reason='needs work/fs (tools/romls.py --unpack)')


def test_noop_retile_is_identity():
    for name in ('screen/battle_base.nbfc', 'screen/title.nbfc'):
        m = gfx.fs_get(name[:-5] + '.nbfs')
        img = gfx.Image4(name, gfx.fs_get(name), m)
        data, mp, notes = img.save()
        assert data == gfx.fs_get(name) and mp == m and not notes


def test_grid_noop_is_identity():
    img = gfx.Image4('screen/button_tool.nbfc', gfx.fs_get('screen/button_tool.nbfc'), None, 8)
    assert img.save()[0] == gfx.fs_get('screen/button_tool.nbfc')


def test_rows_draw_inside_their_rects():
    rows = gfx.load_rows()
    new, _ = gfx.edit_files(gfx.fs_get, rows)
    by_file = {}
    for r in rows:
        by_file.setdefault(r['file'], []).append(r)
    for spec, rs in by_file.items():
        name, grid = gfx.split_name(spec)
        mname = name[:-5] + '.nbfs'
        m0 = gfx.fs_get(mname) if grid is None and (gfx.FS / mname).exists() else None
        a = gfx.Image4(name, gfx.fs_get(name), m0, grid)
        b = gfx.Image4(name, new[name], new.get(mname, m0), grid)
        for y in range(a.H):
            for x in range(a.W):
                if a.px[y][x] != b.px[y][x]:
                    assert any(r['x'] <= x < r['x'] + r['w'] and r['y'] <= y < r['y'] + r['h'] for r in rs), \
                        '%s: pixel %d,%d changed outside every rect' % (name, x, y)
