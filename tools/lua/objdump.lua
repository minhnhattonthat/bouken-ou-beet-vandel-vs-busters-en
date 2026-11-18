-- Find an object in main RAM by a byte pattern and log N bytes around it at the given frames, to diff a field
-- between two screens (e.g. the name-entry keyboard tab before and after touching 英字).
--   --var "PAT='1c0125012f01'" --var "BACK=0xE0" --var "N=0x400" --var "AT='100,400'" [--var "START=0x021C8000"]
--   (START skips the static arm9 copy of the pattern)
-- Log lines: `DUMP fNNN ADDR hex...` (32 bytes per line, ADDR = pattern address - BACK + offset).
local pat = PAT or error("set PAT (hex bytes)")
local back, n = BACK or 0, N or 0x200
local bytes = {}
for h in pat:gmatch("%x%x") do bytes[#bytes + 1] = tonumber(h, 16) end
local at = {}
for f in (AT or "100"):gmatch("%d+") do at[tonumber(f)] = true end

local function find()
  for a = START or 0x02000000, 0x023FFFFF - #bytes, 2 do
    if memory.readbyte(a) == bytes[1] then
      local ok = true
      for i = 2, #bytes do
        if memory.readbyte(a + i - 1) ~= bytes[i] then ok = false; break end
      end
      if ok then return a end
    end
  end
end

L.on_frame(function(f)
  if not at[f] then return end
  local p = find()
  if not p then L.log(string.format("DUMP f%d pattern not found", f)); return end
  local base = p - back
  L.log(string.format("DUMP f%d pattern at %08X base %08X", f, p, base))
  for o = 0, n - 1, 32 do
    local t = {}
    for i = 0, 31 do t[#t + 1] = string.format("%02x", memory.readbyte(base + o + i)) end
    L.log(string.format("DUMP f%d %08X %s", f, base + o, table.concat(t)))
  end
end)
