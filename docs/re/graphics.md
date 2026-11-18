# Graphics text survey (phase 1)

Scope (D5): translate every graphic that carries Japanese text. The full per-file list is
**`docs/re/graphics-survey.tsv`** (sheet, file, text as read, what it is): 315 panels with text, **279 with Japanese**.
Regenerate it with:

    python -X utf8 tools/romls.py --unpack work/fs
    python -X utf8 tools/gfxsweep.py --fs work/fs/fs --out work/gfx     # 840 files -> 857 panels, 43 sheets, 0 skipped
    sh tools/gfxreview.sh work/gfx                                     # read-only codex review, 4 batches -> review_*.tsv

Review method: `codex exec` (read-only, images only), merged and deduplicated by file. Batch 2 (sheets 011-021) is
face portraits and item/saiga icons; it returned no rows, confirmed by reading sheet 020 by eye.

## Formats (verified by rendering)
- `.nbfc` BG tiles: 4bpp (8bpp when the palette has 256 colours); optional u32 size header (u32 == len-4).
- `.nbfs` BG map: u16 width, u16 height (tiles), then u16 entries (tile | hflip<<10 | vflip<<11 | palette<<12).
- `.nbfp` / `.pb` palettes: BGR555, optional u32 size header.
- `.ob` OBJ tiles (4bpp, 1D sprite order: grid renders of multi-tile sprites look scrambled), `.pb` its palette,
  `.ab` animation/cell data (shapes TBD, needed to unscramble OBJ text).

## Japanese graphics text by group (counts from the survey)
| Group | Files | Content | Source guess |
|---|---|---|---|
| `screen/*.nbfc` (+ `.nbfs`) | 228 | menu captions (パーティメニュー PARTY MENU…), buttons (もどる, はい/いいえ, 決定), confirmation banners, quest screens, options, name entry keyboard (かな 英字 記号 削除), shop, trap windows, wireless battle banners (`radio_battle_*`, scrambled) | raw tiles in NitroFS, edit + re-import (`tiles.py`) |
| `bg/credit01-19.nbfc` | 19 | staff credits (D3: translate to English) | raw tiles + map |
| `battle/cutin/*.nbfc` | 23 | character cut-ins; text present but scrambled in the grid render (attack names?) | needs the right map/cell data to read |
| `tengeki/skill_*.ob` | 8 | skill range/type tags: 全体 複数 単体 自分 攻撃 回復 弱体 強化 | OBJ tiles |
| `status/bitmap/main_char_v_parts3.ob` | 1 | 星 | OBJ tile |
| `screen/title.nbfc` | 1 | title logo: 冒険王ビィト + VANDEL VS BUSTERS + ヴァンデル バーサス バスターズ | the game has no official English logo; the English part already exists. Proposed: keep the art, replace the katakana subtitle line (non-blocking note in status.md) |

English-only UI graphics already present (no work): GAME OVER, HIT, ESCAPE, MG, TARGET, USER, SKILL, NAME ENTRY, OPTION…

## Not covered by the static sweep (must be covered by the phase-5 marker tour)
- Graphics banks in `.img` containers (format TBD): `battle/character/battlecharacter.img` (8.6 MB),
  `battle/weapon/battleweapon.img`, `battle/effect/battleeffect.img`, `battle/bgeffect/battlebgeffect.img`,
  `field/field/fieldfield.img` (8.7 MB), `field/object/object.img`, `world/character/worldcharacter.img`,
  `world/weapon/worldweapon.img`. Battle effect banks may hold attack-name or damage text.
- 3D textures `texture/*.tb` (only `miss.tb`: probably the "MISS" popup).
- OBJ text whose cell layout is in `.ab` files: grid renders are scrambled (cut-ins, `radio_battle_*`, `waiting_*`).
- Runtime-drawn text uses the font (`text.md`), not tiles.

**Done for phase 1:** every Japanese element found by the static sweep is a row in `graphics-survey.tsv`; the gaps
above are listed with reasons. The tour half of the survey (marker build, phase 5) adds rows for anything the banks
hold.
