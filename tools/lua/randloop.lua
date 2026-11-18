-- Random-quest sweep (text coverage): reopen a guild counter's Quest Select board again and again with the quest
-- interpreter's random roll (op `23 64`, rand 0..99, stored to ctx+0xC at 0x02010170) held at one value per round,
-- so every `13 lo hi pc` range of the random boards (quest.img 0x11F4.. / 0x1298.., tables 0x11D4 / 0x11E4) is
-- picked once. Run after warp.lua on scene quest_counter or quest_counter2 and before textlog.lua:
--   emu.py build/beet_en.nds --debugger --out work/qa/cover/qrand_1 --script tools/debug/warp.lua
--     --script tools/lua/randloop.lua --script tools/lua/textlog.lua --var "SCENE='quest_counter'" --frames N
-- Globals: RAND_VALUES (Lua table; default = every range start of the six boards), RAND_START (1500),
-- RAND_PERIOD (400). Per round: Take a Quest (t135,59), Details (first row, t14,176), Back, Back. Logs RANDLOOP v.
local vals = RAND_VALUES or { 0, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 23, 25, 26, 27, 29, 31, 33, 34, 37, 38, 41, 42,
  45, 49, 51, 53, 56, 57, 60, 61, 64, 65, 67, 69, 71, 73, 75, 76, 77, 78, 81, 82, 85, 86, 89, 91, 93, 96 }
local start, period = RAND_START or 1500, RAND_PERIOD or 400
local k, cur = 0, nil
L.on_exec(0x02010170, function()
  if cur then memory.setregister("arm9.r0", cur) end
end)
L.on_frame(function(f)
  if f >= start and (f - start) % period == 0 and k < #vals then
    k = k + 1
    cur = vals[k]
    L.log(string.format("RANDLOOP %d f%d", cur, f))
    L.press("t135,59", 6); L.press("-", 120)
    L.press("t14,176", 6); L.press("-", 80)
    L.press("t240,176", 6); L.press("-", 40)
    L.press("t240,176", 6); L.press("-", 60)
  end
end)
