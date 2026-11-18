-- Quest sweep (text coverage): reopen the guild's Quest Select board again and again, each time with one quest
-- block on it, so every fixed quest's title and description (quest/quest.img `20` / `1A` / `2D`) is drawn.
-- Run after warp.lua on scene quest_board and before textlog.lua:
--   emu.py build/beet_en.nds --debugger --out work/qa/p8_quests --script tools/debug/warp.lua
--     --script tools/lua/questloop.lua --script tools/lua/textlog.lua --var "SCENE='quest_board'" --frames N
-- How: the board (rom.img 4F at 0x3C288) runs the selection script at quest.img 0x1144 through the interpreter
-- 0x020111D0(ctx, pc); its slots are story-flag checks, each followed by `05 <quest pc>` (add a quest; handler
-- 0x02013A14 calls 0x02003CE0(obj, pc) at 0x02013AE0). Early in the story every check fails, so the board is
-- empty. Here the interpreter starts at 0x115B (the first slot's 05) instead, and that 05's pc becomes the next
-- quest block (a `20` title right after an FF, read from quest.img: 152 blocks). The other 58 titles live inside
-- the random-quest generators (0x11F4..) and are not reached this way.
-- Inputs per round, every PERIOD frames from START: Take a Quest (t135,59), the board's first row, Details, Back,
-- Back to the counter menu. Logs QUESTLOOP <pc> per forced block.
local function blocks()
  local root = OUT and OUT:match("^(.*)[/\\]work[/\\]")
  local f = io.open(QUEST_IMG or ((root or ".") .. "/work/fs/fs/quest/quest.img"), "rb")
  if not f then L.log("questloop: quest.img not found"); return {} end
  local d = f:read("*a"); f:close()
  local out = {}
  for p = 4, #d - 6 do   -- p = file offset; Lua strings are 1-based
    local op, prev, nxt = d:byte(p + 1), d:byte(p), d:byte(p + 6)
    if op == 0x20 and (p == 4 or prev == 0xFF) and (nxt == 0x1A or nxt == 0x2D) then out[#out + 1] = p end
  end
  return out
end
local pcs = blocks()
L.log("questloop: " .. #pcs .. " quest blocks")
local from, n = QUEST_FROM or 1, QUEST_N or #pcs
local start, period = QUEST_START or 1500, QUEST_PERIOD or 400
local k, cur = 0, nil
L.on_exec(0x020111D0, function()
  if cur and memory.getregister("arm9.r1") == 0x1144 then memory.setregister("arm9.r1", 0x115B) end
end)
L.on_exec(0x02013AE0, function()
  if cur then
    memory.setregister("arm9.r1", cur)
    L.log(string.format("QUESTLOOP %X f%d", cur, L.frame))
  end
end)
L.on_frame(function(f)
  if f >= start and (f - start) % period == 0 and k < n and from + k <= #pcs then
    cur = pcs[from + k]
    k = k + 1
    L.press("t135,59", 6); L.press("-", 120)
    L.press(QUEST_ROW or "t128,40", 6); L.press("-", 40)
    L.press(QUEST_DETAILS or "t14,176", 6); L.press("-", 80)
    L.press("t240,176", 6); L.press("-", 40)
    L.press("t240,176", 6); L.press("-", 60)
  end
end)
