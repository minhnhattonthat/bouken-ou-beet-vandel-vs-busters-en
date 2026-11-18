-- Debug warp for Bouken-ou Beet: Vandel vs. Busters (NDS). Boots cold, starts a new game by touch, and when the
-- field-script interpreter reaches the first event (file offset 0x871..0x875 of field/script/rom.img) it moves the
-- interpreter PC to the scene's event entry, so the game itself loads that event's map, actors and battle.
--
--   emu.py ROM --out DIR --script tools/debug/warp.lua --var "SCENE='name'" --frames N [--sheet]
--   optional globals: SCENES='abs/path/scenes.tsv' (default: found relative to the emulator dir or repo),
--                     GOD=0/1 (default 1 for event/touch: party HP pinned, enemies set down after GOD_WIN
--                     frames of battle; see god_tick), NOMASH=1 (no auto A presses after the warp),
--                     DUMP_AT={f1,f2,..} (L.dump_ppu("fN") at those frames, for vramfind.py).
--   The run fails (exit 2) if the warp never fires or the game resets to the title afterwards (RESET in log).
--
-- Scene kinds (tools/debug/scenes.tsv, columns: name kind arg mash frames set note):
--   title       stay on the title screen (no input)
--   newgame     new game, no warp (opening ship event)
--   namentry    new game, stop pressing at the name-entry screen
--   event       warp PC to hex file offset `arg` (an event entry: a `17 <u32>` jump target, docs/re/scripts.md)
--   gameover    warp to event `arg` (one with a battle), then force battle state 13 (game-over screen)
--   touch       warp to event `arg`, then at @FRAME press the inputs in `set`
--   titletouch  no new game: at @FRAME press the inputs in `set` on the title screen (Story / 通信 / GBA link menus)
-- `mash` = press A every N frames after the warp (0 = never). `set`: space-separated tokens:
--   fNNN / sNNN   story flag bit (opcode 41/96) / event-seen bit (opcode 9A), hex ids, set at warp time
--   qXXXX         queue the script at hex offset XXXX to run from the idle field after `arg` (repeatable, run in
--                 order): NPC talk events, shop/inn counters, routines (save 459); `arg` = a map-load script, e.g.
--                 29BFA = East Village (the field's script-running state 0x02030D44 chains to [field_obj+0x3D8])
--   @FRAME tok..  inputs from absolute frame FRAME (touch/titletouch, and event scenes that have one): a button,
--                 tX,Y (pressed 6 frames, then 90 idle) or wN (idle N frames)
--   books         force the empty buster/vandel book open (see BOOKS below; warp_all adds --debugger)
--   wOFF=HEX      write the hex bytes at save+OFF at warp time ([0x021BA3A0] + OFF, hex)
--   inv           fill the inventory with every item (INV_CATS / INV_N globals; see fill_inventory below)
--   inv=OFF:CAT:FROM:N  fill N inventory slots at save+OFF (hex) with category CAT, ids FROM.. (weapons/armor)
--   writesave     the scene saves and returns to the title on purpose: no reset check; warp_all runs it alone and
--                 keeps the battery save as work/saves/<scene>.dsv
--   sav=NAME      (warp_all) boot with work/saves/NAME.dsv, e.g. sav=clear_save for the post-clear title menus
-- RAM layout (docs/re/scripts.md §Interpreter state): ctx ptr 0x021BEDAC (ctx+8 = PC), save base [0x021BA3A0],
-- slot [0x021BEBE0], flags = [save+0x1580+8], seen = [save+0x158C+8], battle state 0x021BEE90.

local function trim(s) return (s:gsub("^%s+", ""):gsub("%s+$", "")) end

local function find_scenes()
  local root = OUT and OUT:match("^(.*)[/\\]work[/\\]")  -- --out under <repo>/work/
  local cands = { SCENES or false, root and (root .. "/tools/debug/scenes.tsv") or false, "../../debug/scenes.tsv",
    "tools/debug/scenes.tsv", "../tools/debug/scenes.tsv" }
  for i = 1, #cands do
    local p = cands[i]
    if p then
      local f = io.open(p, "r")
      if f then return f, p end
    end
  end
  error("scenes.tsv not found; pass --var \"SCENES='C:/abs/tools/debug/scenes.tsv'\"")
end

local function load_scene(name)
  local f, path = find_scenes()
  local cols
  for line in f:lines() do
    line = line:gsub("\r$", "")
    if line ~= "" and line:sub(1, 1) ~= "#" then
      local t = {}
      for c in (line .. "\t"):gmatch("([^\t]*)\t") do t[#t + 1] = c end
      if not cols then cols = t
      else
        local row = {}
        for i, c in ipairs(cols) do row[c] = t[i] or "" end
        if row.name == name then f:close(); return row, path end
      end
    end
  end
  f:close()
  error("scene not in " .. path .. ": " .. tostring(name))
end

local sc, scpath = load_scene(SCENE or error("set --var \"SCENE='name'\""))
-- EXTRA='tok tok': tokens appended to the scene's `set` for one run: warp-time ones (inv, wOFF=HEX, fNNN ...)
-- and further inputs after the scene's own (e.g. EXTRA='t128,56 w100 a' to buy from a shop list)
if EXTRA then sc.set = (sc.set or "") .. " " .. EXTRA end
local kind = sc.kind
local target = tonumber(sc.arg ~= "" and sc.arg or "0", 16) or 0
local mash = tonumber(sc.mash) or 0
if NOMASH then mash = 0 end
L.log(string.format("scene %s kind %s arg %s mash %d (%s)", sc.name, kind, sc.arg, mash, scpath))

local function ram(a) return a >= 0x02000000 and a < 0x02400000 end
local function ctx() local c = memory.readdword(0x021BEDAC); return ram(c) and c or nil end
local function save_obj(off)
  local s = memory.readdword(0x021BA3A0)
  if not ram(s) then return nil end
  local slot = memory.readdword(0x021BEBE0)
  if slot == 2 then slot = 0 end
  local p = memory.readdword(s + slot * 0x159C + off + 8)
  return ram(p) and p or nil
end
local function setbit(base, id)
  local a = base + math.floor(id / 8)
  local m = 2 ^ (id % 8)
  local v = memory.readbyte(a)
  if math.floor(v / m) % 2 == 0 then memory.writebyte(a, v + m) end
end

-- Input: title -> Story -> new game. Same as tools/routes/newgame.txt up to the first event.
local titleish = (kind == "title" or kind == "titletouch")
if not titleish then
  L.press("-", 500); L.press("t95,88", 6); L.press("-", 200); L.press("t128,88", 6); L.press("-", 200)
  L.press("t128,88", 6); L.press("-", 300)
end

-- GOD mode (default on for event/touch scenes; GOD=0 turns it off): while a battle runs, every party unit's HP is
-- pinned to the highest value seen; GOD_WIN frames (default 300) into the battle every enemy is set down (HP 0,
-- status 10), so the state-4 handler takes its own win path (0x020A347C true -> state 6). Battle object = r0 of the
-- state-4 handler 0x0209E690; units at obj+0x98+side*0x14+i*4 (5 per side), player side [obj+0x58], unit HP u16 at
-- +0x1E, status +0x274 (10 = down), present flag +0x350 (docs/re/scripts.md §Battle). Holding enemy HP at 1 is not
-- enough: ordinary hits never take the last point.
local god = GOD
if god == nil then god = (kind == "event" or kind == "touch") and 1 or 0 end
local god_win = GOD_WIN or 300
local battle_obj, god_max, battle_frames = nil, {}, 0
if god ~= 0 then
  L.on_exec(0x0209E690, function() battle_obj = memory.getregister("arm9.r0") end)
end
local function god_tick()
  local o = battle_obj
  if not o or not ram(o) or memory.readdword(0x021BEE90) ~= 4 then battle_frames = 0; return end
  battle_frames = battle_frames + 1
  local kill = battle_frames >= god_win
  if battle_frames == god_win then L.log(string.format("GOD win forced at f%d", L.frame)) end
  local mine = memory.readdword(o + 0x58)
  for side = 0, 1 do
    for i = 0, 4 do
      local u = memory.readdword(o + 0x98 + side * 0x14 + i * 4)
      if ram(u) and memory.readdword(u + 0x350) ~= 0 then
        local hp = memory.readword(u + 0x1E)
        if side == mine then
          if hp > (god_max[u] or 0) then god_max[u] = hp end
          if hp < god_max[u] then memory.writeword(u + 0x1E, god_max[u]) end
        elseif kill then
          memory.writeword(u + 0x1E, 0)
          memory.writedword(u + 0x274, 10)
        end
      end
    end
  end
end

-- BOOKS cheat (scene `set` token `books`, or --var BOOKS=1; needs emu.py --debugger, which warp_all.py adds): the
-- Info screen (UI state 13, 0x02039674; button id [[ui+0x1C]+0x30]: 3 monster, 4 vandel, 5 buster book) opens a
-- book only if the list it builds has a first entry ([[ui+0x70]+0x40] vandel / [[ui+0x74]+0x4C] buster ~= -1);
-- early in the story both are empty. Force entry 0 so the book screen opens (debug only; shows entry 0's page).
local books = BOOKS or (" " .. (sc.set or "") .. " "):match("%sbooks%s")
if books then
  local function force(field, off)
    return function()
      local ui = memory.getregister("arm9.r4")
      local lst = memory.readdword(ui + field)
      if ram(lst) and memory.readdword(lst + off) == 0xFFFFFFFF then
        memory.writedword(lst + off, 0)
        L.log(string.format("BOOKS f%d forced list %08X+%X = 0", L.frame, lst, off))
      end
    end
  end
  -- hooks on the return addresses of the list builders (block starts: mid-block addresses miss under the JIT)
  L.on_exec(0x02039A3C, force(0x74, 0x4C))  -- buster book, after bl 0x0202EFEC
  L.on_exec(0x0203990C, force(0x70, 0x40))  -- vandel book, after bl 0x0202F068
end

-- BOOKBITS (scene `set` token `bookbits`, or --var BOOKBITS=1): register every buster / vandel the honest way, by
-- setting the bits the list builders test, so the books list every entry. Buster book 0x0208E0B8 loops ids
-- 0..0x32 over the bitset object 0x021BEC58 (0x0200AEA8), vandel book 0x02090960 ids 0..0x12 over 0x021BEC4C
-- (0x0200AEB4); test 0x0201B1D8 = byte [[obj+8] + id>>3] & bit. Held every frame once [obj+8] points into RAM.
if BOOKBITS or (" " .. (sc.set or "") .. " "):match("%sbookbits%s") then
  local sets = { { obj = 0x021BEC58, n = 0x33, name = "buster" }, { obj = 0x021BEC4C, n = 0x13, name = "vandel" } }
  local told = {}
  L.on_frame(function(f)
    for _, s in ipairs(sets) do
      local p = memory.readdword(s.obj + 8)
      if ram(p) then
        for i = 0, s.n - 1 do
          local a, m = p + math.floor(i / 8), 2 ^ (i % 8)
          local b = memory.readbyte(a)
          if math.floor(b / m) % 2 == 0 then memory.writebyte(a, b + m) end
        end
        if not told[s.name] then
          told[s.name] = true
          L.log(string.format("BOOKBITS %s bits at %08X set (%d) f%d", s.name, p, s.n, f))
        end
      end
    end
  end)
end

-- Save-struct pokes (warp-time `set` tokens): wOFF=HEX writes the hex bytes at [0x021BA3A0]+OFF; `inv` fills the
-- inventory list. Inventory (found by a buy diff, 2026-11-18): object at save+0x10D4 (vtable 0x021A95DC), entries
-- of 4 bytes from save+0x10D8: [id+1, category, 0, count]; category 4 = item. INV_CATS (default "4") picks
-- the categories `inv` fills, ids 0..INV_N-1 (default 34) each, count 1.
local function poke(off, hex)
  local base = memory.readdword(0x021BA3A0)
  for i = 1, #hex - 1, 2 do memory.writebyte(base + off + (i - 1) / 2, tonumber(hex:sub(i, i + 1), 16)) end
  L.log(string.format("POKE save+%X = %s", off, hex))
end
function fill_inventory()
  local base, k = memory.readdword(0x021BA3A0) + 0x10D8, 0
  for cat in (INV_CATS or "4"):gmatch("%x+") do
    for id = INV_FROM or 0, (INV_FROM or 0) + (INV_N or 34) - 1 do
      memory.writedword(base + 4 * k, 0x01000000 + tonumber(cat, 16) * 0x100 + id + 1)
      k = k + 1
    end
  end
  L.log(string.format("INV %d entries", k))
end
-- `inv=OFF:CAT:FROM:N` (hex OFF, decimal rest): N entries [id+1, CAT, 0, 0] for ids FROM.. at save+OFF, e.g. the
-- weapon region inv=11E0:1:0:99 (99 slots to 0x136C) or armor inv=136C:2:0:71 (docs/re/scripts.md §Inventory).
local function fill_region(spec)
  local off, cat, from, n = spec:match("^(%x+):(%x+):(%d+):(%d+)$")
  local base = memory.readdword(0x021BA3A0) + tonumber(off, 16)
  for k = 0, tonumber(n) - 1 do
    memory.writedword(base + 4 * k, tonumber(cat, 16) * 0x100 + tonumber(from) + k + 1)
  end
  L.log(string.format("INV save+%s cat %s ids %s..+%s", off, cat, from, n))
end

local warped, warp_frame = false, nil
local idle, reset_at = 0, nil

-- queued follow-up script (qXXXX in `set`): once the field is idle after the warp (field state 1, handler
-- 0x02030EB4), it asks 0x0203D84C for a script triggered at the player's position; the hook on the instruction after
-- that call (0x02030F50 `movs r4, r0`) hands back the queued offset, so the field runs it like a stepped-on trigger.
-- Several q tokens run in order, each once the field has been idle 60 frames again (e.g. a map-load script that
-- does not work as a warp target, then a counter script on that map).
local queue = {}
for tok in (sc.set or ""):gmatch("%S+") do
  local q = tok:match("^q(%x+)$")
  if q then queue[#queue + 1] = tonumber(q, 16) end
end
local idle_field = 0
if #queue > 0 then
  L.on_exec(0x02030F50, function()
    if warped and #queue > 0 then
      idle_field = idle_field + 1
      if idle_field >= 60 then
        local q = table.remove(queue, 1)
        memory.setregister("arm9.r0", q)
        L.log(string.format("QUEUE f%d run script %05X", L.frame, q))
        idle_field = 0
      end
    end
  end)
end
local pc_after = nil
-- touch kind: `set` = "@FRAME tok tok ..." ; tok = a button or tX,Y (pressed 6 frames, then 90 frames idle),
-- or wN (idle N frames). Inputs start at FRAME (absolute, from boot); A-mashing stops 60 frames before it.
-- Event scenes take the same "@FRAME tok .." inputs when `set` has an @FRAME (e.g. close a shopkeeper's greeting
-- and open the shop menu); fNNN/sNNN/qXXXX tokens are warp writes, not inputs. namentry scenes too (type a name,
-- touch 決定 at t243,176; the keyboard opens on 英字 in the English build: row y 64+16*r, column x 86+16*c).
local touches, touch_at = {}, nil
if kind == "touch" or kind == "titletouch"
    or ((kind == "event" or kind == "namentry") and (sc.set or ""):match("@%d+")) then
  for tok in (sc.set or ""):gmatch("%S+") do
    local at = tok:match("^@(%d+)$")
    if at then touch_at = tonumber(at)
    elseif not tok:match("^[fsq]%x+$") and tok ~= "books" and tok ~= "bookbits" and tok ~= "writesave" and tok ~= "inv"
      and not tok:match("=") then touches[#touches + 1] = tok end
  end
  touch_at = touch_at or 3600
end

if DUMP_AT then
  local at = {}
  for _, f in ipairs(DUMP_AT) do at[f] = true end
  L.on_frame(function(n) if at[n] then L.dump_ppu("f" .. n) end end)
end

L.on_frame(function(n)
  local c = ctx()
  if not warped and c then
    local pc = memory.readdword(c + 8)
    if kind == "newgame" or kind == "namentry" then
      if pc >= 0x871 and pc <= 0x875 then warped, warp_frame = true, n; L.log("WARP newgame f" .. n) end
    elseif not titleish and pc >= 0x871 and pc <= 0x875 then
      local fl, se = save_obj(0x1580), save_obj(0x158C)
      for tok in (sc.set or ""):gmatch("%S+") do
        local k, id = tok:match("^([fs])(%x+)$")
        local base = k and ((k == "f") and fl or se)
        if base then setbit(base, tonumber(id, 16)) end
        local off, hex = tok:match("^w(%x+)=(%x+)$")
        if off then poke(tonumber(off, 16), hex) end
        local ma, mhex = tok:match("^m(%x%x%x%x%x%x%x%x)=(%x+)$")  -- mADDR=HEX: bytes at an absolute RAM address
        if ma then
          for i = 1, #mhex - 1, 2 do memory.writebyte(tonumber(ma, 16) + (i - 1) / 2, tonumber(mhex:sub(i, i + 1), 16)) end
          L.log(string.format("POKE %s = %s", ma, mhex))
        end
        if tok == "inv" then fill_inventory() end
        local spec = tok:match("^inv=(.+)$")
        if spec then fill_region(spec) end
      end
      memory.writedword(c + 8, target)
      warped, warp_frame = true, n
      L.log(string.format("WARP f%d pc %05X -> %05X", n, pc, target))
    end
  end
  if warped then
    if god ~= 0 then god_tick() end
    -- reset check: after a lost battle the game goes back to the BANDAI logo and title, where there is no script
    -- context and the battle state word is 0. 600 such frames in a row after the warp = the scene was not reached.
    -- `writesave` scenes end by saving and going back to the title on purpose (clear data), so no reset check.
    if kind ~= "gameover" and not (" " .. (sc.set or "") .. " "):match("%swritesave%s") then
      if not c and memory.readdword(0x021BEE90) == 0 then
        idle = idle + 1
        if idle == 600 then reset_at = n; L.log(string.format("RESET f%d (no script context, no battle)", n)) end
      else idle = 0 end
    end
    local since = n - warp_frame
    if kind == "namentry" then
      -- press A through the opening until the name-entry screen; stop pressing there
      if since < 2100 and since % 30 < 6 then L.press("a", 1) end
    elseif mash > 0 and since > 60 and since % mash < 6 and L.route_done()
        and not (touch_at and n >= touch_at - 60) then
      L.press("a", 1)
    end
    if kind == "gameover" then
      local bs = memory.readdword(0x021BEE90)
      if bs >= 4 and bs <= 6 and not pc_after then
        memory.writedword(0x021BEE90, 13)
        pc_after = n
        L.log(string.format("GAMEOVER forced at f%d (battle state was %d)", n, bs))
      end
      if pc_after and n == pc_after + 150 then
        L.shot("gameover.png")
        L.log(string.format("SHOT gameover.png f%d battle state %d", n, memory.readdword(0x021BEE90)))
      end
    end
  end
  if touch_at and n == touch_at and (warped or kind == "titletouch") then
    for _, t in ipairs(touches) do
      local w = t:match("^w(%d+)$")
      if w then L.press("-", tonumber(w)) else L.press(t, 6); L.press("-", 90) end
    end
    L.log(string.format("TOUCH f%d %s", n, table.concat(touches, " ")))
  end
  if FRAMES and n == FRAMES - 1 then
    local cc = ctx()
    L.log(string.format("END f%d warped=%s ctx=%s pc=%s battle_state=%d", n, tostring(warped),
      cc and string.format("%08X", cc) or "-", cc and string.format("%05X", memory.readdword(cc + 8)) or "-",
      memory.readdword(0x021BEE90)))
    if not titleish and not warped then L.fail("warp never fired (interpreter never reached 0x871)") end
    if reset_at then L.fail(string.format("game reset to the title after the warp (f%d)", reset_at)) end
  end
end)
