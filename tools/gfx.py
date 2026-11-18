"""gfx.py: graphics-text redraws (phase 8). Reads gfx/*.tsv, edits the NitroFS tile files, writes them into the build.

Row format (tab-separated, `#` comments, header line `file ...`):

    file  x  y  w  h  font  ink  shadow  align  erase  en

- file: NitroFS path. `.nbfc` with a `.nbfs` twin is drawn through its map (screen space); without one it is a grid
  of tiles; `path@N` sets the grid width to N tiles (OBJ sprites in 1D order: 64x32 = @8).
- x y w h: the clear rect in that image's pixels (`python -X utf8 tools/gfx.py show FILE` draws a ruler).
- font: 8, 10 or 12 (the game's own full-width Latin glyphs, lc8x8 / lc10x10 / lc12x12, cropped proportionally);
  add `b` for a bold (doubled) stroke: `12b`.
- ink: colour index (4bpp: 0-15 within the cell's palette bank); shadow: index drawn at +1,+1 under the ink, `o:N`
  for a 1 px outline, `-` for none.
- align: l c r (the text box is the rect; vertically centred).
- erase: `fill:N` fills the rect with N; `a,b,c` replaces pixels of those indices (the old lettering) with the
  nearest pixel of another index (keeps gradients and dithered backgrounds); `-` keeps the rect as is.
- en: the English; empty or `-` -> the row only erases.

Map files are re-tiled: cells the edit did not change keep their entries; changed cells reuse a tile with the same
pixels (any flip) or take a tile no unchanged cell uses, else a new tile at the end (reported: the BG's VRAM budget
must allow it). Grid files are edited in place.

    python -X utf8 tools/gfx.py show screen/battle_base.nbfc [--pal P] [--zoom 3] [--out F.png]
    python -X utf8 tools/gfx.py preview [GROUP ...] [--out work/gfx_preview]   # original | English, per file
    import gfx; gfx.apply(rom, log)      # build: replaces the files, logs every changed byte run
"""
import argparse
import collections
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402
import smallfont  # noqa: E402

GFX = ROOT / 'gfx'
FS = ROOT / 'work' / 'fs' / 'fs'
COLS = ['file', 'x', 'y', 'w', 'h', 'font', 'ink', 'shadow', 'align', 'erase', 'en']
FONTS = {8: ('font/lc8x8.bin', 8, 8), 10: ('font/lc10x10.bin', 20, 10), 12: ('font/lc12x12.bin', 24, 12)}
GAP = 1


def load_rows(groups=None):
    rows = []
    for p in sorted(GFX.glob('*.tsv')):
        if groups and p.stem not in groups:
            continue
        lines = p.read_text(encoding='utf-8').splitlines()
        for n, line in enumerate(lines, 1):
            if not line.strip() or line.startswith('#') or line.startswith('file\t'):
                continue
            f = line.split('\t')
            assert len(f) == len(COLS), '%s:%d has %d columns, want %d' % (p.name, n, len(f), len(COLS))
            r = dict(zip(COLS, f))
            if r['en'] == '-':      # erase-only row (an empty last column is lost to editors that trim lines)
                r['en'] = ''
            for k in 'xywh':
                r[k] = int(r[k])
            r['where'] = '%s:%d' % (p.name, n)
            rows.append(r)
    return rows


def split_name(spec):
    name, _, gw = spec.partition('@')
    return name, int(gw) if gw else None


def body_off(b):
    return 4 if len(b) >= 4 and struct.unpack_from('<I', b)[0] == len(b) - 4 else 0


