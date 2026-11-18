# Window budgets (width gate, phase 5)

Every box variant with its limit, **measured** (with the shot) or **guess** (to measure before translators get it).
Widths are pixels of the English engine (`tools/engine.py` `Engine.width(text, font)`; `tools/textwidth.py "text"`
prints them); byte limits are for fixed slots (pair codes: 2 bytes per code, usually two letters). The lint
(`tools/lint.py`, run by `tools/check.py`) reads the machine copy of this table, `tools/budgets.json`.
Tours: `work/qa/marker2` (2026-11-18, 100/100 ok, 966 ids seen; `tools/markerscan.py`, `tools/kindreport.py`).
Width tests: `tools/build.py --marker --out build/beet_qa.nds --qa ID=TEXT` (repeatable) + a warp. Extra cheats per
run: `--var "EXTRA='inv'" --var INV_CATS=4 --var INV_FROM=0 --var INV_N=34` (warp.lua appends EXTRA to the scene's
`set`, so further inputs go there too, e.g. a shop buy `EXTRA='t128,56 w120 t128,56 w120 a w120'`).

| Variant | Kinds | Font | Limit | Status / evidence |
|---|---|---|---|---|
| Dialogue box | rom `msg` | 12 | x starts at 8; lines 1-2 <= 240 px, line 3 <= 222 px (page arrow at ~x 232); 3 lines per page (`{br}`, `{page}`) | measured, `work/qa/p5_t2/f001250.png` (torture line; text past x 256 wraps onto the next row of the window buffer, so the limit is hard) |
| Dialogue message length | rom `msg` | - | <= 255 codes after `{hero}` etc. expansion (0x200-byte stack buffer, docs/re/vwf.md) | measured from code |
| Speaker tag | rom `speaker` | 12 | <= 64 px | measured: 64 px fits with ~8 px each side (`work/qa/p5_spk2/f001300.png`); 90 px and 120 px names are not drawn at all; 72 px drawn (glyph log x=10) but not seen in a shot |
| arm9 fixed slots | all `a9.<table>.*` | - | `max - 2` bytes (a 0000 must stay inside the slot) | measured: full slots ran into the next record |
| Item / weapon / armor list row | `item.name`, `weapon.name`, `armor.name` | 12 | <= 126 px (x 48, count digits from ~x 179; shop: x 46, MG price label ~x 200) and the slot (18 bytes = 9 codes, ~16-18 letters) | measured, `work/qa/p5_inv/final.png` (menu_items_all, `inv` cheat), `work/qa/marker2/shop_weapon_buy/final.png` |
| Item description (menus) | `*.desc` of item/weapon/armor/keyitem | 12 | one line, <= 194 px (box x 6-216, text x 16; a second row is off the box) | measured, `work/qa/p5_inv/final.png`; JP originals are <= 16 chars (192 px) |
| Shop description | weapon/armor `desc` | 8 | one line, <= 210 px (the 8 px loop wraps at ~x 222, the 2nd line is off screen) | measured, `work/qa/marker2/shop_weapon_buy/final.png`; the 12 px menu limit binds first |
| Battle shout | `shout.sNN` | 12 | one line, x 40, <= 204 px (box to ~x 248); slot 30 bytes | measured, `work/qa/p5_shout/f002460.png` |
| Battle party panel | `party.name` | 12 | <= 62 px (name x ~68, window edge ~136, longer names are clipped) | measured, `work/qa/p5_shout/f002460.png` |
| Monster book name / area | `monster.name`, `monster.area` | 12 | <= 120 px each (10-code canvases; longer text is clipped, not wrapped); slot cap max-2 (the old 16-byte cap came from mistaking the 属性 沼 for a stray glyph) | measured, `work/qa/p5_elem/final.png` (`--qa a9.monster.000.area=Byonrin Volcano Rui` clipped at ~x 186) |
| Monster attribute (属性) | `elem.name` (10 one-kanji names: 沼 窟 渦 砂 地 鉱 樹 極 骨 絶) | 12 | <= 18 px (2 letters): a tiny canvas at the top right; table relocated to 16-byte slots (`engine.RELOC`), so a wider canvas only needs the draw code (0x0208FF1C buffer +0x100, also 0x020654F8) | measured, `work/qa/p5_elem/final.png` (`Swamp` shows `Sw`) |
| Generic buster names | `name` | 12 | 14 bytes; <= 84 px jp-bound | slot size (status/bustername) |
| Not reached yet (jp-bound) | skills, tengeki/meigeki, key items, books (buster/vandel names), quests (`title`, `desc`), `quest` labels, area names, `special.name`, `title.name`, `wpntype.name`, `item/weapon.name2` | 12 | each kind's longest Japanese line at 12 px (the box holds it), listed in `tools/budgets.json` with status `jp-bound` | lists empty early in the story. Verify in phase 8 when the debug tool fills them. Found so far: weapons are in the inventory at save+0x11E0 ([id+1, 1, 0, 0], 99 slots), armor at save+0x136C ([id+1, 2, 0, 0]), items at save+0x10D8 ([id+1, 4, 0, count]); item ids >= 34 white-screen the item menu; key items are entries with byte1 & 3 in a u16 list read at 0x02076DC4 (not the item menu) |
| Not drawn | `*.reading` (hiragana sort keys, comparator 0x02023940 reads record+0x18), `buster.desc`/`vandel.desc` (all the placeholder 説明) | - | no width; readings get the English name so ならびかえ sorts alphabetically, placeholders stay | `not-drawn` in budgets.json |
| Menus / pointer strings | `ptr` | 12 / 8 | per string: in place, the old string's room (insert assert); no px budget yet (warning) | seen at 12/027C and 8/069C (title 通信 screens, b14) |
