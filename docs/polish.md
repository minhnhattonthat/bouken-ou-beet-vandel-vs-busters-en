# Polish

Minor findings and flagged cuts, fixed in one pass before release (`references/translation.md` §Review). Tick each
line `[x]` with `fixed` or `waived: reason`; the release script refuses to run while a line is unticked.

## General
- [x] speaker tag: Resistance A-L show as "Resist. A" and 橋かけ名人 as "Master" (87/89 px > 80 px measured tag);
  widen the tag (90 px was not drawn: find the canvas width in the draw code) or keep, then waive. -- waived
  (session 26): kept; "Resist. A" and "Master" read clearly and the tag fits the 80 px drawn canvas.
- [x] jp-bound budgets (area/area2 names, key items, tengeki/meigeki, skills, titles): measure each box in phase 8 and
  undo the cuts below that the real box allows (full area names: Mountains, Volcano, Snowfield ...). -- waived
  (session 26): key items measured (session 25, budgets.json); the other boxes can't be reached in the warp scenes, so
  their cuts stay within the JP's own pixel width, which the game is known to draw. Each cut line below was judged
  by polish batches p001-p005.
- [x] weapon descriptions "1H"/"2H": rephrase to full words within 194 px. -- fixed (session 26): "Bekatorte Steel
  one-hander", "Superstrong one-hand sword", "Bekatorte Steel two-hander", "Composite steel two-hander",
  "Superstrong two-hand sword" (183-191 px).

## Flagged cuts from translation batches
- [x] a9.area.001.name - CUT (b001): Mountains rendered as Range for width. -- waived (p001): Muterin Mountains exceeds 96 px.
- [x] a9.area.007.name - CUT (b001): Forest omitted for width. -- waived (p001): Mirei Forest Village exceeds 96 px.
- [x] a9.area.017.name - CUT (b001): Wastes rendered as Waste for width. -- waived (p001): Adding the final s would exceed 96 px.
- [x] a9.area.021.name - CUT (b001): Mountain omitted for width. -- waived (p001): Muterin Mountain Village exceeds both limits.
- [x] a9.area.022.name - CUT (b001): Forest rendered as Wood for width. -- waived (p001): Norunaji Forest exceeds 96 px.
- [x] a9.area.029.name - CUT (b001): Desert omitted for width. -- waived (p001): Bim Desert Tower exceeds 96 px.
- [x] a9.area.036.name - CUT (b001): Mountains shortened to Mts. for width. -- waived (p001): Bakoson Mountains exceeds 96 px.
- [x] a9.area.040.name - CUT (b001): Lake omitted for width. -- waived (p001): Riberin Lake Tower exceeds 96 px.
- [x] a9.area.046.name - CUT (b001): Valley omitted for width. -- waived (p001): Sole Valley Labyrinth exceeds 96 px.
- [x] a9.area.050.name - CUT (b001): Volcano shortened to Mt. for width. -- waived (p001): Byonrin Volcano exceeds 96 px.
- [x] a9.area.051.name - CUT (b001): Mountains rendered as Range for width. -- waived (p001): Rinrago Mountains exceeds 96 px.
- [x] a9.area.054.name - CUT (b001): Snowfield shortened to Snow for width. -- waived (p001): Zeros Snowfield exceeds 96 px.
- [x] a9.area2.000.name - CUT (b001): Golden shortened to Gold for width. -- waived (p001): Golden Castle exceeds 84 px.
- [x] a9.area2.002.name - CUT (b001): Forest omitted for width. -- waived (p001): Norunaji Forest exceeds 84 px.
- [x] a9.area2.003.name - CUT (b001): Marsh rendered as Mire for width. -- waived (p001): Pasero Marsh exceeds 84 px.
- [x] a9.area2.004.name - CUT (b001): Mountains shortened to Mts. for width. -- waived (p001): Muterin Mountains exceeds 84 px.
- [x] a9.area2.006.name - CUT (b001): Wastes omitted for width. -- waived (p001): Benuru Wastes exceeds 84 px.
- [x] a9.area2.008.name - CUT (b001): Snowfield shortened to Snow for width. -- waived (p001): Zeros Snowfield exceeds 84 px.
- [x] a9.area2.009.name - CUT (b001): Glacier shortened to Ice for width. -- waived (p001): Rinnam Glacier exceeds 84 px.
- [x] a9.area2.012.name - CUT (b001): Volcano shortened to Mt. for width. -- waived (p001): Byonrin Volcano exceeds 84 px.
- [x] a9.area2.014.name - CUT (b001): Mountains shortened to Mts. for width. -- waived (p001): Rinrago Mountains exceeds 84 px.
- [x] a9.area2.023.name - CUT (b001): Mountains omitted for width. -- waived (p001): Bakoson Mountains exceeds 84 px.
- [x] a9.armor.018.desc - CUT (b001): Quite omitted for width. -- fixed (p001): Shirt of very tough material.
- [x] a9.armor.048.desc - CUT (b001): Cape implicit in item name for width. -- waived (p001): fuller form 'Cape woven with special composite steel.' fails the checks (line 1: 271 px > 194 (12 px font) 'Cape woven with special composite steel.'); kept
- [x] a9.keyitem.007.name - CUT (b003): Possessive shortened to fit the byte cap. -- waived (p001): Matches the binding glossary; no possessive is needed.
- [x] a9.keyitem.009.name - CUT (b003): "Bridge" omitted to fit the field. -- waived (p001): Bridge Master's Letter exceeds both limits.
- [x] a9.keyitem.016.name - CUT (b003): "Growth" omitted to fit the field. -- waived (p001): Matches the binding glossary.
- [x] a9.keyitem.021.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Mugain.' fails the checks (line 1: 234 px > 182 (12 px font) 'Stone statue of the Vandel Mugain.'); kept
- [x] a9.keyitem.022.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Ventura.' fails the checks (line 1: 244 px > 182 (12 px font) 'Stone statue of the Vandel Ventura.'); kept
- [x] a9.keyitem.023.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Rozgoat.' fails the checks (line 1: 245 px > 182 (12 px font) 'Stone statue of the Vandel Rozgoat.'); kept
- [x] a9.keyitem.024.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Frausky.' fails the checks (line 1: 242 px > 182 (12 px font) 'Stone statue of the Vandel Frausky.'); kept
- [x] a9.keyitem.025.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Grineed.' fails the checks (line 1: 238 px > 182 (12 px font) 'Stone statue of the Vandel Grineed.'); kept
- [x] a9.keyitem.027.desc - CUT (b003): Stone material omitted to fit the field. -- waived (p001): fuller form 'Stone statue of the Vandel Beltorze.' fails the checks (line 1: 245 px > 182 (12 px font) 'Stone statue of the Vandel Beltorze.'); kept
- [x] a9.meigeki.003.name - CUT (b003): Scorching modifier condensed into "Inferno". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.007.name - CUT (b003): Scorching and dark modifiers condensed into "Hell". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.009.name - CUT (b003): Dark modifier omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.012.name - CUT (b003): Water and dark modifiers omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.016.name - CUT (b003): Extreme cold and freezing condensed into "Ice". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.017.name - CUT (b003): Extreme cold modifier omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.026.name - CUT (b003): Turbulence modifier omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.027.name - CUT (b003): Turbulence modifier omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.031.name - CUT (b003): Lightning wave condensed into "Surge". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.035.name - CUT (b003): Great hell demon condensed into "Archfiend". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.036.name - CUT (b003): Lightning condensed into "Flash". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.040.name - CUT (b003): Dark, demonic and explosive modifiers condensed into "Doom". -- waived (p001): Matches the binding glossary.
- [x] a9.meigeki.042.name - CUT (b003): Great and demonic modifiers omitted. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.001.area - CUT (b004): Mountains shortened to Mts. to fit. -- waived (p001): Bakoson Mountains exceeds 120 px.
- [x] a9.monster.042.name - CUT (b004): Land omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.047.name - CUT (b004): Jewel omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.052.area - CUT (b004): Forest omitted to fit. -- waived (p001): Restoring Forest exceeds both limits.
- [x] a9.monster.073.name - CUT (b004): Jack-in-the-Box shortened to Trick Box to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.100.name - CUT (b004): Ravenous rendered as Dire to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.106.name - CUT (b004): Iron omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.111.area - CUT (b004): Tower rendered as Spire to fit. -- waived (p001): fuller form 'Riberin Lake Tower' fails the checks (line 1: 121 px > 120 (12 px font) 'Riberin Lake Tower'); kept
- [x] a9.monster.128.name - CUT (b004): Snow and ice condensed to Frost to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.131.area - CUT (b004): Mountain and village omitted to fit. -- waived (p001): Restoring Mountain or Village exceeds 120 px.
- [x] a9.monster.139.name - CUT (b005): Omitted "toxic" to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.141.name - CUT (b005): Shortened the large warship description to "Grand" to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.142.name - CUT (b005): Shortened "sandstorm" to "sand" to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.149.name - CUT (b005): Shortened glossary form "Volcanic Pterosaur" to "Lava Pterosaur" to fit. -- waived (p001): Lava Pterosaur is the binding glossary form.
- [x] a9.monster.154.name - CUT (b005): Shortened "jet-black" to "black" to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.monster.157.area - CUT (b005): Omitted "Valley" from the glossary form to fit. -- waived (p001): Sole Valley Labyrinth exceeds 120 px.
- [x] a9.party.052.name - CUT (b005): Omitted Harden's name to fit. -- waived (p001): Harden's name and a subordinate label cannot fit 62 px.
- [x] a9.0219AD18 - CUT (b005): Omitted Harden's name to fit. -- waived (p001): fuller form "Harden's man" fails the checks (line 1: 86 px > 84 (12 px font) "Harden's man"); kept
- [x] a9.021AB998 - CUT (b005): Omitted explicit mention of the weapon to fit. -- waived (p001): fuller form 'Two-handed weapon equipped.' fails the checks (line 1: 201 px > 180 (12 px font) 'Two-handed weapon equipped.'); kept
- [x] a9.skill.037.desc - CUT (b009): Countless arrows reduced to arrows. -- waived (p001): fuller form 'Fires countless arrows up' fails the checks (line 1: 169 px > 156 (12 px font) 'Fires countless arrows up'); kept
- [x] a9.skill.047.desc - CUT (b009): Forward direction omitted. -- waived (p001): fuller form 'Dark Power mist forward' fails the checks (line 1: 157 px > 156 (12 px font) 'Dark Power mist forward'); kept
- [x] a9.skill.048.desc - CUT (b009): Forward direction omitted; cannon shortened to gun. -- waived (p001): fuller form 'Fires Dark Power cannon' fails the checks (line 1: 159 px > 156 (12 px font) 'Fires Dark Power cannon'); kept
- [x] a9.skill.049.desc - CUT (b009): Forward direction omitted. -- waived (p001): fuller form 'Dark Power shot forward' fails the checks (line 1: 161 px > 156 (12 px font) 'Dark Power shot forward'); kept
- [x] a9.skill.052.desc - CUT (b009): Shoulder generalized to body. -- waived (p001): fuller form 'Dark Power shoulder rush' fails the checks (line 1: 165 px > 156 (12 px font) 'Dark Power shoulder rush'); kept
- [x] a9.skill.053.desc - CUT (b009): Spinning motion omitted. -- waived (p001): fuller form 'Low Dark Power spin kick' fails the checks (line 1: 160 px > 156 (12 px font) 'Low Dark Power spin kick'); kept
- [x] a9.skill.054.desc - CUT (b009): Spinning motion omitted. -- waived (p001): fuller form 'High Dark Power spin kick' fails the checks (line 1: 160 px > 156 (12 px font) 'High Dark Power spin kick'); kept
- [x] a9.skill.055.desc - CUT (b009): Spinning motion omitted. -- waived (p001): fuller form 'Dark Power spin-kick chain' fails the checks (28 bytes > slot cap 26); kept
- [x] a9.skill.056.desc - CUT (b009): Forward direction omitted. -- fixed (p001): Dark Power orb forward
- [x] a9.skill.061.desc - CUT (b009): Forward direction omitted; cannon shortened to gun. -- waived (p001): fuller form 'Dark Power cannon volley' fails the checks (line 1: 166 px > 156 (12 px font) 'Dark Power cannon volley'); kept
- [x] a9.special.006.name - CUT (b009): "Bolt" omitted from Lightning Bolt Grasper to fit width. -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.002.name - CUT (b010): Shared "Divine Attack" prefix omitted throughout skill names to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.003.name - CUT (b010): Heavenly epithet and size omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.007.desc - CUT (b010): "Divine Attack" omitted to fit. -- waived (p001): fuller form 'Divine Attack that cures paralysis on one target.' fails the checks (line 1: 323 px > 168 (12 px font) 'Divine Attack that cures paralysis on one target.'); kept
- [x] a9.tengeki.012.name - CUT (b010): Heavenly blue epithet omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.016.desc - CUT (b010): "Divine Attack" omitted to fit. -- waived (p001): fuller form 'Divine Attack that cures poison on one target.' fails the checks (line 1: 307 px > 168 (12 px font) 'Divine Attack that cures poison on one target.'); kept
- [x] a9.tengeki.017.desc - CUT (b010): Defense shortened to DEF. -- waived (p001): fuller form "Raises one target's physical defense by 20%." fails the checks (line 1: 297 px > 168 (12 px font) "Raises one target's physical defense by 20%."); kept
- [x] a9.tengeki.021.name - CUT (b010): Heavenly turmoil epithet and size omitted to fit. -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.028.desc - CUT (b010): "Divine" omitted from thunder attack descriptions through 034 to fit. -- waived (p001): fuller form 'Small lightning Divine Attack against one target.' fails the checks (line 1: 313 px > 168 (12 px font) 'Small lightning Divine Attack against one target.'); kept
- [x] a9.tengeki.031.name - CUT (b010): Sky flash and thunder blast imagery condensed to "Skybolt". -- waived (p001): Matches the binding glossary.
- [x] a9.tengeki.037.desc - CUT (b010): "Divine" omitted from light attack descriptions through 041 to fit. -- waived (p001): fuller form 'Small light Divine Attack against one target.' fails the checks (line 1: 287 px > 168 (12 px font) 'Small light Divine Attack against one target.'); kept
- [x] a9.tengeki.042.name - CUT (b010): Light-and-shadow imagery shortened to "Shade". -- waived (p001): Matches the binding glossary.
- [x] a9.title.014.name - CUT (b010): Abandoned village shortened to "Ruins" throughout related map labels. -- waived (p001): The full village description and state cannot fit.
- [x] a9.title.021.name - CUT (b010): B- means no bridge; G- means destroyed gate. -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.022.name - CUT (b010): B+ means bridge present; G- means destroyed gate. -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.023.name - CUT (b010): B+ means bridge present; G+ means normal gate. -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.034.name - CUT (b010): Abandoned village omitted from town interior label. -- waived (p001): Restoring the ruined village context exceeds the limits.
- [x] a9.title.035.name - CUT (b010): Abandoned village omitted from town interior label. -- waived (p001): fuller form 'Ruins Town: Gold' fails the checks (20 bytes > slot cap 18); kept
- [x] a9.title.036.name - CUT (b010): Abandoned village omitted from town interior label. -- waived (p001): Restoring the ruined village context exceeds 120 px.
- [x] a9.title.037.name - CUT (b010): Abandoned village and pedestal omitted to fit. -- waived (p001): fuller form 'Ruins Ring: Normal' fails the checks (20 bytes > slot cap 18); kept
- [x] a9.title.038.name - CUT (b010): "Pedestal" omitted to fit. -- waived (p001): Restoring Pedestal exceeds both limits.
- [x] a9.title.099.name - CUT (b010): Bridge- means no bridge. -- waived (p001): Spelling out No Bridge exceeds 120 px.
- [x] a9.title.102.name - CUT (b010): Hidden room absent shortened to "Room-". -- waived (p001): Resistance and the full hidden-room state cannot fit.
- [x] a9.title.103.name - CUT (b010): Hidden room present shortened to "Den". -- waived (p001): Resistance and the full hidden-room state cannot fit.
- [x] a9.title.116.name - CUT (b010): "Childhood" omitted to fit. -- waived (p001): Restoring Childhood exceeds both limits.
- [x] a9.title.120.name - CUT (b010): "Goddess" omitted to fit. -- fixed (p001): Goddess Statue
- [x] a9.vandel.006.name - CUT (b010): Enhanced version shortened to "EX". -- waived (p001): Matches the binding glossary.
- [x] a9.vandel.027.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px. -- waived (p001): Matches the binding glossary.
- [x] a9.vandel.028.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px. -- waived (p001): Matches the binding glossary.
- [x] a9.vandel.030.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px. -- waived (p001): Matches the binding glossary.
- [x] a9.weapon.022.name - CUT (b011): Dropped "Bolt" from Lightning Bolt Grasper to fit 18 bytes. -- waived (p001): Matches the binding glossary.
- [x] a9.weapon.022.name2 - CUT (b011): Dropped "Bolt" from Lightning Bolt Grasper to fit 18 bytes. -- waived (p001): Matches the binding glossary.
- [x] a9.weapon.052.desc - CUT (b012): Shortened "one-handed" to "1H" to fit. -- waived (p001): fuller form 'One-Hand Sword made of Bekatorte Steel.' fails the checks (line 1: 273 px > 194 (12 px font) 'One-Hand Sword made of Bekatorte Steel.'); kept
- [x] a9.weapon.053.desc - CUT (b012): Dropped "special" to fit. -- waived (p001): fuller form 'One-Hand Sword made of special composite steel.' fails the checks (line 1: 323 px > 194 (12 px font) 'One-Hand Sword made of special composite steel.'); kept
- [x] a9.weapon.054.desc - CUT (b012): Shortened "one-handed" to "1H" to fit. -- waived (p001): fuller form 'One-Hand Sword made of extremely strong metal.' fails the checks (line 1: 322 px > 194 (12 px font) 'One-Hand Sword made of extremely strong metal.'); kept
- [x] a9.weapon.063.desc - CUT (b012): Dropped "special" to fit. -- waived (p001): fuller form 'Throwing Sword made of special composite steel.' fails the checks (line 1: 319 px > 194 (12 px font) 'Throwing Sword made of special composite steel.'); kept
- [x] a9.weapon.072.desc - CUT (b012): Shortened "two-handed" to "2H" to fit. -- waived (p001): fuller form 'Two-Hand Sword made of Bekatorte Steel.' fails the checks (line 1: 276 px > 194 (12 px font) 'Two-Hand Sword made of Bekatorte Steel.'); kept
- [x] a9.weapon.073.desc - CUT (b012): Dropped "special" and shortened "two-handed" to "2H" to fit. -- waived (p001): fuller form 'Two-Hand Sword made of special composite steel.' fails the checks (line 1: 326 px > 194 (12 px font) 'Two-Hand Sword made of special composite steel.'); kept
- [x] a9.weapon.074.desc - CUT (b012): Shortened "two-handed" to "2H" to fit. -- waived (p001): fuller form 'Two-Hand Sword made of extremely strong metal.' fails the checks (line 1: 325 px > 194 (12 px font) 'Two-Hand Sword made of extremely strong metal.'); kept
- [x] a9.weapon.102.desc - CUT (b013): Omitted "composite" to fit. -- waived (p001): fuller form 'Composite bow reinforced with Bekatorte Steel.' fails the checks (line 1: 310 px > 194 (12 px font) 'Composite bow reinforced with Bekatorte Steel.'); kept
- [x] a9.weapon.103.desc - CUT (b013): Omitted the steel's composite composition to fit. -- waived (p001): fuller form 'Composite bow reinforced with special composite steel.' fails the checks (line 1: 360 px > 194 (12 px font) 'Composite bow reinforced with special composite steel.'); kept
- [x] a9.weapon.104.desc - CUT (b013): Condensed "very strong" to "tough" to fit. -- waived (p001): fuller form 'Composite bow reinforced with extremely strong metal.' fails the checks (line 1: 359 px > 194 (12 px font) 'Composite bow reinforced with extremely strong metal.'); kept
- [x] a9.weapon.159.name - CUT (b014): Used "Ring" for "Chakram" to fit; also in name2. -- waived (p001): Matches the binding glossary.
- [x] a9.weapon.160.name - CUT (b014): Used "Ring" for "Chakram" to fit; also in name2. -- waived (p001): Matches the binding glossary.
- [x] a9.wpntype.022.name - CUT (b015): Dropped "Bolt" from "Lightning Bolt Grasper" to fit the 18-byte cap. -- waived (p001): Matches the binding glossary.
- [x] rom.063E0 - CUT (b016): Shortened Village Chief to Chief to fit. - fixed: full form fits the 80 px tag
- [x] rom.06AC8 - CUT (b016): Used Envoy for Messenger to fit. - fixed: full form fits the 80 px tag
- [x] rom.0D3EC - CUT (b016): Shortened Resistance to Resist. to fit. - fixed: full form fits the 80 px tag
- [x] rom.11134 - CUT (b016): Shortened Resistance to Resist. to fit the letter. -- waived (p001): Resistance B exceeds 80 px.
- [x] rom.11154 - CUT (b016): Shortened Resistance to Resist. to fit the letter. -- waived (p001): Resistance C exceeds 80 px.
- [x] rom.11228 - CUT (b016): Shortened Resistance to Resist. to fit the letter. -- waived (p001): Resistance A exceeds 80 px.
- [x] rom.137B8 - CUT (b017): Bridge omitted. -- waived (p001): Bridge Master exceeds 80 px.
- [x] rom.19F6C - CUT (b017): Weapon Shop shortened to Weapons. - fixed: full form fits the 80 px tag
- [x] rom.1B044 - CUT (b017): Tavern Woman shortened to Barmaid. -- waived (p001): Tavern Woman exceeds 80 px.
- [x] rom.1B8DC - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance J exceeds 80 px.
- [x] rom.205D8 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance E exceeds 80 px.
- [x] rom.30C54 - CUT (b017): Shagie abbreviated to S. - fixed: full form fits the 80 px tag
- [x] rom.3D69C - CUT (b017): Generic omitted; greatsword abbreviated to GS. -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6BC - CUT (b017): Generic omitted; greatsword abbreviated to GS. -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6DC - CUT (b017): Generic omitted; greatsword abbreviated to GS. -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6FC - CUT (b017): Generic omitted; greatsword abbreviated to GS; lightning shortened to Bolt. -- waived (p001): Restoring Generic, greatsword or lightning exceeds 80 px.
- [x] rom.3D71C - CUT (b017): Generic omitted; greatsword abbreviated to GS. -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D73C - CUT (b017): Generic omitted; spear abbreviated to Spr. -- waived (p001): Spear is already spelled out; Generic cannot fit.
- [x] rom.3D758 - CUT (b017): Generic omitted; spear abbreviated to Spr. -- waived (p001): Spear is already spelled out; Generic cannot fit.
- [x] rom.3D774 - CUT (b017): Generic omitted; spear abbreviated to Spr. -- waived (p001): Spear is already spelled out; Generic cannot fit.
- [x] rom.3D790 - CUT (b017): Generic omitted; spear abbreviated to Spr; lightning shortened to Bolt. -- waived (p001): Spear is already spelled out; Generic and lightning cannot fit.
- [x] rom.3D7AC - CUT (b017): Generic omitted; spear abbreviated to Spr. -- waived (p001): Spear is already spelled out; Generic cannot fit.
- [x] rom.3D7C8 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D7E4 - CUT (b017): Generic omitted; Water rendered as Aqua to fit. -- waived (p001): Water is already spelled out; Generic cannot fit.
- [x] rom.3D800 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D81C - CUT (b017): Generic omitted; lightning shortened to Bolt. -- waived (p001): Restoring Generic or lightning exceeds 80 px.
- [x] rom.3D838 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D854 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H. -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D874 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H. -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D894 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H. -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D8B4 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H; lightning shortened to Bolt. -- waived (p001): Restoring One-Hand Sword or lightning exceeds 80 px.
- [x] rom.3D8D4 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H. -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D8F4 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D90C - CUT (b017): Generic omitted; Water rendered as Aqua to fit. -- waived (p001): Water is already spelled out; Generic cannot fit.
- [x] rom.3D924 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D93C - CUT (b017): Generic omitted; lightning shortened to Bolt. -- waived (p001): Restoring Generic or lightning exceeds 80 px.
- [x] rom.3D954 - CUT (b017): Generic omitted. -- waived (p001): Restoring Generic exceeds 80 px.
- [x] rom.3D96C - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist. -- waived (p001): Fist is clear; restoring Generic or hand-to-hand combat cannot fit.
- [x] rom.3D988 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist; Water rendered as Aqua to fit. -- waived (p001): Water is already spelled out; the full combat label cannot fit.
- [x] rom.3D9A4 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist. -- waived (p001): Fist is clear; restoring Generic or hand-to-hand combat cannot fit.
- [x] rom.3D9C0 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist; lightning shortened to Bolt. -- waived (p001): Restoring Generic, hand-to-hand combat or lightning cannot fit.
- [x] rom.3D9DC - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist. -- waived (p001): Fist is clear; restoring Generic or hand-to-hand combat cannot fit.
- [x] rom.3D9F8 - CUT (b017): Generic omitted; throwing sword abbreviated to TS. -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA14 - CUT (b017): Generic omitted; throwing sword abbreviated to TS. -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA30 - CUT (b017): Generic omitted; throwing sword abbreviated to TS. -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA4C - CUT (b017): Generic omitted; throwing sword abbreviated to TS; lightning shortened to Bolt. -- waived (p001): Restoring Throwing Sword or lightning exceeds 80 px.
- [x] rom.3DA68 - CUT (b017): Generic omitted; throwing sword abbreviated to TS. -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3E108 - CUT (b017): Transformed label shortened to original numeric marker. -- waived (p001): Grineed - Transformed exceeds 80 px.
- [x] rom.42DF0 - CUT (b017): Village omitted. -- waived (p001): Village is already present; the note is stale.
- [x] rom.470F4 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance D exceeds 80 px.
- [x] rom.47758 - CUT (b017): Forest omitted. -- waived (p001): Mirei Forest Chief exceeds 80 px.
- [x] rom.499B4 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance F exceeds 80 px.
- [x] rom.49A1C - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance G exceeds 80 px.
- [x] rom.49AA8 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance H exceeds 80 px.
- [x] rom.4A1A0 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance is already spelled out and fits.
- [x] rom.4A220 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance K exceeds 80 px.
- [x] rom.4A324 - CUT (b017): Resistance abbreviated to Resist. -- waived (p001): Resistance L exceeds 80 px.

