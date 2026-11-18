-- Dump the field's position-trigger tree (field_obj+0xCC; looked up by 0x0203D84C, node key x,y bytes at +0xC,
-- script offset at +0x10) once, DUMP_AT frames into the run (default 60): every door / step trigger of the
-- current map with its script. The field object is taken from r0 of 0x0203D84C (called every idle field frame).
local fobj = nil
L.on_exec(0x0203D84C, function() fobj = memory.getregister("arm9.r0") end)
local at = DUMP_AT or 60
local function ram(a) return a >= 0x02000000 and a < 0x02400000 end
L.on_frame(function(n)
  if n ~= at then return end
  if not fobj then L.log("no field object yet"); return end
  local head = fobj + 0xCC
  local seen, queue, out = {}, {}, {}
  for k = 0, 2 do
    local p = memory.readdword(head + k * 4)
    if ram(p) then queue[#queue + 1] = p end
  end
  while #queue > 0 do
    local p = table.remove(queue)
    if not seen[p] and p ~= head and p ~= fobj + 0xD0 then
      seen[p] = true
      local x, y, s = memory.readbyte(p + 0xC), memory.readbyte(p + 0xD), memory.readdword(p + 0x10)
      out[#out + 1] = string.format("x%d y%d -> %05X", x, y, s)
      for k = 0, 2 do
        local q = memory.readdword(p + k * 4)
        if ram(q) and not seen[q] then queue[#queue + 1] = q end
      end
    end
  end
  table.sort(out)
  L.log(string.format("field obj %08X, %d trigger nodes", fobj, #out))
  for _, s in ipairs(out) do L.log("TRIG " .. s) end
end)
