# Polish

Minor findings and flagged cuts, fixed in one pass before release (`references/translation.md` §Review). Tick each
line `[x]` with `fixed` or `waived: reason`; the release script refuses to run while a line is unticked.

## General
- [ ] speaker tag: Resistance A-L show as "Resist. A" and 橋かけ名人 as "Master" (87/89 px > 80 px measured tag);
  widen the tag (90 px was not drawn: find the canvas width in the draw code) or keep, then waive.
- [ ] jp-bound budgets (area/area2 names, key items, tengeki/meigeki, skills, titles): measure each box in phase 8 and
  undo the cuts below that the real box allows (full area names: Mountains, Volcano, Snowfield ...).
- [ ] weapon descriptions "1H"/"2H": rephrase to full words within 194 px.

## Flagged cuts from translation batches
- [ ] a9.area.001.name - CUT (b001): Mountains rendered as Range for width.
- [ ] a9.area.007.name - CUT (b001): Forest omitted for width.
- [ ] a9.area.017.name - CUT (b001): Wastes rendered as Waste for width.
- [ ] a9.area.021.name - CUT (b001): Mountain omitted for width.
- [ ] a9.area.022.name - CUT (b001): Forest rendered as Wood for width.
- [ ] a9.area.029.name - CUT (b001): Desert omitted for width.
- [ ] a9.area.036.name - CUT (b001): Mountains shortened to Mts. for width.
- [ ] a9.area.040.name - CUT (b001): Lake omitted for width.
- [ ] a9.area.046.name - CUT (b001): Valley omitted for width.
- [ ] a9.area.050.name - CUT (b001): Volcano shortened to Mt. for width.
- [ ] a9.area.051.name - CUT (b001): Mountains rendered as Range for width.
- [ ] a9.area.054.name - CUT (b001): Snowfield shortened to Snow for width.
- [ ] a9.area2.000.name - CUT (b001): Golden shortened to Gold for width.
- [ ] a9.area2.002.name - CUT (b001): Forest omitted for width.
- [ ] a9.area2.003.name - CUT (b001): Marsh rendered as Mire for width.
- [ ] a9.area2.004.name - CUT (b001): Mountains shortened to Mts. for width.
- [ ] a9.area2.006.name - CUT (b001): Wastes omitted for width.
- [ ] a9.area2.008.name - CUT (b001): Snowfield shortened to Snow for width.
- [ ] a9.area2.009.name - CUT (b001): Glacier shortened to Ice for width.
- [ ] a9.area2.012.name - CUT (b001): Volcano shortened to Mt. for width.
- [ ] a9.area2.014.name - CUT (b001): Mountains shortened to Mts. for width.
- [ ] a9.area2.023.name - CUT (b001): Mountains omitted for width.
- [ ] a9.armor.018.desc - CUT (b001): Quite omitted for width.
- [ ] a9.armor.048.desc - CUT (b001): Cape implicit in item name for width.
- [ ] a9.keyitem.007.name - CUT (b003): Possessive shortened to fit the byte cap.
- [ ] a9.keyitem.009.name - CUT (b003): "Bridge" omitted to fit the field.
- [ ] a9.keyitem.016.name - CUT (b003): "Growth" omitted to fit the field.
- [ ] a9.keyitem.021.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.keyitem.022.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.keyitem.023.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.keyitem.024.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.keyitem.025.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.keyitem.027.desc - CUT (b003): Stone material omitted to fit the field.
- [ ] a9.meigeki.003.name - CUT (b003): Scorching modifier condensed into "Inferno".
- [ ] a9.meigeki.007.name - CUT (b003): Scorching and dark modifiers condensed into "Hell".
- [ ] a9.meigeki.009.name - CUT (b003): Dark modifier omitted.
- [ ] a9.meigeki.012.name - CUT (b003): Water and dark modifiers omitted.
- [ ] a9.meigeki.016.name - CUT (b003): Extreme cold and freezing condensed into "Ice".
- [ ] a9.meigeki.017.name - CUT (b003): Extreme cold modifier omitted.
- [ ] a9.meigeki.026.name - CUT (b003): Turbulence modifier omitted.
- [ ] a9.meigeki.027.name - CUT (b003): Turbulence modifier omitted.
- [ ] a9.meigeki.031.name - CUT (b003): Lightning wave condensed into "Surge".
- [ ] a9.meigeki.035.name - CUT (b003): Great hell demon condensed into "Archfiend".
- [ ] a9.meigeki.036.name - CUT (b003): Lightning condensed into "Flash".
- [ ] a9.meigeki.040.name - CUT (b003): Dark, demonic and explosive modifiers condensed into "Doom".
- [ ] a9.meigeki.042.name - CUT (b003): Great and demonic modifiers omitted.
- [ ] a9.monster.001.area - CUT (b004): Mountains shortened to Mts. to fit.
- [ ] a9.monster.042.name - CUT (b004): Land omitted to fit.
- [ ] a9.monster.047.name - CUT (b004): Jewel omitted to fit.
- [ ] a9.monster.052.area - CUT (b004): Forest omitted to fit.
- [ ] a9.monster.073.name - CUT (b004): Jack-in-the-Box shortened to Trick Box to fit.
- [ ] a9.monster.100.name - CUT (b004): Ravenous rendered as Dire to fit.
- [ ] a9.monster.106.name - CUT (b004): Iron omitted to fit.
- [ ] a9.monster.111.area - CUT (b004): Tower rendered as Spire to fit.
- [ ] a9.monster.128.name - CUT (b004): Snow and ice condensed to Frost to fit.
- [ ] a9.monster.131.area - CUT (b004): Mountain and village omitted to fit.
- [ ] a9.monster.139.name - CUT (b005): Omitted "toxic" to fit.
- [ ] a9.monster.141.name - CUT (b005): Shortened the large warship description to "Grand" to fit.
- [ ] a9.monster.142.name - CUT (b005): Shortened "sandstorm" to "sand" to fit.
- [ ] a9.monster.149.name - CUT (b005): Shortened glossary form "Volcanic Pterosaur" to "Lava Pterosaur" to fit.
- [ ] a9.monster.154.name - CUT (b005): Shortened "jet-black" to "black" to fit.
- [ ] a9.monster.157.area - CUT (b005): Omitted "Valley" from the glossary form to fit.
- [ ] a9.party.052.name - CUT (b005): Omitted Harden's name to fit.
- [ ] a9.0219AD18 - CUT (b005): Omitted Harden's name to fit.
- [ ] a9.021AB998 - CUT (b005): Omitted explicit mention of the weapon to fit.
- [ ] a9.skill.037.desc - CUT (b009): Countless arrows reduced to arrows.
- [ ] a9.skill.047.desc - CUT (b009): Forward direction omitted.
- [ ] a9.skill.048.desc - CUT (b009): Forward direction omitted; cannon shortened to gun.
- [ ] a9.skill.049.desc - CUT (b009): Forward direction omitted.
- [ ] a9.skill.052.desc - CUT (b009): Shoulder generalized to body.
- [ ] a9.skill.053.desc - CUT (b009): Spinning motion omitted.
- [ ] a9.skill.054.desc - CUT (b009): Spinning motion omitted.
- [ ] a9.skill.055.desc - CUT (b009): Spinning motion omitted.
- [ ] a9.skill.056.desc - CUT (b009): Forward direction omitted.
- [ ] a9.skill.061.desc - CUT (b009): Forward direction omitted; cannon shortened to gun.
- [ ] a9.special.006.name - CUT (b009): "Bolt" omitted from Lightning Bolt Grasper to fit width.
- [ ] a9.tengeki.002.name - CUT (b010): Shared "Divine Attack" prefix omitted throughout skill names to fit.
- [ ] a9.tengeki.003.name - CUT (b010): Heavenly epithet and size omitted to fit.
- [ ] a9.tengeki.007.desc - CUT (b010): "Divine Attack" omitted to fit.
- [ ] a9.tengeki.012.name - CUT (b010): Heavenly blue epithet omitted to fit.
- [ ] a9.tengeki.016.desc - CUT (b010): "Divine Attack" omitted to fit.
- [ ] a9.tengeki.017.desc - CUT (b010): Defense shortened to DEF.
- [ ] a9.tengeki.021.name - CUT (b010): Heavenly turmoil epithet and size omitted to fit.
- [ ] a9.tengeki.028.desc - CUT (b010): "Divine" omitted from thunder attack descriptions through 034 to fit.
- [ ] a9.tengeki.031.name - CUT (b010): Sky flash and thunder blast imagery condensed to "Skybolt".
- [ ] a9.tengeki.037.desc - CUT (b010): "Divine" omitted from light attack descriptions through 041 to fit.
- [ ] a9.tengeki.042.name - CUT (b010): Light-and-shadow imagery shortened to "Shade".
- [ ] a9.title.014.name - CUT (b010): Abandoned village shortened to "Ruins" throughout related map labels.
- [ ] a9.title.021.name - CUT (b010): B- means no bridge; G- means destroyed gate.
- [ ] a9.title.022.name - CUT (b010): B+ means bridge present; G- means destroyed gate.
- [ ] a9.title.023.name - CUT (b010): B+ means bridge present; G+ means normal gate.
- [ ] a9.title.034.name - CUT (b010): Abandoned village omitted from town interior label.
- [ ] a9.title.035.name - CUT (b010): Abandoned village omitted from town interior label.
- [ ] a9.title.036.name - CUT (b010): Abandoned village omitted from town interior label.
- [ ] a9.title.037.name - CUT (b010): Abandoned village and pedestal omitted to fit.
- [ ] a9.title.038.name - CUT (b010): "Pedestal" omitted to fit.
- [ ] a9.title.099.name - CUT (b010): Bridge- means no bridge.
- [ ] a9.title.102.name - CUT (b010): Hidden room absent shortened to "Room-".
- [ ] a9.title.103.name - CUT (b010): Hidden room present shortened to "Den".
- [ ] a9.title.116.name - CUT (b010): "Childhood" omitted to fit.
- [ ] a9.title.120.name - CUT (b010): "Goddess" omitted to fit.
- [ ] a9.vandel.006.name - CUT (b010): Enhanced version shortened to "EX".
- [ ] a9.vandel.027.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px.
- [ ] a9.vandel.028.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px.
- [ ] a9.vandel.030.name - CUT (b011): Dropped "Hero" from the protagonist label to fit 108 px.
- [ ] a9.weapon.022.name - CUT (b011): Dropped "Bolt" from Lightning Bolt Grasper to fit 18 bytes.
- [ ] a9.weapon.022.name2 - CUT (b011): Dropped "Bolt" from Lightning Bolt Grasper to fit 18 bytes.
- [ ] a9.weapon.052.desc - CUT (b012): Shortened "one-handed" to "1H" to fit.
- [ ] a9.weapon.053.desc - CUT (b012): Dropped "special" to fit.
- [ ] a9.weapon.054.desc - CUT (b012): Shortened "one-handed" to "1H" to fit.
- [ ] a9.weapon.063.desc - CUT (b012): Dropped "special" to fit.
- [ ] a9.weapon.072.desc - CUT (b012): Shortened "two-handed" to "2H" to fit.
- [ ] a9.weapon.073.desc - CUT (b012): Dropped "special" and shortened "two-handed" to "2H" to fit.
- [ ] a9.weapon.074.desc - CUT (b012): Shortened "two-handed" to "2H" to fit.
- [ ] a9.weapon.102.desc - CUT (b013): Omitted "composite" to fit.
- [ ] a9.weapon.103.desc - CUT (b013): Omitted the steel's composite composition to fit.
- [ ] a9.weapon.104.desc - CUT (b013): Condensed "very strong" to "tough" to fit.
- [ ] a9.weapon.159.name - CUT (b014): Used "Ring" for "Chakram" to fit; also in name2.
- [ ] a9.weapon.160.name - CUT (b014): Used "Ring" for "Chakram" to fit; also in name2.
- [ ] a9.wpntype.022.name - CUT (b015): Dropped "Bolt" from "Lightning Bolt Grasper" to fit the 18-byte cap.
- [x] rom.063E0 - CUT (b016): Shortened Village Chief to Chief to fit. - fixed: full form fits the 80 px tag
- [x] rom.06AC8 - CUT (b016): Used Envoy for Messenger to fit. - fixed: full form fits the 80 px tag
- [x] rom.0D3EC - CUT (b016): Shortened Resistance to Resist. to fit. - fixed: full form fits the 80 px tag
- [ ] rom.11134 - CUT (b016): Shortened Resistance to Resist. to fit the letter.
- [ ] rom.11154 - CUT (b016): Shortened Resistance to Resist. to fit the letter.
- [ ] rom.11228 - CUT (b016): Shortened Resistance to Resist. to fit the letter.
- [ ] rom.137B8 - CUT (b017): Bridge omitted.
- [x] rom.19F6C - CUT (b017): Weapon Shop shortened to Weapons. - fixed: full form fits the 80 px tag
- [ ] rom.1B044 - CUT (b017): Tavern Woman shortened to Barmaid.
- [ ] rom.1B8DC - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.205D8 - CUT (b017): Resistance abbreviated to Resist.
- [x] rom.30C54 - CUT (b017): Shagie abbreviated to S. - fixed: full form fits the 80 px tag
- [ ] rom.3D69C - CUT (b017): Generic omitted; greatsword abbreviated to GS.
- [ ] rom.3D6BC - CUT (b017): Generic omitted; greatsword abbreviated to GS.
- [ ] rom.3D6DC - CUT (b017): Generic omitted; greatsword abbreviated to GS.
- [ ] rom.3D6FC - CUT (b017): Generic omitted; greatsword abbreviated to GS; lightning shortened to Bolt.
- [ ] rom.3D71C - CUT (b017): Generic omitted; greatsword abbreviated to GS.
- [ ] rom.3D73C - CUT (b017): Generic omitted; spear abbreviated to Spr.
- [ ] rom.3D758 - CUT (b017): Generic omitted; spear abbreviated to Spr.
- [ ] rom.3D774 - CUT (b017): Generic omitted; spear abbreviated to Spr.
- [ ] rom.3D790 - CUT (b017): Generic omitted; spear abbreviated to Spr; lightning shortened to Bolt.
- [ ] rom.3D7AC - CUT (b017): Generic omitted; spear abbreviated to Spr.
- [ ] rom.3D7C8 - CUT (b017): Generic omitted.
- [ ] rom.3D7E4 - CUT (b017): Generic omitted; Water rendered as Aqua to fit.
- [ ] rom.3D800 - CUT (b017): Generic omitted.
- [ ] rom.3D81C - CUT (b017): Generic omitted; lightning shortened to Bolt.
- [ ] rom.3D838 - CUT (b017): Generic omitted.
- [ ] rom.3D854 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H.
- [ ] rom.3D874 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H.
- [ ] rom.3D894 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H.
- [ ] rom.3D8B4 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H; lightning shortened to Bolt.
- [ ] rom.3D8D4 - CUT (b017): Generic omitted; one-handed sword abbreviated to 1H.
- [ ] rom.3D8F4 - CUT (b017): Generic omitted.
- [ ] rom.3D90C - CUT (b017): Generic omitted; Water rendered as Aqua to fit.
- [ ] rom.3D924 - CUT (b017): Generic omitted.
- [ ] rom.3D93C - CUT (b017): Generic omitted; lightning shortened to Bolt.
- [ ] rom.3D954 - CUT (b017): Generic omitted.
- [ ] rom.3D96C - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist.
- [ ] rom.3D988 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist; Water rendered as Aqua to fit.
- [ ] rom.3D9A4 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist.
- [ ] rom.3D9C0 - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist; lightning shortened to Bolt.
- [ ] rom.3D9DC - CUT (b017): Generic omitted; hand-to-hand combat shortened to Fist.
- [ ] rom.3D9F8 - CUT (b017): Generic omitted; throwing sword abbreviated to TS.
- [ ] rom.3DA14 - CUT (b017): Generic omitted; throwing sword abbreviated to TS.
- [ ] rom.3DA30 - CUT (b017): Generic omitted; throwing sword abbreviated to TS.
- [ ] rom.3DA4C - CUT (b017): Generic omitted; throwing sword abbreviated to TS; lightning shortened to Bolt.
- [ ] rom.3DA68 - CUT (b017): Generic omitted; throwing sword abbreviated to TS.
- [ ] rom.3E108 - CUT (b017): Transformed label shortened to original numeric marker.
- [ ] rom.42DF0 - CUT (b017): Village omitted.
- [ ] rom.470F4 - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.47758 - CUT (b017): Forest omitted.
- [ ] rom.499B4 - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.49A1C - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.49AA8 - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.4A1A0 - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.4A220 - CUT (b017): Resistance abbreviated to Resist.
- [ ] rom.4A324 - CUT (b017): Resistance abbreviated to Resist.