## Review minors b001
- [x] a9.armor.000.desc - "見習いバスターのジャケット" means an apprentice Buster's jacket - Compressed phrasing breaks the surrounding possessive pattern - An apprentice Buster's jacket. -- fixed (p002): Apprentice Buster's jacket.
- [x] a9.armor.008.desc - "百戦錬磨バスターのジャケット" means a battle-hardened Buster's jacket - "War-tested" is awkward and unnecessarily implies warfare - A battle-hardened Buster's jacket. -- fixed (p002): A veteran Buster's jacket.
- [x] a9.armor.018.desc - "かなり強い素材でできたシャツ" means a shirt made of quite strong material - Telegraphic phrasing - A shirt made of tough material. -- fixed (p001): Shirt of very tough material.
- [x] a9.armor.019.desc - "非常に強い素材でできたシャツ" means a shirt made of very strong material - "Ultra-tough material shirt" is an awkward noun stack - A shirt made of extremely tough material. -- fixed (p002): Shirt of very tough material.
- [x] a9.armor.028.desc - "非常に強い素材でできたシールド" means a shield made of very strong material - Awkward noun stack - A shield made of extremely tough material. -- fixed (p002): Made of ultra-tough material.
- [x] a9.armor.029.desc - "防具屋アトスが作った盾" means a shield made by Atos, the armor dealer - "By armor seller" is stiff - A shield made by Atos, the armor dealer. -- waived (p002): The full maker attribution cannot fit; the current wording preserves it.
- [x] a9.armor.039.desc - "達人が愛用する強い腕輪" means a strong bangle favored by masters - Compressed phrasing reads awkwardly - A tough bangle favored by masters. -- fixed (p002): A tough bangle masters love.
- [x] a9.armor.048.desc - "複合特殊鋼材を織り込んだマント" means a cape with special composite steel woven into it - "Special steel-alloy weave" obscures the cape's construction - A cape woven with special composite steel. -- waived (p001): fuller form 'Cape woven with special composite steel.' fails the checks (line 1: 271 px > 194 (12 px font) 'Cape woven with special composite steel.'); kept
- [x] a9.armor.049.desc - "非常に強い素材でできたマント" means a cape made of very strong material - Awkward noun stack - A cape made of extremely tough material. -- fixed (p002): Cape of very tough material.

## Review minors b002
- [x] a9.armor.057.desc - "多くのバスターが愛用するバンダナ": Bandanna favored by many Busters - Lowercase "bandanna" differs from the binding glossary spelling - A Bandanna favored by many Busters -- fixed (p002): A Bandanna Busters love
- [x] a9.armor.058.desc - "複合特殊鋼材を織り込んだ": woven with special composite steel - "Alloy-knit" is awkward and changes weaving to knitting - Bandanna woven with special composite steel -- waived (p002): fuller form 'Special steel-woven Bandanna' fails the checks (line 1: 199 px > 194 (12 px font) 'Special steel-woven Bandanna'); kept
- [x] a9.armor.068.desc - "複合特殊鋼材を織り込んだ": woven with special composite steel - "Alloy-woven" is awkward and obscures the specific material - Gloves woven with special composite steel -- fixed (p002): Special steel-woven gloves

