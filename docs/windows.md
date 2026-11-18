# Window budgets (width gate, phase 5)

Every box variant with its limit, **measured** (with the shot) or **guess** (to measure before translators get it).
Widths are pixels of the English engine (`tools/engine.py` `Engine.width(text, font)`); byte limits are for fixed
slots (pair codes: 2 bytes per code, usually two letters). Tour: `work/qa/marker` (`tools/markerscan.py`,
`tools/kindreport.py`), 100/100 scenes ok on the marker build.

| Variant | Kinds | Font | Limit | Status / evidence |
|---|---|---|---|---|
| Dialogue box | rom `msg` | 12 | x starts at 8; lines 1-2 <= 240 px, line 3 <= 222 px (page arrow at ~x 232); 3 lines per page (`{br}`, `{page}`) | measured 2026-11-18, `work/qa/p5_t2/f001250.png` (torture line; text past x 256 wraps onto the next row of the window buffer, so the limit is hard) |
| Dialogue message length | rom `msg` | - | <= 255 codes after `{hero}` etc. expansion (0x200-byte stack buffer, docs/re/vwf.md) | measured from code |
| Speaker tag | rom `speaker` | 12 | tag box is 80 px wide; a 120 px name vanished entirely | guess ~70 px; measure with a marker scene showing a long tag |
| arm9 fixed slots | all `a9.<table>.*` | - | `max - 2` bytes (a 0000 must stay inside the slot: full slots ran into the next record) | measured: marker tour before the fix drew `pa0ne...` followed by the next record's bytes |
| Monster book area | `monster.area` | 12 | 18 bytes (copied through a 10-code buffer) | measured: 20 bytes drew a stray 沼 after the text (menu_monsters) |
| Generic buster names | `name` | - | 14 bytes | slot size (status/bustername) |
| Item list, description, shop lists, quests, books, battle shouts, area names, menus | many | 12 / 8 | **to measure** | marker shots show overflow (item list name runs into the count column; item description wraps past its box) |
