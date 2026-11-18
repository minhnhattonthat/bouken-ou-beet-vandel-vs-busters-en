-- Log glyph draws per font: 0x020200B0 (12x12, code in r3) and 0x020202A4 (8x8, code in r3), with x,y and caller.
-- Groups consecutive draws from one caller into one line: "G12 lr x,y codes...". Phase 5 renderer RE / width gate.
local cur, frame = nil, 0
local function flush()
  if cur then L.log(string.format("f%d %s lr=%08X x=%d y=%d n=%d %s", cur.f, cur.font, cur.lr, cur.x, cur.y, #cur.c,
    table.concat(cur.c, " "))) end
  cur = nil
end
L.on_frame(function(n) frame = n; flush() end)
local function hook(addr, font)
  L.on_exec(addr, function()
    local lr = memory.getregister("arm9.r14")
    local x, y = memory.getregister("arm9.r1"), memory.getregister("arm9.r2")
    local code = memory.getregister("arm9.r3")
    if not (cur and cur.font == font and cur.lr == lr and cur.y == y) then
      flush()
      cur = { f = frame, font = font, lr = lr, x = x, y = y, c = {} }
    end
    cur.c[#cur.c + 1] = string.format("%04X", code)
  end)
end
hook(0x020200B0, "G12")
hook(0x020202A4, "G8")
