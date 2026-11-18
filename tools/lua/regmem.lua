-- regmem.lua: when REGMEM_PC runs, log r0-r12 and REGMEM_N words (default 16) at [reg REGMEM_REG] + REGMEM_OFF,
-- optionally through one more pointer (REGMEM_DEREF = offset of a pointer field in that object, read first).
-- At most REGMEM_MAX lines (default 5). Finds what list/struct a screen routine walks, e.g. the Saiga skill list:
--   --script tools/lua/regmem.lua --var REGMEM_PC=0x020C85E0 --var "REGMEM_REG='r8'" --var REGMEM_DEREF=0xF0
--   --var REGMEM_OFF=0xE0
local n, max = 0, REGMEM_MAX or 5
L.on_exec(REGMEM_PC, function()
  if n >= max then return end
  n = n + 1
  local g = function(r) return memory.getregister("arm9." .. r) end
  local regs = {}
  for i = 0, 12 do regs[#regs + 1] = string.format("r%d=%08X", i, g("r" .. i)) end
  L.log(string.format("REGMEM %08X f%d lr=%08X %s", REGMEM_PC, L.frame, g("r14"), table.concat(regs, " ")))
  local base = g(REGMEM_REG or "r0")
  if REGMEM_DEREF then base = memory.readdword(base + REGMEM_DEREF) end
  base = base + (REGMEM_OFF or 0)
  local w = {}
  for i = 0, (REGMEM_N or 16) - 1 do w[#w + 1] = string.format("%08X", memory.readdword(base + i * 4)) end
  L.log(string.format("REGMEM mem %08X: %s", base, table.concat(w, " ")))
end)