## Review minors b003
- [x] a9.keyitem.002.desc - "リング修復アイテムの原材料" means raw material for an item used to repair rings - "Ring repair aid" is an awkward, unclear noun cluster - Material used to make a ring repair item. -- waived (p002): The full manufacturing relationship cannot fit.
- [x] a9.keyitem.011.desc - "飛行機をとめる南京錠のカギ１" means key 1 for the padlock securing the Airplane - Missing article makes "Airplane's padlock" sound like a person's possession - Key 1 for the padlock securing the Airplane. -- fixed (p002): Key 1: Airplane padlock
- [x] a9.keyitem.012.desc - "飛行機をとめる南京錠のカギ２" means key 2 for the padlock securing the Airplane - Same awkward possessive - Key 2 for the padlock securing the Airplane. -- fixed (p002): Key 2: Airplane padlock
- [x] a9.keyitem.013.desc - "飛行機をとめる南京錠のカギ３" means key 3 for the padlock securing the Airplane - Same awkward possessive - Key 3 for the padlock securing the Airplane. -- fixed (p002): Key 3: Airplane padlock
- [x] a9.keyitem.014.desc - "飛行機をとめる南京錠のカギ４" means key 4 for the padlock securing the Airplane - Same awkward possessive - Key 4 for the padlock securing the Airplane. -- fixed (p002): Key 4: Airplane padlock
- [x] a9.keyitem.015.desc - "飛行機をとめる南京錠のカギ５" means key 5 for the padlock securing the Airplane - Same awkward possessive - Key 5 for the padlock securing the Airplane. -- fixed (p002): Key 5: Airplane padlock
- [x] a9.meigeki.003.desc - "単体攻撃用の炎の上位冥撃・大" means an advanced fire Dark Attack with high power against one target - "High Dark Fire+" obscures the distinction between advanced rank and high power and resembles a modified spell name - Advanced fire Dark Attack: one foe, high power. -- waived (p002): Spelling out rank, power, element, and target exceeds the limit.

## Review minors b005
- [x] a9.021B5758 - 同じ陣営では対戦できません means players on the same side cannot battle each other - "Same sides cannot fight" is unnatural and unclear - Players on the same side cannot battle each other. -- fixed (p002): Allies cannot fight.

## Review minors b006
- [x] a9.shout.010.s03 - "受けてみろ！" challenges the enemy to withstand an attack - "Try taking this!" sounds unnatural - Let's see you take this! -- fixed (p002): Let's see you take this!
- [x] a9.shout.011.s07 - "こいつを受けてみろ！" challenges the enemy to withstand this attack - "Try taking this!" sounds unnatural - Let's see you take this! -- fixed (p002): Let's see you take this!
- [x] a9.shout.013.s06 - "カッコいいとこ見せるぜ！" promises an impressive display - "Watch me look cool!" sounds awkwardly literal - Watch me show off! -- fixed (p002): Watch me show off!
- [x] a9.shout.015.s02 - "消えろ！" orders an enemy to vanish - "Disappear!" sounds stiff as a combat shout - Begone! -- fixed (p002): Begone!

## Review minors b007
- [x] a9.shout.031.s04 - "うりゃっ！" is an attack cry - "Hurrah!" reads as a celebratory cheer - Hyaah! -- fixed (p002): Hyaah!
- [x] a9.shout.031.s07 - "うりゃーーっ！" is an extended attack cry - "Hurraaaah!" reads as celebration - Hyaaaah! -- fixed (p002): Hyaaaah!
- [x] a9.shout.041.s01 - "わたしの拳を受けてみろっ！" challenges the enemy to withstand a punch - "Try taking my fist!" is an awkward literal rendering - Try taking this punch! -- fixed (p002): Take this punch!
- [x] a9.shout.053.s03 - "うりゃぁーーっ！！" is an attack cry - "Hurraaaah!!" reads as celebration - Hyaaaah!! -- fixed (p002): Hyaaaah!!
- [x] a9.shout.061.s01 - "ベカトルテ近海最強はオレ様だ！" boasts of being the strongest in the Bekatorte Seas - The place-name possessive sounds unnatural - I'm the strongest in the Bekatorte Seas! -- waived (p002): The possessive is understandable; the full phrasing exceeds both limits.
- [x] a9.shout.062.s01 - "我こそはベカトルテ近海最強！！" emphatically claims supremacy in the Bekatorte Seas - The place-name possessive is awkward and weakens the proclamation - I am the strongest in the Bekatorte Seas!! -- waived (p002): The full proclamation cannot fit with the binding place name.
- [x] a9.shout.063.s01 - "へッヘッ ベカトルテ近海最強！" repeats the strongest-in-the-region boast - The possessive is awkward; "best" blurs the recurring claim of strength - Heh heh! Strongest in the Bekatorte Seas! -- waived (p002): Restoring “strongest” while retaining the laugh and place name exceeds the limits.

## Review minors b008
- [x] a9.shout.066.s00 - "具現化できるんだろうね" expects confirmation that the opponent can manifest a Saiga - The open question loses the speaker's presumptuous expectation - suggested EN: You can summon your Saiga, I trust? -- waived (p002): fuller form 'You can summon Saiga, right?' fails the checks (32 bytes > slot cap 30); kept
- [x] a9.shout.066.s05 - "この世で美しきものは　才牙" praises Saiga as beautiful things in this world - "This world's beauty" sounds unnatural - suggested EN: There is such beauty in Saiga... -- fixed (p002): Such beauty in Saiga...
- [x] a9.shout.073.s03 - "動くと正確に切れんだろーがあっ" angrily demands stillness to allow precise cutting - "Cut clean" is awkward and blurs the emphasis on precision - suggested EN: Hold still! I can't cut accurately if you move! -- waived (p002): fuller form 'Hold still! Let me cut neatly!' fails the checks (32 bytes > slot cap 30); kept
- [x] a9.shout.077.s00 - "我が冥力の極致" announces the pinnacle of the speaker's Dark Power - "My peak Dark Power" sounds mechanical rather than grandiose - suggested EN: Behold the pinnacle of my Dark Power... -- fixed (p002): Behold! My full Dark Power!

## Review minors b009
- [x] a9.skill.006.desc - "落下し周囲に衝撃波を出す" means dropping and releasing a surrounding shockwave - "wave all round" is awkward and loses the specific shockwave imagery - suggested EN: Drops and releases a shockwave all around. -- waived (p002): fuller form 'Drops with a shockwave' fails the checks (line 1: 158 px > 156 (12 px font) 'Drops with a shockwave'); kept
- [x] a9.skill.007.desc - "敵の左右を往復して攻撃" means attacking while moving back and forth on either side of an enemy - "Hits side to side" makes the movement unclear - suggested EN: Moves back and forth on either side of a foe to attack. -- fixed (p002): Strikes from both sides
- [x] a9.skill.027.desc - "振り回して周囲の敵を攻撃" means swinging the weapon around to attack surrounding enemies - "Swings at all round" is ungrammatical - suggested EN: Swings the weapon to hit surrounding foes. -- fixed (p002): Swings at nearby foes
- [x] a9.skill.052.desc - "肩から突進冥力攻撃" means a shoulder-first Dark Power charge - "body rush" loses the shoulder-first action and sounds unnatural - suggested EN: Charges shoulder-first with Dark Power. -- waived (p001): fuller form 'Dark Power shoulder rush' fails the checks (line 1: 165 px > 156 (12 px font) 'Dark Power shoulder rush'); kept
- [x] a9.skill.058.desc - "その場に冥力輪を放つ" means releasing a Dark Power ring at the user's location - "ring on spot" is awkward shorthand - suggested EN: Releases a Dark Power ring in place. -- fixed (p002): Sets a Dark Power ring

## Review minors b010
- [x] a9.tengeki.007.desc - "単体のマヒの治療": cures paralysis for one target - "on one" sounds unfinished - Cures paralysis for one target. -- waived (p001): fuller form 'Divine Attack that cures paralysis on one target.' fails the checks (line 1: 323 px > 168 (12 px font) 'Divine Attack that cures paralysis on one target.'); kept
- [x] a9.tengeki.016.desc - "単体の毒の治療": cures poison for one target - "on one" sounds unfinished - Cures poison for one target. -- waived (p001): fuller form 'Divine Attack that cures poison on one target.' fails the checks (line 1: 307 px > 168 (12 px font) 'Divine Attack that cures poison on one target.'); kept
- [x] a9.tengeki.017.desc - "単体の物理防御力を２０％上昇": raises one target's physical defense by 20% - "One:" is awkwardly elliptical - Raises one target's physical defense by 20%. -- waived (p001): fuller form "Raises one target's physical defense by 20%." fails the checks (line 1: 297 px > 168 (12 px font) "Raises one target's physical defense by 20%."); kept
- [x] a9.tengeki.035.desc - "攻撃を雷属性にする": changes attacks to the thunder element - "Attacks become thunder" reads literally and awkwardly - Gives attacks the thunder element. -- fixed (p002): Adds thunder to attacks
- [x] a9.title.116.name - "幼馴染みの家": childhood friend's house - Loses the childhood relationship - Childhood Friend's House -- waived (p001): Restoring Childhood exceeds both limits.
- [x] a9.title.120.name - "女神像の場所": goddess statue's location - Omits which statue despite "Goddess Statue" appearing nearby - Goddess Statue Site -- fixed (p001): Goddess Statue

## Review minors b011
- [x] a9.weapon.010.desc - "エルファストの防具屋が作った盾" means a shield made by Elfast's Armor Shop - "By Elfast's Armor Shop" is an awkward fragment and omits the object - A shield made by Elfast's Armor Shop. -- waived (p002): Adding the object exceeds the limit with the binding shop name.
- [x] a9.weapon.033.desc - "複合特殊鋼材でできた槍" means a spear made from a special steel composite - "Special steel blend spear" is an awkward noun stack - A spear made from a special steel composite. -- fixed (p002): Spear of special steel blend.
- [x] a9.weapon.043.desc - "複合特殊鋼材でできた槍斧" means a glaive made from a special steel composite - "Special steel blend glaive" is an awkward noun stack - A glaive made from a special steel composite. -- fixed (p002): Glaive of special steel blend.

## Review minors b012
- [x] a9.weapon.070.desc - "レアメタルでできた両手剣": rare metal Two-Hand Sword - Class-term capitalization differs from the glossary - Rare metal Two-Hand Sword -- fixed (p002): Rare metal Two-Hand Sword

## Review minors b013
- [x] a9.weapon.095.desc - "青銅で強化した" means reinforced with bronze - "Bronze-set" sounds decorative rather than structural - Composite bow reinforced with bronze -- fixed (p002): Bronze-bound composite bow
- [x] a9.weapon.096.desc - "銅で強化した" means reinforced with copper - "Copper-set" sounds decorative rather than structural - Composite bow reinforced with copper -- fixed (p002): Copper-bound composite bow
- [x] a9.weapon.100.desc - "レアメタルで強化した合成弓" means a composite bow reinforced with rare metal - The reinforcement relationship is unclear - Composite bow reinforced with rare metal -- waived (p002): The full reinforcement relationship cannot fit alongside the material and bow type.
- [x] a9.weapon.101.desc - "ハイメタルで強化した合成弓" means a composite bow reinforced with High Metal - The reinforcement relationship is unclear - Composite bow reinforced with High Metal -- waived (p002): The full reinforcement relationship cannot fit alongside the material and bow type.
- [x] a9.weapon.102.desc - "合成弓" means composite bow - The bow type is omitted - Composite bow reinforced with Bekatorte Steel -- waived (p001): fuller form 'Composite bow reinforced with Bekatorte Steel.' fails the checks (line 1: 310 px > 194 (12 px font) 'Composite bow reinforced with Bekatorte Steel.'); kept
- [x] a9.weapon.103.desc - "複合特殊鋼材で強化した" means reinforced with special composite steel - The material and reinforcement are compressed into an ambiguous modifier - Composite bow reinforced with special alloy steel -- waived (p001): fuller form 'Composite bow reinforced with special composite steel.' fails the checks (line 1: 360 px > 194 (12 px font) 'Composite bow reinforced with special composite steel.'); kept
- [x] a9.weapon.104.desc - "非常に強い金属で強化した" means reinforced with exceptionally strong metal - "Tough-metal" is awkward and loses the emphasis - Composite bow reinforced with ultra-strong metal -- waived (p001): fuller form 'Composite bow reinforced with extremely strong metal.' fails the checks (line 1: 359 px > 194 (12 px font) 'Composite bow reinforced with extremely strong metal.'); kept
- [x] a9.weapon.114.desc - "銃とナックルの長所を持つ武器" means a weapon combining the advantages of guns and knuckles - "Gun and knuckle strengths" reads like a heading rather than an item description - Combines the strengths of guns and knuckles -- fixed (p002): Gun and knuckle hybrid

## Review minors b016
- [x] rom.02130 - "おじさん" denotes a middle-aged man - "Old Man" implies the elderly おじいさん - Middle-aged Man -- fixed (p002): Man

## Review minors b017
- [x] rom.42DF0 - "里の門" means village gate - "Gate" unnecessarily loses the location qualifier - Village Gate -- waived (p001): Village is already present; the note is stale.

