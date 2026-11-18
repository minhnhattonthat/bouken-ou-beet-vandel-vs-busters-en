# Window budgets (width gate, phase 5)

Every box variant with its limit, **measured** (with the shot) or **guess** (to measure before translators get it).
Widths are pixels of the English engine (`tools/engine.py` `Engine.width(text, font)`; `tools/textwidth.py "text"`
prints them); byte limits are for fixed slots (pair codes: 2 bytes per code, usually two letters). The lint
(`tools/lint.py`, run by `tools/check.py`) reads the machine copy of this table, `tools/budgets.json`.
Tours: `work/qa/marker2` (2026-11-18, 100/100 ok, 966 ids seen; `tools/markerscan.py`, `tools/kindreport.py`).
Width tests: `tools/build.py --marker --out build/beet_qa.nds --qa ID=TEXT` (repeatable) + a warp.

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
| Monster book area | `monster.area` | 12 | 16 bytes (copied through a 10-code buffer; 18 and 20 bytes drew a stray 沼) | measured (menu_monsters) |
| Generic buster names | `name` | - | 14 bytes | slot size (status/bustername) |
| Skills, tengeki/meigeki, key items, books (buster/vandel), quests (`title`, `desc`), area names, menus (`ptr`), `special.name`, `title.name`, 8x8 texts | many | 12 / 8 | **to measure** | not drawn in any tour scene yet: their lists are empty early in the story. Fill them like `inv` (find the save field by a diff, `tools/lua/ramsave.lua`) and add `*_all` scenes |
