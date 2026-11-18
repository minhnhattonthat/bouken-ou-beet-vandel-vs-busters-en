-- Dump RAM to OUT/ram_<frame>.bin at frame AT (default 30) or every EVERY frames: SIZE bytes from BASE, where BASE
-- defaults to the save struct [0x021BA3A0] (docs/re/scripts.md). Pair two dumps (before/after an action) with a
-- byte diff to find where the game keeps a value.
--   emu.py ROM --out DIR --state-in S --script tools/lua/ramsave.lua --var AT=30 --var SIZE=0x4000 --frames 40
local at, every, size = AT or 30, EVERY, SIZE or 0x4000
local function dump(n)
  local base = BASE or memory.readdword(0x021BA3A0)
  local f = assert(io.open(string.format("%s/ram_%06d.bin", OUT or ".", n), "wb"))
  local t = {}
  for i = 0, size - 1 do t[#t + 1] = string.char(memory.readbyte(base + i)) end
  f:write(table.concat(t))
  f:close()
  L.log(string.format("f%d dump base %08X size %X", n, base, size))
end
L.on_frame(function(n)
  if n == at or (every and n % every == 0) then dump(n) end
end)