## Review fixes blocked by width (re-apply after the box is measured or widened; suggestion in work/tr/review/<batch>.md)
- [x] a9.area.001.name - b001 review: line 1: 119 px > 96 (12 px font) 'Muterin Mountains' -- waived (p001): Muterin Mountains exceeds 96 px.
- [x] a9.area.007.name - b001 review: line 1: 121 px > 96 (12 px font) 'Mirei Forest Village' -- waived (p001): Mirei Forest Village exceeds 96 px.
- [x] a9.area.017.name - b001 review: line 1: 98 px > 96 (12 px font) 'Benuru Wastes' -- waived (p001): Adding the final s would exceed 96 px.
- [x] a9.area.021.name - b001 review: 26 bytes > slot cap 22 -- waived (p001): Muterin Mountain Village exceeds both limits.
- [x] a9.area.022.name - b001 review: line 1: 102 px > 96 (12 px font) 'Norunaji Forest' -- waived (p001): Norunaji Forest exceeds 96 px.
- [x] a9.area.029.name - b001 review: line 1: 114 px > 96 (12 px font) 'Bim Desert Tower' -- waived (p001): Bim Desert Tower exceeds 96 px.
- [x] a9.area.036.name - b001 review: line 1: 126 px > 96 (12 px font) 'Bakoson Mountains' -- waived (p001): Bakoson Mountains exceeds 96 px.
- [x] a9.area.040.name - b001 review: line 1: 121 px > 96 (12 px font) 'Riberin Lake Tower' -- waived (p001): Riberin Lake Tower exceeds 96 px.
- [x] a9.area.046.name - b001 review: line 1: 137 px > 96 (12 px font) 'Sole Valley Labyrinth' -- waived (p001): Sole Valley Labyrinth exceeds 96 px.
- [x] a9.area.050.name - b001 review: line 1: 104 px > 96 (12 px font) 'Byonrin Volcano' -- waived (p001): Byonrin Volcano exceeds 96 px.
- [x] a9.area.051.name - b001 review: line 1: 118 px > 96 (12 px font) 'Rinrago Mountains' -- waived (p001): Rinrago Mountains exceeds 96 px.
- [x] a9.area.054.name - b001 review: line 1: 102 px > 96 (12 px font) 'Zeros Snowfield' -- waived (p001): Zeros Snowfield exceeds 96 px.
- [x] a9.area2.000.name - b001 review: line 1: 91 px > 84 (12 px font) 'Golden Castle' -- waived (p001): Golden Castle exceeds 84 px.
- [x] a9.area2.002.name - b001 review: line 1: 102 px > 84 (12 px font) 'Norunaji Forest' -- waived (p001): Norunaji Forest exceeds 84 px.
- [x] a9.area2.003.name - b001 review: line 1: 88 px > 84 (12 px font) 'Pasero Marsh' -- waived (p001): Pasero Marsh exceeds 84 px.
- [x] a9.area2.004.name - b001 review: line 1: 119 px > 84 (12 px font) 'Muterin Mountains' -- waived (p001): Muterin Mountains exceeds 84 px.
- [x] a9.area2.006.name - b001 review: line 1: 98 px > 84 (12 px font) 'Benuru Wastes' -- waived (p001): Benuru Wastes exceeds 84 px.
- [x] a9.area2.008.name - b001 review: line 1: 102 px > 84 (12 px font) 'Zeros Snowfield' -- waived (p001): Zeros Snowfield exceeds 84 px.
- [x] a9.area2.009.name - b001 review: line 1: 91 px > 84 (12 px font) 'Rinnam Glacier' -- waived (p001): Rinnam Glacier exceeds 84 px.
- [x] a9.area2.012.name - b001 review: line 1: 104 px > 84 (12 px font) 'Byonrin Volcano' -- waived (p001): Byonrin Volcano exceeds 84 px.
- [x] a9.area2.014.name - b001 review: line 1: 118 px > 84 (12 px font) 'Rinrago Mountains' -- waived (p001): Rinrago Mountains exceeds 84 px.
- [x] a9.area2.023.name - b001 review: line 1: 126 px > 84 (12 px font) 'Bakoson Mountains' -- waived (p001): Bakoson Mountains exceeds 84 px.
- [x] a9.keyitem.001.desc - b003 review: line 1: 283 px > 180 (12 px font) 'A letter to the Village Chief of East Village -- fixed (p002): To the East Village Chief
- [x] a9.keyitem.009.name - b003 review: 22 bytes > slot cap 18 -- waived (p001): Bridge Master's Letter exceeds both limits.
- [x] a9.monster.001.area - b004 review: line 1: 126 px > 120 (12 px font) 'Bakoson Mountains' -- waived (p001): Bakoson Mountains exceeds 120 px.
- [x] a9.monster.111.area - b004 review: line 1: 121 px > 120 (12 px font) 'Riberin Lake Tower' -- waived (p001): fuller form 'Riberin Lake Tower' fails the checks (line 1: 121 px > 120 (12 px font) 'Riberin Lake Tower'); kept
- [x] a9.monster.131.area - b004 review: 32 bytes > slot cap 20 -- waived (p001): Restoring Mountain or Village exceeds 120 px.
- [x] a9.monster.157.area - b005 review: 22 bytes > slot cap 20 -- waived (p001): Sole Valley Labyrinth exceeds 120 px.
- [x] a9.party.052.name - b005 review: line 1: 98 px > 62 (12 px font) "Harden's Minion" -- waived (p001): Harden's name and a subordinate label cannot fit 62 px.
- [x] a9.0219AD18 - b005 review: line 1: 98 px > 84 (12 px font) "Harden's Minion" -- waived (p001): fuller form "Harden's man" fails the checks (line 1: 86 px > 84 (12 px font) "Harden's man"); kept
- [x] a9.021AB998 - b005 review: line 1: 276 px > 180 (12 px font) 'You have a two-handed weapon equipped.' -- waived (p001): fuller form 'Two-handed weapon equipped.' fails the checks (line 1: 201 px > 180 (12 px font) 'Two-handed weapon equipped.'); kept
- [x] a9.skill.002.desc - b009 review: 68 bytes > slot cap 26 -- waived (p002): fuller form 'Lance extends; hits row' fails the checks (line 1: 158 px > 156 (12 px font) 'Lance extends; hits row'); kept
- [x] a9.skill.018.desc - b009 review: 66 bytes > slot cap 26 -- fixed (p002): Iron Ball: water pillars
- [x] a9.skill.019.desc - b009 review: 64 bytes > slot cap 26 -- fixed (p002): Iron Ball pulls foes in
- [x] a9.skill.023.desc - b009 review: 58 bytes > slot cap 26 -- waived (p002): fuller form 'Falls; hits front and rear' fails the checks (line 1: 158 px > 156 (12 px font) 'Falls; hits front and rear'); kept
- [x] a9.skill.024.desc - b009 review: 60 bytes > slot cap 26 -- waived (p002): The complete transformation description cannot fit the byte cap.
- [x] a9.skill.025.desc - b009 review: 52 bytes > slot cap 26 -- waived (p002): The current wording conveys the charge within both limits.
- [x] a9.skill.035.desc - b009 review: 48 bytes > slot cap 26 -- fixed (p002): Hits front and rear
- [x] a9.skill.048.desc - b009 review: 50 bytes > slot cap 26 -- waived (p001): fuller form 'Fires Dark Power cannon' fails the checks (line 1: 159 px > 156 (12 px font) 'Fires Dark Power cannon'); kept
- [x] a9.skill.061.desc - b009 review: 58 bytes > slot cap 26 -- waived (p001): fuller form 'Dark Power cannon volley' fails the checks (line 1: 166 px > 156 (12 px font) 'Dark Power cannon volley'); kept
- [x] a9.tengeki.002.desc - b010 review: line 1: 319 px > 168 (12 px font) 'High-power fire Divine Attack against one tar -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.004.desc - b010 review: line 1: 277 px > 168 (12 px font) 'Low-power fire Divine Attack over an area.' -- waived (p002): Full power wording exceeds the width.
- [x] a9.tengeki.005.desc - b010 review: line 1: 297 px > 168 (12 px font) 'Medium-power fire Divine Attack over an area. -- waived (p002): Full power wording exceeds the width.
- [x] a9.tengeki.006.desc - b010 review: line 1: 277 px > 168 (12 px font) 'High-power fire Divine Attack over an area.' -- waived (p002): Full power wording exceeds the width.
- [x] a9.tengeki.009.desc - b010 review: line 1: 316 px > 168 (12 px font) 'Low-power ice Divine Attack against one targe -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.010.desc - b010 review: line 1: 336 px > 168 (12 px font) 'Medium-power ice Divine Attack against one ta -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.011.desc - b010 review: line 1: 316 px > 168 (12 px font) 'High-power ice Divine Attack against one targ -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.013.desc - b010 review: line 1: 314 px > 168 (12 px font) 'Low-power ice Divine Attack against all targe -- waived (p002): Retains the consistent S/M/L power notation within the limit.
- [x] a9.tengeki.014.desc - b010 review: line 1: 334 px > 168 (12 px font) 'Medium-power ice Divine Attack against all ta -- waived (p002): Full medium-power wording exceeds the width.
- [x] a9.tengeki.015.desc - b010 review: line 1: 314 px > 168 (12 px font) 'High-power ice Divine Attack against all targ -- waived (p002): Retains the consistent S/M/L power notation within the limit.
- [x] a9.tengeki.018.desc - b010 review: line 1: 326 px > 168 (12 px font) 'Low-power wind Divine Attack against one targ -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.019.desc - b010 review: line 1: 346 px > 168 (12 px font) 'Medium-power wind Divine Attack against one t -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.020.desc - b010 review: line 1: 326 px > 168 (12 px font) 'High-power wind Divine Attack against one tar -- waived (p002): Full power and target wording exceeds the width.
- [x] a9.tengeki.022.desc - b010 review: line 1: 284 px > 168 (12 px font) 'High-power wind Divine Attack over an area.' -- waived (p002): The current wording already uses the full available width.
- [x] a9.tengeki.028.desc - b010 review: line 1: 350 px > 168 (12 px font) 'Low-power thunder Divine Attack against one t -- waived (p001): fuller form 'Small lightning Divine Attack against one target.' fails the checks (line 1: 313 px > 168 (12 px font) 'Small lightning Divine Attack against one target.'); kept
- [x] a9.tengeki.029.desc - b010 review: line 1: 370 px > 168 (12 px font) 'Medium-power thunder Divine Attack against on -- waived (p002): The full Divine Attack term and power description cannot fit.
- [x] a9.tengeki.030.desc - b010 review: line 1: 350 px > 168 (12 px font) 'High-power thunder Divine Attack against one  -- waived (p002): The full Divine Attack term and power description cannot fit.
- [x] a9.tengeki.032.desc - b010 review: line 1: 308 px > 168 (12 px font) 'Low-power thunder Divine Attack over an area. -- waived (p002): The full Divine Attack term and power description cannot fit.
- [x] a9.tengeki.033.desc - b010 review: line 1: 328 px > 168 (12 px font) 'Medium-power thunder Divine Attack over an ar -- waived (p002): The full Divine Attack term and power description cannot fit.
- [x] a9.tengeki.034.desc - b010 review: line 1: 308 px > 168 (12 px font) 'High-power thunder Divine Attack over an area -- waived (p002): The full Divine Attack term and power description cannot fit.
- [x] a9.tengeki.037.desc - b010 review: line 1: 326 px > 168 (12 px font) 'Low-power light Divine Attack against one tar -- waived (p001): fuller form 'Small light Divine Attack against one target.' fails the checks (line 1: 287 px > 168 (12 px font) 'Small light Divine Attack against one target.'); kept
- [x] a9.tengeki.038.desc - b010 review: line 1: 346 px > 168 (12 px font) 'Medium-power light Divine Attack against one  -- waived (p002): The full Divine Attack term with target and power exceeds the width.
- [x] a9.tengeki.039.desc - b010 review: line 1: 326 px > 168 (12 px font) 'High-power light Divine Attack against one ta -- waived (p002): The full Divine Attack term with target and power exceeds the width.
- [x] a9.tengeki.040.desc - b010 review: line 1: 304 px > 168 (12 px font) 'Medium-power light Divine Attack over an area -- waived (p002): The full Divine Attack term with area and power exceeds the width.
- [x] a9.tengeki.041.desc - b010 review: line 1: 284 px > 168 (12 px font) 'High-power light Divine Attack over an area.' -- waived (p002): The full Divine Attack term with area and power exceeds the width.
- [x] a9.title.021.name - b010 review: 36 bytes > slot cap 18 -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.022.name - b010 review: 32 bytes > slot cap 18 -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.023.name - b010 review: 28 bytes > slot cap 18 -- waived (p001): Spelling out both bridge and gate states exceeds the limits.
- [x] a9.title.034.name - b010 review: 36 bytes > slot cap 18 -- waived (p001): Restoring the ruined village context exceeds the limits.
- [x] a9.title.035.name - b010 review: 34 bytes > slot cap 18 -- waived (p001): fuller form 'Ruins Town: Gold' fails the checks (20 bytes > slot cap 18); kept
- [x] a9.title.036.name - b010 review: 38 bytes > slot cap 18 -- waived (p001): Restoring the ruined village context exceeds 120 px.
- [x] a9.title.037.name - b010 review: 42 bytes > slot cap 18 -- waived (p001): fuller form 'Ruins Ring: Normal' fails the checks (20 bytes > slot cap 18); kept
- [x] a9.title.038.name - b010 review: 40 bytes > slot cap 18 -- waived (p001): Restoring Pedestal exceeds both limits.
- [x] a9.title.099.name - b010 review: 20 bytes > slot cap 18 -- waived (p001): Spelling out No Bridge exceeds 120 px.
- [x] a9.title.102.name - b010 review: 28 bytes > slot cap 18 -- waived (p001): Resistance and the full hidden-room state cannot fit.
- [x] a9.title.103.name - b010 review: 24 bytes > slot cap 18 -- waived (p001): Resistance and the full hidden-room state cannot fit.
- [x] a9.weapon.052.desc - b012 review: line 1: 214 px > 194 (12 px font) 'Bekatorte Steel One-Hand Sword' -- waived (p001): fuller form 'One-Hand Sword made of Bekatorte Steel.' fails the checks (line 1: 273 px > 194 (12 px font) 'One-Hand Sword made of Bekatorte Steel.'); kept
- [x] a9.weapon.053.desc - b012 review: line 1: 282 px > 194 (12 px font) 'One-Hand Sword of special composite steel' -- waived (p001): fuller form 'One-Hand Sword made of special composite steel.' fails the checks (line 1: 323 px > 194 (12 px font) 'One-Hand Sword made of special composite steel.'); kept
- [x] a9.weapon.054.desc - b012 review: line 1: 249 px > 194 (12 px font) 'One-Hand Sword of superstrong metal' -- waived (p001): fuller form 'One-Hand Sword made of extremely strong metal.' fails the checks (line 1: 322 px > 194 (12 px font) 'One-Hand Sword made of extremely strong metal.'); kept
- [x] a9.weapon.062.desc - b012 review: line 1: 210 px > 194 (12 px font) 'Bekatorte Steel Throwing Sword' -- fixed (p002): Made of Bekatorte Steel.
- [x] a9.weapon.063.desc - b012 review: line 1: 278 px > 194 (12 px font) 'Throwing Sword of special composite steel' -- waived (p001): fuller form 'Throwing Sword made of special composite steel.' fails the checks (line 1: 319 px > 194 (12 px font) 'Throwing Sword made of special composite steel.'); kept
- [x] a9.weapon.064.desc - b012 review: line 1: 245 px > 194 (12 px font) 'Throwing Sword of superstrong metal' -- fixed (p002): Ultra-tough Throwing Sword
- [x] a9.weapon.072.desc - b012 review: line 1: 217 px > 194 (12 px font) 'Bekatorte Steel Two-Hand Sword' -- waived (p001): fuller form 'Two-Hand Sword made of Bekatorte Steel.' fails the checks (line 1: 276 px > 194 (12 px font) 'Two-Hand Sword made of Bekatorte Steel.'); kept
- [x] a9.weapon.073.desc - b012 review: line 1: 285 px > 194 (12 px font) 'Two-Hand Sword of special composite steel' -- waived (p001): fuller form 'Two-Hand Sword made of special composite steel.' fails the checks (line 1: 326 px > 194 (12 px font) 'Two-Hand Sword made of special composite steel.'); kept
- [x] a9.weapon.074.desc - b012 review: line 1: 252 px > 194 (12 px font) 'Two-Hand Sword of superstrong metal' -- waived (p001): fuller form 'Two-Hand Sword made of extremely strong metal.' fails the checks (line 1: 325 px > 194 (12 px font) 'Two-Hand Sword made of extremely strong metal.'); kept
- [x] a9.weapon.162.desc - b014 review: line 1: 212 px > 194 (12 px font) 'Special steel composite chakram' -- fixed (p002): Composite steel Chakram
- [x] a9.weapon.163.name2 - b014 review: 20 bytes > slot cap 18 -- waived (p002): fuller form 'Master Luna Circle' fails the checks (20 bytes > slot cap 18); kept
- [x] name.m054 - b015 review: 22 bytes > slot cap 12 -- waived (p002): The current transliteration fits both limits.
- [x] rom.11134 - b016 review: line 1: 85 px > 80 (12 px font) 'Resistance B' -- waived (p001): Resistance B exceeds 80 px.
- [x] rom.11154 - b016 review: line 1: 86 px > 80 (12 px font) 'Resistance C' -- waived (p001): Resistance C exceeds 80 px.
- [x] rom.11228 - b016 review: line 1: 87 px > 80 (12 px font) 'Resistance A' -- waived (p001): Resistance A exceeds 80 px.
- [x] rom.137B8 - b017 review: line 1: 89 px > 80 (12 px font) 'Bridge Master' -- waived (p001): Bridge Master exceeds 80 px.
- [x] rom.19F6C - b017 review: line 1: 86 px > 80 (12 px font) 'Weapon Shop' -- waived (p002): The binding “Weapon Shop” is explicitly measured at 86 px, exceeding the 80 px limit.
- [x] rom.1B044 - b017 review: line 1: 95 px > 80 (12 px font) 'Tavern Woman' -- waived (p001): Tavern Woman exceeds 80 px.
- [x] rom.1B8DC - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance J' -- waived (p001): Resistance J exceeds 80 px.
- [x] rom.205D8 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance E' -- waived (p001): Resistance E exceeds 80 px.
- [x] rom.3D69C - b017 review: line 1: 103 px > 80 (12 px font) 'Greatsword Fire' -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6BC - b017 review: line 1: 118 px > 80 (12 px font) 'Greatsword Water' -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6DC - b017 review: line 1: 108 px > 80 (12 px font) 'Greatsword Wind' -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D6FC - b017 review: line 1: 106 px > 80 (12 px font) 'Greatsword Bolt' -- waived (p001): Restoring Generic, greatsword or lightning exceeds 80 px.
- [x] rom.3D71C - b017 review: line 1: 113 px > 80 (12 px font) 'Greatsword Light' -- waived (p001): Generic and the full weapon name cannot fit.
- [x] rom.3D854 - b017 review: line 1: 133 px > 80 (12 px font) 'One-Hand Sword Fire' -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D874 - b017 review: line 1: 148 px > 80 (12 px font) 'One-Hand Sword Water' -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D894 - b017 review: line 1: 138 px > 80 (12 px font) 'One-Hand Sword Wind' -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D8B4 - b017 review: line 1: 136 px > 80 (12 px font) 'One-Hand Sword Bolt' -- waived (p001): Restoring One-Hand Sword or lightning exceeds 80 px.
- [x] rom.3D8D4 - b017 review: line 1: 143 px > 80 (12 px font) 'One-Hand Sword Light' -- waived (p001): One-Hand Sword and the element cannot fit.
- [x] rom.3D9F8 - b017 review: line 1: 129 px > 80 (12 px font) 'Throwing Sword Fire' -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA14 - b017 review: line 1: 144 px > 80 (12 px font) 'Throwing Sword Water' -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA30 - b017 review: line 1: 134 px > 80 (12 px font) 'Throwing Sword Wind' -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3DA4C - b017 review: line 1: 132 px > 80 (12 px font) 'Throwing Sword Bolt' -- waived (p001): Restoring Throwing Sword or lightning exceeds 80 px.
- [x] rom.3DA68 - b017 review: line 1: 139 px > 80 (12 px font) 'Throwing Sword Light' -- waived (p001): Throwing Sword and the element cannot fit.
- [x] rom.3E108 - b017 review: line 1: 84 px > 80 (12 px font) 'Transformed' -- waived (p001): Grineed - Transformed exceeds 80 px.
- [x] rom.470F4 - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance D' -- waived (p001): Resistance D exceeds 80 px.
- [x] rom.47758 - b017 review: line 1: 112 px > 80 (12 px font) 'Mirei Forest Chief' -- waived (p001): Mirei Forest Chief exceeds 80 px.
- [x] rom.499B4 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance F' -- waived (p001): Resistance F exceeds 80 px.
- [x] rom.49A1C - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance G' -- waived (p001): Resistance G exceeds 80 px.
- [x] rom.49AA8 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance H' -- waived (p001): Resistance H exceeds 80 px.
- [x] rom.4A220 - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance K' -- waived (p001): Resistance K exceeds 80 px.
- [x] rom.4A324 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance L' -- waived (p001): Resistance L exceeds 80 px.

