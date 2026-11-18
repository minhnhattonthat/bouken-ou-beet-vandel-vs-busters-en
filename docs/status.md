# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 8. QA in the emulator, in progress (phase 7 done 2026-11-18; phase-7 review fixes done 2026-11-19).
  Build sha1 9d8be14834b33334d9f6d3eca98b2015f7cd99cf (session 12; arm9 changed), check.py green (68 tests).
  **The tour work/qa/en is on the old build 50c319fb: re-tour + vqasheets + qa_gate before the final gate** (Next (1)).
  Left for the done-when: **text coverage** (7,534 shown + 111 waived of 9,472; quests now complete) and the
  Vandel-mode list (Next (4)).
- **Phase 8 session 12 (2026-11-19), Orca worker: quests done (637 -> 0 missing), two quest draw bugs fixed.**
  - Quest RE in `docs/re/scripts.md` §Quest boards: the board conditions `1C` test event-**seen** bits (warp `sNNN`,
    not `fNNN`); session 10's empty board came from skipping the slot setup `11 00 00`. Real counters: scenes
    `quest_counter` (rom 0x2AFC0) / `quest_counter2` (0x2AFA6) fill 3 random quests at the start of the game.
  - Fixed (seen in game, `work/qa/p12_qb6b5`, `work/qa/p12_gc3`): Quest Detail description and the board preview drew
    letter pairs at x = col*12 (overlapping / gappy) and auto-wrapped at 19 / 15 codes: `engine.SITES` 0x0207523C
    `qd_x`, 0x02074200 `qb_x` (+ wrap off). Deadline "No Deadline" -> "None" at x 8 (clear of the redrawn label).
  - New kind `brief` = quest.img `2D` (board preview, 180 px x 4 lines, `tools/budgets.json`; `extract.py
    QUEST_KINDS`, re-extracted with `--force`); `1A` stays `desc` (Detail, 216 px x 6). New `tools/rewrap.py KIND
    [--write]` re-fits a kind after a budget change (28 briefs re-wrapped, quest.0447C shortened by hand).
  - Coverage runs in work/qa/cover: `quest_00..03` (questloop `QUEST_REG=1`, 101 blocks with `17 <own pc>`),
    `quest2_00..01` (`QUEST_REG=2`, 41 with `15/16 <own pc>`), `quest3` (`QUEST_PCS={0x35F7,0x4BF3,0x5F83}`), all
    with `EXTRA='s6B' QUEST_NOREDIR=1 QUEST_ROW='-'` on quest_board; `qrand_quest_counter{,2}` (`tools/lua/randloop.lua`
    holds the board roll, 49 values). Sample sheets `work/qa/p12_quest_sheet.png`, `p12_quest2_sheet.png`,
    `p12_qrand_sheet.png`: all drew right. 10 unused blocks (0x4..0x1AF: no registration op, no reference) waived.
  - Coverage left (waivers on): weapon 380, rom.msg 278, name 256, skill 134, buster 132, meigeki 126, tengeki 108,
    ptr 94, keyitem 90, vandel 78, wpntype 68, special 30, party 28, area2 25, title 3 (a9 titles?), brief/desc 0.
- **Phase 8 session 11 (2026-11-19), Orca worker: map-table waiver, party sweep, area2 switch (context limit).**
  - Coverage report with waivers: `python -X utf8 tools/textcov.py report work/qa/en work/qa/gallery work/qa/cover
    --waive docs/text_unshown.tsv` (textcov now expands `prefix*` waiver ids; every waiver needs a reason and must
    match an id). Release must pass the same `--waive`.
  - `a9.title.*` waived (docs/text_unshown.tsv): the "title" table is the map table, its name a dev label never drawn
    (one accessor 0x0201419C, one table literal; callers 0x0203DF3C / 0x0204E35C read only fields 0x14-0x48).
    Note the 39 "shown" title records were only fetched by map loads, never drawn either.
  - Party names (accessor 0x020140DC, 1-based) are copied into the member struct when a member joins (call from
    0x02018D38 at new-game f952), and the menus draw from RAM. `tools/debug/idsweep.py` (new): one warp run per id,
    idloop forcing the first call; `--scene menu_status --acc 0x020140DC --ids 1-53 --out work/qa/cover/party`:
    the status screen then shows that record's name (id 2 -> "Beet", `work/qa/cover/party/002/final.png`).
    22 ids draw (1 2 B F 10 16-1F 2A-2E 34 35; strip `work/qa/p8_party_reset/ok_sheet*.png`). The other 31
    (3-A C-E 11-15 20-29 2F-33) **reset the game to the title** at f2316 as the hero record (exit 2), so they are
    moved to `work/qa/p8_party_reset/` and do NOT count (the report still says party 0 missing only while those runs
    were in cover/: now 31 missing). Next: force a later join instead (b29_my_castle joins id 5 at f1613, lr
    0x02018D38: `--var IDLOOP_AFTER=1600`) and show that member's status page.
  - Coverage now (waivers on): 6,912 shown, 91 waived, 2,469 failing (party 28: 3 of the reset ids are reached in
    other scenes); left: quest desc/title 637, weapon 380,
    rom.msg 278, name 256, skill 134, buster 132, meigeki 126, tengeki 108, ptr 99, keyitem 90, vandel 78,
    wpntype 68, party 31, special 30, area2 25.
  - Key items: the real accessor starts at 0x020141FC (`and r0,#0xFF`, falls into 0x02014200, so textlog's hook
    still fires); callers 0x02023994 0x020239A8 0x02023F48 0x02023F5C 0x02076DD0 0x02077060 0x02077E38 0x0207AFBC
    0x020BF4E0 0x020BFE68 0x020C019C. No tour scene holds a key item.
  - New probes: `tools/lua/callcount.lua` (every call of FNS with frame, lr, r0: when/how often a screen fetches),
    `tools/lua/memset.lua` (hold any RAM word, direct or [ptr]+off).
  - area2 (25): accessor 0x020146E0 is used instead of area when [[0x021BEDA4]+0xC] is not 0/1 (0x020D3084;
    0 in the Beet story). Holding it at 2 on field_nash makes the field board fetch 70 area2 ids
    (lr 0x020D30B8) but draws no names there (`work/qa/p8_area2/m2`). Next: find the screen that labels areas
    (what mode 2 is: GBA link / wireless / Vandel side?), else waive with that reason.
  - Skills (Saiga list, accessor 0x020142E0) are never fetched: the hero has none learned in any tour scene (the
    Saiga screen is empty); 23 BL callers (0x0205FF7C, 0x020A7628.., 0x020C864C..). Next: find the learned-skill
    list in the member struct and fill it (then the Saiga screen pages through them), same for tengeki/meigeki.
