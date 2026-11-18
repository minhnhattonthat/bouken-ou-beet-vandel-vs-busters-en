# Graphics brief - Bouken-ou Beet: Vandel vs. Busters (NDS)

You redraw Japanese text drawn as graphics (menu captions, buttons, banners, windows, credits) in English for a fan
patch. Work only on the groups named in your dispatch, one at a time in the order given, each finished before the
next. Do all the drawing yourself; do not dispatch subagents.

## Read first
1. `docs/gfx-groups.tsv`: your group's rows (file, Japanese as read by the survey, what it is).
2. The pilot: `gfx/battle.tsv` (a BG screen with a map: caption tab, footer hints) and `gfx/buttons.tsv` (64x32 OBJ
   buttons, made by `tools/gfx_buttons.py`); the generator `tools/gfx.py` (its docstring is the row format).
   Copy the pilot's approach; don't invent another one.
3. `glossary.md` (read it in parts: offset/limit) and `docs/fonts.md`. Names exactly as in the glossary.
4. `$SKILL/references/graphics.md` §Edit and re-import, §Lettering.

## How
- `python -X utf8 tools/gfx.py show FILE[@N]` renders the image with a ruler (`work/gfx_show/<name>.png`); a `.nbfc`
  with a `.nbfs` twin is drawn through its map, others as a grid of N tiles per row (OBJ sprites: 32 tiles = `@8`
  (64x32), 64 tiles = `@16` (128x32), 16 tiles = `@4`; check the render isn't scrambled).
- `python -X utf8 tools/gfx.py index FILE x,y,w,h` prints the colour indices of a rect: pick the lettering's indices
  (they go in `erase`), the ink (darkest stroke) and the shadow from them.
- `python -X utf8 tools/gfx.py preview GROUP` writes original | English per file to `work/gfx_preview/` (palette: the
  file's own `.nbfp` or a grey ramp; the game picks most palettes in code, so judge shapes, not colours). Read
  every preview zoomed: every letter readable, nothing left of the Japanese, nothing touching a frame.
- The generator fails a row whose text doesn't fit its rect; the test `tests/test_gfx.py` fails any pixel changed
  outside the declared rects.

## You may write only
`gfx/<group>.tsv` for your groups. Don't edit `tools/gfx.py`, the build, `glossary.md` or another group's file;
don't run the build or an emulator; don't commit. If you need a generator change (a new font size, an OBJ layout the
grid can't show), describe it in your report.

## Style (one font per label class, as the pilot)
- Caption tabs (screen titles, top left): `s`, ink 15, shadow 13 (the pilot's `Battle Menu`). Buttons: `sb`, two-line
  labels `s` (`Party|Orders`). Field labels inside panels (攻撃 防御 命中 回避, Lv, 所持数 ...): `s`, the Japanese's ink,
  no shadow unless the Japanese had one. Windows' sentences (このモンスターを腹心にします): `s` or 10/12 if they fit,
  `|` for a second line.
- Most screens already carry the game's own English subtitle (PARTY MENU, EQUIP, HONE, FORCE ORDER, ...): leave
  it; use its wording for the caption where it fits (EQUIP -> `Equip`).
- Full words; no abbreviations to fit except standard stat ones (Lv, ATK/DEF if a column really has < 16 px). If
  something still won't fit, report it with the shortest wording you'd accept.
- UI words already used (keep them): 道具 Items, 隊列 Lineup, 戦術 Tactics, 特技 Skills, もどる Back, 決定 OK, 詳細 Details,
  装備 Equip, 情報 Info, 指示 Orders, パーティ Party, 軍団 Force, 名前 Name, はい Yes, いいえ No, ステータス Status,
  才牙 Saiga, 天撃 Divine Attack, 冥撃 Dark Attack, 技 Skills, 図鑑 Book (Buster Book, Monster Book, Vandel Book),
  取り込み Uptake, ならびかえ Sort, 種類 Type, 罠 Trap, セーブ Save, オプション Options, クエスト Quests, 武器 Weapons,
  防具 Armor, 貴重品 Treasure, はずす Remove, いれかえ Swap, 派遣 Dispatch, あきらめる Give Up, 完了報告 Report.
- Erase with the lettering's index list (keeps gradients/dither), never `fill:` over artwork.

## Report (your final message)
Per group: files done, files not done and why, new terms (`JP<TAB>EN`), generator changes you need.
