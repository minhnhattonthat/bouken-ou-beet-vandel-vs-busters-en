-- Debug warp for Bouken-ou Beet: Vandel vs. Busters (NDS). Boots cold, starts a new game by touch, and when the
-- field-script interpreter reaches the first event (file offset 0x871..0x875 of field/script/rom.img) it moves the
-- interpreter PC to the scene's event entry, so the game itself loads that event's map, actors and battle.
--
--   emu.py ROM --out DIR --script tools/debug/warp.lua --var "SCENE='name'" --frames N [--sheet]
--   optional globals: SCENES='abs/path/scenes.tsv' (default: found relative to the emulator dir or repo),
--                     GOD=1 (party HP pinned; see god_tick), NOMASH=1 (no auto A presses after the warp).
--
-- Scene kinds (tools/debug/scenes.tsv, columns: name kind arg mash frames set note):
--   title       stay on the title screen (no input)
--   newgame     new game, no warp (opening ship event)
--   namentry    new game, stop pressing at the name-entry screen
--   event       warp PC to hex file offset `arg` (an event entry: a `17 <u32>` jump target, docs/re/scripts.md)
--   gameover    warp to event `arg` (one with a battle), then force battle state 13 (game-over screen)
--   touch       warp to event `arg`, and after `frames`-300 frames tap the touch points in `set`
-- `mash` = press A every N frames after the warp (0 = never). `set` (event kind): space-separated writes applied at
-- warp time: fNNN = story flag bit (opcode 41/96), sNNN = event-seen bit (opcode 9A), hex ids.
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
if kind ~= "title" then
  L.press("-", 500); L.press("t95,88", 6); L.press("-", 200); L.press("t128,88", 6); L.press("-", 200)
  L.press("t128,88", 6); L.press("-", 300)
end

local warped, warp_frame = false, nil
local pc_after = nil
-- touch kind: `set` = "@FRAME tok tok ..." ; tok = a button or tX,Y (pressed 6 frames, then 90 frames idle),
-- or wN (idle N frames). Inputs start at FRAME (absolute, from boot); A-mashing stops 60 frames before it.
local touches, touch_at = {}, nil
if kind == "touch" then
  for tok in (sc.set or ""):gmatch("%S+") do
    local at = tok:match("^@(%d+)$")
    if at then touch_at = tonumber(at) else touches[#touches + 1] = tok end
  end
  touch_at = touch_at or 3600
end

L.on_frame(function(n)
  local c = ctx()
  if not warped and c then
    local pc = memory.readdword(c + 8)
    if kind == "newgame" or kind == "namentry" then
      if pc >= 0x871 and pc <= 0x875 then warped, warp_frame = true, n; L.log("WARP newgame f" .. n) end
    elseif kind ~= "title" and pc >= 0x871 and pc <= 0x875 then
      local fl, se = save_obj(0x1580), save_obj(0x158C)
      for k, id in (sc.set or ""):gmatch("([fs])(%x+)") do
        local base = (k == "f") and fl or se
        if base then setbit(base, tonumber(id, 16)) end
      end
      memory.writedword(c + 8, target)
      warped, warp_frame = true, n
      L.log(string.format("WARP f%d pc %05X -> %05X", n, pc, target))
    end
  end
  if warped then
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
    if kind == "touch" and n == touch_at then
      for _, t in ipairs(touches) do
        local w = t:match("^w(%d+)$")
        if w then L.press("-", tonumber(w)) else L.press(t, 6); L.press("-", 90) end
      end
      L.log(string.format("TOUCH f%d %s", n, table.concat(touches, " ")))
    end
  end
  if FRAMES and n == FRAMES - 1 then
    local cc = ctx()
    L.log(string.format("END f%d warped=%s ctx=%s pc=%s battle_state=%d", n, tostring(warped),
      cc and string.format("%08X", cc) or "-", cc and string.format("%05X", memory.readdword(cc + 8)) or "-",
      memory.readdword(0x021BEE90)))
    if kind ~= "title" and not warped then L.fail("warp never fired (interpreter never reached 0x871)") end
  end
end)