class Glyphs:
    def __init__(self, getfile):
        self.fonts = {k: getfile(v[0]) for k, v in FONTS.items()}
        self.cache = {}

    def glyph(self, ch, size):
        """list of rows of 0/1, cropped to ink (space -> blank columns)."""
        key = (ch, size)
        if size == 's':
            if ch not in smallfont.GLYPHS:
                raise SystemExit('small font has no %r' % ch)
            return smallfont.GLYPHS[ch]
        if key not in self.cache:
            _, nb, rows = FONTS[size]
            if ch == ' ':
                self.cache[key] = [[0] * {8: 3, 10: 3, 12: 4}[size] for _ in range(rows)]
            else:
                i = engine.glyph_index(ch)
                f = self.fonts[size]
                if size == 8:
                    g = [f[i * 8 + r] << 8 for r in range(8)]
                else:
                    g = [int.from_bytes(f[i * nb + r * 2:i * nb + r * 2 + 2], 'big') for r in range(rows)]
                cols = [c for c in range(16) if any(r >> (15 - c) & 1 for r in g)]
                lo, hi = min(cols), max(cols)
                self.cache[key] = [[r >> (15 - c) & 1 for c in range(lo, hi + 1)] for r in g]
        return self.cache[key]

    def render(self, text, size, bold=False):
        """(width, rows) bitmap of text; rows trimmed to the font's ink rows."""
        rows = smallfont.ROWS if size == 's' else FONTS[size][2]
        out = [[] for _ in range(rows)]
        for k, ch in enumerate(text):
            g = self.glyph(ch, size)
            if bold and ch != ' ':
                g = [[a | b for a, b in zip(r + [0], [0] + r)] for r in g]
            for r in range(rows):
                out[r] += g[r] + ([0] * GAP if k < len(text) - 1 else [])
        return len(out[0]), out