## Review minors b001
- [ ] a9.armor.000.desc - "見習いバスターのジャケット" means an apprentice Buster's jacket - Compressed phrasing breaks the surrounding possessive pattern - An apprentice Buster's jacket.
- [ ] a9.armor.008.desc - "百戦錬磨バスターのジャケット" means a battle-hardened Buster's jacket - "War-tested" is awkward and unnecessarily implies warfare - A battle-hardened Buster's jacket.
- [ ] a9.armor.018.desc - "かなり強い素材でできたシャツ" means a shirt made of quite strong material - Telegraphic phrasing - A shirt made of tough material.
- [ ] a9.armor.019.desc - "非常に強い素材でできたシャツ" means a shirt made of very strong material - "Ultra-tough material shirt" is an awkward noun stack - A shirt made of extremely tough material.
- [ ] a9.armor.028.desc - "非常に強い素材でできたシールド" means a shield made of very strong material - Awkward noun stack - A shield made of extremely tough material.
- [ ] a9.armor.029.desc - "防具屋アトスが作った盾" means a shield made by Atos, the armor dealer - "By armor seller" is stiff - A shield made by Atos, the armor dealer.
- [ ] a9.armor.039.desc - "達人が愛用する強い腕輪" means a strong bangle favored by masters - Compressed phrasing reads awkwardly - A tough bangle favored by masters.
- [ ] a9.armor.048.desc - "複合特殊鋼材を織り込んだマント" means a cape with special composite steel woven into it - "Special steel-alloy weave" obscures the cape's construction - A cape woven with special composite steel.
- [ ] a9.armor.049.desc - "非常に強い素材でできたマント" means a cape made of very strong material - Awkward noun stack - A cape made of extremely tough material.

