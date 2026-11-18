-- Log the battle object and its units while a battle runs (append after tools/debug/warp.lua).
-- State-4 handler 0x0209E690 gets the battle object in r0 (docs/re/scripts.md §Battle). Units: obj+0x98+side*0x14+i*4
-- (5 per side), player side = [obj+0x58]. Unit fields: +0x1E HP, +0x20/+0x32 second gauge, +0x274 status (10 = down),
-- +0x350 present.
local obj, last = nil, -1
L.on_exec(0x0209E690, function() obj = memory.getregister("arm9.r0") end)
L.on_frame(function(n)
  if obj and n % 60 == 0 then
    local parts = { string.format("f%d obj %08X side %d bs %d", n, obj, memory.readdword(obj + 0x58),
      memory.readdword(0x021BEE90)) }
    for side = 0, 1 do
      for i = 0, 4 do
        local u = memory.readdword(obj + 0x98 + side * 0x14 + i * 4)
        if u >= 0x02000000 and u < 0x02400000 and memory.readdword(u + 0x350) ~= 0 then
          parts[#parts + 1] = string.format("%d.%d@%08X hp%d/%d g%d st%d", side, i, u, memory.readword(u + 0x1E),
            memory.readword(u + 0x20), memory.readword(u + 0x32), memory.readdword(u + 0x274))
        end
      end
    end
    L.log(table.concat(parts, " | "))
  end
end)
