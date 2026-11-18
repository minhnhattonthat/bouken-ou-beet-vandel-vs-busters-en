-- Log which code reads the loaded fonts (phase 5 renderer RE). FontManager = [0x021BA394]; +4 a8x8,
-- +8 lc8x8, +0xC lc10x10, +0x10 lc12x12 (docs/re/text.md). Logs each new (font, pc, lr) once.
local SIZES = { [4] = 256 * 8, [8] = 7332 * 8, [0xC] = 7332 * 20, [0x10] = 7332 * 24 }
local NAMES = { [4] = "a8x8", [8] = "lc8x8", [0xC] = "lc10x10", [0x10] = "lc12x12" }
local hooked, seen = {}, {}
L.on_frame(function(n)
  local fm = memory.readdword(0x021BA394)
  if fm < 0x02000000 or fm >= 0x02400000 then return end
  for off, size in pairs(SIZES) do
    local base = memory.readdword(fm + off)
    if base >= 0x02000000 and base < 0x02400000 and hooked[off] ~= base then
      hooked[off] = base
      L.log(string.format("f%d %s at %08X", n, NAMES[off], base))
      memory.registerread(base, size, function(addr)
        local pc = memory.getregister("arm9.r15")
        local lr = memory.getregister("arm9.r14")
        local k = string.format("%s %08X %08X", NAMES[off], pc, lr)
        if not seen[k] then
          seen[k] = true
          L.log(string.format("f%d READ %s glyph %d", n, k, math.floor((addr - base) / math.max(math.floor(size / 7332), 8))))
        end
      end)
    end
  end
end)