## Review minors b002
- [ ] a9.armor.057.desc - "多くのバスターが愛用するバンダナ": Bandanna favored by many Busters - Lowercase "bandanna" differs from the binding glossary spelling - A Bandanna favored by many Busters
- [ ] a9.armor.058.desc - "複合特殊鋼材を織り込んだ": woven with special composite steel - "Alloy-knit" is awkward and changes weaving to knitting - Bandanna woven with special composite steel
- [ ] a9.armor.068.desc - "複合特殊鋼材を織り込んだ": woven with special composite steel - "Alloy-woven" is awkward and obscures the specific material - Gloves woven with special composite steel

## Review minors b003
- [ ] a9.keyitem.002.desc - "リング修復アイテムの原材料" means raw material for an item used to repair rings - "Ring repair aid" is an awkward, unclear noun cluster - Material used to make a ring repair item.
- [ ] a9.keyitem.011.desc - "飛行機をとめる南京錠のカギ１" means key 1 for the padlock securing the Airplane - Missing article makes "Airplane's padlock" sound like a person's possession - Key 1 for the padlock securing the Airplane.
- [ ] a9.keyitem.012.desc - "飛行機をとめる南京錠のカギ２" means key 2 for the padlock securing the Airplane - Same awkward possessive - Key 2 for the padlock securing the Airplane.
- [ ] a9.keyitem.013.desc - "飛行機をとめる南京錠のカギ３" means key 3 for the padlock securing the Airplane - Same awkward possessive - Key 3 for the padlock securing the Airplane.
- [ ] a9.keyitem.014.desc - "飛行機をとめる南京錠のカギ４" means key 4 for the padlock securing the Airplane - Same awkward possessive - Key 4 for the padlock securing the Airplane.
- [ ] a9.keyitem.015.desc - "飛行機をとめる南京錠のカギ５" means key 5 for the padlock securing the Airplane - Same awkward possessive - Key 5 for the padlock securing the Airplane.
- [ ] a9.meigeki.003.desc - "単体攻撃用の炎の上位冥撃・大" means an advanced fire Dark Attack with high power against one target - "High Dark Fire+" obscures the distinction between advanced rank and high power and resembles a modified spell name - Advanced fire Dark Attack: one foe, high power.

## Review minors b005
- [ ] a9.021B5758 - 同じ陣営では対戦できません means players on the same side cannot battle each other - "Same sides cannot fight" is unnatural and unclear - Players on the same side cannot battle each other.

## Review minors b006
- [ ] a9.shout.010.s03 - "受けてみろ！" challenges the enemy to withstand an attack - "Try taking this!" sounds unnatural - Let's see you take this!
- [ ] a9.shout.011.s07 - "こいつを受けてみろ！" challenges the enemy to withstand this attack - "Try taking this!" sounds unnatural - Let's see you take this!
- [ ] a9.shout.013.s06 - "カッコいいとこ見せるぜ！" promises an impressive display - "Watch me look cool!" sounds awkwardly literal - Watch me show off!
- [ ] a9.shout.015.s02 - "消えろ！" orders an enemy to vanish - "Disappear!" sounds stiff as a combat shout - Begone!

## Review minors b007
- [ ] a9.shout.031.s04 - "うりゃっ！" is an attack cry - "Hurrah!" reads as a celebratory cheer - Hyaah!
- [ ] a9.shout.031.s07 - "うりゃーーっ！" is an extended attack cry - "Hurraaaah!" reads as celebration - Hyaaaah!
- [ ] a9.shout.041.s01 - "わたしの拳を受けてみろっ！" challenges the enemy to withstand a punch - "Try taking my fist!" is an awkward literal rendering - Try taking this punch!
- [ ] a9.shout.053.s03 - "うりゃぁーーっ！！" is an attack cry - "Hurraaaah!!" reads as celebration - Hyaaaah!!
- [ ] a9.shout.061.s01 - "ベカトルテ近海最強はオレ様だ！" boasts of being the strongest in the Bekatorte Seas - The place-name possessive sounds unnatural - I'm the strongest in the Bekatorte Seas!
- [ ] a9.shout.062.s01 - "我こそはベカトルテ近海最強！！" emphatically claims supremacy in the Bekatorte Seas - The place-name possessive is awkward and weakens the proclamation - I am the strongest in the Bekatorte Seas!!
- [ ] a9.shout.063.s01 - "へッヘッ ベカトルテ近海最強！" repeats the strongest-in-the-region boast - The possessive is awkward; "best" blurs the recurring claim of strength - Heh heh! Strongest in the Bekatorte Seas!

## Review minors b008
- [ ] a9.shout.066.s00 - "具現化できるんだろうね" expects confirmation that the opponent can manifest a Saiga - The open question loses the speaker's presumptuous expectation - suggested EN: You can summon your Saiga, I trust?
- [ ] a9.shout.066.s05 - "この世で美しきものは　才牙" praises Saiga as beautiful things in this world - "This world's beauty" sounds unnatural - suggested EN: There is such beauty in Saiga...
- [ ] a9.shout.073.s03 - "動くと正確に切れんだろーがあっ" angrily demands stillness to allow precise cutting - "Cut clean" is awkward and blurs the emphasis on precision - suggested EN: Hold still! I can't cut accurately if you move!
- [ ] a9.shout.077.s00 - "我が冥力の極致" announces the pinnacle of the speaker's Dark Power - "My peak Dark Power" sounds mechanical rather than grandiose - suggested EN: Behold the pinnacle of my Dark Power...

