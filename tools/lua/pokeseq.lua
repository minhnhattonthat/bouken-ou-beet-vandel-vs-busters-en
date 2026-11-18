-- pokeseq.lua: when POKESEQ_PC runs inside a loop, write POKESEQ_VALS[idx + 1] (u32) to reg(POKESEQ_REG) +
-- POKESEQ_OFF, where idx = reg(POKESEQ_IDX), the loop counter. Fills a per-slot array just before the loop reads it.
-- Logs each slot's first write: POKESEQ <addr> slot <i> was <old> now <val>.
-- e.g. the Vandel-mode Status part cells (loop 0x020654D0: r0 = [obj+0x78] + 4*r8, reads [r0+0x254] = monster id
-- of part r8 or -1, then draws that monster's element short form in window 25+r8):
--   --script tools/lua/pokeseq.lua --var POKESEQ_PC=0x020654D8 --var "POKESEQ_REG='r0'" --var POKESEQ_OFF=0x254
--   --var "POKESEQ_IDX='r8'" --var "POKESEQ_VALS={0,1,3,36,5,33}"
local vals = assert(POKESEQ_VALS, "set POKESEQ_VALS")
local seen = {}
L.on_exec(assert(POKESEQ_PC, "set POKESEQ_PC"), function()
  local i = memory.getregister("arm9." .. (POKESEQ_IDX or "r0"))
  local v = vals[i + 1]
  if v == nil then return end
  local a = memory.getregister("arm9." .. (POKESEQ_REG or "r0")) + (POKESEQ_OFF or 0)
  if not seen[i] then
    seen[i] = true
    L.log(string.format("POKESEQ %08X slot %d was %X now %X", a, i, memory.readdword(a), v))
  end
  memory.writedword(a, v)
end)