- **Phase 8 session 10 (2026-11-19), Orca worker: shout sweep, quest-board probe (context limit).**
  - Coverage report now: `python -X utf8 tools/textcov.py report work/qa/en work/qa/gallery work/qa/cover`
    (`work/qa/cover/` = probe runs that count). **6,892/9,472**; shouts complete (891/891).
  - `tools/lua/idloop.lua` (new): every call of one accessor gets the next id in r0 (append before textlog.lua).
    Shouts: v14_battle7 with `GOD_WIN=100000`, accessor 0x020140B0 (one caller, lr 0x020A55A4), ids 1..0x51
    (1-based: id 0 reads before the table and draws junk in the original too; the 0..0x50 run in
    `work/qa/cover/shout` plus `cover/shout_51`). Banners draw right with the matching portrait
    (`work/qa/p8_shout_shots/strip.png`, `work/qa/cover/shout_51/strip.png`). No contact sheets for the 81 yet.
  - Quests: scene `quest_board` (29BFA + q3C288) opens the guild counter menu (Appraisal / Take a Quest / ...);
    "Take a Quest" = t135,59 opens an **empty** Quest Select this early in the story. The board runs quest.img
    0x1144 (slot checks `11 00 00; 1C <flag> 00; 12; 06; ...; 03 <next slot>; 05 <quest pc>`; op 05 handler
    0x02013A14 calls 0x02003CE0(obj, pc) at 0x02013AE0; op 03 calls 0x02003E00). `tools/lua/questloop.lua`
    starts the interpreter at 0x115B and rewrites the 05 pc to each of the 152 quest blocks (`20` title right after
    an FF; the other 58 titles are inside the random generators 0x11F4..): QST lines appear for the title and
    description, **but the board still draws empty**, so those runs (`work/qa/p8_quests`) are NOT in work/qa/cover.
    Next: find what filters the added quest (the block's later ops 30/2F/2E/27/17, or the board's 5 slots of 0x58
    bytes at [obj+0x28], free when [slot+0x3C] == -1, filled at 0x02010E30) and make one row draw; then Details
    (t14,176) shows title + description.
  - Names: generic busters come from script opcodes 58/5A/5B (callers of 0x02019590); no tour scene makes one.
- **Phase 8 session 9 (2026-11-19), Orca worker: re-tour, verdict run 5, list/book coverage probes.**
  - Full re-tour on 50c319fb: 101/101 ok (`work/qa/tour_run.txt`), `tools/tagbox.py`: 160 tag shots, 0 off-centre.
    vqasheets + `qa_gate init` (2 stale v04/v05 sheet_2 lines dropped), verdict run 5 through codex
    (`work/qa/vqa_run5.txt`): 2 issues, both capture timing (empty box between pages / as an NPC talk reopens;
    the lines are drawn in the next shots): recheck ok in `work/qa/verdicts/recheck_main_6.tsv`. New scenes' sheets
    judged too. **`qa_gate check` exit 0, 171 sheets.** The message gallery was NOT re-run (its keys are original
    rom.img offsets, so coverage still holds; re-run it only if pages must be eyeballed).
  - textcov.py bug fixed: the weapon accessor (0x02014684) is `and r1,r0,#0xFF; sub r1,r1,#1` (ids 0x1nn) and the
    vandel/buster ones add a literal (first ids 0x13F / 0x15E): their TAB lines mapped to no record before. Test
    `test_tab_ids_map_to_records`.
  - warp.lua token `inv=OFF:CAT:FROM:N` (weapon region 11E0 cat 1, armor 136C cat 2; inventory byte = record+1).
    New scenes: `shop_wsell_1` (weapons 25-123), `shop_wsell_2` (124-173), `shop_asell` (all 71 armor),
    `menu_items_pages` (all 34 items), paged with R. Weapon records 0-24 (shields, 才牙光り/詠唱光り/天撃 effects,
    special weapons), 174-223 (プレイヤー/ヒーロー placeholder weapons) and 224-253 (named weapons, then character
    names) **hang the sell list** (screen fades, never draws): they need another screen (equip / battle / Vandel
    mode) or a waiver with that reason.
  - `tools/lua/bookloop.lua` + scene `book_monsters`: reopens the monster book 319 times with the start entry
    forced (r4 at 0x0202F108 -> [obj+0x48]); all 319 monster records covered, sheets ok. Buster/vandel: writing the
    table id (0x15E.. / 0x13F..) into the Info screen's list entry ([[ui+0x74]+0x4C] / [[ui+0x70]+0x40]) still
    draws an empty page (`work/qa/p8_bbuster`): the book has another check (registration bit or a different list
    format; the list may hold indexes, and the page draws from something else). Not solved.
  - Coverage now **6,075/9,472** (was 4,254): area/armor/item/monster/elem complete. Left: shout 814, weapon 380
    (records above), desc (quest.img) 427, title 301, rom.msg 278, name 256, skill 134, buster 132, meigeki 126,
    tengeki 108, ptr 99, keyitem 90, vandel 81, wpntype 68, party 48, special 30, area2 25.