## Review minors b009
- [ ] a9.skill.006.desc - "落下し周囲に衝撃波を出す" means dropping and releasing a surrounding shockwave - "wave all round" is awkward and loses the specific shockwave imagery - suggested EN: Drops and releases a shockwave all around.
- [ ] a9.skill.007.desc - "敵の左右を往復して攻撃" means attacking while moving back and forth on either side of an enemy - "Hits side to side" makes the movement unclear - suggested EN: Moves back and forth on either side of a foe to attack.
- [ ] a9.skill.027.desc - "振り回して周囲の敵を攻撃" means swinging the weapon around to attack surrounding enemies - "Swings at all round" is ungrammatical - suggested EN: Swings the weapon to hit surrounding foes.
- [ ] a9.skill.052.desc - "肩から突進冥力攻撃" means a shoulder-first Dark Power charge - "body rush" loses the shoulder-first action and sounds unnatural - suggested EN: Charges shoulder-first with Dark Power.
- [ ] a9.skill.058.desc - "その場に冥力輪を放つ" means releasing a Dark Power ring at the user's location - "ring on spot" is awkward shorthand - suggested EN: Releases a Dark Power ring in place.

## Review minors b010
- [ ] a9.tengeki.007.desc - "単体のマヒの治療": cures paralysis for one target - "on one" sounds unfinished - Cures paralysis for one target.
- [ ] a9.tengeki.016.desc - "単体の毒の治療": cures poison for one target - "on one" sounds unfinished - Cures poison for one target.
- [ ] a9.tengeki.017.desc - "単体の物理防御力を２０％上昇": raises one target's physical defense by 20% - "One:" is awkwardly elliptical - Raises one target's physical defense by 20%.
- [ ] a9.tengeki.035.desc - "攻撃を雷属性にする": changes attacks to the thunder element - "Attacks become thunder" reads literally and awkwardly - Gives attacks the thunder element.
- [ ] a9.title.116.name - "幼馴染みの家": childhood friend's house - Loses the childhood relationship - Childhood Friend's House
- [ ] a9.title.120.name - "女神像の場所": goddess statue's location - Omits which statue despite "Goddess Statue" appearing nearby - Goddess Statue Site

## Review minors b011
- [ ] a9.weapon.010.desc - "エルファストの防具屋が作った盾" means a shield made by Elfast's Armor Shop - "By Elfast's Armor Shop" is an awkward fragment and omits the object - A shield made by Elfast's Armor Shop.
- [ ] a9.weapon.033.desc - "複合特殊鋼材でできた槍" means a spear made from a special steel composite - "Special steel blend spear" is an awkward noun stack - A spear made from a special steel composite.
- [ ] a9.weapon.043.desc - "複合特殊鋼材でできた槍斧" means a glaive made from a special steel composite - "Special steel blend glaive" is an awkward noun stack - A glaive made from a special steel composite.

## Review minors b012
- [ ] a9.weapon.070.desc - "レアメタルでできた両手剣": rare metal Two-Hand Sword - Class-term capitalization differs from the glossary - Rare metal Two-Hand Sword

## Review minors b013
- [ ] a9.weapon.095.desc - "青銅で強化した" means reinforced with bronze - "Bronze-set" sounds decorative rather than structural - Composite bow reinforced with bronze
- [ ] a9.weapon.096.desc - "銅で強化した" means reinforced with copper - "Copper-set" sounds decorative rather than structural - Composite bow reinforced with copper
- [ ] a9.weapon.100.desc - "レアメタルで強化した合成弓" means a composite bow reinforced with rare metal - The reinforcement relationship is unclear - Composite bow reinforced with rare metal
- [ ] a9.weapon.101.desc - "ハイメタルで強化した合成弓" means a composite bow reinforced with High Metal - The reinforcement relationship is unclear - Composite bow reinforced with High Metal
- [ ] a9.weapon.102.desc - "合成弓" means composite bow - The bow type is omitted - Composite bow reinforced with Bekatorte Steel
- [ ] a9.weapon.103.desc - "複合特殊鋼材で強化した" means reinforced with special composite steel - The material and reinforcement are compressed into an ambiguous modifier - Composite bow reinforced with special alloy steel
- [ ] a9.weapon.104.desc - "非常に強い金属で強化した" means reinforced with exceptionally strong metal - "Tough-metal" is awkward and loses the emphasis - Composite bow reinforced with ultra-strong metal
- [ ] a9.weapon.114.desc - "銃とナックルの長所を持つ武器" means a weapon combining the advantages of guns and knuckles - "Gun and knuckle strengths" reads like a heading rather than an item description - Combines the strengths of guns and knuckles

## Review minors b016
- [ ] rom.02130 - "おじさん" denotes a middle-aged man - "Old Man" implies the elderly おじいさん - Middle-aged Man

## Review minors b017
- [ ] rom.42DF0 - "里の門" means village gate - "Gate" unnecessarily loses the location qualifier - Village Gate

