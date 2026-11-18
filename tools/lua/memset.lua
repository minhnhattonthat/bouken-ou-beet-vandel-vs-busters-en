-- Hold one RAM word (any address, not just the save struct; warp.lua's wOFF tokens cover that): from frame
-- MEMSET_FROM (default 0) on, write MEMSET_VAL to MEMSET_ADDR, or to [MEMSET_PTR] + MEMSET_OFF once that pointer is
-- set. MEMSET_SIZE 1/2/4 (default 4). Logs the value it found the first time: MEMSET <addr> was <old> now <val>.
-- e.g. the area/area2 table switch [[0x021BEDA4]+0xC] (0/1 = area, else area2; 0x020D3084):
--   --script tools/lua/memset.lua --var MEMSET_PTR=0x021BEDA4 --var MEMSET_OFF=0xC --var MEMSET_VAL=2
local from, val, size = MEMSET_FROM or 0, MEMSET_VAL or 0, MEMSET_SIZE or 4
local rd = ({ [1] = memory.readbyte, [2] = memory.readword, [4] = memory.readdword })[size]
local wr = ({ [1] = memory.writebyte, [2] = memory.writeword, [4] = memory.writedword })[size]
local told = false
L.on_frame(function(f)
  if f < from then return end
  local a = MEMSET_ADDR
  if MEMSET_PTR then
    local p = memory.readdword(MEMSET_PTR)
    if p < 0x02000000 or p >= 0x02400000 then return end
    a = p + (MEMSET_OFF or 0)
  end
  if not a then return end
  if not told then
    told = true
    L.log(string.format("MEMSET %08X was %X now %X f%d", a, rd(a), val, f))
  end
  wr(a, val)
end)
