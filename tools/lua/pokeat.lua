-- Poke a field of an object reached from a register, whenever a pc runs (from frame POKE_FROM on):
-- addr = reg(POKE_REG) + POKE_OFF, then for each POKE_DEREF offset: addr = [addr] + off. Writes POKE_VAL (POKE_SIZE
-- 1/2/4, default 1) and logs the first write: POKEAT <addr> was <old> now <val>.
-- e.g. the Saiga screen's learn-confirm flag ([[ui+0xD0]+0xBF] = 1, read by UI state 25 at 0x02035F0C; r5 = ui):
--   --script tools/lua/pokeat.lua --var POKE_PC=0x02035F18 --var "POKE_REG='r5'" --var POKE_OFF=0xD0
--   --var "POKE_DEREF='0xBF'" --var POKE_VAL=1
local size, from = POKE_SIZE or 1, POKE_FROM or 0
local rd = ({ [1] = memory.readbyte, [2] = memory.readword, [4] = memory.readdword })[size]
local wr = ({ [1] = memory.writebyte, [2] = memory.writeword, [4] = memory.writedword })[size]
local derefs = {}
for s in string.gmatch(POKE_DEREF or "", "[^%s,]+") do derefs[#derefs + 1] = tonumber(s) end
local told = false
L.on_exec(assert(POKE_PC, "set POKE_PC"), function()
  if L.frame < from then return end
  local a = memory.getregister("arm9." .. (POKE_REG or "r0")) + (POKE_OFF or 0)
  for _, off in ipairs(derefs) do
    local p = memory.readdword(a)
    if p < 0x02000000 or p >= 0x02400000 then return end
    a = p + off
  end
  if not told then
    told = true
    L.log(string.format("POKEAT %08X was %X now %X f%d", a, rd(a), POKE_VAL or 0, L.frame))
  end
  wr(a, POKE_VAL or 0)
end)