## Review minors b018
- [x] quest.009C0 - "渦の杯をみたせ" means fill the Whirlpool Chalice - Drops the objective verb retained in the other chalice titles - Fill the Whirlpool Chalice -- waived (p003): Adding “Fill” would exceed 120 px.
- [x] quest.00C0C - "極の杯をみたせ" means fill the Ultimate Chalice - Drops the objective verb retained in the other chalice titles - Fill the Ultimate Chalice -- waived (p003): Adding “Fill” would exceed 120 px.
- [x] quest.00E44 - "ジーク戦士団登場" announces Zeke's Squad's appearance - "Is In" sounds awkward and leaves its meaning unclear - Enter Zeke's Squad -- waived (p003): fuller form "Enter Zeke's Squad" fails the checks (line 1: 126 px > 120 (12 px font) "Enter Zeke's Squad"); kept
- [x] quest.0059C - review suggestion blocked by width: Lurker in the Underground Lake (120 px title) -- waived (p003): The full location and objective cannot fit.
- [x] quest.00658 - review suggestion blocked by width: The Underground Lake Gate -- waived (p003): The full location and gate cannot fit.
- [x] quest.01108 - review suggestion blocked by width: All Sealing Rings Destroyed -- waived (p003): The fuller destruction wording cannot fit.
- [x] quest.04430 - CUT: 再会、ビィト戦士団 "The Beet Warriors" drops the reunion ("Beet Warriors Again" 126 px > 120 jp-bound title) -- waived (p003): The reunion wording cannot fit with Beet Warriors.

