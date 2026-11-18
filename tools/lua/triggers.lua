-- Log position-trigger registrations (script opcode 07 -> 0x0204B218 -> 0x0203D920(field, x, y, w, [sp] h,
-- [sp+4] script offset)): the door and step triggers of every map the run loads, with their script offsets.
L.on_exec(0x0203D920, function()
  local r = function(n) return memory.getregister("arm9." .. n) end
  local sp = r("r13")
  local h = memory.readword(sp)
  local scr = memory.readdword(sp + 4)
  local c = memory.readdword(0x021BEDAC)
  local pc = (c >= 0x02000000 and c < 0x02400000) and memory.readdword(c + 8) or 0
  L.log(string.format("f%d TRIG x%d y%d w%d h%d -> %05X (script pc %05X)", L.frame, r("r1"), r("r2"), r("r3"), h, scr, pc))
end)