## Review fixes blocked by width (re-apply after the box is measured or widened; suggestion in work/tr/review/<batch>.md)
- [ ] a9.area.001.name - b001 review: line 1: 119 px > 96 (12 px font) 'Muterin Mountains'
- [ ] a9.area.007.name - b001 review: line 1: 121 px > 96 (12 px font) 'Mirei Forest Village'
- [ ] a9.area.017.name - b001 review: line 1: 98 px > 96 (12 px font) 'Benuru Wastes'
- [ ] a9.area.021.name - b001 review: 26 bytes > slot cap 22
- [ ] a9.area.022.name - b001 review: line 1: 102 px > 96 (12 px font) 'Norunaji Forest'
- [ ] a9.area.029.name - b001 review: line 1: 114 px > 96 (12 px font) 'Bim Desert Tower'
- [ ] a9.area.036.name - b001 review: line 1: 126 px > 96 (12 px font) 'Bakoson Mountains'
- [ ] a9.area.040.name - b001 review: line 1: 121 px > 96 (12 px font) 'Riberin Lake Tower'
- [ ] a9.area.046.name - b001 review: line 1: 137 px > 96 (12 px font) 'Sole Valley Labyrinth'
- [ ] a9.area.050.name - b001 review: line 1: 104 px > 96 (12 px font) 'Byonrin Volcano'
- [ ] a9.area.051.name - b001 review: line 1: 118 px > 96 (12 px font) 'Rinrago Mountains'
- [ ] a9.area.054.name - b001 review: line 1: 102 px > 96 (12 px font) 'Zeros Snowfield'
- [ ] a9.area2.000.name - b001 review: line 1: 91 px > 84 (12 px font) 'Golden Castle'
- [ ] a9.area2.002.name - b001 review: line 1: 102 px > 84 (12 px font) 'Norunaji Forest'
- [ ] a9.area2.003.name - b001 review: line 1: 88 px > 84 (12 px font) 'Pasero Marsh'
- [ ] a9.area2.004.name - b001 review: line 1: 119 px > 84 (12 px font) 'Muterin Mountains'
- [ ] a9.area2.006.name - b001 review: line 1: 98 px > 84 (12 px font) 'Benuru Wastes'
- [ ] a9.area2.008.name - b001 review: line 1: 102 px > 84 (12 px font) 'Zeros Snowfield'
- [ ] a9.area2.009.name - b001 review: line 1: 91 px > 84 (12 px font) 'Rinnam Glacier'
- [ ] a9.area2.012.name - b001 review: line 1: 104 px > 84 (12 px font) 'Byonrin Volcano'
- [ ] a9.area2.014.name - b001 review: line 1: 118 px > 84 (12 px font) 'Rinrago Mountains'
- [ ] a9.area2.023.name - b001 review: line 1: 126 px > 84 (12 px font) 'Bakoson Mountains'
- [ ] a9.keyitem.001.desc - b003 review: line 1: 283 px > 180 (12 px font) 'A letter to the Village Chief of East Village
- [ ] a9.keyitem.009.name - b003 review: 22 bytes > slot cap 18
- [ ] a9.monster.001.area - b004 review: line 1: 126 px > 120 (12 px font) 'Bakoson Mountains'
- [ ] a9.monster.111.area - b004 review: line 1: 121 px > 120 (12 px font) 'Riberin Lake Tower'
- [ ] a9.monster.131.area - b004 review: 32 bytes > slot cap 20
- [ ] a9.monster.157.area - b005 review: 22 bytes > slot cap 20
- [ ] a9.party.052.name - b005 review: line 1: 98 px > 62 (12 px font) "Harden's Minion"
- [ ] a9.0219AD18 - b005 review: line 1: 98 px > 84 (12 px font) "Harden's Minion"
- [ ] a9.021AB998 - b005 review: line 1: 276 px > 180 (12 px font) 'You have a two-handed weapon equipped.'
- [ ] a9.skill.002.desc - b009 review: 68 bytes > slot cap 26
- [ ] a9.skill.018.desc - b009 review: 66 bytes > slot cap 26
- [ ] a9.skill.019.desc - b009 review: 64 bytes > slot cap 26
- [ ] a9.skill.023.desc - b009 review: 58 bytes > slot cap 26
- [ ] a9.skill.024.desc - b009 review: 60 bytes > slot cap 26
- [ ] a9.skill.025.desc - b009 review: 52 bytes > slot cap 26
- [ ] a9.skill.035.desc - b009 review: 48 bytes > slot cap 26
- [ ] a9.skill.048.desc - b009 review: 50 bytes > slot cap 26
- [ ] a9.skill.061.desc - b009 review: 58 bytes > slot cap 26
- [ ] a9.tengeki.002.desc - b010 review: line 1: 319 px > 168 (12 px font) 'High-power fire Divine Attack against one tar
- [ ] a9.tengeki.004.desc - b010 review: line 1: 277 px > 168 (12 px font) 'Low-power fire Divine Attack over an area.'
- [ ] a9.tengeki.005.desc - b010 review: line 1: 297 px > 168 (12 px font) 'Medium-power fire Divine Attack over an area.
- [ ] a9.tengeki.006.desc - b010 review: line 1: 277 px > 168 (12 px font) 'High-power fire Divine Attack over an area.'
- [ ] a9.tengeki.009.desc - b010 review: line 1: 316 px > 168 (12 px font) 'Low-power ice Divine Attack against one targe
- [ ] a9.tengeki.010.desc - b010 review: line 1: 336 px > 168 (12 px font) 'Medium-power ice Divine Attack against one ta
- [ ] a9.tengeki.011.desc - b010 review: line 1: 316 px > 168 (12 px font) 'High-power ice Divine Attack against one targ
- [ ] a9.tengeki.013.desc - b010 review: line 1: 314 px > 168 (12 px font) 'Low-power ice Divine Attack against all targe
- [ ] a9.tengeki.014.desc - b010 review: line 1: 334 px > 168 (12 px font) 'Medium-power ice Divine Attack against all ta
- [ ] a9.tengeki.015.desc - b010 review: line 1: 314 px > 168 (12 px font) 'High-power ice Divine Attack against all targ
- [ ] a9.tengeki.018.desc - b010 review: line 1: 326 px > 168 (12 px font) 'Low-power wind Divine Attack against one targ
- [ ] a9.tengeki.019.desc - b010 review: line 1: 346 px > 168 (12 px font) 'Medium-power wind Divine Attack against one t
- [ ] a9.tengeki.020.desc - b010 review: line 1: 326 px > 168 (12 px font) 'High-power wind Divine Attack against one tar
- [ ] a9.tengeki.022.desc - b010 review: line 1: 284 px > 168 (12 px font) 'High-power wind Divine Attack over an area.'
- [ ] a9.tengeki.028.desc - b010 review: line 1: 350 px > 168 (12 px font) 'Low-power thunder Divine Attack against one t
- [ ] a9.tengeki.029.desc - b010 review: line 1: 370 px > 168 (12 px font) 'Medium-power thunder Divine Attack against on
- [ ] a9.tengeki.030.desc - b010 review: line 1: 350 px > 168 (12 px font) 'High-power thunder Divine Attack against one 
- [ ] a9.tengeki.032.desc - b010 review: line 1: 308 px > 168 (12 px font) 'Low-power thunder Divine Attack over an area.
- [ ] a9.tengeki.033.desc - b010 review: line 1: 328 px > 168 (12 px font) 'Medium-power thunder Divine Attack over an ar
- [ ] a9.tengeki.034.desc - b010 review: line 1: 308 px > 168 (12 px font) 'High-power thunder Divine Attack over an area
- [ ] a9.tengeki.037.desc - b010 review: line 1: 326 px > 168 (12 px font) 'Low-power light Divine Attack against one tar
- [ ] a9.tengeki.038.desc - b010 review: line 1: 346 px > 168 (12 px font) 'Medium-power light Divine Attack against one 
- [ ] a9.tengeki.039.desc - b010 review: line 1: 326 px > 168 (12 px font) 'High-power light Divine Attack against one ta
- [ ] a9.tengeki.040.desc - b010 review: line 1: 304 px > 168 (12 px font) 'Medium-power light Divine Attack over an area
- [ ] a9.tengeki.041.desc - b010 review: line 1: 284 px > 168 (12 px font) 'High-power light Divine Attack over an area.'
- [ ] a9.title.021.name - b010 review: 36 bytes > slot cap 18
- [ ] a9.title.022.name - b010 review: 32 bytes > slot cap 18
- [ ] a9.title.023.name - b010 review: 28 bytes > slot cap 18
- [ ] a9.title.034.name - b010 review: 36 bytes > slot cap 18
- [ ] a9.title.035.name - b010 review: 34 bytes > slot cap 18
- [ ] a9.title.036.name - b010 review: 38 bytes > slot cap 18
- [ ] a9.title.037.name - b010 review: 42 bytes > slot cap 18
- [ ] a9.title.038.name - b010 review: 40 bytes > slot cap 18
- [ ] a9.title.099.name - b010 review: 20 bytes > slot cap 18
- [ ] a9.title.102.name - b010 review: 28 bytes > slot cap 18
- [ ] a9.title.103.name - b010 review: 24 bytes > slot cap 18
- [ ] a9.weapon.052.desc - b012 review: line 1: 214 px > 194 (12 px font) 'Bekatorte Steel One-Hand Sword'
- [ ] a9.weapon.053.desc - b012 review: line 1: 282 px > 194 (12 px font) 'One-Hand Sword of special composite steel'
- [ ] a9.weapon.054.desc - b012 review: line 1: 249 px > 194 (12 px font) 'One-Hand Sword of superstrong metal'
- [ ] a9.weapon.062.desc - b012 review: line 1: 210 px > 194 (12 px font) 'Bekatorte Steel Throwing Sword'
- [ ] a9.weapon.063.desc - b012 review: line 1: 278 px > 194 (12 px font) 'Throwing Sword of special composite steel'
- [ ] a9.weapon.064.desc - b012 review: line 1: 245 px > 194 (12 px font) 'Throwing Sword of superstrong metal'
- [ ] a9.weapon.072.desc - b012 review: line 1: 217 px > 194 (12 px font) 'Bekatorte Steel Two-Hand Sword'
- [ ] a9.weapon.073.desc - b012 review: line 1: 285 px > 194 (12 px font) 'Two-Hand Sword of special composite steel'
- [ ] a9.weapon.074.desc - b012 review: line 1: 252 px > 194 (12 px font) 'Two-Hand Sword of superstrong metal'
- [ ] a9.weapon.162.desc - b014 review: line 1: 212 px > 194 (12 px font) 'Special steel composite chakram'
- [ ] a9.weapon.163.name2 - b014 review: 20 bytes > slot cap 18
- [ ] name.m054 - b015 review: 22 bytes > slot cap 12
- [ ] rom.11134 - b016 review: line 1: 85 px > 80 (12 px font) 'Resistance B'
- [ ] rom.11154 - b016 review: line 1: 86 px > 80 (12 px font) 'Resistance C'
- [ ] rom.11228 - b016 review: line 1: 87 px > 80 (12 px font) 'Resistance A'
- [ ] rom.137B8 - b017 review: line 1: 89 px > 80 (12 px font) 'Bridge Master'
- [ ] rom.19F6C - b017 review: line 1: 86 px > 80 (12 px font) 'Weapon Shop'
- [ ] rom.1B044 - b017 review: line 1: 95 px > 80 (12 px font) 'Tavern Woman'
- [ ] rom.1B8DC - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance J'
- [ ] rom.205D8 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance E'
- [ ] rom.3D69C - b017 review: line 1: 103 px > 80 (12 px font) 'Greatsword Fire'
- [ ] rom.3D6BC - b017 review: line 1: 118 px > 80 (12 px font) 'Greatsword Water'
- [ ] rom.3D6DC - b017 review: line 1: 108 px > 80 (12 px font) 'Greatsword Wind'
- [ ] rom.3D6FC - b017 review: line 1: 106 px > 80 (12 px font) 'Greatsword Bolt'
- [ ] rom.3D71C - b017 review: line 1: 113 px > 80 (12 px font) 'Greatsword Light'
- [ ] rom.3D854 - b017 review: line 1: 133 px > 80 (12 px font) 'One-Hand Sword Fire'
- [ ] rom.3D874 - b017 review: line 1: 148 px > 80 (12 px font) 'One-Hand Sword Water'
- [ ] rom.3D894 - b017 review: line 1: 138 px > 80 (12 px font) 'One-Hand Sword Wind'
- [ ] rom.3D8B4 - b017 review: line 1: 136 px > 80 (12 px font) 'One-Hand Sword Bolt'
- [ ] rom.3D8D4 - b017 review: line 1: 143 px > 80 (12 px font) 'One-Hand Sword Light'
- [ ] rom.3D9F8 - b017 review: line 1: 129 px > 80 (12 px font) 'Throwing Sword Fire'
- [ ] rom.3DA14 - b017 review: line 1: 144 px > 80 (12 px font) 'Throwing Sword Water'
- [ ] rom.3DA30 - b017 review: line 1: 134 px > 80 (12 px font) 'Throwing Sword Wind'
- [ ] rom.3DA4C - b017 review: line 1: 132 px > 80 (12 px font) 'Throwing Sword Bolt'
- [ ] rom.3DA68 - b017 review: line 1: 139 px > 80 (12 px font) 'Throwing Sword Light'
- [ ] rom.3E108 - b017 review: line 1: 84 px > 80 (12 px font) 'Transformed'
- [ ] rom.470F4 - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance D'
- [ ] rom.47758 - b017 review: line 1: 112 px > 80 (12 px font) 'Mirei Forest Chief'
- [ ] rom.499B4 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance F'
- [ ] rom.49A1C - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance G'
- [ ] rom.49AA8 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance H'
- [ ] rom.4A220 - b017 review: line 1: 86 px > 80 (12 px font) 'Resistance K'
- [ ] rom.4A324 - b017 review: line 1: 85 px > 80 (12 px font) 'Resistance L'