## Flagged cuts (added)
- [x] quest.0059C - CUT (b018): "Underground" omitted from the title to fit. -- waived (p003): The full location and objective cannot fit.
- [x] quest.00658 - CUT (b018): "Underground" omitted from the title to fit. -- waived (p003): The full location and gate cannot fit.
- [x] quest.009C0 - CUT (b018): "Fill" omitted from the title to preserve Whirlpool Chalice. -- waived (p003): Adding “Fill” would exceed 120 px.
- [x] quest.00C0C - CUT (b018): "Fill" omitted from the title to preserve Ultimate Chalice. -- waived (p003): Adding “Fill” would exceed 120 px.
- [x] quest.00D6C - CUT (b018): Former crookedness left implicit in "Reformed" to fit. -- waived (p003): “Reformed” already implies former wrongdoing.
- [x] quest.01E40 - CUT (b018): Gathering action omitted from the title to preserve Medicinal Flowers. -- waived (p003): The gathering verb cannot fit with Medicinal Flower.
- [x] quest.025E4 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.026D4 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.027D0 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.028C0 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.029A4 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.02A94 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.02B78 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.02C68 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.02D58 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.02E48 - CUT (b018): "Monster" omitted from the title to fit. -- waived (p003): Adding “Monster” would exceed the limit.
- [x] quest.04070 - CUT (b019): Omitted explicit "Arrive" from the title. -- waived (p003): The exclamation conveys the entrance; an explicit verb cannot fit.
- [x] quest.04194 - CUT (b019): Omitted explicit "Monsters" from the title. -- waived (p003): “Mountain Monsters” would exceed the limit.
- [x] quest.04254 - CUT (b019): Omitted "Buster" from the title. -- waived (p003): The full Courier Buster title and rescue verb cannot fit.
- [x] quest.04298 - CUT (b019): Omitted "Silver" from the title. -- fixed (p003): Silver Miner Horey
- [x] quest.049E4 - CUT (b019): Shortened "Bridge Master" to "Master" in the title. -- waived (p003): Bridge Master and a protection verb cannot fit.
- [x] quest.04A74 - CUT (b019): Omitted "Learn" from the title. -- waived (p003): “Learn” cannot fit with Secret Technique.
- [x] quest.05578 - CUT (b019): Omitted "village" from the title. -- waived (p003): Adding “village” would exceed the limit.
- [x] quest.055B4 - CUT (b019): Omitted "Statue" from the title. -- waived (p003): Silver Goddess Statue exceeds the limit.
- [x] quest.055D8 - CUT (b019): Omitted "Golden" from the title. -- waived (p003): Golden Castle and a construction verb cannot fit.
- [x] quest.05900 - CUT (b020): Omitted Dark Notes from the lender's title. -- waived (p003): Dark Notes cannot fit alongside Ganeer and his lending role.
- [x] quest.05ABC - CUT (b020): Omitted explicit mention of the mine to fit the title. -- waived (p003): Adding the mine would exceed the limit.
- [x] quest.05C3C - CUT (b020): Omitted Sealing to fit the title. -- waived (p003): Sealing Ring and a destruction verb cannot fit.
- [x] quest.05CA8 - CUT (b020): Omitted Lord of Dreams to fit the title. -- waived (p003): Lord of Dreams and Orozon cannot fit together.
- [x] quest.05ED0 - CUT (b020): Omitted explicit emphasis on total conquest to fit the title. -- waived (p003): “Fall” adequately conveys conquest within the limit.
- [x] quest.05F00 - CUT (b020): Omitted explicit mention of hope to fit the title. -- waived (p003): “Rally” implies renewed hope and a reversal.
- [x] quest.06564 - CUT (b020): Omitted Deadly Blade to fit the title. -- waived (p003): Deadly Blade and Histario cannot fit together.
- [x] quest.06594 - CUT (b020): Omitted Immovable Giant to fit the title. -- waived (p003): Immovable Giant and Garonute cannot fit together.
- [x] quest.06708 - CUT (b020): Omitted Giant Butterfly to fit the title. -- waived (p003): Giant Butterfly and the farther-flight objective cannot fit together.
- [x] quest.06750 - CUT (b020): Omitted Vandel from the epithet to fit the title. -- waived (p003): Vandel Scholar and Noa cannot fit together.
- [x] rom.011F4 - CUT (b021): Compressed to fit: omitted the sudden arrival, explicit castle-base role, and Appraiser's expected role in opposing the invasion. -- waived (p003): The current text already includes all three supposedly omitted details.
- [x] rom.0393C - CUT (b022): Shortened the worldwide origins and combat explanation; omitted the explicit size of Vandel bounties. -- waived (p003): The current text already preserves the origins, combat explanation, and enormous bounties.
- [x] rom.03B54 - CUT (b022): Shortened Kingdom of Gransista to Gransista; omitted the father reference, Association support explanation, nationwide hut network and request-based reward scaling. -- waived (p003): The current text already includes every detail identified as omitted.
- [x] rom.0410C - CUT (b022): Omitted the conversational replies, offer to teach basics and final comprehension question; compressed the branding explanation and gradual improvement. -- waived (p003): The current text already preserves the replies, teaching offer, branding, improvement, and closing question.
- [x] rom.07B00 - CUT (b025): Shortened recognition, pauses, repeated throat-clearing and emphasis on the silver's special nature to fit 255 codes. (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.08944 - CUT (b025): Shortened the uncertain causal explanation, monsters' location in golden areas, island-protection motive, mining and flame-keeping details, and the hero's return as a strong Buster to fit 255 codes. (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.1352C - CUT (b031): Condensed repeated musings and omitted hearsay qualifiers to fit the code cap. -- waived (p003): The current text already retains the musings and hearsay qualifiers.
- [x] rom.1CCC4 - CUT (b035): Shortened titles and repeated names; omitted panting, stammering, hell imagery, repeated urgency and farewell to fit the 255-code cap. (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.27BA0 - CUT (b036): Condensed repeated purchasing instructions and verbal flourishes to fit the code cap. -- waived (p003): The repeated purchasing instructions and characteristic flourishes are already present.
- [x] rom.2B134 - CUT (b037): Abbreviated Association to Assoc. to fit the width limit. -- waived (p003): Buster Association exceeds 120 px.
- [x] rom.41168 - CUT (b042): Compressed the Lounge's value as a social gathering place and the invitation to use the door on future visits. -- waived (p003): The Lounge's social value and invitation to use the door are already explicit.
- [x] rom.41378 - CUT (b042): Omitted the explicit explanation that the Dark Vein is a vein of Dark Power. -- fixed (p003): Speaking of which... {vandel}-sama... // You embarked on this expedition knowing of the "Dark Vein" that lies dormant... // Intricately entwined with the island's gold deposits... A vein of Dark Power, one might call it... // My, my... How utterly splendid!! // Harden-sama seeks the gold released by destroying the "Sealing Rings"... // But you have something else in mind... // You intend to claim the tremendous power of the "Dark Vein"... // And gain strength to rival even a "Seven-Star" Vandel... Is that not so...? // Though you are still "Two-Star," you are pursuing an opportunity no one else has even noticed... // Oh, just thinking about it fills me with excitement...!
- [x] rom.419B0 - CUT (b042): Compressed the Dark Note standard metaphor and repeated emphasis on the tiny interest charge. -- fixed (p005): Now, now... Please, no need to get so heated... // Build Ants are rather expensive, after all... // And that is where my services come in! // A pleasure to meet you... My name is "Ganeer"... // I am known as the "Debt Collector of the Dark Century"... // Dark Notes are everything... They set the standard here... You need them for everything... // Of course, there may be times when your funds are looking rather meager... // That is when I can offer you a loan of Dark Notes... // Naturally, I cannot lend them free of charge... // You simply repay me with a tiny bit of interest... // Just a tiny bit... Kufufu...
- [x] rom.4F2B0 - CUT (b049): Condensed greetings, praise and the reference to the magnificent plan to fit the code cap. -- waived (p003): kept as is after review
- [x] rom.4F468 - CUT (b049): Condensed the introductory explanation, repeated promotion and location references, and closing invitations to fit the code cap. -- waived (p003): The introduction, repeated promotion and location references, and closing invitations are already present.

## Review minors b019
- [x] quest.04030 - "行方不明となったゼナを探しだす" means find Zena, who has gone missing - "The missing Zena" sounds unnatural - Find Zena, who has gone missing. -- fixed (p003): Find Zena, who has gone missing.
- [x] quest.04070 - "ビィト戦士団登場" announces the Beet Warriors' arrival - The title drops the arrival - The Beet Warriors Arrive -- waived (p003): The exclamation conveys the entrance; an explicit verb cannot fit.
- [x] quest.04618 - "アーク戦士団登場" announces Ark's Squad's arrival - "Ark's Squad Here" reads like clipped translationese - Ark's Squad Arrives -- fixed (p003): Enter Ark's Squad
- [x] quest.03FBC - review suggestion blocked by width: line 1: 166 px > 120 (12 px font) 'Infiltrate the Twin Islands' -- waived (p003): The explicit infiltration wording cannot fit with Twin Islands.
- [x] quest.04254 - review suggestion blocked by width: line 1: 156 px > 120 (12 px font) 'Save the Courier Buster' -- waived (p003): The full Courier Buster title and rescue verb cannot fit.
- [x] quest.04298 - review suggestion blocked by width: line 1: 142 px > 120 (12 px font) 'Silver Miner Horey-san' -- fixed (p003): Silver Miner Horey
- [x] quest.04430 - review suggestion blocked by width: line 1: 197 px > 120 (12 px font) 'Reunite with the Beet Warriors' -- waived (p003): The reunion wording cannot fit with Beet Warriors.
- [x] quest.049E4 - review suggestion blocked by width: line 1: 171 px > 120 (12 px font) 'Protect the Bridge Master' -- waived (p003): Bridge Master and a protection verb cannot fit.
- [x] quest.04A74 - review suggestion blocked by width: line 1: 169 px > 120 (12 px font) 'Learn a Secret Technique' -- waived (p003): “Learn” cannot fit with Secret Technique.
- [x] quest.055B4 - review suggestion blocked by width: line 1: 145 px > 120 (12 px font) 'Silver Goddess Statue' -- waived (p003): Silver Goddess Statue exceeds the limit.
- [x] quest.055D8 - review suggestion blocked by width: line 1: 153 px > 120 (12 px font) 'Build the Golden Castle!' -- waived (p003): Golden Castle and a construction verb cannot fit.

## Review minors b020
- [x] quest.057D4 - "山門を破れ" means breach the mountain gate - Drops the gate's identifying qualifier retained in the description - Breach the Mountain Gate -- waived (p003): The mountain qualifier and breach objective cannot fit together.
- [x] quest.05ABC - "坑道　暗闇の先に" means the mine tunnel: beyond the darkness - Drops the location from the title - The Mine: Beyond the Darkness -- waived (p003): Adding the mine would exceed the limit.
- [x] quest.05DE0 - "最後の防御線" means the last line of defense - Last Defense Line is an awkward English formulation - The Last Line of Defense -- fixed (p004): Last Defense
- [x] quest.05900 - review suggestion blocked by width: line 1: 202 px > 120 (12 px font) 'Ganeer, the Dark Notes Lender' -- waived (p003): Dark Notes cannot fit alongside Ganeer and his lending role.
- [x] quest.05BE8 - review suggestion blocked by width: line 1: 163 px > 120 (12 px font) 'Capture the Village Chief' -- waived (p003): Village Chief and a capture verb cannot fit together.
- [x] quest.05C3C - review suggestion blocked by width: line 1: 167 px > 120 (12 px font) 'Destroy the Sealing Rings' -- waived (p003): Sealing Ring and a destruction verb cannot fit.
- [x] quest.05CA8 - review suggestion blocked by width: line 1: 152 px > 120 (12 px font) 'Orozon, Lord of Dreams' -- waived (p003): Lord of Dreams and Orozon cannot fit together.
- [x] quest.05D38 - review suggestion blocked by width: line 1: 191 px > 120 (12 px font) 'The Flame for the Repair Item' -- waived (p003): The full repair-item relationship cannot fit.
- [x] quest.06564 - review suggestion blocked by width: line 1: 135 px > 120 (12 px font) 'Deadly Blade Histario' -- waived (p003): Deadly Blade and Histario cannot fit together.
- [x] quest.06594 - review suggestion blocked by width: line 1: 198 px > 120 (12 px font) 'Garonute, the Immovable Giant' -- waived (p003): Immovable Giant and Garonute cannot fit together.
- [x] quest.06618 - review suggestion blocked by width: line 1: 130 px > 120 (12 px font) 'Monster Lieutenant' -- waived (p003): The full lieutenant wording exceeds the limit.
- [x] quest.06708 - review suggestion blocked by width: line 1: 190 px > 120 (12 px font) 'Giant Butterfly: Even Farther' -- waived (p003): Giant Butterfly and the farther-flight objective cannot fit together.
- [x] quest.06750 - review suggestion blocked by width: line 1: 126 px > 120 (12 px font) 'Vandel Scholar Noa' -- waived (p003): Vandel Scholar and Noa cannot fit together.

## Review minors b023
- [x] rom.04A90 - "何の武器が得意なの？" asks which weapon he is skilled with - "What do you use?" loses the proficiency distinction - {hero}! Off to hunt monsters? Kissu says you're new at this. // To thank you for helping Beet, I'll explain weapons. What weapon are you best with, {hero}? // Swords, spears, guns... There are lots of types. Try the Weapon Shop. // You'll have strengths and weaknesses, {hero}, so some weapons may be off limits. I can't carry axes. Too heavy! Try different ones, okay? -- fixed (p003): {hero}! Off to hunt monsters? Kissu says you're new at this. // To thank you for helping Beet, I'll explain weapons. What weapon are you best with, {hero}? // Swords, spears, guns... There are lots of types. Try the Weapon Shop. // You'll have strengths and weaknesses, {hero}, so some weapons may be off limits. // I can't carry axes. Too heavy! Try different ones, okay?
- [x] rom.05820 - "高価買取キャンペーン中" advertises temporarily generous purchase prices - "buyback sale" sounds like she is selling goods rather than buying them - I'll give ya a good deal, so buy something! I buy stuff, too!! I'm paying top coin right now!! -- fixed (p003): I'll give ya a good deal, so buy something! I buy stuff, too!! I'm paying top coin right now!!

## Review minors b026
- [x] rom.0ADA4 - "いつもの夫婦ゲンカ" teasingly calls their familiar bickering a marital spat - "Another married-couple quarrel" sounds stiff and weakens the joke - (Here we go again! Bickering like an old married couple!) -- fixed (p003): (Here we go again! Bickering like an old married couple!)
- [x] rom.0AF20 - "おまえ 二刀流なのか!?" expresses surprise that the hero fights with two weapons - "You use Dual Wielding" sounds like a menu description - Oh... // Whoa!! {hero}, you know Dual Wielding?! -- fixed (p003): Oh... // Whoa!! {hero}, you know Dual Wielding?!
- [x] rom.09A98 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b021
- [x] rom.011F4 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b022
- [x] rom.03294 - "いつもの夫婦ゲンカ" teasingly calls their habitual bickering a marital quarrel - "Their usual married-couple quarrel" sounds stiff and weakens the joke - suggested EN: (They always bicker like an old married couple...) -- fixed (p003): (They always bicker like an old married couple...)
- [x] rom.0393C - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.03B54 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.0410C - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b024
- [x] rom.06050 - "たすけて あ げ る": flirtatiously drawn-out offer to help - "A helping... little... hand" sounds awkward and misplaces the teasing emphasis - Let this superheroine of justice, BB Milfa, help... you... out! // Let's see... -- fixed (p003): Let this superheroine of justice, BB Milfa, help... you... out! // Let's see...
- [x] rom.066A0 - "おそらく": probably; monsters are suspected of stopping the pigeons - "No doubt" overstates the Chief's certainty - A carrier pigeon recently arrived from Mirei Forest Village... // They report that many monsters have begun appearing in Mirei Forest... // Monsters alone would be troubling enough, but something resembling a Vandel has also been sighted... // East Island, too, may be falling into the Vandels' clutches, starting with Mirei Forest... // I wish I knew what has happened since, but no more pigeons have arrived... // Likely the work of monsters... // I fear for Mirei Forest Village, my boy... -- fixed (p003): A carrier pigeon recently arrived from Mirei Forest Village... // They report that many monsters have begun appearing in Mirei Forest... // Monsters alone would be troubling enough, but something resembling a Vandel has also been sighted... // East Island, too, may be falling into the Vandels' clutches, starting with Mirei Forest... // I wish I knew what has happened since, but no more pigeons have arrived... // Likely the work of monsters... // I fear for Mirei Forest Village, my boy...

## Review minors b025
- [x] rom.07B00 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.08944 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b027
- [x] rom.0CF48 - "モンスターとは桁違いのプレッシャーじゃん" describes the Vandel's overwhelmingly intimidating presence - "The pressure's on a whole other level from a monster" is a stiff calque - Th-this is bad... So this is a Vandel... // Monsters have nothing on this guy... Talk about intimidating... -- fixed (p003): Th-this is bad... So this is a Vandel... // Monsters have nothing on this guy... Talk about intimidating...

## Review minors b028
- [x] rom.0DD68 - "この島の出身とは心強い" expresses encouragement at meeting a local - "Having someone from this island is reassuring" sounds stiff for Rend - Really!? It's good to have someone who knows this island! Right, Ark-san? -- fixed (p003): Really!? It's good to have someone who knows this island! Right, Ark-san?
- [x] rom.0E6CC - "でも・・・それじゃ・・・" means "But... if things stay that way..." - "But... If I..." creates an awkward dangling clause - {hero}... I... // You see... Until now, I've only thought about my own feelings... // But... I can't go on like that, can I...? // Even now... I don't want you to be put in danger... // But... I know... // Nothing will get better if all I do is wait... -- fixed (p004): {hero}... I... // You see... Until now, I've only thought about my own feelings... // But... I can't go on like that, can I...? // Even now... I don't want you to be put in danger... // But... If things stay that way... // Nothing will get better if all I do is wait...

## Review minors b030
- [x] rom.1263C - 「{hero}のお父さんの仇かもしれない」 means he may be the killer of {hero}'s father - "the father of {hero}" is awkwardly impersonal - suggested EN: Beet... The Vandel from the "Golden Castle" might have killed {hero}'s father... -- waived (p004): The suggested possessive suffix is forbidden after {hero}; the current wording preserves the meaning.
- [x] rom.12D2C - 「知的に考えたまえ」 tells them to use their intellect - "Think intellectually" is a stiff calque - suggested EN: Are you the one who awakened me? // Apply your intellect... The fact that I emerged from a stone statue means... -- fixed (p004): Are you the one who awakened me? // Apply your intellect... The fact that I emerged from a stone statue means...

## Review minors b031
- [x] rom.1352C - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b032
- [x] rom.169D8 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.16CA8 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.17450 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b033
- [x] rom.19318 - 「命がいくらあっても足りない」 means even countless lives would not be enough - "No number of lives will save you" is a stiff calque that weakens Slade's dry warning - Wander around carelessly and you'll blunder into traps. You'll run out of lives fast... -- fixed (p004): Wander around carelessly and you'll blunder into traps. You'll run out of lives fast...

## Review minors b034
- [x] rom.1AF34 - "願いが込められた手作りのお守り・・・って" repeats the explanation incredulously: a handmade charm imbued with a wish - "You mean..." awkwardly suggests an unfinished clarification - suggested EN: ... Uh-huh... // A handmade charm with a wish woven into it... You're sayin'... -- fixed (p004): ... Uh-huh... // A handmade charm with a wish woven into it... You say?
- [x] rom.1B5D4 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b035
- [x] rom.1CCC4 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b036
- [x] rom.23FEC - "倒れた木を壊した!" means the fallen tree was destroyed - "Broke the fallen tree" sounds unnatural for clearing an obstacle - You smashed the fallen tree! -- fixed (p004): You smashed the fallen tree!
- [x] rom.27BA0 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b037
- [x] rom.2AD18 - "ウッ・・・ グスッ・・・" conveys choked sobbing - "Ugh" suggests disgust or frustration rather than tears - We're just leaving it all to you, {hero}... // Making you do everything dangerous... // If anything happened to you, {hero}... I... I... // *sob*... *sniff*... -- fixed (p004): We're just leaving it all to you, {hero}... // Making you do everything dangerous, {hero}... // If anything happened to you, {hero}... I... I... // *sob*... *sniff*...
- [x] rom.2B29C - "依頼されていたモンスターを無事に討伐することができた" means successfully defeating the monsters specified in the request - "defeated the monsters for the request" is awkward English - You defeated the monsters specified in the request! Go report to the Appraisal Hut! -- fixed (p004): You defeated the monsters named in the request! Go report to the Appraisal Hut!
- [x] rom.2B134 - review suggestion blocked by width: line 1: 125 px > 120 (12 px font) 'Buster Association' -- waived (p003): Buster Association exceeds 120 px.

## Review minors b038
- [x] rom.32360 - "見苦しい言い訳はしない" means refusing to make disgraceful excuses for losing - "sully a loss" is an unnatural collocation - I won't disgrace myself by making excuses for losing. That's a gambler's etiquette... -- fixed (p004): I won't make excuses for losing. That's a gambler's etiquette...
- [x] rom.325D4 - "この二ッ星の切れ味を味わえ" threatens the opponent with this Two-Star assassin's sharpness - "the cutting edge of this Two-Star" reads as a stiff calque - Gehihyaha! I'm Shaderiko, the "Dark Claw"! // Taste my blades! I'm a Two-Star feared as an assassin!! -- fixed (p004): Gehihyaha! I'm Shaderiko, the "Dark Claw"! // Taste my blades! I'm a Two-Star feared as an assassin!!

## Review minors b041
- [x] rom.3E4B4 - 「薬草を手に入れた」 means "obtained a medicinal herb" - Missing article makes the notification awkward - Obtained a Medicinal Herb. -- fixed (p004): Obtained a Medicinal Herb.
- [x] rom.3E568 - 「アイテムゲット」 labels item acquisition - "Item Get" is unnatural English, even as a debug sound label - Item Obtained -- fixed (p004): Item Obtained

## Review minors b042
- [x] rom.409E0 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.41168 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.41378 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.419B0 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b043
- [x] rom.42518 - 島中を黄金に染める: turn the whole island to gold - "These whole islands" is unnatural English - A Vandel's power can destroy a mere "Sealing Ring" in one blow... // You might not even need to strike it... // When you find a "Sealing Ring," just try touching it... // That's all it takes to destroy a "Sealing Ring"!! // Heh heh heh... // I can hardly stand it... // Oh, don't worry... // Even a greenhorn like you can't possibly mess this up... // Go...! Turn every inch of the island to gold, just as I desire!! -- fixed (p004): A Vandel's power can destroy a mere "Sealing Ring" in one blow... // You might not even need to strike it... // When you find a "Sealing Ring," just try touching it... // That's all it takes to destroy a "Sealing Ring"!! // Heh heh heh... // I can hardly stand it... // Oh, don't worry... // Even a greenhorn like you can't possibly mess this up... // Go...! Turn the whole island to gold, just as I desire!!
- [x] rom.4330C - 目指す「七ッ星」まではまだまだ遠い道のり: a long road remains to the Seven-Star rank - "Before your goal of Seven-Star" reads awkwardly - Congratulations!! // Though you still have quite a way to go before you reach the rank of "Seven-Star"...!! // Keep up the fine work...! Now, farewell...!! // Oh, yes... These are the Build Ants entrusted to me by Harden-sama. // He ordered them to build a gold mine. -- fixed (p004): Congratulations!! // Though you still have a long way to go to reach the rank of "Seven-Star"...!! // Keep up the fine work...! Now, farewell...!! // Oh, yes... These are the Build Ants entrusted to me by Harden-sama. // He ordered them to build a gold mine.

## Review minors b044
- [x] rom.45344 - Diam boasts that the island's rumors have reached even him, then realizes who he is addressing - "Even I... heard!" is awkwardly incomplete, and the compressed opening loses his suspicious question - Hey! Don't tell me you've come to uncover this island's secret too... // This island's been quite the topic of conversation around the Bekatorte Seas lately... // Naturally, those rumors reached even me, "Steel Claw" Diam-sama, the strongest in the Bekatorte Seas... // If the "Greedy Overlord" himself has come here, there must be something to it... // They say he's brought an underling with conspicuously long horns... // ...!! // Oh, no! Those horns! Don't tell me...! I let that slip! // No matter... I'll just have to silence you! // SEYAAAAAA!! -- fixed (p004): Hey! Don't tell me you've come to uncover this island's secret too... // This island's been the talk of the Bekatorte Seas lately... // Even I, "Steel Claw" Diam-sama, the strongest in the Bekatorte Seas, have heard the rumors... // If the "Greedy Overlord" himself came here, there must be something to it... // They say he's brought an underling with strikingly long horns... // ...!! // Blast! Those horns! Don't tell me...! I let that slip! // No matter... I'll just have to silence you! // SEYAAAAAA!!
- [x] rom.44EEC - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b045
- [x] rom.46E34 - "このあたいが キャーだって" expresses disbelief that she herself screamed - "Like a little girl" adds a disparaging comparison absent from the Japanese - Haha... Seriously? Me, screaming like that...? This is really bad... // {hero}... I don't think I'm gonna make it... -- fixed (p004): Haha... Seriously? Me, screaming like that...? This is really bad... // {hero}... I don't think I'm gonna make it...

## Review minors b046
- [x] rom.49564 - "ふざけるな" means "Don't give me that!" - "Don't you dare" suggests a warning rather than defiant rejection of the question - D-don't give me that...! -- fixed (p004): D-don't give me that...!

## Review minors b047
- [x] rom.49E64 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b048
- [x] rom.4C7E4 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b049
- [x] rom.4F2B0 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] rom.4F468 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)

