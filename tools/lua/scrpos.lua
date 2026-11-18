-- Log writes to the script FSFile position (field/script/rom.img reader): pc, lr, new file offset.
--   emu.py ... --script tools/lua/scrpos.lua [--var "POS=0x0225E26C"] [--var "TOP=0x017B9E00"]
local pos = POS or 0x0225E26C
local top = TOP or 0x017B9E00
local seen = {}
L.on_write(pos, pos + 3, function(addr, size)
  local pc = memory.getregister("arm9.r15")
  local lr = memory.getregister("arm9.r14")
  local v = memory.readdword(pos)
  local key = string.format("%08X/%08X", pc, lr)
  local n = (seen[key] or 0) + 1
  seen[key] = n
  if n <= (MAXLOG or 40) then
    L.log(string.format("f%d pc=%08X lr=%08X off=%05X", L.frame, pc, lr, v - top))
  end
end)
