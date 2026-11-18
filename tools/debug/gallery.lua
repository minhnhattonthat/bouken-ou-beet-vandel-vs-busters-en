-- gallery.lua: message gallery for text coverage (phase 8). Append after tools/debug/warp.lua on the `newgame`
-- scene with NOMASH=1, plus tools/lua/textlog.lua (tools/debug/gallery_run.py does all that; no --debugger needed:
-- both hooks are block starts).
-- The opening event runs until its first message has been closed (PC 0x8C1: the message window and the top screen
-- are set up); from then on the field-script interpreter is fed one dialogue span after another from the list
-- tools/debug/gallery.py writes (work/qa/gallery/pcs.txt, `START END` hex per line: `2A` open window, [`9E`
-- speaker], `70` message, `34` wait for A and close), so the game's own message code fetches and draws every
-- script message and speaker tag; tools/lua/textlog.lua logs them for tools/textcov.py.
-- Globals: GALLERY='FROM-TO' (1-based, inclusive line numbers), GALLERY_PCS='abs/path' (default
-- <repo>/work/qa/gallery/pcs.txt), GALLERY_SHOTS=1 (shot g<NNNN>.png of each span's first page),
-- GALLERY_STUCK=N (frames before a span is skipped, default 900).
-- How (docs/re/scripts.md §Interpreter state): the main loop 0x0204E630 reads the opcode at ctx+8 and calls its
-- handler; a handler returning 0 yields (34 does, until A), else the loop advances PC by the opcode length and reads
-- the next one at 0x0204E6F4. Both points are hooked: once the PC there leaves the current span, the span is done
-- and PC is set to the next span's start.
-- Log: GAL <n> <start> f<frame> per span, GALSTUCK <n> <start> f<frame> when skipped, GALDONE f<frame>.

local function root()
  return OUT and OUT:match("^(.*)[/\\]work[/\\]")
end
local path = GALLERY_PCS or ((root() or ".") .. "/work/qa/gallery/pcs.txt")
local list = {}
do
  local f = io.open(path, "r") or error("gallery list not found: " .. path .. " (run tools/debug/gallery.py)")
  for line in f:lines() do
    local a, b = line:match("^(%x+)%s+(%x+)")
    if a then list[#list + 1] = { tonumber(a, 16), tonumber(b, 16) } end
  end
  f:close()
end
local range = GALLERY or ("1-" .. #list)
local from, to = range:match("^(%d+)%-(%d+)$")
from, to = tonumber(from) or 1, math.min(tonumber(to) or #list, #list)
local stuck_after = GALLERY_STUCK or 900
local ARM_PC = 0x8C1
L.log(string.format("GALLERY %d-%d of %d (%s)", from, to, #list, path))

local CTX = 0x021BEDAC
local function ctx()
  local c = memory.readdword(CTX)
  return (c >= 0x02000000 and c < 0x02400000) and c or nil
end

local armed, done = false, false
local i, started, began_at, shot_pending = from - 1, false, 0, nil

local function start(c)
  memory.writedword(c + 8, list[i][1])
  started, began_at = true, L.frame
  shot_pending = GALLERY_SHOTS and (L.frame + 40) or nil
  L.log(string.format("GAL %d %X f%d", i, list[i][1], L.frame))
end

local function feed()
  if done then return end
  local c = ctx()
  if not c then return end
  local p = memory.readdword(c + 8)
  if not armed then
    if p == ARM_PC then armed = true; L.log("GALARM f" .. L.frame) else return end
  end
  if started and (p < list[i][1] or p >= list[i][2]) then started = false end
  if not started then
    i = i + 1
    if i > to then
      done = true
      L.log(string.format("GALDONE f%d", L.frame))
      return
    end
    start(c)
  end
end
L.on_exec(0x0204E630, feed)
L.on_exec(0x0204E6F4, feed)

local boot = nil
L.on_frame(function(n)
  if done then return end
  local c = ctx()
  if not boot and c then
    local p = memory.readdword(c + 8)
    if p >= 0x871 and p <= 0x875 then boot = n end
  end
  if not boot then return end
  if shot_pending and n == shot_pending then
    L.shot(string.format("g%04d.png", i))
    shot_pending = nil
  end
  local since = started and (n - began_at) or (n - boot)
  -- A: held 5 frames every 16, starting 44 frames into a span (after its shot)
  if since >= 44 and (since - 44) % 16 < 5 then L.press("a", 1) end
  if started and since >= stuck_after then
    L.log(string.format("GALSTUCK %d %X f%d", i, list[i][1], n))
    started = false
    if c then
      i = i + 1
      if i <= to then start(c) end
    end
  end
end)