- **Phase 8 session 8 (2026-11-19), Orca worker: verdict run 4 fixed, widows, tag centring (context limit).**
  - Verdict run 4's 13 issues fixed. Speaker tags: 里の門 now "Village Gate" (78 px); "Master" (橋かけ名人, 89 px in
    full), "Mirei Chief" (112 px) and area "Muterin Range" (119 px) kept as short forms with glossary notes
    (rechecks in `work/qa/verdicts/recheck_main_5.tsv`). Graphics: cut-left `button_detail`/`button_order` (only
    sprite x 32..60 is on screen) now font `s` in box x 32 w 28; shop 必要Lv. = "Req. Lv" (gfx/shops.tsv; the
    digit is 47 px in). Re-toured those scenes (work/qa/en, build 14508a33), run 5 verdicts all ok but one more
    widow, which led to:
  - **One-word last lines everywhere:** `lint.widow` (error: a page of 2+ lines ends on one word and the line above
    has 2+ words and no sentence end) + `batches.py unwidow [-v] [--write]` (moves the last word of the line above
    down when it fits; also run by `wrap()` on merge). 398 entries rewrapped (rom 343, quest 53, ptr 2), one
    reworded (rom.4CF10). Tests in tests/test_lint.py.
  - **Speaker tags off-centre** (`tools/tagbox.py work/qa/en`, new: inkbox on every shot with the tag, rect
    178,121,77,17 --ink 90,66,74): 81 of 148 off by up to 7 px. The tag x had a second `6*count` site at 0x020951C8
    (the branch dialogue uses); hooked with `name_half2` (docs/re/vwf.md). After: 11/11 centred (`work/qa/p8_tag`).
  - Coverage: `--debugger` makes no difference to textlog (same 80 TAB lines on menu_items_all), so drop it. The
    table gap is because list screens fetch only the visible rows: menu_items_all shows page 1/9 (4 items). Close it
    with scenes (or `EXTRA`) that page through each list (R / d-pad; check warp.lua's button tokens) and select each
    row for its description.
- **Phase 8 session 7 (2026-11-19), Orca worker: re-tour, message gallery, coverage probes, verdict run 4.**
  - Tour `work/qa/en` on bf77ae45: 101/101 ok (cold scenes in the first run, whose summary was lost to a crash; the
    9 save scenes + menu_quests re-run from `work/qa/beet_tour.nds`, same bytes, `summary_save.tsv`). Sheets
    `work/qa/vqa_en`, manifest re-initialised (156 sheets, 148 changed), chunks `work/qa/chunks/chunk_ac7f49ec0b5d_*`,
    verdict run 4 via `tools/visualqa.py` (log `work/qa/vqa_run4.txt`). `qa_gate check`: 153 sheets, all with
    verdicts, **13 not ok** (3 stale sheet_2 ids of scenes that now make one sheet were dropped from the manifest by
    hand; old copy `work/qa/manifest_stale.tsv`). To fix:
    - one-word last lines: b07_newbie "job...", b08_guild "reach...", b12_zena/sheet_2 "business!!", b20_lena_sleep
      "dreamland!", b27_golden_castle "splendor?", v09_charge/sheet_2 "Rings" (rewrap or reword those messages);
    - speaker tags vs glossary: "Gate" (Village Gate, v05/v11), "Master" (橋かけ名人 Bridge Master, b23), "Mirei Chief"
      (Mirei Forest Chief, v10); place "Muterin Range" vs Muterin Mountains (v05). Check the 80 px tag budget: if
      the full form does not fit, add the short form to the glossary note and record a recheck verdict;
    - graphics: "Orders" button (menu_orders/sheet_2 (1,3)) and "Details" button (menu_quests/sheet_2 (1,3)) clipped at
      the left screen edge; shop_weapon_buy "Required Lv" label overlaps the level digit 1.
    After fixes: rebuild, re-tour the changed scenes, vqasheets, `qa_gate init --build`, visualqa on the todo chunks.
  - **Message gallery** `tools/debug/gallery.py` + `gallery.lua` + `gallery_run.py`: every script string a `70`/`9E`
    op points at (4,100 of 4,120) goes through the real interpreter as a dialogue span (`2A` open, `9E`, `70`, `34`;
    a bare `70` draws nothing), fed at the loop's read points 0x0204E630 / 0x0204E6F4 after the opening's first
    message. 2,243 spans in 8 chunks into `work/qa/gallery/c<k>/` (g<NNNN>.png = first page). Runs under the JIT
    (no --debugger: 260 fps vs 12). It copies the ROM to `gallery.nds`: a shared Battery/beet_en.dsv made warp_all's
    writesave scene crash.
  - textlog.lua now also logs `QST <pc>` (quest.img interpreter, docs/re/scripts.md), `PTR <word>` (read watch on the
    146 ptr.json pointer words) and `NAM m|w <idx>` (generic buster name pick); textcov.py maps them, and `report`
    takes several dirs (`report work/qa/en work/qa/gallery`, converted logs in `work/qa/_textcov`).
  - Coverage with tour + full gallery: **4,254/9,472** (rom.msg 3,842/4,120). The 278 rom strings left: 129
    speaker+message pairs whose span was fed but whose 9E/70 handlers never logged (the pc of a 9E/70 in
    work/qa/rom_missing.txt's strings, e.g. 0x134CB-area span at 79051 = 0x134CB? check with GAL lines: maybe the span
    starts at an op the loop never reads, or a branch inside it), 20 reached only by quest ops 4F/99, 4 spans stuck
    (GALSTUCK 0x3B6B7 0x3BD3B 0x3C2D7 0x3C2EB in c6: likely choices/waits other than 34). (Earlier: 2,720.) Left
    besides: table records (weapon ~1012
    fields, monster 897, shout 770, title/desc = quest.img 637, name 256, buster 153, skill 134, tengeki/meigeki,
    keyitem 90, vandel 93, ptr 103). menu_quests logs no QST (no quests in the list that early).
- **Phase 8 session 6 (2026-11-19), Orca worker: element icons, coverage pipeline (tour killed for low memory).**
  - The 魔賓館 card element book icon is `battle/face/mon_<elem>_{l,m,s}.ob` (30 files, 24x24, 4bpp, @3; not
    mastery_icon, which holds weapon/element pictograms with no text). Redrawn with the elem.json short forms in the
    small font (`gfx/elemicons.tsv`, plate x 6 y 5 11x11, fill 1, ink 6); seen in game: `work/qa/p8_book2/zoom.png`
    (Ma / Ca). Survey rows added (sheet 041); gfxgroups 0 pending. gfx.py now reads 8bpp tile files (`path:8`).
  - So 0x02065504 (`elem_short`, six cells, list object vtable 0x021AA898 at [obj+0x78]+0x254) is NOT the card
    screen; it is a 6-monster list only reachable in real Vandel mode. Not yet seen. Tried: v04_castle_works reaches
    an idle field by f3000, but the party/status there is Beet's (the warp does not switch mode). v01 runs the real
    Vandel intro: name entry (OK = t235,176), then an epithet entry; mashing A loops back to the entry after Harden's
    "My epithet is..." line (top screen black). Needs a look at that loop (choice? touch to advance?), or the save
    byte that selects Vandel mode (diff a Vandel-mode battery save vs clear_save).
  - Text coverage: `tools/lua/textlog.lua` (exec hooks on the opcode 70/9E handlers 0x0205128C / 0x0204F630 and
    the 18 arm9 table accessors; needs `--debugger`, now `warp_all.py --debugger`) + `tools/textcov.py report
    LOGDIR [--waive F]` (writes `build/strings.tsv`, maps SCR pcs through the original rom.img, runs the skill's
    textcover.py, prints per-kind counts). Test `tests/test_textcov.py`. Not probed yet: quest.img (427 desc + 210
    titles), names.json (256), arm9 ptr strings (115). Table coverage is per record.
  - Tour `work/qa/en` (build bf77ae45, glyphlog + textlog) was killed by the system for low memory after 69 of ~101
    scenes. Coverage on those 69: 783/9472 shown (rom.msg 491/4120). Earlier sheets/manifest were deleted with
    the old work/qa/en; work/states/ for some scenes may be from an aborted run on the JP ROM (warp_all's default
    ROM is the original: always pass build/beet_en.nds). Re-run warp_all with --jobs 2 (memory).
  - inkbox: the only font-drawn centred text is the speaker tag (choices/menus are gfx.py buttons, centred by
    construction); measure the tag rect on a tour dialogue shot, then run inkbox over every tour shot with a tag.
- **Phase 8 session 5 (2026-11-19), Orca worker: elem.name engine work (handed back at the context limit).**
  - Monster book 属性 value in English, seen in game (`work/qa/p8_elem/zoom.png`; longest "Severance" via
    `--qa` in `work/qa/p8_elem_long`): the window comes from a stack rect built at 0x0208F7BC (x 25 y 3 w 2 h 2) and
    passed to the rect helper 0x0202BFDC; `engine.SITES` 0x0208F7D0 -> `elem_rect` stub sets `engine.ELEM_WIN`
    (x 23 y 5 w 9: 72 px at (184, 40), one row under the Element label, right of the HP digits). The label graphic is
    unchanged. Budget elem.name 72 px; keep_jp TEMPORARY lines and `batches.DEFER_KINDS` entry removed.
  - Second caller 0x02065504 = Vandel-mode status screen (`screen/v_status_base`): six 2x2-tile cells (windows
    25-30 at x 1/6, y 14/16/18) one element each. `elem_short` + 0x0206551C -> 8 px loop 0x02020660 draw the new
    `short` field of script/arm9/elem.json (Ma Ca Wh Sa Ea Or Tr Ul Bo Se; `engine.ESHORT_SLOT` table, lint checks
    <= 16 px at 8 px, tests/test_lint.py). **Not yet seen in game**: no scene reaches the Vandel status screen (warps
    to v01 / mhall end in dialogue; needs an idle Vandel-mode field scene + `start t18,40 t210,62` or similar).
  - Found a graphics-text gap: the 魔賓館 monster buy cards show the element as a kanji inside a yellow book icon
    (`work/qa/p8_eshort/zoom.png`); it is a sprite, not font text. Likely `bitmap/mastery_icon.nbfc` (3328 bytes,
    `.nbfp` 512 bytes = 256 colours, so 8bpp: 13 icons of 16x16; also `status/bitmap/mastery_icon.ob`). gfx.py is
    4bpp only. Not in the graphics survey; add a row, redraw with the short forms (glossary §Graphics UI labels).
  - New probes: `tools/lua/windump.lua` (window structs), `tools/lua/winlog.lua` (window inits / rect helper args /
    `WIN_WATCH` write watch), `tools/lua/execlog.lua` (`EXEC_AT={..}`, needs `--debugger`). Ruling D9 recorded.
- **Phase 8 session 4 (2026-11-19), Orca worker: last graphics, re-tour, verdict run.**
  - Graphics survey closed: `tools/gfxgroups.py` lists 0 pending. Credits (19 panels, `gfx/credits.tsv`, codex via
    gfxagent; provisional name readings in its comments) seen in game on the `credits` warp, all panels clean
    (`work/qa/p8_credits/crops*.png`). By hand: radio win/lose/draw banners (YOU|WIN!, YOU|LOSE, D|R|A|W, new font
    scale `sx3`/`sx4` in gfx.py; wireless only, no warp), skill-type tags Atk/Buff/Weak/Heal, body-part buttons,
    ★ for the 8x8 星 mark (glyph added to smallfont), Vandel House tab without shadow. `gfxgroups.SKIP` records
    files with no text (all 23 cut-ins: portraits only; tengeki arrows; main_v_parts is Latin "BL") and the kept
    title logo (D5).
  - Build sha1 41aad77da2470fb3728585b046af3131c908042a (after the fixes below). Full tour `work/qa/en` 101/101 ok on
    the build before them; v14_battle7 + credits re-run on this one. `qa_gate.py check work/qa/manifest.tsv
    work/qa/verdicts`: 155 sheets, all with verdicts, **1 not ok: menu_monsters/sheet_2 (沼 element value, below)**.
    Run 3: 48 ok, 104 issue, 101 of them the title logo only (accepted under D5 in `verdicts/recheck_logo_3.tsv`;
    `docs/visual-qa-brief.md` now says so). Fixed: orphaned "expenses..." page in rom.4B7F8; stale
    v06_wrong_way/sheet_2 manifest line (that scene now has one sheet). Main-thread rechecks
    (`verdicts/recheck_main_4.tsv`): "Ribenin Lake" was a misread (crop reads Riberin), "Mirei Village" is the 96 px
    area.name short form (glossary note added).
  - gfx.py: font 10/12 `j` overlaps its hook under the previous letter ("Ko ji" gap in the credits).
  - Not yet set up: `textcover.py` (needs `build/strings.tsv` from the build and a `TEXT <addr>` log line from a
    text hook, e.g. in glyphlog.lua or a new probe) and `inkbox.py` on choice/centred boxes.
- **Phase 8 session 3 (2026-11-19), Orca worker: graphics waves.**
  - Waves via `tools/gfxagent.py` (codex): menus, windows, shopbuttons, shops, radio, info, title, obj, nameopt all
    merged; agents' reports in `work/gfx_agents/<group>.md`. Build sha1 e36a3686a71980fa832391ad958f6f53656eac0d,
    check green, smoke ok; title buttons Story / GBA Link seen in game (`work/qa/p8_title/final.png`). Everything else
    not yet seen in game: re-tour + visualqa. Watch: radio adds 19 tiles to the party menu BG (VRAM budget); info uses
    回避 Evasion where menus use Evade (unify in the polish pass, glossary has no row).
  - Fixed by hand: menus pending (Quick Cmd., Mastery, Gear, tactics plates Arms/Strike/Heal/Guard/Divine/Dark; short
    forms in glossary §Graphics UI labels); 昇格値 battle-result banner = `screen/exp.nbfc` (Rank|Pts, gfx/battle.tsv;
    found with `warp.lua` `DUMP_AT={..}` + `vramfind.py --fmt gba4 --lo A0000 --hi E0000` on work/fs/fs).
  - `gfx.py`: `path@WxH` = sprites of WxH tiles side by side (the 64-tile shop buttons are two 64x32 OBJs: @8x4); `-`
    in `en` = erase-only row (editors strip a trailing tab); outlined left-aligned text no longer wraps its ring.
  - Still pending: body-part buttons `button_v_*` (map files, scrambled), `main_v_parts` 星 Star (16x16),
    party_order2 sort strip, cutins (23, scrambled: cell data), credits (19, whole panels), title logo katakana line.
  - Verdict run: 150/152 sheets have verdicts (missing v17_noah, v18_last); 136 issue, nearly all graphics text, so
    re-tour + re-verdict after the graphics land. "Vandels." one-word line already fixed in the script (tour was older).
    "Resist. D" stays: the speaker tag is 80 px and "Resistance D" is 85 (glossary note).
- **Phase 8 session 2 (2026-11-19), Orca worker: graphics pipeline + pilot.**
  - `tools/gfx.py` + `gfx/*.tsv` (row format in its docstring), wired into `tools/build.py` and `tools/romcheck.py`
    (writes logged, CHANGEABLE = files the rows name); `tests/test_gfx.py`; notes in `docs/re/graphics.md` §Redraw
    pipeline. Narrow label font `tools/smallfont.py` (font `s`/`sb`, drawn for the project; `docs/fonts.md`).
  - Pilot done and seen in game (zoomed cold-boot warp `b14_idiot`, `work/qa/p8_battle2/z.png`): `gfx/battle.tsv`
    (バトルメニュー caption, ターゲット/ポーズ footer) and `gfx/buttons.tsv` (57 OBJ buttons, from
    `tools/gfx_buttons.py` LABELS: battle 道具/隊列/戦術/特技 are sprites, not the BG). Only the battle buttons and caption
    are confirmed in game so far; the other buttons need a shot on their screens (menu_* warps). UI words: glossary
    §Graphics UI labels.
  - Remaining: 221 survey rows in 11 groups, `docs/gfx-groups.tsv` (`tools/gfxgroups.py` regenerates it, dropping
    files already in gfx/*.tsv): menus 39, shopbuttons 30 (64-tile shop buttons @16, v_* body-part buttons have
    their own .nbfs), radio 24, cutins 23 (scrambled: need the cell/map data first), windows 22, shops 21,
    credits 19, title 16, obj 14, info 9, nameopt 4. Brief `docs/graphics-brief.md`; runner
    `python -X utf8 tools/gfxagent.py GROUP.. --jobs 2` (codex exec, workspace-write, writes gfx/<group>.tsv only;
    check `git status` after). After each wave: preview, build, warp each screen for a zoomed shot.
  - Visual-QA verdict run of chunks 004-025 was running in the background at the end of the session
    (`work/qa/vqa_run2.txt`; 23 verdict files by then, 13 ok / 125 issue, nearly all graphics text). Text issues
    from it: area.name short forms Norunaji Wood / Byonrin Mt. are fits for the 96 px label (now noted in the
    glossary); still open: "Vandels." one-word last line (b13_vandel_fight sheet_2 (1,4)), "Resist. D" vs glossary
    Resistance (v09_charge sheet_2 (1,4)), 昇格値 battle-result banner (not in the survey: find its file),
    `mode_begin.nbfc` はじめから (survey had '?').
  - `menu_main` warp exits 2 (Lua error) when run alone with `--frames 900`: use warp_all's settings.
- **Phase 8 session 1 (2026-11-19), Orca worker:**
  - Phase-7 review fixed: `tools/romcheck.py` now checks the ROM header (invariant bytes vs the dump, regenerated
    offset/size words vs the image, header CRC; test zeroes the ARM9 entry); `lint.glossary_check` makes glossary
    Avoid spellings errors in any case and across `{br}` (Sealing Ring / Rank Points restored in rom.07B00 08944
    03B54). `lint --terms` lists 483 entries whose glossary term English is missing (mostly paraphrase/plural, e.g.
    戦士団 -> "squad"; audit them in the polish pass, not errors).
  - Tours: English `work/qa/en` 101/101 ok (with `glyphlog.lua`; `markerscan.py`: font-drawn Japanese only 沼 (elem)
    and the full-width A-Z keyboard keys), original `work/qa/tour_jp` 100/101 (clear_save fixture writer timed out,
    not needed). Full-size sheets: `python -X utf8 tools/vqasheets.py work/qa/en work/qa/vqa_en` (and tour_jp ->
    vqa_jp); manifest `work/qa/manifest.tsv` (152 sheets, `--build` recorded; re-run tours + vqasheets + init after
    every rebuild).
  - Visual QA via `tools/visualqa.py` (codex exec, read-only, sheets attached with JP twins; brief
    `docs/visual-qa-brief.md`). 24 of 152 sheets have verdicts (chunks 000-003): 5 ok, 19 issue, all but two are
    graphics text (title logo katakana, title バスター/もどる buttons, copyright, battle header バトルメニュー,
    道具/隊列/戦術/特技 buttons, ターゲット/ポーズ footer, 昇格値 banner). The run of the other chunks was stopped by the
    system for low memory. Resume: `qa_gate.py todo work/qa/manifest.tsv work/qa/verdicts --size 6 --out-dir
    work/qa/chunks`, then `python -X utf8 tools/visualqa.py <new chunk files> --en work/qa/vqa_en --jp work/qa/vqa_jp
    --jobs 2` (lower jobs if memory is short). Note: the build changed since the tour (quote fix), so re-tour before
    the final gate.
  - Fixed from verdicts: ASCII `"` always drew the closing ”; `engine.OPEN_QUOTE` now draws an opening one as “
    (new letter slot; seen in game, `work/qa/p8_quote/bot.png`); one-word last line in rom.0D434.
- **Next (phase 8), in order:** (1) done in session 9 (re-tour + verdicts, gate green). After any later build
  change: re-tour (`python -X utf8 tools/debug/warp_all.py build/beet_en.nds --jobs 2 --out work/qa/en --script
  tools/lua/glyphlog.lua --script tools/lua/textlog.lua`; `book_monsters` needs `--script tools/lua/bookloop.lua`
  too: run it with `--only book_monsters`), tagbox, vqasheets, `qa_gate init`, todo `--size 6`, visualqa;
  (2) coverage, biggest first (shouts done in session 10, quests in session 12; report over work/qa/en
  work/qa/gallery work/qa/cover with `--waive docs/text_unshown.tsv`):
  names (force r0 at 0x02019608), skills/tengeki/meigeki (skill menu / tactics lists, page them), buster/vandel books
  (session 9 note), key items (screen unknown: u16 list at [ui+0x118]), the weapon records that hang the sell list,
  rom.msg 278 (session 7 note). Then waivers with reasons in `docs/text_unshown.tsv`. Earlier notes: `python -X utf8 tools/debug/gallery_run.py` (if not complete: `--only K`), then
  `tools/textcov.py report work/qa/en work/qa/gallery --list`; close the table gaps with list scenes that fill the
  data first (weapons/armor via `inv` + INV_CATS 1/2 in the shop sell lists, monster/buster/vandel books with every
  registration bit set, skills); quests and names need the random pick forced (quest board 4F at 0x3C288; name
  index r0 at 0x02019608, docs/re/scripts.md); waive only what is shown unreachable in `docs/text_unshown.tsv`
  (ptr.comm = wireless partner, ptr.gba = GBA game in slot 2, ptr.keyboard = kept Japanese by design); lists fetch only
  their visible rows, so page through them (session 8); (3) inkbox: speaker tags fixed and checked by tagbox.py
  (above), choices/menus are gfx.py buttons (centred by construction); (4) the Vandel-mode list screen
  (0x02065504, above); (5) `qa_gate check` exit 0 on the final build. Graphics: all survey rows done or in `gfxgroups.SKIP`; zoomed in-game shots still to take
  for wave-3 screens not yet warped (radio screens need a wireless partner: note as unreachable).
  Open items carried into phase 8:
  - `elem.name`: done in session 5 (above); leftovers are in Next (1). Also seen: the longest monster name (119 px,
    "Crimson Nightmare") in the 120 px name window (x 48) would end at x 167, ~3 px under the Element label (x 164):
    check one such entry in the book during the re-tour.
  - Polish list from phase 5 (below) and `docs/polish.md` (review minors, all unticked lines must be done by phase 9).
- **Phase 7 session (2026-11-18), Orca worker, no subagents:**
  - The "255-code" limit was a misreading: the dialogue expansion buffer is 0x400 bytes (frame 0x41C, sp+0x1C), the
    0x200 was only the memset, now patched to 0x400 (`engine.SITES` 0x0204BF00). Limit 511 codes
    (`engine.MSG_CODES`); speaker tags go through a second, 12-code buffer (`engine.SPEAKER_CODES` = 11, lint
    checks both). Proven in game: 411-code, 12-page message (`work/qa/p7_long`). docs/re/vwf.md updated.
  - Merged the 3 deferred appraiser messages (`docs/long-messages.tsv` now empty) and the 24 review suggestions that
    had been blocked by the old limit (`tools/review.py apply bNNN --only id,...`; polish.md lines ticked, 27 incl.
    three translator CUT notes). Do not run `review.py apply` without `--only` on a reviewed batch: it re-applies
    every suggestion over hand fixes (Sealing Ring spellings).
  - `tools/romcheck.py` (per NitroFS file; a whole-image romdiff is meaningless after ndspy re-lays files): only
    arm9, rom.img, quest.img and the two buster-name files may change; every changed byte is behind a logged write
    whose original bytes match the clean dump, no overlaps or overwritten writes, appends past the old end,
    relocated pointer strings leave no un-repointed word. `engine.patch_arm9` now logs every write (sites, module
    params, arena literal, reloc literals, pointer words) as `arm9 OFF ORIG NEW what`. Tests:
    `tests/test_romcheck.py` (synthetic failures + the real English build), wired into `tools/check.py` via pytest.
  - Lint: `script/keep_jp.txt` (99 ids with reasons: 82 説明 placeholders, 7 kana-keyboard rows, 10 elem.name
    TEMPORARY); any other entry with Japanese and no English, or a stale keep line, is an error.
- **Phase 6 session 2 (2026-11-18):** review run for b021-b051 finished (`--jobs 3`, memory) and applied; NEW TERM
  reports merged (missing ones added to glossary Terms: 封印のリング Sealing Ring with "Seal Ring" in Avoid, so lint
  now errors on it; エルファスト Elfast; 網膜鑑定 retinal appraisal; 昇格値 Rank Points); all 31 "Seal Ring"/lower-case
  lines fixed one by one in the batch outputs. Bugs fixed: `review.py suggested()` kept a literal "suggested EN:"
  prefix (6 lines, now stripped, `tests/test_review.py`); `review.py apply` merges without `--defer-long`, so a
  batch with a deferred message (b032) never merged: after any apply run
  `python -X utf8 tools/batches.py merge b001 ... b051 --defer-long`. New `tools/review_left.py`: Critical/Important
  findings neither applied nor in polish.md (prints `left: 0` now). Lint 0 errors, 9,369 / 9,472 translated
  (3 deferred dialogue + not-drawn/kept kinds). Build `build/beet_en.nds` sha1 3ebdce16512c246d842fb68fab4966e5423d3e65,
  smoke ok.
- **Phase 6 session 1 (2026-11-18), Orca worker, no subagents: translation and review run through `codex exec`.**
  - Done: `docs/synopsis.md` (codex read of the whole script: file -> chapter map, plot of both stories, cast and voice
    guide), `glossary.md` (rulings, ~270 binding terms, generated "Names from the game tables" section via
    `tools/glosstables.py`), `docs/translator-brief.md`, `docs/reviewer-brief.md`.
  - Tools: `tools/batches.py` (split / prompt / check / merge / wrap / status; one row per distinct (kind, jp), the
    merge writes every copy; dialogue is written as prose and wrapped to the box by `wrap()`; readings filled from
    names; `--defer-long`), `tools/codex_run.py` (parallel translate + check + 2 fix rounds), `tools/review.py`
    (review via codex, `apply` puts Critical/Important suggested EN in line by line and keeps width-failing ones out,
    Minors + blocked fixes -> `docs/polish.md`), `tools/mkpolish.py` (translator CUT lines -> polish), `tools/dumpstory.py`.
    Batch files, prompts, outputs, reviews: `work/tr/` (gitignored; b001-b017 tables, b018-b051 dialogue).
  - Tables b001-b017 reviewed and fixes applied in session 1.
  - Budget changes: speaker tag 64 -> 80 px (8 x W name drawn in `work/qa/ne_w2`); lint lets every multi-line kind
    (desc, ptr.msg) re-wrap, not only msg.
  - Deferred: 3 appraiser tutorial messages (rom.169D8 16CA8 17450; 1711C now fits after review) need ~350 codes > the 255-code expansion
    buffer (docs/re/vwf.md: 0x200-byte stack buffer at 0x0201F4A4 / sp+0x1C); English kept in
    `docs/long-messages.tsv`. Phase 7: enlarge the buffer (static buffer in the hook block), then merge them.
    `elem.name` (10 属性 kanji) not translated: 18 px canvas, widen the draw code first (`batches.DEFER_KINDS`).
  (`tools/build.py` default = English from `en`, `--identity` = dump, `--marker`, `--qa ID=TEXT` overrides one entry.)
- **Phase 5 session 3 (2026-11-18):**
  - Name entry: the game already has an 英字 (A-Z a-z) tab; `ne_init` (engine.SITES 0x0202B6F0) opens the keyboard on
    it, and the hooks draw/measure the full-width Latin codes names are stored in as proportional letters
    (`engine.FW`, `fullwidth_code`). Max 8 letters (10 for entry types 2/4). 8 x W fits the speaker tag and spaces right
    in dialogue (`work/qa/ne_w2`). Lint stand-ins: `{hero}`/`{vandel}` = 8 x M (80 px), `{name93}` 10. RE in
    `docs/re/vwf.md` §Name entry; RAM-diff probe `tools/lua/objdump.lua`; warp.lua namentry scenes take `@FRAME`
    inputs (type a name, 決定 at t243,176).
  - Pointer strings: kinds `ptr.<group>` (`arm9text.PTR_GROUPS`: msg, speaker, label, line, comm, gba, keyboard).
    Over-long strings are relocated into the hook block (`engine.relocate_string`, pointer words repointed; tested,
    and seen in game). Budgets: comm 128 px at 8 px (box wraps by itself at ~130, mid-word), gba 212 px at 12 px,
    measured; msg/speaker reuse those budgets; label 84, line 180 jp-bound. `ptr.keyboard` (kana keyboard + kana list)
    is never inserted (`insert.KEEP_KINDS`; lint error if `en` set).
  - `jp_left.py --orig` on the marker build: only old copies of relocated pointer strings (unreferenced), the kana
    keyboard, name-entry kana class lists and code noise. For phase 9 pass the relocated list as `--known` or use
    `--slots`.
- **Phase 5 so far (2026-11-18):**
  - Font decision made and proven in game: VWF with **letter-pair codes** (0x2000 + a*128 + b), letters cropped from
    the game's own full-width Latin glyphs, rendered by an arm9 hook block (new autoload section at 0x021C7EC0,
    arena-lo raised). ~35 chars per dialogue line. RE + design: `docs/re/vwf.md`; code `tools/engine.py`; tests
    `tests/test_engine.py`. Glyph torture line (all ASCII, `…×♪★`, double spaces) renders right
    (`work/qa/p5_t2/f001250.png`). Speaker-tag centring patched (0x02095314) but not yet seen in a shot.
  - Inserter `tools/insert.py`: rom.img/quest.img in place or append + repoint refs; names; arm9 slots (max-2 bytes,
    `KIND_CAP`); arm9 pointer strings in place only (relocation still to do). Marker mode = `[id]` + filler.
  - Marker tour: `python -X utf8 tools/debug/warp_all.py build/beet_marker.nds --jobs 6 --out work/qa/marker
    --states work/states_marker --script tools/lua/glyphlog.lua` (warp_all got `--script`), then
    `tools/markerscan.py work/qa/marker` (Japanese still drawn, ids seen, draw sites) and `tools/kindreport.py
    work/qa/marker/scan_ids.tsv` (per kind: seen, site, x). Last run: 100/100 ok, 966 ids seen, Japanese left only
    in name entry (kana keyboard) and one stray glyph (fixed by `KIND_CAP`, not re-toured).
  - Budgets: `docs/windows.md` (evidence) + `tools/budgets.json` (lint data). Measured 2026-11-18: dialogue,
    speaker tag (64 px), item/weapon/armor list rows (126 px + 18-byte slot), descriptions (one line, 194 px at
    12 px; shop 8 px 210 px), battle shouts (204 px), battle party panel (62 px), monster area (16 bytes).
  - Lint `tools/lint.py` (Japanese left, encodable, controls JP==EN, slot caps, 255-code messages, px per line and
    lines per page from budgets.json, one warning line for kinds without a budget) wired into `tools/check.py`;
    tests `tests/test_lint.py`. Width helper `tools/textwidth.py` (`--fill N` makes N-px test strings).
  - Debug tool: `wOFF=HEX` save pokes and `inv` (every item in the inventory) set tokens; scene `menu_items_all`.
    Save RAM dump probe `tools/lua/ramsave.lua` (diff two dumps to find a field). Inventory layout in
    `docs/re/scripts.md`.
  - Marker tour re-run (`work/qa/marker2`, 100/100 ok, 966 ids): Japanese left only in name entry and the monster
    book's 属性 沼.
  - Session 2 (2026-11-18): the 沼 is the monster attribute, also in the original: new arm9 table `elem` (10 one-kanji
    4-byte slots at 0x021233D8, wrongly in NOT_TEXT before), extracted to `script/arm9/elem.json` and **relocated**
    into the hook block at 16-byte slots (`engine.RELOC`: accessor literal + stride patched; inserter writes
    `Engine.reloc`; tested in `tests/test_engine.py`, seen in game). Its canvas shows only ~18 px (2 letters):
    budget 18, widening = draw-code work (docs/windows.md). The `monster.area` 16-byte KIND_CAP was a misdiagnosis
    (removed); monster name/area measured at 120 px (10-code canvases clip). Inventory regions mapped (weapons
    save+0x11E0, armor +0x136C; docs/re/scripts.md). warp.lua: `EXTRA='tokens'` var (append cheats/inputs to any
    scene), `INV_FROM`. Budgets for every remaining kind in `tools/budgets.json`: `jp-bound` (longest JP line at
    12 px; lists not reachable yet, verify in phase 8) or `not-drawn` (readings = sort keys, 説明 placeholders);
    lint skips width for `not-drawn`.
- **Phase 6 plan as written at phase 5 end (mostly done above):** translate in batches (`references/translation.md`): translators get `tools/budgets.json` +
  `docs/windows.md` + `glossary.md`; readings = English name, 説明 placeholders stay, `ptr.keyboard` stays empty,
  GBA-news fragments are one line each (word order across fragments), `a9.021B1820` follows a name ("<name> joined
  the party"). Polish for later (phase 8): name-entry key letters sit at the cell's left edge (centre them); the comm
  box wraps mid-word (word-wrap hook or keep strings <= 128 px); speaker tag 72 px in a shot; other `count * 12`
  centring; widen the 属性 canvas; full-width digits look wide; fill skills/quests/books/key items in the debug tool
  to replace the jp-bound budgets.
- **Done:**
  - Step 0: ROM pinned (`rom.sha1`), DeSmuME QA fork qa-2 in `tools/desmume/`, guard hook wired in
    `.claude/settings.json` (canary blocked), pre-commit runs `tools/check.py` (a failing test was rejected), smoke boot
    of the original ROM ok, touch input and Lua logging proven (`tools/routes/boot.txt`, `tools/lua/probe_hello.lua`).
  - Phase 1: encoding verified (code = glyph index + 1, JIS order with rows 9-15 closed up; `tbl/jp.tbl` from
    `tools/mktbl.py`, `tests/test_text.py`). Text sources mapped: `field/script/rom.img` (~3,900 strings, u32 pointer
    operands `70`/`9E`), `quest/quest.img`, arm9 fixed-record tables + pointer-referenced messages, buster-name lists,
    `kanakan.img`. Free space: ~1.6 MiB past the used ROM size; script files can grow (append + repoint). Graphics
    static sweep: 279 Japanese panels in `docs/re/graphics-survey.tsv`; unswept `.img` banks listed in
    `docs/re/graphics.md`. No earlier fan patch exists; official English names from Viz (`docs/re/prior-work.md`).
  - Phase 2 (done): `tools/debug/warp.lua` + `tools/debug/scenes.tsv` (100 scenes) + `tools/debug/warp_all.py`
    (`python -X utf8 tools/debug/warp_all.py --jobs 6`: all scenes from cold boot, states into `work/states/`, battery
    save fixtures into `work/saves/`; last run 100/100 ok, every row checked by eye in `work/qa/m1..m6.png`,
    `work/qa/exp/fac/finals*.png`, `work/qa/check_p2.png`). Coverage: title (before and after a clear: Story submenu
    Buster/Vandel, 通信 link check + 受付/検索, GBA link), new game, name entry, both story spines (b02-b31, v01-v18),
    credits, game over, field board, all 17 field menus incl. buster/vandel books (`books` cheat forces the empty book
    open), East Village weapon/armor/item shops with buy/sell/forge lists, inn, appraiser greeting, 魔賓館 reception +
    item/monster trade + aide screens, save prompt + "saved", quest abandon / quest done messages.
    Mechanisms: warp the interpreter PC at the opening event; `qXXXX` queues scripts from the idle field (talk events,
    shop counters, routines); `@FRAME` inputs; GOD mode; reset check; `writesave` / `sav=NAME` save fixtures
    (clear_save.dsv = Buster clear). RE in `docs/re/scripts.md` (UI state machine, door-trigger tree, facility table).
    Probes: `tools/lua/{uistate,trigdump,triggers,scrpc,scrpos,varlog,statelog,battlelog}.lua`.
  - Phase 3 (done): `tools/build.py` checks `rom.sha1`, loads with ndspy, rebuilds, then restores the 0x1000 word,
    the 0x00 inter-region padding (ndspy pads 0xFF) and the cartridge length. `tests/test_build.py` asserts the
    rebuild is byte-identical (also after replacing every file with its own bytes); a one-byte edit gives exactly one
    diff. Edits slot in at the `# Edits go here` line of `build()`.
  - Phase 4 (done): `python -X utf8 tools/extract.py [--force] [--only rom,quest,names,arm9]` writes `script/`
    (9,462 entries: `rom/NN.json` 4,120 messages/speakers/quest labels with `speaker` context, `quest/NN.json` 637,
    `names.json` 256 generic buster names (16-byte slots), `arm9/<table>.json` 4,334 fixed-slot fields with `addr` and
    `max`, `arm9/ptr.json` 115 pointer strings with their pointer words). Never clobbers `en`. Parsers:
    `tools/scr.py` (scr container: code / S-aligned string pools / data, two-pass on pointer evidence),
    `tools/arm9text.py` (+ `tools/a9tables.py` accessor scan), codec `tools/text16.py`. `tests/test_extract.py`:
    every byte of both script containers explained, every string operand on a string start, every jump on an
    instruction, all JSON `jp` re-encode to the ROM bytes, no kana run in arm9 outside the extracted slots (7 waived
    numeric words). New controls in `tbl/jp.tbl`: `{hero}` FF90, `{vandel}` FF92, `{name93}`, `{monster}`, `{count}`.
    Not text (documented, tested): rom.img data tail 0x51BB4-, quest.img table 0x11D4, file names, kanakan.img.
- **Debug-tool gaps (grow later, not blocking):** appraiser's appraisal choice (`4F`, needs story var 0x93); quest
  accept/turn-in flow from quest NPCs (quest.img scripts) beyond the two engine messages; the books show an empty entry 0
  (fill the registration bits for full text coverage in phase 8); shops of other towns if any (only East Village uses
  the AF/10/53 shop opcodes in rom.img); VS battles over 通信 need a second DS and are out of reach.
- **Open questions for later phases:** meanings of `{hero}`/`{vandel}`/`{name93}`/`{monster}`/`{count}` are guesses
  (check in the marker build); whether hiragana `reading` fields and the `desc` 説明 placeholders of the vandel/buster
  tables are ever shown; arm9 inline name fields only hold 9-10 full-width chars, so English needs
  half-width/VWF codes or relocated tables (phase 5); FF71/FF72 meaning (guess); OBJ cut-in text needs `.ab` cell data
  to read; `.img` graphics bank format. Shop/menu UI text (買う/売る, 武器購入 headers) is not in arm9 as tbl text:
  probably graphics; check in the phase 5 marker build.
- **Open bugs:** none.
- **Waiting on the user:** (non-blocking) Title logo: keep 冒険王ビィト art and the existing English "VANDEL VS
  BUSTERS", replace only the katakana subtitle with English. Proceeding with that default (D5: no official English logo
  for this game).
