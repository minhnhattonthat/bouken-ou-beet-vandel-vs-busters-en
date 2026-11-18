# arm9 text and data tables

arm9.bin: 0x1B7CB8 bytes at RAM 0x02000000, **not compressed**, **no overlays**. Sections (ndspy): main 0x02000000
size 0x1B7620; ITCM 0x01FF8000 size 0x620; DTCM 0x027E0000 size 0x60. Module params footer `2106C0DE` in post-data.

## Record tables (verified 2026-11-18; extracted by `tools/arm9text.py`, config `TABLES`)
The game reads every record table through a leaf accessor `get(id) = base + (id - first) * size`
(`tools/a9tables.py` finds them all: 0x02014040-0x020146E0 plus 0x02020230). Text fields are fixed slots of u16 codes,
ended by 0000 or by the end of the slot. Fields (byte offset, slot limit) per table:

| Key | Base | Size x count | Text fields |
|---|---|---|---|
| armor | 0x0210D430 | 0xA0 x 71 | name 4-24, reading 24-44, desc 44-122 |
| shout | 0x0211A6AC | 0x168 x 81 | 11 battle shouts, 32 bytes each |
| party | 0x02121BD4 | 0x74 x 53 | name 0-20 |
| title | 0x02123400 | 0x4C x 130 | name 0-20 |
| keyitem | 0x0212AFE4 | 0x88 x 30 | name, reading, desc (as armor) |
| item | 0x0212BFD4 | 0xA4 x 34 | as armor + name2 132-152 (second display name) |
| monster | 0x0212D59C | 0x10C x 319 (0-based) | name 0-22, reading 22-44, area 44-66 |
| special | 0x02142390 | 0x24 x 36 | name 0-24 |
| skill | 0x021428A0 | 0x48 x 67 | name 0-20, desc 20-48 |
| tengeki / meigeki | 0x02143B8C / 0x0214591C | 0xB0 x 43 each | name 0-14 (7 chars), reading 14-40, desc 40-120 |
| vandel / buster | 0x021476AC / 0x0214AB78 | 0x1B4 x 31 / 51 (ids 0x13F.. / 0x15E..) | name 0-22, name2 22-44, desc 44-104 (説明 placeholder) |
| wpntype | 0x02150254 | 0x1C x 79 | name 0-20 (12 categories, then special weapons) |
| weapon | 0x02150AF8 | 0x438 x 254 | as item (name2 132-152) |
| area / area2 | 0x02193E08 / 0x02194B28 | 0x30 x 70 / 25 | name 0-24 |

Tables with no text: 0x02110090, 0x021152D4, 0x02119084, 0x0211A344, 0x02121894, 0x02125A98, 0x02129FA8,
0x0212AC74, 0x02193A88 (their "text" hits in scans are numbers). Slot `max` in `script/arm9/*.json` = original text
plus the zero bytes after it inside the slot. Readings (hiragana) are probably for sorting; check if displayed (phase 5).

## Old survey (phase 1; superseded by the table above)
| Range | Content (sample) | Record shape |
|---|---|---|
| 0x0210D402-0x02110022 | armour: 見習いのジャケット / みならいのじゃけっと / description | name 20 B, reading 20 B, description; record 120 or 140 B |
| 0x0211A6CC-0x02121874 | battle shouts: 行くぜッ！！, くらえェ！！ | 32-byte fields (some 40/64/72) |
| 0x02121C48-0x021222A8 | party characters: ビィト, ポアラ, キッス, スレッド, ミルファ, ゴラン | record 116 B |
| 0x021232F0-0x02125A54 | titles / affiliations: ヒーロー, ハーデンの配下, 黄金城 | ~76 B |
| 0x0212AFE8-0x02139FFF | items: シルバーチャーム / しるばーちゃーむ / レナからもらった銀のお守り | name 20 B, reading 20 B, description |
| 0x0213A000-0x02150B8E | monsters: 砂ふくろう / すなふくろう / area ビム砂漠 | name 22 B, reading 22 B, area, ... |
| 0x02157BFC-0x021925xx (many 0x438-byte blocks) | weapons: 鉄の槍 / てつのやり / 鉄でできた槍 | per-weapon block with name/reading/description |
| 0x02193E38-0x02194FB0 | area / dungeon names: ミュテリン山地, オーラン洞窟 | 48 B |

Readings (hiragana) are probably for sorting or the Buster Book index; check whether they are ever displayed.
**Engine risk:** English names longer than the inline fields (9-10 full-width characters in 20-22 bytes) need either
a narrower encoding (half-width/VWF codes packing 2 letters per code) or relocated tables with the readers patched.
Decide in phase 5.

## Pointer-referenced strings (verified: u32 pointers in literal pools)
Extracted: every 4-aligned word pointing at a clean string outside the tables (115 strings, `script/arm9/ptr.json`,
with the pointer words in `ptrs`), minus `arm9text.NOT_TEXT` (numeric words and the name-entry kana class lists at
0x021AE0C8-0x021AE34C). Messages use `[FF00]`/`[FF01]` parameters (appraiser: name, level / reward). Coverage test:
no run of kana outside the extracted slots, except 7 numeric words (`tests/test_extract.py` ARM9_WAIVED).
- System and wireless-play messages 0x021B4EC8-0x021B6CC2 (陣営を選択して下さい。, 通信エラーが発生しました。…),
  pointed at from code (e.g. 0x020DD818 → 0x021B573C).
- Scattered: 0x0211A6AC (さぁーて！！はじめようぜ！), 0x02121BD4, 0x02123400, and clusters at 0x0219B030, 0x021A9D04,
  0x021AA110, 0x021AAE9C (strings just before the path `/field/script/rom.img`), 0x021ADF44, 0x021AE554, 0x021B424C,
  0x021B60A4, 0x021B63A8. ~134 strings in all; can be repointed into new space.

## Free space for code and data (candidates, not yet proven)
- Append a new autoload block or grow arm9 (see `references/platform-nds.md` "Reserve hook RAM"); arena bounds must be
  raised. Not yet measured: BSS end and arena-lo. Phase 5.