## Review minors b050
- [x] rom.4FD60 - "長らく販売を中止しており ご迷惑をおかけしていた" apologizes for the prolonged suspension of sales - "Sorry for the long wait!" and the subsequent fragments make Shagie's sales pitch noticeably brusquer than neighboring dialogue - suggested EN: We apologize for the prolonged inconvenience, but "Hoverfish" are now back on sale at the Vandel House! // Although their stops are limited, they allow you to travel long distances far faster than on foot...! // Here on the Twin Islands, for instance... Yes, you can travel from the Golden Castle to Rinnam Glacier...! // They are a little costly, but do consider purchasing one...! // Tarotos awaits you at the Vandel House with lively "Hoverfish" ready for sale...! // Please do make use of our services...! // Was that explanation clear? -- fixed (p004): Our apologies for the long wait! "Hoverfish" are back on sale at the Vandel House! // Although their stops are limited... // They let you travel long distances far faster than on foot...! // Here on the Twin Islands, you can travel from the Golden Castle to Rinnam Glacier...! // They are a little costly, but do consider buying one...! // Tarotos awaits you at the Vandel House with lively "Hoverfish" ready for sale...! // Please do make use of our services...! // Was that explanation clear?
- [x] rom.503EC - "ぜひお買い求めくださいませ" courteously urges a purchase - "A little pricier ... but do buy one!" sounds blunt; restoring the courteous sales language would better match Shagie's other announcements - suggested EN: We apologize for the prolonged inconvenience, but the "Giant Butterfly" is now back on sale at the Vandel House! // Although its stops are limited, it allows you to travel long distances far faster even than a "Hoverfish"...! // Here on the Twin Islands, for instance... Yes, you can travel from the Golden Castle to Zeros Snowfield...! // It is a little more costly than a "Hoverfish," but do consider purchasing one...! // Tarotos awaits you at the Vandel House with a lively "Giant Butterfly" ready for sale...! // Please do make use of our services...! // Was that explanation clear? -- fixed (p004): Our apologies for the long wait! The "Giant Butterfly" is back on sale at the Vandel House! // Its stops are limited, but it covers long distances far faster even than a "Hoverfish"...! // Here on the Twin Islands, you can travel from the Golden Castle to Zeros Snowfield...! // It costs a little more than a "Hoverfish," but do consider buying one...! // Tarotos awaits you at the Vandel House with a lively "Giant Butterfly" ready for sale...! // Please do make use of our services...! // Was that explanation clear?
- [x] rom.4F8C8 - review suggestion blocked by width: message over 255 codes (done: limit raised to 511 codes, review suggestion applied)
- [x] engine - numbers expanded into dialogue ({count}/[FF01], e.g. a9.021AAEF4 "Your reward this time is 1 0 0 Maggy.", work/qa/cover/appraisal_reward) are full-width digit codes drawn at 12 px pitch; map full-width digits to proportional digits in the dialogue expansion only (status columns right-align full-width digits and must keep them) -- fixed (session 26): engine hook num_pc at the two int-to-digits calls in message
  expansion (0x0201F6E8 [FF01], 0x02024E98 quest {count}) maps them to proportional digit codes; seen in game
  (work/qa/p26_reward: "Your reward this time is 100 Maggy."); status columns still full-width (work/qa/p26_menu_status).

## Story pass minors quest_00
- [x] quest.00E44 - Zeke's Squad makes its entrance - "Zeke's Squad Is In" sounds awkward and departs from the recurring "Enter..." introduction phrasing, including this event's other two entries - Suggested EN: "Enter Zeke's Squad". -- waived (p003): fuller form "Enter Zeke's Squad" fails the checks (line 1: 126 px > 120 (12 px font) "Enter Zeke's Squad"); kept

## Story pass minors quest_01
- [x] quest.02E64, quest.02EB4, quest.02F04; recurring hunt descriptions through quest.035C0 - Defeat {count} of {monster} found in the named region and elsewhere - "The monsters called {monster}" is cumbersome stock phrasing and unnecessarily departs from the earlier hunt template. Standardize these descriptions while preserving each location. Suggested EN for quest.02E64: "Hunt {monster} in Pasero Marsh and elsewhere. Please defeat {count} in all." Apply the same pattern to the subsequent regions, using "at" for Byonrin Volcano. -- fixed (p004): Hunt {monster} in Pasero Marsh and elsewhere. Please defeat {count} in all.; Hunt {monster} in Pasero Marsh and elsewhere. Please defeat {count} in all.; Hunt {monster} in Pasero Marsh and elsewhere. Please defeat {count} in all.; Hunt {monster} in the Muterin Mountains and elsewhere. Please defeat {count} in all.; Hunt {monster} in Pasero Marsh and elsewhere. Please defeat {count} in all.

## Story pass minors quest_02
- [x] quest.04430 - Reunion with the Beet Warriors - "The Beet Warriors" drops the reunion cue distinguishing this event from their introduction. - Suggested EN: "Beet Warriors Return" -- waived (p003): The reunion wording cannot fit with Beet Warriors.
- [x] quest.04618, quest.05E34 - Ark's Squad appears - "Ark's Squad Here" is awkward stock phrasing in both routes. - Suggested EN: "Enter Ark's Squad" -- waived (p004): kept as is after review; kept as is after review
- [x] quest.05B7C - Sealing Ring restoration - The imperative "Repair Sealing Ring" sounds like a Vandel objective, whereas the accompanying descriptions correctly describe restoration as an event. - Suggested EN: "Ring Restoration" -- waived (p004): "Ring Restoration" drops the binding Sealing Ring term; its full form cannot fit.
- [x] quest.05DE0 - Last line of defense - "Last Defense Line" is unnatural compared with the accompanying descriptions. - Suggested EN: "Last Defense" -- fixed (p004): Last Defense

## Story pass minors quest_03
- [x] quest.06564 - Deadly Blade Histario - Omits the epithet retained in both corresponding descriptions, weakening consistency with the other named encounters. Suggested EN: "Deadly Blade Histario". -- waived (p003): Deadly Blade and Histario cannot fit together.
- [x] quest.06594 - Immovable Giant Garonute - Drops the identifying epithet retained in the descriptions. Suggested EN: "Immovable Giant Garonute". -- waived (p003): Immovable Giant and Garonute cannot fit together.
- [x] quest.06618, quest.06628, quest.06638 - Lieutenant monster - "Monster Aide" and "Monster Lieutenant" give the same mechanic different names within one entry. Suggested EN: "Lieutenant Monster" throughout. -- waived (p004): "Lieutenant Monster" has the same width as "Monster Lieutenant": 130 px, exceeding the title limit.; "Monster Lieutenant" is natural English; the title requires a shorter label.; "Monster Lieutenant" is natural English and matches the brief.
- [x] quest.066A8 - Hoverfish extension - "Extend Hoverfish" sounds like physically lengthening the creature; the descriptions already offer clearer stock phrasing. Suggested EN: "Hoverfish Extension". -- waived (p004): "Hoverfish Extension" would exceed 120 px; the current wording conveys the extension within the limit.
- [x] quest.06750 - Vandel Scholar Noa - Shortens the binding epithet to "Scholar," unlike the corresponding descriptions. Suggested EN: "Vandel Scholar Noa". -- waived (p003): Vandel Scholar and Noa cannot fit together.

## Story pass minors rom_00
- [x] rom.03E34 - They must quickly find the Vandel responsible - “The Vandel you seek revenge on soon” is awkward and makes “soon” attach ambiguously. Suggested EN: “We must soon find the Vandel who killed your father...” Keep the remaining pages unchanged. -- fixed (p004): We must soon find the Vandel who killed your father... // I intend to gather information here as well... // You shall continue to have my full support. Let us both do our best... // Gather whatever information you can too, {hero}... I'm counting on you...

## Story pass minors rom_01
- [x] rom.04C74 - Poala associates Busters with Saiga - "Busters mean Saiga, right?" sounds like a terminology definition rather than her enthusiastic recommendation - Suggested EN: "And what's a Buster without a Saiga? Master your best weapon, and I think you'll learn to form one." -- fixed (p004): And what's a Buster without a Saiga? // Master your best weapon, and I think you'll learn to form one. // A Saiga requires you to raise your Divine Power to its limit. // So your strongest Divine Attack element might affect the Saiga you form... // I can't form a Saiga myself, so who am I to act like an expert...! // Well? Make sense? Basically, you've got to keep training...!! // Give it your best!!
- [x] rom.066A0 - Someone apparently resembling a Vandel has been spotted - "A possible Vandel" sounds clinical in the Chief's worried account - Suggested EN: "Worse, something that looked like a Vandel was sighted..." -- fixed (p003): A carrier pigeon recently arrived from Mirei Forest Village... // They report that many monsters have begun appearing in Mirei Forest... // Monsters alone would be troubling enough, but something resembling a Vandel has also been sighted... // East Island, too, may be falling into the Vandels' clutches, starting with Mirei Forest... // I wish I knew what has happened since, but no more pigeons have arrived... // Likely the work of monsters... // I fear for Mirei Forest Village, my boy...
- [x] rom.05820 - Zena advertises generous purchase prices - "Buyback sale" muddles her offer to buy the player's goods with selling discounted stock - Suggested EN: "I'll give ya a good deal, so buy something! I buy stuff, too!! Paying top coin for your goods right now!!" -- fixed (p003): I'll give ya a good deal, so buy something! I buy stuff, too!! I'm paying top coin right now!!

## Story pass minors rom_02
- [x] rom.096F4 - The murdered Mirei Forest Chief was the Village Chief's younger brother - "Younger brother-san" sounds unintentionally comic during a bereavement revelation; attach the retained honorific to his title - Suggested EN: "{hero}... The murdered Mirei Forest Chief-san was the Village Chief's younger brother." -- fixed (p004): {hero}... The murdered Mirei Forest Chief was the Village Chief's younger brother.
- [x] rom.0AF20 - Beet excitedly notices the hero fighting with two weapons - "You use Dual Wielding?!" sounds like interface terminology spoken aloud - Suggested EN: "Oh... // Whoa!! {hero}, you fight with two weapons?!" -- fixed (p003): Oh... // Whoa!! {hero}, you know Dual Wielding?!
- [x] rom.0AF60 - Beet eagerly asks to learn the technique - "Teach me Dual Wielding" repeats the stiff phrasing and blunts his enthusiasm - Suggested EN: "A-awesome! That's so cool!! // Hey, hey! Teach me to fight like that!!" -- fixed (p004): A-awesome! That's so cool!! // Hey, hey! Show me how Dual Wielding works!!

## Story pass minors rom_03
- [x] rom.0CF48 - Zena feels a Vandel's overwhelming menace - "The pressure's on a whole other level" sounds analytical during her frightened breakdown. - Suggested EN: "Th-this is bad... So this is a Vandel... // Monsters don't come close to being this scary..." -- fixed (p003): Th-this is bad... So this is a Vandel... // Monsters have nothing on this guy... Talk about intimidating...
- [x] rom.0F5D4 - Zena masks a sincere request for company with her recurring joke - "I'd be happy if you came along" briefly loses her casual voice. Preserve "Just kidding..." as the callback. - Suggested EN: "It'd be great if you came along too!! Just kidding..." -- fixed (p004): It'd be great if you came along too!! Just kidding...

## Story pass minors rom_04
- [x] rom.11438 - Friendly acknowledgment after welcoming the hero - "Glad to join you!" suggests recruitment rather than the hideout's promised support - Suggested EN: "Glad to help!" -- fixed (p004): Glad to help!
- [x] rom.1263C - The castle's Vandel may have killed the hero's father - "the father of {hero}" sounds stiff during a sensitive exchange - Suggested EN: "Beet... That Vandel might have killed his father... That's who {hero} is looking for..." -- waived (p004): The suggested possessive suffix is forbidden after {hero}; the current wording preserves the meaning.
- [x] rom.1342C - Shagie laughs at the stranded Busters - "Oho... Ohohohoho" changes his recurring laugh and conflicts with the binding ウフフ rendering - Suggested EN: "Ufu... Ufufufufu...! I can hardly wait to see how they respond!!" -- waived (p004): Oho kept (natural English laugh)

## Story pass minors rom_05
- [x] rom.17FD0 - Grest repeats Badu's automatic "Yes..." before protesting - "Right..." obscures the verbal echo that sets up the joke after Badu's two identical replies. Suggested EN: "Yes... Hey, you...!" -- fixed (p004): Yes... Hey, you...!

## Story pass minors rom_06
- [x] rom.19318 - Careless wandering into traps will cost you your life, however many lives you have - "No number of lives will save you" sounds unnatural and weakens Slade's dry warning - Suggested EN: "Wander around carelessly and you'll stumble into traps. You'd need nine lives..." -- fixed (p004): Wander around carelessly and you'll blunder into traps. You'll run out of lives fast...

## Story pass minors rom_09
- [x] rom.25DC0, rom.25DEC, rom.25E04 - Break the obstructing ice / cancel breaking it - Singular "it" conflicts with "ice pillars" and "them" in the surrounding prompts. - Suggested EN: "Break them with a Saiga?" / "You decided not to break them." -- fixed (p005): Break them with a Saiga?; You decided not to break them.; You decided not to break them.

## Story pass minors rom_0A
- [x] rom.2AD18 - Lena breaks down crying over the danger imposed on the hero - "Ugh" suggests disgust or discomfort rather than a choked sob, weakening the end of her emotional speech - Suggested EN ending: "*sob*... *sniff*..." -- fixed (p004): We're just leaving it all to you, {hero}... // Making you do everything dangerous, {hero}... // If anything happened to you, {hero}... I... I... // *sob*... *sniff*...
- [x] rom.2B134, rom.2B150 - Buster Association label - "Buster Assoc." breaks the binding spelling and no-abbreviations ruling - Suggested EN: "Buster Association". -- waived (p005): The full "Buster Association" would exceed 120 px.; The full "Buster Association" would exceed 120 px.
- [x] rom.2BE94 - The Chief remembers a bridge-building expert visiting the village - "a Master bridge builder" awkwardly mixes a capitalized title with a generic description and obscures the established role name - Suggested EN: "Come to think of it, the Bridge Master should be here in the village... Would you speak with him?" -- fixed (p005): To think they'd destroy the bridge to the Golden Castle... What are we to do...? // Come to think of it, the Bridge Master should be here in the village... Would you speak with him?

