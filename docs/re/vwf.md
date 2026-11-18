# Text renderer and the English engine (phase 5)

## The game's renderer (verified 2026-11-18: probes `tools/lua/{memread,vramwrite,glyphlog}.lua`, disassembly)
- Fonts are **not resident**: `CFontManager` (vtable 0x0219AC54) keeps file handles; per glyph it seeks the font
  file to `(code-1)*bytes` and reads one glyph. Loaded fonts: idx 0 `lc8x8` and idx 2 `lc12x12` (callers of
  0x02007FD4 pass 0 and 2 only); `lc10x10` is never loaded; `a8x8` via 0x02008014 (numbers, tile-aligned).
- Tables: bytes/glyph 0x0210D328 = [8, 20, 24]; size/advance 0x0210D32C = [8, 10, 12] (also the row count, and the
  line height in 0x020205C8).
- Glyph fetch: 0x02007910 (12x12: 12 rows x 2 bytes = **16 px per row**), 0x02007AA4 (8x8: 8 rows x 1 byte). Both
  expand MSB-first bits into a 3x3-tile 4bpp buffer at renderer+0x14 (pixels, colour nibble) and +0x134 (mask, F =
  transparent), renderer = [0x021BA3A4]. 0x02007A54 / 0x02007BE8 then shift it by x&7, y&7.
- Glyph draw at **any pixel x**: 0x020200B0 (12px), 0x020202A4 (8px) composite the 3x3 tiles into the window.
- String loops, each `draw; bl 0x02020230 (advance table[font]); x += [r0]`: 0x020201BC (12px, max count),
  0x02020240 (12px), 0x020204B0, 0x02020524 (8px, wraps at a pixel width), 0x020205C8 (8px, FF70 = new line),
  0x02020660 (8px). 0x020203B0 right-aligns numbers with count x advance.
- Dialogue typewriter 0x02022640..0x02022914, window object sl: +0x50 line-start index (u16), +0x54 column, +0x58
  line (3 per page), text inline at +0x5E or at [+0x64] (bit 0 of +0x5C). x = col*12 + 8, y = line*16 + 16, one
  char per call of 0x020201BC. Auto line break after 19 codes (`cmp r0, #0x13` at 0x02022884) unless the next code
  is FF70/71/72.
- Message expansion 0x0201F4A4 ({hero} etc., FF90-FF94) into a **0x200-byte stack buffer** (0x0204BEE0: sp+0x1C):
  a message may hold at most 255 codes after expansion.

## English engine (`tools/engine.py`, tests `tests/test_engine.py`)
- Codes 0x2000-0x5FFF = letter pairs: `0x2000 + a*128 + b` (slots in `engine.LETTERS`: ASCII 0x20-0x7E then
  `…×♪★☆○●◎→←↑↓「」『』・※〜―`; b = 0 means a single letter). Pairs are formed greedily while the two widths
  (12 px font) sum to <= 16 px. A pair costs one code (2 bytes): about half the bytes of one-code-per-letter, which
  is what lets English fit the arm9 fixed slots and the 255-code message buffer.
- Letters = the game's own full-width Latin/punctuation glyphs from `lc12x12.bin` / `lc8x8.bin`, cropped to ink +
  1 px gap; space = 4 px (12) / 3 px (8). About 35 characters per 228 px dialogue line.
- Hook block (6.4 KB) = a new autoload section at 0x021C7EC0 (the old main-arena start; the arena-lo literal at
  0x020F97D8 is raised past it). Sites (`engine.SITES`, original bytes asserted at build time): both glyph fetch
  entries -> render English codes; the six advance calls -> pair width; typewriter x -> 8 + sum of widths of the
  line so far; the 19-code auto-wrap -> off (the script carries explicit `{br}`).
- Verified in game 2026-11-18 (`work/qa/p5_t1`, b03_village with `--qa rom.0213C=...`): proportional text, no
  clipping, page breaks and close work.