## Review minors b018
- [ ] quest.009C0 - "渦の杯をみたせ" means fill the Whirlpool Chalice - Drops the objective verb retained in the other chalice titles - Fill the Whirlpool Chalice
- [ ] quest.00C0C - "極の杯をみたせ" means fill the Ultimate Chalice - Drops the objective verb retained in the other chalice titles - Fill the Ultimate Chalice
- [ ] quest.00E44 - "ジーク戦士団登場" announces Zeke's Squad's appearance - "Is In" sounds awkward and leaves its meaning unclear - Enter Zeke's Squad
- [ ] quest.0059C - review suggestion blocked by width: Lurker in the Underground Lake (120 px title)
- [ ] quest.00658 - review suggestion blocked by width: The Underground Lake Gate
- [ ] quest.01108 - review suggestion blocked by width: All Sealing Rings Destroyed
- [ ] quest.04430 - CUT: 再会、ビィト戦士団 "The Beet Warriors" drops the reunion ("Beet Warriors Again" 126 px > 120 jp-bound title)

## Flagged cuts (added)
- [ ] quest.0059C - CUT (b018): "Underground" omitted from the title to fit.
- [ ] quest.00658 - CUT (b018): "Underground" omitted from the title to fit.
- [ ] quest.009C0 - CUT (b018): "Fill" omitted from the title to preserve Whirlpool Chalice.
- [ ] quest.00C0C - CUT (b018): "Fill" omitted from the title to preserve Ultimate Chalice.
- [ ] quest.00D6C - CUT (b018): Former crookedness left implicit in "Reformed" to fit.
- [ ] quest.01E40 - CUT (b018): Gathering action omitted from the title to preserve Medicinal Flowers.
- [ ] quest.025E4 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.026D4 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.027D0 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.028C0 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.029A4 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.02A94 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.02B78 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.02C68 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.02D58 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.02E48 - CUT (b018): "Monster" omitted from the title to fit.
- [ ] quest.04070 - CUT (b019): Omitted explicit "Arrive" from the title.
- [ ] quest.04194 - CUT (b019): Omitted explicit "Monsters" from the title.
- [ ] quest.04254 - CUT (b019): Omitted "Buster" from the title.
- [ ] quest.04298 - CUT (b019): Omitted "Silver" from the title.
- [ ] quest.049E4 - CUT (b019): Shortened "Bridge Master" to "Master" in the title.
- [ ] quest.04A74 - CUT (b019): Omitted "Learn" from the title.
- [ ] quest.05578 - CUT (b019): Omitted "village" from the title.
- [ ] quest.055B4 - CUT (b019): Omitted "Statue" from the title.
- [ ] quest.055D8 - CUT (b019): Omitted "Golden" from the title.
- [ ] quest.05900 - CUT (b020): Omitted Dark Notes from the lender's title.
- [ ] quest.05ABC - CUT (b020): Omitted explicit mention of the mine to fit the title.
- [ ] quest.05C3C - CUT (b020): Omitted Sealing to fit the title.
- [ ] quest.05CA8 - CUT (b020): Omitted Lord of Dreams to fit the title.
- [ ] quest.05ED0 - CUT (b020): Omitted explicit emphasis on total conquest to fit the title.
- [ ] quest.05F00 - CUT (b020): Omitted explicit mention of hope to fit the title.
- [ ] quest.06564 - CUT (b020): Omitted Deadly Blade to fit the title.
- [ ] quest.06594 - CUT (b020): Omitted Immovable Giant to fit the title.
- [ ] quest.06708 - CUT (b020): Omitted Giant Butterfly to fit the title.
- [ ] quest.06750 - CUT (b020): Omitted Vandel from the epithet to fit the title.
- [ ] rom.011F4 - CUT (b021): Compressed to fit: omitted the sudden arrival, explicit castle-base role, and Appraiser's expected role in opposing the invasion.
- [ ] rom.0393C - CUT (b022): Shortened the worldwide origins and combat explanation; omitted the explicit size of Vandel bounties.
- [ ] rom.03B54 - CUT (b022): Shortened Kingdom of Gransista to Gransista; omitted the father reference, Association support explanation, nationwide hut network and request-based reward scaling.
- [ ] rom.0410C - CUT (b022): Omitted the conversational replies, offer to teach basics and final comprehension question; compressed the branding explanation and gradual improvement.
- [ ] rom.07B00 - CUT (b025): Shortened recognition, pauses, repeated throat-clearing and emphasis on the silver's special nature to fit 255 codes.
- [ ] rom.08944 - CUT (b025): Shortened the uncertain causal explanation, monsters' location in golden areas, island-protection motive, mining and flame-keeping details, and the hero's return as a strong Buster to fit 255 codes.
- [ ] rom.1352C - CUT (b031): Condensed repeated musings and omitted hearsay qualifiers to fit the code cap.
- [ ] rom.1CCC4 - CUT (b035): Shortened titles and repeated names; omitted panting, stammering, hell imagery, repeated urgency and farewell to fit the 255-code cap.
- [ ] rom.27BA0 - CUT (b036): Condensed repeated purchasing instructions and verbal flourishes to fit the code cap.
- [ ] rom.2B134 - CUT (b037): Abbreviated Association to Assoc. to fit the width limit.
- [ ] rom.41168 - CUT (b042): Compressed the Lounge's value as a social gathering place and the invitation to use the door on future visits.
- [ ] rom.41378 - CUT (b042): Omitted the explicit explanation that the Dark Vein is a vein of Dark Power.
- [ ] rom.419B0 - CUT (b042): Compressed the Dark Note standard metaphor and repeated emphasis on the tiny interest charge.
- [ ] rom.4F2B0 - CUT (b049): Condensed greetings, praise and the reference to the magnificent plan to fit the code cap.
- [ ] rom.4F468 - CUT (b049): Condensed the introductory explanation, repeated promotion and location references, and closing invitations to fit the code cap.

