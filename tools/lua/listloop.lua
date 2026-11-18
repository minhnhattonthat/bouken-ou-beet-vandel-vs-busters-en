-- listloop.lua: page a 4-row list screen through every record id by writing the ids into the list the screen draws
-- from and forcing its redraw (text coverage for lists the story never fills: Saiga skills, Tengeki, Meigeki).
-- The screen routine LISTLOOP_PC runs every frame with the screen object in LISTLOOP_REG; the rows are words at
-- [obj + LISTLOOP_LIST] + LISTLOOP_OFF + 4*i (or obj + LISTLOOP_OFF when LISTLOOP_LIST is nil), LISTLOOP_ROWS of
-- them (default 4), LISTLOOP_SIZE bytes each (default 4); the redraw is forced by writing LISTLOOP_DIRTY_VAL
-- (default 0xFFFFFFFF) to obj + LISTLOOP_DIRTY. Every LISTLOOP_PERIOD frames (default 120) from LISTLOOP_FROM the next
-- page of ids (LISTLOOP_FIRST.. LISTLOOP_FIRST+LISTLOOP_N-1) is written and the redraw forced; logs LISTLOOP <first
-- id> f<frame> (LISTLOOP_POKES = {{off, word}, ..} are written to obj first, e.g. the list count) and takes a shot (L.shot) LISTLOOP_SHOT frames later (default 30). Saiga skills (session 14):
--   --script tools/lua/listloop.lua --var LISTLOOP_PC=0x020C8594 --var "LISTLOOP_REG='r8'" --var LISTLOOP_LIST=0xF0
--   --var LISTLOOP_OFF=0xEC --var LISTLOOP_DIRTY=0x11C --var LISTLOOP_FIRST=1 --var LISTLOOP_N=67
local obj
local rows, size = LISTLOOP_ROWS or 4, LISTLOOP_SIZE or 4
local first, n = LISTLOOP_FIRST or 1, LISTLOOP_N or 1
local period, from, shotd = LISTLOOP_PERIOD or 120, LISTLOOP_FROM or 0, LISTLOOP_SHOT or 30
local wr = ({ [1] = memory.writebyte, [2] = memory.writeword, [4] = memory.writedword })[size]
local page, shot_at = 0, nil

L.on_exec(LISTLOOP_PC, function()
  obj = memory.getregister("arm9." .. (LISTLOOP_REG or "r0"))
end)

L.on_frame(function(f)
  if shot_at and f == shot_at then
    L.shot(string.format("list_%03X.png", first + (page - 1) * rows))
    shot_at = nil
  end
  if not obj or f < from or (f - from) % period ~= 0 then return end
  local id0 = first + page * rows
  if id0 >= first + n then return end
  local base = LISTLOOP_LIST and memory.readdword(obj + LISTLOOP_LIST) or obj
  if base < 0x02000000 or base >= 0x02400000 then return end
  for i = 0, rows - 1 do
    local id = id0 + i
    wr(base + (LISTLOOP_OFF or 0) + i * size, id < first + n and id or 0)
  end
  for _, p in ipairs(LISTLOOP_POKES or {}) do memory.writedword(obj + p[1], p[2]) end
  memory.writedword(obj + LISTLOOP_DIRTY, LISTLOOP_DIRTY_VAL or 0xFFFFFFFF)
  L.log(string.format("LISTLOOP %X f%d", id0, f))
  page = page + 1
  shot_at = f + shotd
end)
