# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 2. Debug tool in progress (all 71 scene rows land by eye; GOD mode and reset check done; shops, inn,
  quest board, save point, VS mode still to add to the scene list).
  Last build: none yet (build.py arrives in phase 3).
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
  - Phase 2 so far (2026-11-18): script interpreter state found and documented (`docs/re/scripts.md` §Interpreter
    state: PC at [0x021BEDAC]+8, opcode-length table 0x021953D0, flag/event-seen bitfields, battle state 0x021BEE90).
    `tools/debug/warp.lua` warps by moving the interpreter PC to an event entry when the opening event starts; kinds
    title/newgame/namentry/event/gameover/touch (menus). `tools/debug/scenes.tsv` has 71 scenes (story spine of both
    modes, credits, game over, 17 field menus incl. quests). `tools/debug/warp_all.py` runs all from cold boot into
    `work/qa/warps/<scene>/` + `work/states/<scene>.dst`. Recon helpers: `tools/scrdis.py` (bytecode disassembler),
    `tools/debug/events.py` (event entries), `tools/callers.py` (ARM call chains), `tools/lua/{scrpc,scrpos,varlog,
    statelog}.lua`, `tools/routes/newgame.txt`.
  - Verified by eye (work/qa/story_sheet.png, menus_sheet.png): title, newgame, namentry, credits (19 staff panels),
    gameover (banner, `gameover.png`), field_nash, all menus except menu_busters/menu_vandels (books don't open this
    early: they stay on the Info screen), and story scenes b02-b05, b07-b10, b12-b15, b19, b21, b25, b26, b28, b29,
    v02-v05, v10, v11.
  - Phase 2, session 2 (2026-11-18): **GOD mode** in warp.lua (default on for event/touch; party HP pinned, enemies
    set down 300 battle frames in, so the game's own win path runs: battle object/unit layout in `docs/re/scripts.md`
    §Battle object). **Reset check**: warp.lua fails (RESET in log) when, after the warp, there is no script context
    and no battle for 600 frames. **Talk events**: `qXXXX` in `set` runs an NPC talk event from the idle field after
    warping to a map-load script (`tools/debug/maploads.py` lists them; b22, b30, b31, v07, v15-v18 use it). Story
    frames raised to 4000. Verified by eye (montages `work/qa/m1.png`..`m6.png`, `tools/debug/montage.py`): b06,
    b11, b16-b18, b20, b22-b25, b27, b30, b31, v01 (lands on the Vandel name-entry screen), v06-v09, v12-v18 — every
    story row now shows its scene. Helpers: `tools/debug/tsvset.py` (TSV cell writer), `tools/lua/battlelog.lua`.
- **Next (phase 2):**
  1. Last full run `python -X utf8 tools/debug/warp_all.py --jobs 6`: 71/71 ok with the reset check, states
     regenerated in `work/states/`. Re-run after any warp.lua change.
  2. Shops (item/weapon/armor, Vandel-mode 魔賓館 monster shop): shop UI is a field submodule (state table 0x0219527C,
     owner object methods 0x021959B8, field-submode table 0x02195918); town signs are `field/animation/shop_*.ab`.
     D-pad on the field board only moves the panel cursor; find how a town's facilities open (touch the sign on the top
     screen? a town panel action?) or call the shop module from Lua. Also: inn/guild, quest board accept/complete
     ("クエストの終了条件" @0x3E950), save point (routine 0x459), name entry for the Vandel player, VS mode (title
     second button), 禁断のヴァンデルモード unlock. Leads from session 2: top-level mode word 0x021BEBF0 (4 =
     0x020D8274, which loops over sub-modes in 0x02195918; sub-mode 1 0x020DF480 owns the 0x021959B8 methods), so
     the shop may be a top-level sub-mode, not a field submodule; tapping the town icon on Nash Plain's board did
     nothing. Weapon-shop strings (武器屋 / いらっしゃい) at rom.img 0x19F6C/0x1A134 belong to story events, not
     the shop UI; shop UI text is probably in arm9. Try: hook 0x020D8274/0x020DF480 entry while walking the
     board into East Village (map 70, warp `29BFA`), or set 0x021BEBF0 and the sub-mode from Lua.
  3. Then phase 2 is done when every scenes.tsv row lands by eye; add the scene list's command to status and move to
     phase 3 (identity build).
- **Open questions for later phases:** opcode lengths now known (table 0x021953D0) but `00`/`FF`/`BF` and string pools
  need an entry-point walker (phase 4); arm9 inline name fields only hold 9-10 full-width chars, so English needs
  half-width/VWF codes or relocated tables (phase 5); FF71/FF72 meaning (guess); OBJ cut-in text needs `.ab` cell data
  to read; `.img` graphics bank format.
- **Open bugs:** none.
- **Waiting on the user:** (non-blocking) Title logo: keep 冒険王ビィト art and the existing English "VANDEL VS
  BUSTERS", replace only the katakana subtitle with English. Proceeding with that default (D5: no official English logo
  for this game).