## Story pass minors rom_0B
- [x] rom.2FA98 - A flirtatious greeting ends with a coy laugh - "Hmhm" obscures the laugh and departs from the glossary's ウフフ → "Ufufu" convention - Suggested EN: "Oh, you look as cute as ever today, dear... // Ufu." -- waived (p005): Hmhm kept (natural English laugh)

## Story pass minors rom_0C
- [x] rom.30CF8 - Tarotos respectfully welcomes the player - "{vandel}-sama" attaches a suffix to a player-name variable, contrary to the glossary ruling - Suggested EN: "Welcome, {vandel}. How may we serve you today?" -- fixed (p005): Welcome, {vandel}-sama. How may we serve you today?
- [x] rom.32360 - Canbal accepts defeat without undignified excuses - "Sully a loss" sounds unnatural and muddies his otherwise suave acceptance of the wager's outcome - Suggested EN: "I won't make excuses for losing. That's a gambler's etiquette..." -- fixed (p004): I won't make excuses for losing. That's a gambler's etiquette...
- [x] rom.326C0 - Shaderiko's characteristic snicker - "Gehihi" deviates from the binding ゲヒヒ → "Gehehe" rendering - Suggested EN: "Gehehe!!" -- fixed (p005): Gehehe!!

## Story pass minors rom_0E
- [x] rom.395E8 - A healing fountain restores health and Divine Power - "It's a fountain of medicinal water" sounds clinical and cumbersome for a recurring recovery message - Suggested EN: "It's a healing fountain. / Health and Divine Power restored!" -- fixed (p005): It's a healing fountain. Health and Divine Power restored!

## Story pass minors rom_0F
- [x] rom.3EF50, rom.3F514, rom.3FC88 - Harden's booming laugh - "Gwahaha" shortens the glossary's prescribed laugh shape. Suggested EN: "Gwahahaha!!" (rom.3FC88: "Gwahahaha!! Look at that trash..."). -- fixed (p005): Gwahahaha!!; Gwahahaha!!; Gwahahaha!! Look at that trash...; Gwahahaha!! Look at that trash...
- [x] rom.3E568 - Item acquisition sound-test label - "Item Get" is awkward English stock phrasing. Suggested EN: "Item Acquired". -- fixed (p004): Item Obtained
- [x] rom.3E588 - Quest completion sound-test label - "Quest Clear" is less natural than the established stock phrasing. Suggested EN: "Quest Complete". -- fixed (p005): Quest Complete

## Story pass minors rom_10
- [x] rom.401A0, rom.40510, rom.40F2C, rom.4102C, rom.41378, rom.415B0, rom.43214 - Shagie respectfully addresses the player Vandel - `{vandel}-sama` glues a suffix onto a player-name variable, contrary to the binding rule. Preserve his deference through wording instead - Suggested EN: use `{vandel}` without the suffix; retain the surrounding courteous phrasing. -- fixed (p005): Ah, "Greedy Overlord" Harden-sama...! // As stern as ever...!! // My... How splendid...!! // Just as a Vandel should be...! // And this dazzling golden glow! // Truly superb...!! // Silver is the Twin Islands' main Ore, yet their gold veins hold almost as much... // The ancient islanders knew of this gold. They sealed it with two giant goddess statues and // eighteen "Sealing Rings" enshrined on silver pedestals across the islands... // And you saw the opportunity, {vandel}-sama...!; Oh dear... Dear me... How very careless of me! My sincerest apologies...!! // Harden-sama... {vandel}-sama... Splendid work. // Now, {vandel}-sama, for destroying the "Silver Goddess Statue" and wiping out the village... // I hereby award you one "Star"!! // Please, accept your reward...!; Speaking of which... {vandel}-sama... // You set out knowing what lies entwined with the island's gold deposits... // The "Dark Vein"... A vein of dormant Dark Power... // My, my... How utterly splendid!! // Harden-sama seeks the gold released by destroying the "Sealing Rings"... // But you have something else in mind... // You intend to claim the tremendous power of the "Dark Vein"... // And gain strength to rival even a "Seven-Star" Vandel... Is that not so...? // Though you are still "Two-Star," you are pursuing an opportunity no one else has even noticed... // Oh, just thinking about it fills me with excitement...!
- [x] rom.419B0, rom.41CD8 - Ganeer's sinister クフフ laugh - “Kuhuhu” conflicts with both the prescribed “Kufufu” and his later laugh at rom.41EE0 - Suggested EN: “Just a tiny bit... Kufufu...” / “Th-thank you very much... Then, here you are... Kufufu...” -- waived (p005): kept as is after review; kept as is after review; Already uses the prescribed "Kufufu" consistently.
- [x] rom.40618 - Congratulations on attaining two stars - “Congratulations on becoming ‘Two-Star’” is awkward stock phrasing - Suggested EN: “Congratulations on your promotion to ‘Two-Star’!!” -- fixed (p005): Congratulations on your promotion to "Two-Star"!! // Though you still have quite a way to go before reaching your goal of "Seven-Star"...!! // Oh, that fountain in front of the gate appears to be gushing Dark Power. // I suspect it could restore your health and Dark Power. Why not put it to use? // Do keep up the good work...! // Now, if you'll excuse me...!!
- [x] rom.42518 - Harden commands that the islands be turned gold - “These whole islands” is unnatural and weakens the closing command - Suggested EN: “Go...! Turn these entire islands to gold, just as I desire!!” -- fixed (p004): A Vandel's power can destroy a mere "Sealing Ring" in one blow... // You might not even need to strike it... // When you find a "Sealing Ring," just try touching it... // That's all it takes to destroy a "Sealing Ring"!! // Heh heh heh... // I can hardly stand it... // Oh, don't worry... // Even a greenhorn like you can't possibly mess this up... // Go...! Turn the whole island to gold, just as I desire!!

## Story pass minors rom_11
- [x] rom.45344 - Diam boasts about hearing the island rumors, then recognizes the subordinate's horns - Compressed phrases such as “strongest in these seas, heard!” make his theatrical boasting sound like notes rather than dialogue - Suggested EN: `Hey! You're not after this island's secret too, are you? // It's the talk of the Bekatorte Seas! Even I, "Steel Claw" Diam-sama, the strongest here, heard the rumors! // If the "Greedy Overlord" came, something must be here! His underling has long horns, they say... // ...!! Those horns!? Blast! I said too much! // No matter... I'll silence you! SEYAAAAAA!!` -- fixed (p004): Hey! Don't tell me you've come to uncover this island's secret too... // This island's been the talk of the Bekatorte Seas lately... // Even I, "Steel Claw" Diam-sama, the strongest in the Bekatorte Seas, have heard the rumors... // If the "Greedy Overlord" himself came here, there must be something to it... // They say he's brought an underling with strikingly long horns... // ...!! // Blast! Those horns! Don't tell me...! I let that slip! // No matter... I'll just have to silence you! // SEYAAAAAA!!
- [x] rom.45BD0; rom.465BC; rom.46698; rom.46D94 - Desperate or angry curses - “Daaarn it” and “Darn it” soften the Resistance's desperation and Baleas's rough voice, particularly beside Diam's “D-damn you” - Suggested EN: `Damn it!!` / `Damn it!` / `Damn it!` / `Damn it! Zena, get out of here!!` -- waived (p005): Darn kept (all-ages tone); Darn kept (all-ages tone); Darn kept (all-ages tone); Darn kept (all-ages tone)
- [x] rom.47C88 - Shagie gleefully watches the consequences of the chief's deception - “Hmhm... Hmhmhmhm” loses his binding, recognizable laugh - Suggested EN for the closing laugh: `Ufu... Ufufufufu...!!` -- fixed (p005): That Village Chief was lying... // We really should have kept him alive... // Now, what will you do, {vandel}...? Allow me to observe... // Ufu... Ufufufufu...!!
- [x] rom.47C88; rom.47DDC; rom.47F40 - Shagie's deferential address to the player - The detached `-sama` introduces inconsistent spacing and, at rom.47C88, an awkward line break - Suggested EN fragments: `Now, what will you do, {vandel}-sama...? Allow me to observe...` / `My, my... {vandel}-sama, splendid work as always!!` / `{vandel}-sama, you are as magnificent as ever...!!` -- fixed (p005): That Village Chief was lying... // We really should have kept him alive... // Now, what will you do, {vandel}...? Allow me to observe... // Ufu... Ufufufufu...!!; My, my... {vandel}-sama, splendid work as always!! // This golden radiance, brimming with wicked Dark Power!! // As magnificent as ever...!! // Now, for conquering another village, I present you with another "Star"!! // Please, accept it...!; My, my... Splendid work!! // {vandel}-sama, you are as magnificent as ever...!! // Thank you for finding and destroying West Island's "Sealing Rings," and reporting back. // Now, I present you with another "Star"!! // Please, accept it...!; That Village Chief was lying... // We really should have kept him alive... // Now, what will you do, {vandel}...? Allow me to observe... // Ufu... Ufufufufu...!!

## Story pass minors rom_12
- [x] rom.49D64, rom.4AEB8, rom.4B650, rom.4B7F8 - Shagie addresses the player respectfully - `{vandel}-sama` glues a suffix onto a player variable, contrary to the glossary and earlier chapter usage - Suggested EN: use `{vandel} -sama` throughout. -- fixed (p005): Congratulations!! // At last, you are a "Seven-Star" Vandel, the highest rank in the world...!! // {vandel}-sama, as you absorb this immense Dark Power, your strength should grow without limit... // I expect great things from you...! // Now, your first task as a "Seven-Star" Vandel of the world's highest rank...! // Defeat the "Beet Warriors"...!! // Keep up the good work, and aim to join the "Eight Shining Stars"!! // And with that, I shall take my leave...!!
- [x] rom.4A9BC - A fallen militiaman begs the hero for help - `{hero}-san` likewise glues an honorific onto the variable - Suggested EN: `{hero} -san... // H-help... Please...` -- waived (p005): kept as is after review
- [x] rom.49E64 - Shagie chuckles with excitement at the final seal's impending destruction - “Hmhm... Hmhmhm...” departs from his binding ウフフ laugh and weakens his recognizable mannerism - Suggested EN: “Ufu... Ufufu... How very exciting...!! Do give it your all...!!” -- fixed (p005): There was still one more target left to destroy... // One goddess statue at the Golden Castle... // Nine "Sealing Rings" on West Island... And nine on East Island... // And finally, the goddess statue in East Village... // With all the other "Sealing Rings" destroyed and the Dark Power awakened, now is your chance...! // You should have no trouble passing the door that barred your way to the goddess statue...! // Now is your chance to destroy that statue... The very last seal...! // In other words...!! // The world's highest rank, "Seven-Star" Vandel, is almost within your grasp...!! // Ufu... Ufufu... How very exciting...!! Do give it your all...!!
- [x] rom.4BFAC - Gantry admits he loses track of time admiring the castle - The final “eh...” makes his absorbed observation sound like a request for agreement - Suggested EN: “And yet... I lose track of time just gazing at it...” -- fixed (p005): Hmm... No matter how often I see it, that castle is astounding... All made of gold... // What fearsome creatures these Vandels are... // And yet... I lose track of time just gazing at it...

## Story pass minors rom_13
- [x] rom.4C228 - Monsters help torment humans efficiently and powerfully - "With ease and force" is awkward stock phrasing that weakens Harden's sneering delivery - Suggested EN: "Oh... A monster servant...? Handy for tormenting humans efficiently and brutally..." -- waived (p005): adds a stray {close} mid-sentence
- [x] rom.4F798, rom.4F8C8 - Promotion grants monsters lieutenant status and command privileges - Switching from "Lieutenant Monster" to "monster lieutenant" immediately after the introductory explanation makes the recurring service terminology inconsistent - Suggested EN: Use "Lieutenant Monster" throughout; "I see you've used our Lieutenant Monster promotion service." -- fixed (p005): Well, well, {vandel}-sama! Welcome to the Vandel House! // I see you've used our Lieutenant Monster promotion service. // Thank you very much! // Your Lieutenant Monster will help you, {vandel}-sama, // become a "Seven-Star" with its powerful support. // Oh, I can hardly wait...! // Now, as for how best to employ your Lieutenant Monster...; One way to destroy "Sealing Rings" efficiently is to "Dispatch an Army"! // With another army destroying rings alongside you, {vandel}-sama... // You can conquer the island on several fronts...! // Each army may contain up to five members. // You will need to register one of them as its leader. // Any Vandel may serve as a leader. // Monsters can also lead if promoted to Lieutenant Monster at the Vandel House! // Regrettably, Vandels cannot be assigned to serve under a Lieutenant Monster... // We kindly ask for your understanding... // Was that explanation clear?
- [x] rom.4FD60 - Shagie courteously announces resumed Hoverfish sales - The compressed "Sorry for the long wait!" and "A little pricey, but do buy one!" lose some of his established lavish salesmanship - Suggested EN: "We apologize for the long wait! \"Hoverfish\" are back on sale at the Vandel House!" / "A little costly, but we do hope you will purchase one!" -- fixed (p004): Our apologies for the long wait! "Hoverfish" are back on sale at the Vandel House! // Although their stops are limited... // They let you travel long distances far faster than on foot...! // Here on the Twin Islands, you can travel from the Golden Castle to Rinnam Glacier...! // They are a little costly, but do consider buying one...! // Tarotos awaits you at the Vandel House with lively "Hoverfish" ready for sale...! // Please do make use of our services...! // Was that explanation clear?
- [x] rom.4E1F4, rom.4ECD4 - Harden's booming signature laugh - "Gwahaha" shortens the glossary's binding laugh shape - Suggested EN: "Gwahahaha!!" / "Gwahahaha!!!" -- fixed (p005): Gwahahaha!!; Gwahahaha!!!
- [x] rom.4E518 - Histario's instrument sounds - Sound effects lack the glossary's required asterisks - Suggested EN: "*strum*... *strummm*... *strum*..." -- fixed (p005): *strum*... *strummm*... *strum*...

## Story pass minors rom_14
- [x] rom.50DF0 - Rodina coyly asks whether she looks like a "Little Devil," then laughs ウフフ - "Hmhmhm..." misses the binding laugh rendering - Suggested EN: `Do I look like a "Little Devil" to you...? / Ufufu...` -- fixed (p005): Oh, you are... Let me see... // Ah, yes... {vandel}, was it? // I have heard tales of your exploits on the Twin Islands... // How do you do? I am Rodina... // Everyone calls me the "Little Devil," but... // I wonder... // Do I look like a "Little Devil" to you...? Ufufu... // How wonderful, being able to serve under Harden-sama... // It has been so long. I would love to see him again...
- [x] rom.51398, rom.5143C, rom.515AC, rom.51660, rom.51728 - Harden's booming ガーッハッハッ punctuates his recurring "Instinct!!" boast - Consistent within this chapter, but shortened from the glossary's prescribed laugh - Suggested EN: `Gwahahaha!!` -- fixed (p005): Gwahahaha!!; Gwahahaha!!; Gwahahaha!!; Gwahahaha!!; Gwahahaha!!