class Image4:
    """Pixel indices of a tile file as one image: map files in screen space, grid files tile by tile."""

    def __init__(self, name, data, mapdata=None, grid=None):
        self.name = name
        self.data = data
        self.off = body_off(data)
        raw = data[self.off:]
        self.bpp = 4
        self.tsize = 32
        self.ntiles = len(raw) // self.tsize
        self.tiles = [self._tile(raw, t) for t in range(self.ntiles)]
        self.mapdata = mapdata
        if mapdata is not None:
            self.mw, self.mh = struct.unpack_from('<HH', mapdata)
            self.entries = [struct.unpack_from('<H', mapdata, 4 + 2 * k)[0] for k in range(self.mw * self.mh)]
            self.W, self.H = self.mw * 8, self.mh * 8
        else:
            self.gw = grid or 32
            self.W, self.H = self.gw * 8, (self.ntiles + self.gw - 1) // self.gw * 8
        self.px = [[0] * self.W for _ in range(self.H)]
        self.bank = [[0] * self.W for _ in range(self.H)]
        for cell in range(self._ncells()):
            t, hf, vf, b = self._cell(cell)
            cx, cy = self._cellxy(cell)
            tile = self.tiles[t] if t < self.ntiles else [0] * 64
            for i in range(64):
                x, y = i % 8, i // 8
                x, y = (7 - x if hf else x), (7 - y if vf else y)
                self.px[cy + y][cx + x] = tile[i]
                self.bank[cy + y][cx + x] = b
        self.orig = [r[:] for r in self.px]

    def _tile(self, raw, t):
        b = raw[t * 32:t * 32 + 32]
        return [b[i // 2] >> (4 * (i & 1)) & 15 for i in range(64)]

    def _ncells(self):
        return len(self.entries) if self.mapdata is not None else self.ntiles

    def _cellxy(self, cell):
        w = self.mw if self.mapdata is not None else self.gw
        return cell % w * 8, cell // w * 8

    def _cell(self, cell):
        if self.mapdata is None:
            return cell, False, False, 0
        e = self.entries[cell]
        return e & 0x3FF, bool(e & 0x400), bool(e & 0x800), e >> 12

    def block(self, cell):
        cx, cy = self._cellxy(cell)
        return tuple(self.px[cy + i // 8][cx + i % 8] for i in range(64))

    @staticmethod
    def flips(t):
        rows = [t[i * 8:i * 8 + 8] for i in range(8)]
        for hf in (False, True):
            for vf in (False, True):
                r2 = [r[::-1] if hf else r for r in (rows[::-1] if vf else rows)]
                yield hf, vf, tuple(v for r in r2 for v in r)

    def pack_tile(self, t):
        return bytes(t[i] | t[i + 1] << 4 for i in range(0, 64, 2))

    def save(self):
        """(tile file bytes, map bytes or None, notes)."""
        notes = []
        if self.mapdata is None:
            tiles = list(self.tiles)
            for cell in range(self.ntiles):
                tiles[cell] = list(self.block(cell))
            raw = b''.join(self.pack_tile(t) for t in tiles)
            return self.data[:self.off] + raw + self.data[self.off + len(raw):], None, notes
        ncell = len(self.entries)
        changed = [self.block(c) != tuple(v for v in self._orig_block(c)) for c in range(ncell)]
        keep = {self.entries[c] & 0x3FF for c in range(ncell) if not changed[c]}
        tiles = [tuple(t) for t in self.tiles]
        index = {}
        for t in sorted(keep):
            if t < len(tiles):
                for hf, vf, v in self.flips(tiles[t]):
                    index.setdefault(v, (t, hf, vf))
        free = [t for t in range(self.ntiles) if t not in keep and t != 0]
        entries = list(self.entries)
        grown = 0
        for c in range(ncell):
            if not changed[c]:
                continue
            blk = self.block(c)
            bank = self.entries[c] >> 12
            if blk in index:
                t, hf, vf = index[blk]
            else:
                if free:
                    t = free.pop(0)
                    tiles[t] = blk
                else:
                    t = len(tiles)
                    tiles.append(blk)
                    grown += 1
                hf = vf = False
                for h2, v2, v in self.flips(blk):
                    index.setdefault(v, (t, h2, v2))
            entries[c] = t | hf << 10 | vf << 11 | bank << 12
        if grown:
            notes.append('%s: %d new tiles (%d -> %d)' % (self.name, grown, self.ntiles, len(tiles)))
        raw = b''.join(self.pack_tile(t) for t in tiles)
        tail = self.data[self.off + self.ntiles * 32:]
        data = self.data[:self.off] + raw + tail
        if self.off:
            data = struct.pack('<I', len(data) - 4) + data[4:]
        m = bytearray(self.mapdata)
        for c, e in enumerate(entries):
            struct.pack_into('<H', m, 4 + 2 * c, e)
        return data, bytes(m), notes

    def _orig_block(self, cell):
        cx, cy = self._cellxy(cell)
        return [self.orig[cy + i // 8][cx + i % 8] for i in range(64)]


def erase(img, r):
    x0, y0, x1, y1 = r['x'], r['y'], r['x'] + r['w'], r['y'] + r['h']
    spec = r['erase']
    if spec == '-':
        return
    if spec.startswith('fill:'):
        v = int(spec[5:])
        for y in range(y0, y1):
            for x in range(x0, x1):
                img.px[y][x] = v
        return
    bad = {int(v) for v in spec.split(',')}
    todo = {(x, y) for y in range(y0, y1) for x in range(x0, x1) if img.px[y][x] in bad}
    # grow inward from the good pixels, ring by ring
    while todo:
        done = {}
        for (x, y) in todo:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < img.W and 0 <= ny < img.H and (nx, ny) not in todo and \
                        (img.px[ny][nx] not in bad or not (x0 <= nx < x1 and y0 <= ny < y1)) and \
                        img.px[ny][nx] not in bad:
                    done[(x, y)] = img.px[ny][nx]
                    break
        if not done:
            raise SystemExit('%s: erase cannot fill %d pixels' % (r['where'], len(todo)))
        for (x, y), v in done.items():
            img.px[y][x] = v
        todo -= set(done)


LINE = {'s': 9, 8: 9, 10: 11, 12: 13}   # line pitch for two-line labels (`a|b`)


def draw(img, r, glyphs):
    text = r['en']
    if not text:
        return
    if '|' in text:
        lines = text.split('|')
        size = r['font'].rstrip('b')
        pitch = LINE['s' if size == 's' else int(size)]
        cap = 7 if size == 's' else int(size) - 2
        total = pitch * (len(lines) - 1) + cap
        y0 = r['y'] + (r['h'] - total) // 2
        for k, line in enumerate(lines):
            sub = dict(r, en=line, y=y0 + k * pitch, h=r['h'] - (y0 - r['y']) - k * pitch)
            sub['h'] = min(sub['h'], pitch + 1)
            draw(img, sub, glyphs)
        return
    size = r['font'].rstrip('b')
    size = 's' if size == 's' else int(size)
    bold = r['font'].endswith('b')
    shadow = r['shadow']
    w, bm = glyphs.render(text, size, bold=bold)
    if bold and w + (shadow != '-') > r['w']:     # a tight bold label drops its drop shadow, then to regular
        if w <= r['w'] and not shadow.startswith('o:'):
            shadow = '-'
        else:
            w, bm = glyphs.render(text, size)
    # vertical box: cap top to baseline (descenders hang below it); the 12/10/8 fonts: their ink rows
    if size == 's':
        top, bot = 0, 6
    else:
        ink_rows = [i for i, row in enumerate(bm) if any(row)]
        top, bot = min(ink_rows), max(ink_rows)
    h = bot - top + 1
    pad = 1 if shadow != '-' else 0
    if w + pad > r['w'] or h + pad > r['h']:
        raise SystemExit('%s: %r is %dx%d px, rect %dx%d' % (r['where'], text, w + pad, h + pad, r['w'], r['h']))
    x = {'l': r['x'] + (1 if shadow.startswith('o:') else 0),      # the outline ring needs a column on the left
         'c': r['x'] + (r['w'] - w - pad) // 2 + (1 if shadow.startswith('o:') else 0),
         'r': r['x'] + r['w'] - w - pad}[r['align']]
    y = r['y'] + (r['h'] - h - pad + 1) // 2 + (1 if shadow.startswith('o:') else 0)
    ink = int(r['ink'])
    low = max((rr for rr in range(len(bm)) if any(bm[rr])), default=bot)   # lowest ink row (descenders)
    y = min(y, r['y'] + r['h'] - pad - (low - top + 1))                     # lift text whose tail would spill
    on = {(x + c, y + rr - top) for rr in range(len(bm)) for c in range(w) if bm[rr][c]}
    out = [(a, b) for a, b in on if not (r['x'] <= a < r['x'] + r['w'] and r['y'] <= b < r['y'] + r['h'] - pad)]
    if out:
        raise SystemExit('%s: %r runs out of its rect at %s' % (r['where'], text, out[:3]))
    if shadow.startswith('o:'):
        sv = int(shadow[2:])
        ring = {(a + dx, b + dy) for a, b in on for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - on
        bad = [(a, b) for a, b in ring if not (0 <= a < img.W and 0 <= b < img.H)]
        if bad:     # a negative index would wrap to the far edge of the image
            raise SystemExit('%s: %r outline leaves the image at %s' % (r['where'], text, bad[:3]))
        for a, b in ring:
            img.px[b][a] = sv
    elif shadow != '-':
        sv = int(shadow)
        for a, b in on:
            if (a + 1, b + 1) not in on:
                img.px[b + 1][a + 1] = sv
    for a, b in on:
        img.px[b][a] = ink


def edit_files(getfile, rows):
    """{name: (new tile bytes, new map bytes or None)}, notes."""
    glyphs = Glyphs(getfile)
    by_file = collections.OrderedDict()
    for r in rows:
        by_file.setdefault(r['file'], []).append(r)
    out, notes = {}, []
    for spec, rs in by_file.items():
        name, grid = split_name(spec)
        mname = name[:-5] + '.nbfs'
        mapdata = None
        if grid is None:
            try:
                mapdata = getfile(mname)
            except (KeyError, ValueError, FileNotFoundError):
                mapdata = None
        img = Image4(name, getfile(name), mapdata, grid)
        for r in rs:
            erase(img, r)
        for r in rs:
            draw(img, r, glyphs)
        data, m, n = img.save()
        notes += n
        out[name] = data
        if m is not None:
            out[mname] = m
    return out, notes


def files(rows=None):
    """Every NitroFS file the redraws may change (romcheck's CHANGEABLE)."""
    names = set()
    for r in rows if rows is not None else load_rows():
        name, grid = split_name(r['file'])
        names.add(name)
        if grid is None:
            names.add(name[:-5] + '.nbfs')
    return names


def apply(rom, log):
    rows = load_rows()
    if not rows:
        return 0

    def getfile(n):
        return bytes(rom.getFileByName(n))
    new, notes = edit_files(getfile, rows)
    for n in notes:
        print('gfx:', n)
    for name, data in new.items():
        old = getfile(name)
        if data == old:
            continue
        i, end = 0, min(len(old), len(data))
        while i < end:
            if old[i] == data[i]:
                i += 1
                continue
            j = i
            while j < end and old[j] != data[j]:
                j += 1
            log.append('%s %X %s %s gfx' % (name, i, old[i:j].hex(), data[i:j].hex()))
            i = j
        if len(data) > len(old):
            log.append('%s append %X gfx' % (name, len(old)))
        rom.setFileByName(name, data)
    return len(new)


# ---- previews -------------------------------------------------------------------------------------------------

def fs_get(n):
    return (FS / n).read_bytes()


def palette_for(name, pal=None):
    """RGB list: --pal file, the file's own .nbfp/.pb, or a grey ramp (index readable, colours not)."""
    for p in ([Path(pal)] if pal else []) + [FS / (name[:-5] + '.nbfp'), FS / (name[:-5] + '.pb')]:
        if p.exists():
            b = p.read_bytes()
            b = b[body_off(b):]
            return [((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31)
                    for v in struct.unpack_from('<%dH' % (len(b) // 2), b)]
    return [(255 - i * 17,) * 3 for i in range(16)] * 16


def to_png(img, pal, zoom=1, use_orig=False):
    from PIL import Image
    src = img.orig if use_orig else img.px
    im = Image.new('RGB', (img.W, img.H))
    for y in range(img.H):
        for x in range(img.W):
            v = src[y][x]
            im.putpixel((x, y), (0, 96, 96) if v == 0 else pal[(img.bank[y][x] * 16 + v) % len(pal)])
    return im.resize((img.W * zoom, img.H * zoom), Image.NEAREST) if zoom > 1 else im


def cmd_show(a):
    name, grid = split_name(a.file)
    m = None
    if grid is None and (FS / (name[:-5] + '.nbfs')).exists():
        m = fs_get(name[:-5] + '.nbfs')
    img = Image4(name, fs_get(name), m, grid)
    from PIL import ImageDraw
    im = to_png(img, palette_for(name, a.pal), a.zoom)
    d = ImageDraw.Draw(im)
    for x in range(0, img.W, 8):
        d.line([(x * a.zoom, 0), (x * a.zoom, (3 if x % 32 else 8) * a.zoom)], fill=(255, 0, 0))
    for y in range(0, img.H, 8):
        d.line([(0, y * a.zoom), ((3 if y % 32 else 8) * a.zoom, y * a.zoom)], fill=(255, 0, 0))
    out = a.out or str(ROOT / 'work' / 'gfx_show' / (Path(name).stem + '.png'))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    hist = collections.Counter(v for row in img.px for v in row)
    print(out, '%dx%d' % (img.W, img.H), 'tiles', img.ntiles, 'indices', dict(sorted(hist.items())))


def cmd_index(a):
    """Print the pixel indices of a rect (to pick ink / shadow / erase values)."""
    name, grid = split_name(a.file)
    m = fs_get(name[:-5] + '.nbfs') if grid is None and (FS / (name[:-5] + '.nbfs')).exists() else None
    img = Image4(name, fs_get(name), m, grid)
    x, y, w, h = map(int, a.rect.split(','))
    for yy in range(y, y + h):
        print('%3d ' % yy + ''.join('%X' % img.px[yy][xx] for xx in range(x, x + w)))


def cmd_preview(a):
    from PIL import Image
    rows = load_rows(a.groups)
    new, notes = edit_files(fs_get, rows)
    for n in notes:
        print('gfx:', n)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pals = {}
    for r in rows:
        if r.get('pal'):
            pals[r['file']] = r['pal']
    for spec in dict.fromkeys(r['file'] for r in rows):
        name, grid = split_name(spec)
        mname = name[:-5] + '.nbfs'
        m0 = fs_get(mname) if grid is None and (FS / mname).exists() else None
        a0 = Image4(name, fs_get(name), m0, grid)
        a1 = Image4(name, new[name], new.get(mname, m0), grid)
        pal = palette_for(name, PREVIEW_PAL.get(name))
        i0, i1 = to_png(a0, pal, a.zoom), to_png(a1, pal, a.zoom)
        im = Image.new('RGB', (i0.width * 2 + 8, i0.height), (255, 0, 255))
        im.paste(i0, (0, 0))
        im.paste(i1, (i0.width + 8, 0))
        p = out / (Path(name).stem + '.png')
        im.save(p)
        print(p)


# palettes for previews of files that have none of their own (found from VRAM dumps; the game picks them in code)
PREVIEW_PAL = {}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('show')
    s.add_argument('file')
    s.add_argument('--pal')
    s.add_argument('--zoom', type=int, default=3)
    s.add_argument('--out')
    s = sub.add_parser('index')
    s.add_argument('file')
    s.add_argument('rect')
    s = sub.add_parser('preview')
    s.add_argument('groups', nargs='*')
    s.add_argument('--zoom', type=int, default=3)
    s.add_argument('--out', default=str(ROOT / 'work' / 'gfx_preview'))
    a = ap.parse_args()
    {'show': cmd_show, 'index': cmd_index, 'preview': cmd_preview}[a.cmd](a)


if __name__ == '__main__':
    main()
