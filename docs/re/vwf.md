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
- Message expansion 0x0201F4A4 ({hero} etc., FF90-FF94; writes a 0000 after every code) has two callers:
  - dialogue 0x0204BE9C: frame 0x41C, buffer sp+0x1C..sp+0x41C = **0x400 bytes = 511 codes** + terminator. The game
    clears only 0x200 of it (`mov r2, #0x200` at 0x0204BF00, patched to 0x400 by `engine.SITES`); phase 6 wrongly
    read that memset as the buffer size (limit 255). Proven 2026-11-18: a 411-code, 12-page message (rom.4F468 put
    into rom.0213C, `work/qa/p7_long`) draws every page and the event carries on.
  - speaker tag 0x0204BDCC: buffer sp+0xC..sp+0x24 = 0x18 bytes = **11 codes** + terminator (longest English
    speaker: 7 codes). Lint: `engine.MSG_CODES`, `engine.SPEAKER_CODES`.
  - tag layout 0x02095008: window width w = 10 tiles (count < 6) else count + 5; text x = 4w - 6*count (+ 8*(13-w)
    in the [obj+0x10] = 0 branch at 0x02095314; the other branch at 0x020951C8 is the one dialogue tags use). Both
    `6*count` products are hooked to half the pixel width (`name_half`, `name_half2`); before the second hook tags
    drifted up to 7 px (2026-11-19, `tools/tagbox.py work/qa/p8_tag`: 11/11 centred after).

## English engine (`tools/engine.py`, tests `tests/test_engine.py`)
- Codes 0x2000-0x5FFF = letter pairs: `0x2000 + a*128 + b` (slots in `engine.LETTERS`: ASCII 0x20-0x7E then
  `…×♪★☆○●◎→←↑↓「」『』・※〜―`; b = 0 means a single letter). Pairs are formed greedily while the two widths
  (12 px font) sum to <= 16 px. A pair costs one code (2 bytes): about half the bytes of one-code-per-letter, which
  is what lets English fit the arm9 fixed slots and the 511-code message buffer.
- Letters = the game's own full-width Latin/punctuation glyphs from `lc12x12.bin` / `lc8x8.bin`, cropped to ink +
  1 px gap; space = 4 px (12) / 3 px (8). About 35 characters per 228 px dialogue line.
- Hook block (6.4 KB) = a new autoload section at 0x021C7EC0 (the old main-arena start; the arena-lo literal at
  0x020F97D8 is raised past it). Sites (`engine.SITES`, original bytes asserted at build time): both glyph fetch
  entries -> render English codes; the six advance calls -> pair width; typewriter x -> 8 + sum of widths of the
  line so far; the 19-code auto-wrap -> off (the script carries explicit `{br}`).
- Verified in game 2026-11-18 (`work/qa/p5_t1`, b03_village with `--qa rom.0213C=...`): proportional text, no
  clipping, page breaks and close work.

## Name entry (phase 5, session 3)
- The game already has a Latin keyboard: tabs かな / 英字 / 記号 (graphics buttons). Object (heap, e.g. 0x0225EF60):
  keyboard rows at +0xE0 + k*0x16 (18 rows of 10 codes, copied by 0x02029A14 from the arm9 strings 0x021AA0F8..;
  rows 0-5 kana, 6-11 `ＡＢＣ..ｕｖｗｘｙｚ`, 12-17 digits/symbols), **mode at +0xDC** (0 かな, 1 英字, 2 記号, 3 kana
  candidates; set by 0x0202A2F8, cycled by a button at 0x0202B2AC), max length at +0x364 (constructor 0x0202B6DC:
  8 for entry types 0/1/3, 10 for 2/4; type at +0xD8). Found by RAM diff (`tools/lua/objdump.lua`).
- Names are stored as full-width codes (Ａ = 0x00DD.., ａ = 0x00FD..). The hooks map those 52 codes to the single
  proportional letter (`engine.FW`, `fullwidth_code`) in both glyph fetches and in `wcode`, so a typed name looks like
  the English around it in the tag, dialogue and menus. Digits and symbols stay full-width (right-aligned number code
  counts 12 px per digit).
- `ne_init` (site 0x0202B6F0) makes the keyboard open on 英字. Proven 2026-11-18 (`work/qa/ne_m`, `ne_hero`,
  `ne_w`, `ne_w2`): 8 x W fits the speaker tag (it widens), `{hero}` in dialogue spaces right. The key cells now draw
  their letter at the cell's left edge instead of centred (polish).

## Numbers in messages (phase 9, session 26)
- 0x0201F7EC: int -> full-width digit string (`add r3, r1, #0xCC`, leading ０ skipped; static buffer 0x021BED14,
  returns a pointer into it). ~60 callers (status columns, shops, ...), which right-align with count x 12 px.
- Message formatter 0x0201F670 (varargs wrapper 0x0201F730, callers 0x02048804 / 0x02048944 = appraiser):
  FF00 = string arg, FF01 = int arg via `bl 0x0201F7EC` at **0x0201F6E8**. Quest expansion 0x02024D.. (switch on
  FFA0+): `{count}` via `bl 0x0201F7EC` at **0x02024E98**.
- Both bls -> engine `num_pc`: calls 0x0201F7EC, then rewrites 0x00CC..0x00D5 in the returned string as the
  single-letter pair codes of '0'..'9' (PC_D0 + d*128), so they draw and measure proportionally. Seen in game:
  `work/qa/p26_reward` ("Your reward this time is 100 Maggy."); status unchanged (`work/qa/p26_menu_status`).