## Review minors b019
- [ ] quest.04030 - "行方不明となったゼナを探しだす" means find Zena, who has gone missing - "The missing Zena" sounds unnatural - Find Zena, who has gone missing.
- [ ] quest.04070 - "ビィト戦士団登場" announces the Beet Warriors' arrival - The title drops the arrival - The Beet Warriors Arrive
- [ ] quest.04618 - "アーク戦士団登場" announces Ark's Squad's arrival - "Ark's Squad Here" reads like clipped translationese - Ark's Squad Arrives
- [ ] quest.03FBC - review suggestion blocked by width: line 1: 166 px > 120 (12 px font) 'Infiltrate the Twin Islands'
- [ ] quest.04254 - review suggestion blocked by width: line 1: 156 px > 120 (12 px font) 'Save the Courier Buster'
- [ ] quest.04298 - review suggestion blocked by width: line 1: 142 px > 120 (12 px font) 'Silver Miner Horey-san'
- [ ] quest.04430 - review suggestion blocked by width: line 1: 197 px > 120 (12 px font) 'Reunite with the Beet Warriors'
- [ ] quest.049E4 - review suggestion blocked by width: line 1: 171 px > 120 (12 px font) 'Protect the Bridge Master'
- [ ] quest.04A74 - review suggestion blocked by width: line 1: 169 px > 120 (12 px font) 'Learn a Secret Technique'
- [ ] quest.055B4 - review suggestion blocked by width: line 1: 145 px > 120 (12 px font) 'Silver Goddess Statue'
- [ ] quest.055D8 - review suggestion blocked by width: line 1: 153 px > 120 (12 px font) 'Build the Golden Castle!'

## Review minors b020
- [ ] quest.057D4 - "山門を破れ" means breach the mountain gate - Drops the gate's identifying qualifier retained in the description - Breach the Mountain Gate
- [ ] quest.05ABC - "坑道　暗闇の先に" means the mine tunnel: beyond the darkness - Drops the location from the title - The Mine: Beyond the Darkness
- [ ] quest.05DE0 - "最後の防御線" means the last line of defense - Last Defense Line is an awkward English formulation - The Last Line of Defense
- [ ] quest.05900 - review suggestion blocked by width: line 1: 202 px > 120 (12 px font) 'Ganeer, the Dark Notes Lender'
- [ ] quest.05BE8 - review suggestion blocked by width: line 1: 163 px > 120 (12 px font) 'Capture the Village Chief'
- [ ] quest.05C3C - review suggestion blocked by width: line 1: 167 px > 120 (12 px font) 'Destroy the Sealing Rings'
- [ ] quest.05CA8 - review suggestion blocked by width: line 1: 152 px > 120 (12 px font) 'Orozon, Lord of Dreams'
- [ ] quest.05D38 - review suggestion blocked by width: line 1: 191 px > 120 (12 px font) 'The Flame for the Repair Item'
- [ ] quest.06564 - review suggestion blocked by width: line 1: 135 px > 120 (12 px font) 'Deadly Blade Histario'
- [ ] quest.06594 - review suggestion blocked by width: line 1: 198 px > 120 (12 px font) 'Garonute, the Immovable Giant'
- [ ] quest.06618 - review suggestion blocked by width: line 1: 130 px > 120 (12 px font) 'Monster Lieutenant'
- [ ] quest.06708 - review suggestion blocked by width: line 1: 190 px > 120 (12 px font) 'Giant Butterfly: Even Farther'
- [ ] quest.06750 - review suggestion blocked by width: line 1: 126 px > 120 (12 px font) 'Vandel Scholar Noa'

## Review minors b023
- [ ] rom.04A90 - "何の武器が得意なの？" asks which weapon he is skilled with - "What do you use?" loses the proficiency distinction - {hero}! Off to hunt monsters? Kissu says you're new at this. // To thank you for helping Beet, I'll explain weapons. What weapon are you best with, {hero}? // Swords, spears, guns... There are lots of types. Try the Weapon Shop. // You'll have strengths and weaknesses, {hero}, so some weapons may be off limits. I can't carry axes. Too heavy! Try different ones, okay?
- [ ] rom.05820 - "高価買取キャンペーン中" advertises temporarily generous purchase prices - "buyback sale" sounds like she is selling goods rather than buying them - I'll give ya a good deal, so buy something! I buy stuff, too!! I'm paying top coin right now!!

## Review minors b026
- [ ] rom.0ADA4 - "いつもの夫婦ゲンカ" teasingly calls their familiar bickering a marital spat - "Another married-couple quarrel" sounds stiff and weakens the joke - (Here we go again! Bickering like an old married couple!)
- [ ] rom.0AF20 - "おまえ 二刀流なのか!?" expresses surprise that the hero fights with two weapons - "You use Dual Wielding" sounds like a menu description - Oh... // Whoa!! {hero}, you know Dual Wielding?!
- [ ] rom.09A98 - review suggestion blocked by width: message over 255 codes

## Review minors b021
- [ ] rom.011F4 - review suggestion blocked by width: message over 255 codes

## Review minors b022
- [ ] rom.03294 - "いつもの夫婦ゲンカ" teasingly calls their habitual bickering a marital quarrel - "Their usual married-couple quarrel" sounds stiff and weakens the joke - suggested EN: (They always bicker like an old married couple...)
- [ ] rom.0393C - review suggestion blocked by width: message over 255 codes
- [ ] rom.03B54 - review suggestion blocked by width: message over 255 codes
- [ ] rom.0410C - review suggestion blocked by width: message over 255 codes

## Review minors b024
- [ ] rom.06050 - "たすけて あ げ る": flirtatiously drawn-out offer to help - "A helping... little... hand" sounds awkward and misplaces the teasing emphasis - Let this superheroine of justice, BB Milfa, help... you... out! // Let's see...
- [ ] rom.066A0 - "おそらく": probably; monsters are suspected of stopping the pigeons - "No doubt" overstates the Chief's certainty - A carrier pigeon recently arrived from Mirei Forest Village... // They report that many monsters have begun appearing in Mirei Forest... // Monsters alone would be troubling enough, but something resembling a Vandel has also been sighted... // East Island, too, may be falling into the Vandels' clutches, starting with Mirei Forest... // I wish I knew what has happened since, but no more pigeons have arrived... // Likely the work of monsters... // I fear for Mirei Forest Village, my boy...

## Review minors b025
- [ ] rom.07B00 - review suggestion blocked by width: message over 255 codes
- [ ] rom.08944 - review suggestion blocked by width: message over 255 codes

## Review minors b027
- [ ] rom.0CF48 - "モンスターとは桁違いのプレッシャーじゃん" describes the Vandel's overwhelmingly intimidating presence - "The pressure's on a whole other level from a monster" is a stiff calque - Th-this is bad... So this is a Vandel... // Monsters have nothing on this guy... Talk about intimidating...

## Review minors b028
- [ ] rom.0DD68 - "この島の出身とは心強い" expresses encouragement at meeting a local - "Having someone from this island is reassuring" sounds stiff for Rend - Really!? It's good to have someone who knows this island! Right, Ark-san?
- [ ] rom.0E6CC - "でも・・・それじゃ・・・" means "But... if things stay that way..." - "But... If I..." creates an awkward dangling clause - {hero}... I... // You see... Until now, I've only thought about my own feelings... // But... I can't go on like that, can I...? // Even now... I don't want you to be put in danger... // But... I know... // Nothing will get better if all I do is wait...

