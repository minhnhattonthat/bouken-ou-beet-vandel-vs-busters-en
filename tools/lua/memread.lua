-- Log each distinct (pc, lr) that reads LO..HI (globals), with the first address and frame. Default: the RAM copy
-- of field/script/rom.img (base 0x02275108, docs/re/text.md), to find the message renderer.
local lo, hi = LO or 0x02275108, HI or (0x02275108 + 0x57800)
local seen, frame = {}, 0
L.on_frame(function(n) frame = n end)
memory.registerread(lo, hi - lo, function(addr)
  local pc = memory.getregister("arm9.r15")
  local lr = memory.getregister("arm9.r14")
  local k = string.format("%08X %08X", pc, lr)
  if not seen[k] then
    seen[k] = true
    L.log(string.format("f%d R %s addr %08X", frame, k, addr))
  end
end)
