# Text encoding and fonts

Dump: `rom.sha1`. Game code ABVJ, internal title `BEET(V-VS-B)`.

## Encoding (verified)
- **16-bit little-endian codes; code = font glyph index + 1.** Verified by decoding a known on-screen line: the first
  ship dialogue reads 「もう　少しだ！ / がんばれ！」 on screen (`work/qa/story2/f001200.png`), and its bytes in RAM
  (0x02275D90) and in `field/script/rom.img` @0xC88 decode to that with `tbl/jp.tbl`. Relative search found the RAM copy
  first (`relsearch.py ... がんばれ --width 2`, base 0x011B = ぁ).
- **Font glyph order = JIS X 0208 rows, with gaps closed:** font rows 0-7 = ku 1-8, font row 8 = ku 13 (NEC special
  characters ①②…), font rows 9-77 = ku 16-84 (all of level 1 and level 2 kanji). 78 rows x 94 = 7332 glyphs.
  Verified: kana (rows 4/5) and kanji (少, 島, 着岸準備, 船員) all decode right; `tools/mktbl.py` builds `tbl/jp.tbl`.
- `0x0001` = full-width space (glyph 0), `0x000A` = ！ (glyph 9). There is **no** newline in the glyph range.
- Shift-JIS appears nowhere in the game's text (textscan.py `sjis` hits are graphics noise).

## Control codes (from the decoded script; meaning = guess from context unless marked)
| Code | Meaning | State |
|---|---|---|
| `0x0000` | end of string | verified (every string ends with it) |
| `0xFF70` | line break inside a box | verified on screen (もう少しだ！ / がんばれ！ on two lines) |
| `0xFF72` | wait for input, then clear the box (new page) | guess: sits between pages of one speech |
| `0xFF71` | wait for input, close message (last page) | guess: last code before `0x0000` of every message |
| `0x5353` ("SS") | separator written before each string in script pools; the pointer skips it | verified: pointers target the byte after it |
| `0xFF00`-`0xFFFF` others | seen in arm9 tables (`0xFFFF` fill) and battle text (`[FF1E]`) | unknown, map in phase 4 |

## Fonts (`font/`, raw, no header)
| File | Glyph cell | Bytes/glyph | Glyphs |
|---|---|---|---|
| `lc12x12.bin` | 16x12, 1bpp, MSB-first, 2 bytes per row; glyphs use 12 px | 24 | 7332 |
| `lc10x10.bin` | 16x10, same packing | 20 | 7332 |
| `lc8x8.bin` | 8x8 1bpp | 8 | 7332 |
| `a8x8.bin` | 8x8 1bpp | 8 | 256 (ASCII-ordered; unused by script text, check in phase 5) |

`tools/fontsheet.py FONT 16 12 1 OUT.png --msb --first N --count 512` renders labelled sheets. The renderer looks
fixed-pitch 12 px (full-width cells); VWF is a phase-5 decision. Latin A-Z/a-z exist only as full-width glyphs (row 3).

## Where text lives (summary; details in `scripts.md`, `arm9.md`)
| Source | Strings (approx.) | How it is referenced |
|---|---|---|
| `field/script/rom.img` (358 KB, `scr\x1a`) | ~3,900 messages/names, ~86k chars | u32 file offsets in bytecode operands (`70 <u32>` message, `9E <u32>` speaker) |
| `quest/quest.img` (26 KB, `scr\x1a`) | ~630, ~7k chars | u32 operands of opcodes `20` (title), `1A`, `2D` (bodies) |
| arm9 fixed-record tables | ~4,000 fields | inline fixed-width fields inside structs (no pointer) |
| arm9 system messages 0x021B4EC8-0x021B6CC2 (+ scattered) | ~134 | u32 pointers (0x02xxxxxx) in code literal pools |
| `status/bustername/busterman.bin`, `busterwoman.bin` | 146 + 101 names | fixed 22-byte records |
| `kanakan.img` | name-entry kana→kanji dictionary | offset table at start (0x2E entries) |
| graphics | see `graphics.md` | tiles |

Not text (scan noise, checked): `enemy/enemy.bin`, `battle/*.img`, `field/field/fieldfield.img`, `.nbfs` maps,
`sound_data.sdat`, face/animation files.
