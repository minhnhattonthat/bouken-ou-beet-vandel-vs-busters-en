# arm9 text and data tables

arm9.bin: 0x1B7CB8 bytes at RAM 0x02000000, **not compressed**, **no overlays**. Sections (ndspy): main 0x02000000
size 0x1B7620; ITCM 0x01FF8000 size 0x620; DTCM 0x027E0000 size 0x60. Module params footer `2106C0DE` in post-data.

## Tables with inline fixed-width text fields (guess: stride from string spacing; confirm field sizes in phase 4)
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
- System and wireless-play messages 0x021B4EC8-0x021B6CC2 (陣営を選択して下さい。, 通信エラーが発生しました。…),
  pointed at from code (e.g. 0x020DD818 → 0x021B573C).
- Scattered: 0x0211A6AC (さぁーて！！はじめようぜ！), 0x02121BD4, 0x02123400, and clusters at 0x0219B030, 0x021A9D04,
  0x021AA110, 0x021AAE9C (strings just before the path `/field/script/rom.img`), 0x021ADF44, 0x021AE554, 0x021B424C,
  0x021B60A4, 0x021B63A8. ~134 strings in all; can be repointed into new space.

## Free space for code and data (candidates, not yet proven)
- Append a new autoload block or grow arm9 (see `references/platform-nds.md` "Reserve hook RAM"); arena bounds must be
  raised. Not yet measured: BSS end and arena-lo. Phase 5.
