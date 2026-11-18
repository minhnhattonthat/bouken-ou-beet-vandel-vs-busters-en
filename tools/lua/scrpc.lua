-- Log the field-script interpreter PC (file offset into field/script/rom.img) every EVERY frames when it changes.
-- Interpreter context pointer at 0x021BEDAC; ctx+4 = file object, ctx+8 = PC (docs/re/scripts.md).
local every = EVERY or 30
local last = -1
L.on_frame(function(n)
  if n % every ~= 0 then return end
  local ctx = memory.readdword(0x021BEDAC)
  if ctx < 0x02000000 or ctx >= 0x02400000 then return end
  local pc = memory.readdword(ctx + 8)
  if pc ~= last then
    L.log(string.format("f%d ctx=%08X pc=%05X", n, ctx, pc))
    last = pc
  end
end)
