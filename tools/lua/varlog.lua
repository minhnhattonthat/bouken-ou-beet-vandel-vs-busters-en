-- Log changes to the script's byte variables ([[0x021BEBDC]+4][0..NVAR-1], opcode 4C) and story flag bits
-- (save block flag bitfield, opcode 41/96/9B/50), with the interpreter PC. docs/re/scripts.md §State.
local NVAR = NVAR or 256
local NFLAGB = NFLAGB or 64
local prevv, prevf = {}, {}
local function flagbase()
  local s = memory.readdword(0x021BA3A0)
  if s < 0x02000000 or s >= 0x02400000 then return nil end
  local slot = memory.readdword(0x021BEBE0)
  if slot == 2 then slot = 0 end
  local fb = memory.readdword(s + slot * 0x159C + 0x1580 + 8)
  if fb < 0x02000000 or fb >= 0x02400000 then return nil end
  return fb
end
local function varbase()
  local o = memory.readdword(0x021BEBDC)
  if o < 0x02000000 or o >= 0x02400000 then return nil end
  local v = memory.readdword(o + 4)
  if v < 0x02000000 or v >= 0x02400000 then return nil end
  return v
end
L.on_frame(function(n)
  if n % (EVERY or 10) ~= 0 then return end
  local ctx = memory.readdword(0x021BEDAC)
  local pc = (ctx >= 0x02000000 and ctx < 0x02400000) and memory.readdword(ctx + 8) or -1
  local vb = varbase()
  if vb then
    for i = 0, NVAR - 1 do
      local x = memory.readbyte(vb + i)
      if prevv[i] ~= nil and prevv[i] ~= x then L.log(string.format("f%d pc=%05X var[%02X] %d -> %d", n, pc, i, prevv[i], x)) end
      prevv[i] = x
    end
  end
  local fb = flagbase()
  if fb then
    for i = 0, NFLAGB - 1 do
      local x = memory.readbyte(fb + i)
      if prevf[i] ~= nil and prevf[i] ~= x then
        for b = 0, 7 do
          local m = 2 ^ b
          local o, nw = math.floor(prevf[i] / m) % 2, math.floor(x / m) % 2
          if o ~= nw then L.log(string.format("f%d pc=%05X flag %03X %d -> %d", n, pc, i * 8 + b, o, nw)) end
        end
      end
      prevf[i] = x
    end
  end
end)