## Review minors b030
- [ ] rom.1263C - 「{hero}のお父さんの仇かもしれない」 means he may be the killer of {hero}'s father - "the father of {hero}" is awkwardly impersonal - suggested EN: Beet... The Vandel from the "Golden Castle" might have killed {hero}'s father...
- [ ] rom.12D2C - 「知的に考えたまえ」 tells them to use their intellect - "Think intellectually" is a stiff calque - suggested EN: Are you the one who awakened me? // Apply your intellect... The fact that I emerged from a stone statue means...

## Review minors b031
- [ ] rom.1352C - review suggestion blocked by width: message over 255 codes

## Review minors b032
- [ ] rom.169D8 - review suggestion blocked by width: message over 255 codes
- [ ] rom.16CA8 - review suggestion blocked by width: message over 255 codes
- [ ] rom.17450 - review suggestion blocked by width: message over 255 codes

## Review minors b033
- [ ] rom.19318 - 「命がいくらあっても足りない」 means even countless lives would not be enough - "No number of lives will save you" is a stiff calque that weakens Slade's dry warning - Wander around carelessly and you'll blunder into traps. You'll run out of lives fast...

## Review minors b034
- [ ] rom.1AF34 - "願いが込められた手作りのお守り・・・って" repeats the explanation incredulously: a handmade charm imbued with a wish - "You mean..." awkwardly suggests an unfinished clarification - suggested EN: ... Uh-huh... // A handmade charm with a wish woven into it... You're sayin'...
- [ ] rom.1B5D4 - review suggestion blocked by width: message over 255 codes

## Review minors b035
- [ ] rom.1CCC4 - review suggestion blocked by width: message over 255 codes

## Review minors b036
- [ ] rom.23FEC - "倒れた木を壊した!" means the fallen tree was destroyed - "Broke the fallen tree" sounds unnatural for clearing an obstacle - You smashed the fallen tree!
- [ ] rom.27BA0 - review suggestion blocked by width: message over 255 codes

## Review minors b037
- [ ] rom.2AD18 - "ウッ・・・ グスッ・・・" conveys choked sobbing - "Ugh" suggests disgust or frustration rather than tears - We're just leaving it all to you, {hero}... // Making you do everything dangerous... // If anything happened to you, {hero}... I... I... // *sob*... *sniff*...
- [ ] rom.2B29C - "依頼されていたモンスターを無事に討伐することができた" means successfully defeating the monsters specified in the request - "defeated the monsters for the request" is awkward English - You defeated the monsters specified in the request! Go report to the Appraisal Hut!
- [ ] rom.2B134 - review suggestion blocked by width: line 1: 125 px > 120 (12 px font) 'Buster Association'

## Review minors b038
- [ ] rom.32360 - "見苦しい言い訳はしない" means refusing to make disgraceful excuses for losing - "sully a loss" is an unnatural collocation - I won't disgrace myself by making excuses for losing. That's a gambler's etiquette...
- [ ] rom.325D4 - "この二ッ星の切れ味を味わえ" threatens the opponent with this Two-Star assassin's sharpness - "the cutting edge of this Two-Star" reads as a stiff calque - Gehihyaha! I'm Shaderiko, the "Dark Claw"! // Taste my blades! I'm a Two-Star feared as an assassin!!

## Review minors b041
- [ ] rom.3E4B4 - 「薬草を手に入れた」 means "obtained a medicinal herb" - Missing article makes the notification awkward - Obtained a Medicinal Herb.
- [ ] rom.3E568 - 「アイテムゲット」 labels item acquisition - "Item Get" is unnatural English, even as a debug sound label - Item Obtained

## Review minors b042
- [ ] rom.409E0 - review suggestion blocked by width: message over 255 codes
- [ ] rom.41168 - review suggestion blocked by width: message over 255 codes
- [ ] rom.41378 - review suggestion blocked by width: message over 255 codes
- [ ] rom.419B0 - review suggestion blocked by width: message over 255 codes

## Review minors b043
- [ ] rom.42518 - 島中を黄金に染める: turn the whole island to gold - "These whole islands" is unnatural English - A Vandel's power can destroy a mere "Sealing Ring" in one blow... // You might not even need to strike it... // When you find a "Sealing Ring," just try touching it... // That's all it takes to destroy a "Sealing Ring"!! // Heh heh heh... // I can hardly stand it... // Oh, don't worry... // Even a greenhorn like you can't possibly mess this up... // Go...! Turn every inch of the island to gold, just as I desire!!
- [ ] rom.4330C - 目指す「七ッ星」まではまだまだ遠い道のり: a long road remains to the Seven-Star rank - "Before your goal of Seven-Star" reads awkwardly - Congratulations!! // Though you still have quite a way to go before you reach the rank of "Seven-Star"...!! // Keep up the fine work...! Now, farewell...!! // Oh, yes... These are the Build Ants entrusted to me by Harden-sama. // He ordered them to build a gold mine.

## Review minors b044
- [ ] rom.45344 - Diam boasts that the island's rumors have reached even him, then realizes who he is addressing - "Even I... heard!" is awkwardly incomplete, and the compressed opening loses his suspicious question - Hey! Don't tell me you've come to uncover this island's secret too... // This island's been quite the topic of conversation around the Bekatorte Seas lately... // Naturally, those rumors reached even me, "Steel Claw" Diam-sama, the strongest in the Bekatorte Seas... // If the "Greedy Overlord" himself has come here, there must be something to it... // They say he's brought an underling with conspicuously long horns... // ...!! // Oh, no! Those horns! Don't tell me...! I let that slip! // No matter... I'll just have to silence you! // SEYAAAAAA!!
- [ ] rom.44EEC - review suggestion blocked by width: message over 255 codes

## Review minors b045
- [ ] rom.46E34 - "このあたいが キャーだって" expresses disbelief that she herself screamed - "Like a little girl" adds a disparaging comparison absent from the Japanese - Haha... Seriously? Me, screaming like that...? This is really bad... // {hero}... I don't think I'm gonna make it...

## Review minors b046
- [ ] rom.49564 - "ふざけるな" means "Don't give me that!" - "Don't you dare" suggests a warning rather than defiant rejection of the question - D-don't give me that...!

## Review minors b047
- [ ] rom.49E64 - review suggestion blocked by width: message over 255 codes

## Review minors b048
- [ ] rom.4C7E4 - review suggestion blocked by width: message over 255 codes

## Review minors b049
- [ ] rom.4F2B0 - review suggestion blocked by width: message over 255 codes
- [ ] rom.4F468 - review suggestion blocked by width: message over 255 codes

## Review minors b050
- [ ] rom.4FD60 - "長らく販売を中止しており ご迷惑をおかけしていた" apologizes for the prolonged suspension of sales - "Sorry for the long wait!" and the subsequent fragments make Shagie's sales pitch noticeably brusquer than neighboring dialogue - suggested EN: We apologize for the prolonged inconvenience, but "Hoverfish" are now back on sale at the Vandel House! // Although their stops are limited, they allow you to travel long distances far faster than on foot...! // Here on the Twin Islands, for instance... Yes, you can travel from the Golden Castle to Rinnam Glacier...! // They are a little costly, but do consider purchasing one...! // Tarotos awaits you at the Vandel House with lively "Hoverfish" ready for sale...! // Please do make use of our services...! // Was that explanation clear?
- [ ] rom.503EC - "ぜひお買い求めくださいませ" courteously urges a purchase - "A little pricier ... but do buy one!" sounds blunt; restoring the courteous sales language would better match Shagie's other announcements - suggested EN: We apologize for the prolonged inconvenience, but the "Giant Butterfly" is now back on sale at the Vandel House! // Although its stops are limited, it allows you to travel long distances far faster even than a "Hoverfish"...! // Here on the Twin Islands, for instance... Yes, you can travel from the Golden Castle to Zeros Snowfield...! // It is a little more costly than a "Hoverfish," but do consider purchasing one...! // Tarotos awaits you at the Vandel House with a lively "Giant Butterfly" ready for sale...! // Please do make use of our services...! // Was that explanation clear?
- [ ] rom.4F8C8 - review suggestion blocked by width: message over 255 codes
