-- Log each distinct (pc, lr) that writes VRAM (BG/OBJ, both engines), with the first address and frame.
-- Phase 5 renderer RE: which routine puts glyph pixels into tiles. Optional LO/HI globals narrow the range.
local seen, frame = {}, 0
L.on_frame(function(n) frame = n end)
local function hook(lo, size)
  memory.registerwrite(lo, size, function(addr)
    local pc = memory.getregister("arm9.r15")
    local lr = memory.getregister("arm9.r14")
    local k = string.format("%08X %08X", pc, lr)
    if not seen[k] then
      seen[k] = true
      L.log(string.format("f%d W %s addr %08X", frame, k, addr))
    end
  end)
end
if LO then hook(LO, HI - LO) else
  hook(0x06000000, 0x80000)
  hook(0x06200000, 0x20000)
  hook(0x06400000, 0x40000)
  hook(0x06600000, 0x20000)
end
