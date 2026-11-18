# Glossary - Bouken-ou Beet: Vandel vs. Busters (NDS)

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py` reads the table rows (`| JP | EN | max | notes | Avoid |`; `a/b` in JP = variants) and warns when
a batch line has the JP term without the EN form.

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated, only where the Japanese has them (-san, -kun, -chan, -sama, sensei). Name order:
  Western (D1).
- Romanisation source: official English (Viz manga / English anime) where it exists, else readable Hepburn without
  macrons (D2). Game-original names are marked in the notes.
- Credits: English (D3).
- Register / flavour: shonen adventure, kid-friendly but lively; villains comic and theatrical; voices per
  docs/synopsis.md "Cast and voice guide". Sound effects: English words in asterisks (*sniff*, *chomp*).
- Abbreviations: none; engine work first, abbreviate only as a flagged last resort (D4).

## Style rules
- Punctuation map: 「」 -> "...", 『』 -> '...' (or "..." standing alone), ・・・/… -> ..., ！？ -> !?, ー/〜 stretch ->
  repeated letters ("Heeey"), full-width letters -> ASCII. Plain ASCII only.
- Laughs keep their shape: クックックッ -> "Heh heh heh...", ガーッハッハッ -> "Gwahahaha!", ウフフ -> "Ufufu",
  クフフ -> "Kufufu", ヘッヘッヘッ -> "Heh heh heh", ゲヒヒ -> "Gehehe".
- Player name codes `{hero}` / `{vandel}`: no suffix glued on, no a/an before.
- Dialogue is written as prose; `tools/batches.py` wraps it (240 px x 3 lines per page). ` // ` marks a page break.
- Table names (items, weapons, monsters, skills): English game names; katakana loanwords become the English word.

## Terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ビィト | Beet |  | Person: Fixed. |  |
| ポアラ | Poala |  | Person: Fixed. |  |
| キッス | Kissu |  | Person: Fixed. |  |
| スレッド | Slade |  | Person: Fixed; never "Thread." |  |
| ミルファ | Milfa |  | Person: Fixed. |  |
| ゼノン | Zenon |  | Person: Mentioned through his party. |  |
| レナ | Lena |  | Person: Elder twin. |  |
| ゼナ | Zena |  | Person: Younger twin; distinct from Zenon. |  |
| ハーデン | Harden |  | Person: Gold-obsessed ruler. |  |
| ホーレイ | Horey |  | Person: Readable romanization; retain in password. |  |
| ガントリィ | Gantry |  | Person: Natural name rendering. |  |
| アーク | Ark |  | Person: Party leader. |  |
| レンド | Rend |  | Person: Ark's companion. |  |
| シグサ | Shigusa |  | Person: Ark's companion. |  |
| グレスト | Grest |  | Person: Reformed rogue. |  |
| バドゥ | Badu |  | Person: Grest's companion. |  |
| ジーク | Zeke |  | Person: Readable name rendering. |  |
| リュック | Ryuk |  | Person: Avoid translating as "backpack." |  |
| ナック | Nack |  | Person: Zeke's companion. |  |
| ゴラン | Goran |  | Person: Mercenary. |  |
| シバ | Shiba |  | Person: Mercenary. |  |
| シャギー | Shagie |  | Person: Fixed. |  |
| グリニデ | Grineed |  | Person: Fixed. |  |
| グリニデ２ | Grineed - Transformed |  | Debug label: Same character, not another person. |  |
| ベルトーゼ | Beltorze |  | Person: Fixed; portrait-test occurrence here. |  |
| ガロニュート | Garonute |  | Person: Fixed. |  |
| ベンチュラ | Ventura |  | Person: game-original or unconfirmed spelling. Effigy and debug dialogue. |  |
| フラウスキー | Frausky |  | Person: game-original or unconfirmed spelling. Effigy. |  |
| ロズゴート | Rozgoat |  | Person: game-original or unconfirmed spelling. Effigy. |  |
| ムガイン | Mugain |  | Person: game-original or unconfirmed spelling. Effigy in optional event. |  |
| バレアス | Baleas |  | Person: game-original or unconfirmed spelling. Metal-eating Vandel. |  |
| ディアム | Diam |  | Person: game-original or unconfirmed spelling. Steel Claw. |  |
| エルダー | Elder |  | Person: game-original or unconfirmed spelling. Steel Horn. |  |
| ガネール | Ganeer |  | Person: game-original or unconfirmed spelling. Moneylender. |  |
| バロン | Baron |  | Person: game-original or unconfirmed spelling. Sky King. |  |
| ヒスタリオ | Histario |  | Person: game-original or unconfirmed spelling. Silent musician here. |  |
| ロディーナ | Rodina |  | Person: game-original or unconfirmed spelling. Elegant Vandel visitor. |  |
| ノア | Noa |  | Person: game-original or unconfirmed spelling. Researcher. |  |
| メルマーデ | Melmade |  | Person: game-original or unconfirmed spelling. Sends Ark's party; does not speak. |  |
| ギルス | Gils |  | Person: Fire-associated Vandel. |  |
| ザンデ | Zande |  | Person: Lightning-associated Vandel. |  |
| メルモンド | Melmond |  | Person: Saiga collector. |  |
| オロゾン | Orozon |  | Person: Sleep/mental-attack specialist. |  |
| ヤギール | Yagil |  | Person: Debt collector and recruit. |  |
| キャンバル | Canbal |  | Person: Gambler; preserve name separately from epithet. |  |
| ピルゴア/ビルゴア | Pilgoa |  | Person: Recruitment uses ピ; debug portraits use ビ. Provisional normalization. |  |
| ブランドゥ | Brandu |  | Person: Recruitable Vandel. |  |
| グラニャオース | Granyaos |  | Person: Recruitable Vandel. |  |
| レボーク/レボーグ | Revok |  | Person: Recruitment/debug spelling discrepancy; provisional normalization. |  |
| ライリー | Riley |  | Person: Recruitable Vandel. |  |
| シャデリコ | Shaderiko |  | Person: Two-star assassin. |  |
| タロトス/タナトス | Tarotos |  | Person: Live service text uses タロトス; portrait test uses タナトス. Do not assume "Thanatos" without confirmation. |  |
| シャギーガール | Shagie Girl |  | Role/name: House hostess; preserve link to Shagie. |  |
| ヒーロー | Hero |  | Placeholder: Demo speaker label; not a separate named character. |  |
| ？？？？ | ???? |  | Speaker label: Concealed identity. |  |
| 強欲君主 | Greedy Overlord |  | Epithet: Harden; proposed rendering. |  |
| 地獄の稲妻 | Hell's Lightning |  | Epithet: Zande. |  |
| 銀色の魔手 | Silver Hand |  | Epithet: Melmond; "Hand" keeps it short. |  |
| 赤熱の烈火 | Blazing Inferno |  | Epithet: Gils. |  |
| 鋼鉄の爪 | Steel Claw |  | Epithet: game-original or unconfirmed spelling. Diam. |  |
| 鋼鉄の牙 | Steel Fang |  | Epithet: game-original or unconfirmed spelling. Baleas. |  |
| 鋼鉄の角 | Steel Horn |  | Epithet: game-original or unconfirmed spelling. Elder. |  |
| 夢幻の覇者 | Lord of Dreams |  | Epithet: Orozon. |  |
| 金色の博徒 | Golden Gambler |  | Epithet: Canbal. |  |
| 闇の爪 | Dark Claw |  | Epithet: Shaderiko. |  |
| 天空王 | Sky King |  | Epithet: game-original or unconfirmed spelling. Baron. |  |
| 凶刃 | Deadly Blade |  | Epithet: game-original or unconfirmed spelling. Histario. |  |
| 不動巨人 | Immovable Giant |  | Epithet: game-original or unconfirmed spelling. Garonute. |  |
| 魔人博士 | Vandel Scholar |  | Epithet: game-original or unconfirmed spelling. Noa; avoids implying a medical doctor. |  |
| 小悪魔 | Little Devil |  | Epithet: game-original or unconfirmed spelling. Rodina; flirtatious double meaning. |  |
| 暗黒の世紀の催促人 | Debt Collector of the Dark Century |  | Epithet: game-original or unconfirmed spelling. Ganeer's elaborate self-introduction. |  |
| フォージェミニ島 | Forjemini Island |  | Place: Proposed formal name. |  |
| 双子島 | Twin Islands |  | Place: Common name for the same two-island territory. |  |
| 東の島/東方の島 | East Island |  | Place: Directional island designation. |  |
| 西の島/西方の島 | West Island |  | Place: Directional island designation. |  |
| 東の里 | East Village |  | Place: Hero's home and principal Buster hub. |  |
| 西の里/西の女神像の里 | West Village |  | Place: Destroyed village beneath the Golden Castle. |  |
| 謁見の間 | Audience Hall |  | Place: Castle confrontation area. |  |
| 城主の間 | Lord's Chamber |  | Place: Keep distinct from Audience Hall. |  |
| ナッシュ平原 | Nash Plains |  | Place: Near East Village. |  |
| バコソン山地 | Bakoson Mountains |  | Place: Early hunting area. |  |
| ダチャレイ洞窟 | Dacharei Cave |  | Place: Outer cave area. |  |
| ダチャレイ坑道 | Dacharei Mine |  | Place: Deeper workings where Horey hides; distinct from cave. |  |
| ミレイの森 | Mirei Forest |  | Place: Forest region. |  |
| ミレイ森の里 | Mirei Forest Village |  | Place: Destroyed village. |  |
| ビム砂漠 | Bim Desert |  | Place: Sandstorms require goggles. |  |
| ビム砂漠の塔 | Bim Desert Tower |  | Place: Near the chief's false cache location. |  |
| ゼロス雪原/ゼロセス雪原 | Zeros Snowfield |  | Place: ゼロセス is an isolated variant; normalize provisionally. |  |
| ルブレイ湖 | Rubrei Lake |  | Place: Aqua Dog assignment. |  |
| ソーレ谷 | Sole Valley |  | Place: Valley region. |  |
| ソーレ谷の迷宮 | Sole Valley Labyrinth |  | Place: Optional encounters and rare-monster hints. |  |
| ベヌル荒野 | Benuru Wastes |  | Place: Gathering/hunting area. |  |
| パセロ湿地/パセロ湿原 | Pasero Marsh |  | Place: Treat as wording variants of one region. |  |
| ミュテリン山地 | Muterin Mountains |  | Place: Western region. |  |
| ミュテリン山の里/ミュテリン里 | Muterin Mountain Village |  | Place: Converted into forced-labor mine. |  |
| リンブロ平原 | Rinburo Plains |  | Place: Castle approach/bridge assignment. |  |
| ノルナージの森 | Norunaji Forest |  | Place: Western region. |  |
| リンラーゴ山地 | Rinrago Mountains |  | Place: Do not merge with Rinnam Glacier. |  |
| リンナム氷河 | Rinnam Glacier |  | Place: Transport destination. |  |
| オーラン洞窟 | Oran Cave |  | Place: Distinct map name from mine. |  |
| オーラン坑道 | Oran Mine |  | Place: Resistance hideout, ambush and aircraft. |  |
| リーベリン湖 | Riberin Lake |  | Place: Lake containing a hideout tower. |  |
| リーベリン湖の塔 | Riberin Lake Tower |  | Place: Resistance hideout. |  |
| ビョンリン火山/ピョンリン火山 | Byonrin Volcano |  | Place: Main spelling uses ビョ; flight dialogue uses ピョ. Normalize provisionally. |  |
| ビョンリン火山の遺跡/ピョンリン火山の遺跡 | Byonrin Ruins |  | Place: Hideout and aircraft destination. |  |
| 地底湖 | Underground Lake |  | Place: Chalice quest chain. |  |
| ベカトルテ | Bekatorte |  | Place: game-original or unconfirmed spelling. Nearby territory; official spelling uncertain. |  |
| ベカトルテ近海 | Bekatorte Seas |  | Place: game-original or unconfirmed spelling. Waters surrounding Bekatorte. |  |
| トロワナ | Torowana |  | Place: game-original or unconfirmed spelling. Bridge Master's earlier work. |  |
| アサド山地 | Asado Mountains |  | Place: game-original or unconfirmed spelling. Mountains in Torowana. |  |
| グランシスタ王国 | Kingdom of Gransista |  | Place/state: game-original or unconfirmed spelling. Founded the Buster Association. |  |
| ヴァンデル/魔人 | Vandel |  | Species: Fixed; 魔人 is often an alternate reference, not a separate species. |  |
| バスター | Buster |  | Profession: Fixed. |  |
| ヴァンデルバスター | Vandel Buster |  | Profession: Full form. |  |
| バスター協会 | Buster Association |  | Organization: Supports Busters through appraisal facilities. |  |
| 戦士団 | Buster Squad |  | Group/system: game-original or unconfirmed spelling. Party formation; use consistently in group names. |  |
| ゼノン戦士団 | Zenon Warriors |  | Group: Established franchise group name. |  |
| ビィト戦士団 | Beet Warriors |  | Group: Beet, Poala and Kissu here. |  |
| アーク戦士団 | Ark's Squad |  | Group: Ark, Rend, Shigusa. |  |
| ジーク戦士団 | Zeke's Squad |  | Group: Zeke, Ryuk, Nack. |  |
| レジスタンス | Resistance |  | Group: Civilian survivors opposing the occupation. |  |
| レジスタンスＡ～Ｌ | Resistance A-L |  | Speaker labels: Internal distinctions; avoid inventing personal names. |  |
| 鑑定士 | Appraiser |  | Role: Current mentor or murdered predecessor according to context. |  |
| 鑑定小屋 | Appraisal Hut |  | Facility: Quest acceptance, reporting and advancement. |  |
| 里長 | Village Chief |  | Role: Normally East Village's chief unless qualified. |  |
| ミレイ森の里長 | Mirei Forest Chief |  | Role: East Chief's younger brother. |  |
| ミュテリン山の里長 | Muterin Village Chief |  | Role: Reported dead. |  |
| 銀掘り職人/銀堀職人 | Silver Miner |  | Role: JP spelling variation; Horey's profession. |  |
| 橋かけ名人 | Bridge Master |  | Role/name: Recurring character's title, not a personal name. |  |
| 名人 | Master |  | Address: Bridge Master's preferred shortened title. |  |
| 橋かけ名ちゃん/名ちゃん | Bridgey |  | Nickname: Horey's affectionate nickname; localization proposal. |  |
| ホーレイちゃん | Old Horey |  | Address: Friendly affection between craftsmen; not a child. |  |
| 伝達兵 | Messenger |  | Role: More than one messenger appears; do not assume the dead one returns. |  |
| 配達バスター | Courier Buster |  | Role: Quest wording differs from dialogue's Messenger. |  |
| 船長 | Captain |  | Role: Opening ship. |  |
| 船員 | Sailor |  | Role: More than one generic sailor may share label. |  |
| 犬 | Dog |  | Speaker label: Animal sounds. |  |
| 酒場の女 | Tavern Woman |  | Role: No personal name. |  |
| 武器屋 | Weapon Shop |  | Facility/role: "Weaponsmith" when the speaking proprietor is intended. |  |
| 防具屋 | Armor Shop |  | Facility: Shop category. |  |
| 道具屋/アイテムやさん | Item Shop |  | Facility/role: "Item seller" in prose when needed. |  |
| 酒場 | Tavern |  | Facility: Recruitment hub. |  |
| 魔賓館 | Vandel House |  | Facility: game-original or unconfirmed spelling. Proposed franchise rendering; monster sales and social hub. |  |
| 館長 | Manager |  | Role: Shagie's title. |  |
| 管理官 | Administrator |  | Role: Tarotos's position. |  |
| 総合受付 | Reception |  | Facility/UI: Main service desk. |  |
| 談話スペース | Lounge |  | Facility: Vandel social area. |  |
| 暗黒の世紀 | Dark Century |  | World term: Age of Vandel domination. |  |
| 銀の女神像 | Silver Goddess Statue |  | Sacred object: Two major seals; separate from eighteen field rings. |  |
| 聖なる銀/聖なる銀ホーリーシルバー | Holy Silver |  | Material: Raw material; not usable directly for repairs. |  |
| 聖なる炎 | Sacred Flame |  | Sacred power: Lena tends it. |  |
| 聖なる銀のしずく | Holy Silver Drops |  | Key item: One unit per repaired ring. |  |
| シルバーチャーム | Silver Charm |  | Key item: Lena's handmade protective charm. |  |
| ランプ | Lamp |  | Key item: Lena's silver lamp; mine lighting and ritual vessel. |  |
| ゴーグル | Goggles |  | Key item: Sandstorm traversal; also gifted to Grest/Badu. |  |
| 東の里の里長への手紙 | Letter to the East Chief |  | Key item: Dying messenger's letter. |  |
| ゼナへの薬草 | Herbs for Zena |  | Key item: Delivery item; distinct from ordinary herb inventory. |  |
| ゼナ体力丸 | Zena's Vitality Pill |  | Key item: Return gift before the ordinary pill reward. |  |
| ホーレイさんの手紙 | Horey's Letter |  | Key item: Craftsmen's correspondence. |  |
| 橋かけ名人の手紙 | Bridge Master's Letter |  | Key item: Reply. |  |
| するどく光る銀 | Keen Silver |  | Material: Proposed short name; description links its sheen to a sharp blade. |  |
| 銀の剣 | Silver Sword |  | Weapon: Forged from Keen Silver. |  |
| 角を大きくする薬 | Horn Growth Tonic |  | Key item: Ineffective vanity medicine. |  |
| 背を高くする薬 | Height Tonic |  | Key item: Another ineffective medicine. |  |
| ホーリーシルバーホーレイホーレイ | Holy Silver, Horey, Horey |  | Password: Correct phrase; keep its repetitive joke. |  |
| ホーリーホーレイホーリーホーリー | Holy Horey, Holy, Holy |  | Password: Incorrect choice; must remain distinguishable. |  |
| ペンダント | Pendant |  | Story object: Appraiser's keepsake. |  |
| バンダナ | Bandanna |  | Story object: Hero's keepsake; emblem matters to late reveal. |  |
| ベカトルテ鋼 | Bekatorte Steel |  | Material: game-original or unconfirmed spelling. Refining-request material. |  |
| 樹の杯 | Tree Chalice |  | Quest object: 地底湖 chain. |  |
| 絶の杯 | Severance Chalice |  | Quest object: Meaning provisional; 絶 lacks explanatory context. |  |
| 沼の杯 | Marsh Chalice |  | Quest object: Same chain. |  |
| 窟の杯 | Cavern Chalice |  | Quest object: Same chain. |  |
| 渦の杯 | Whirlpool Chalice |  | Quest object: Same chain. |  |
| 砂の杯 | Sand Chalice |  | Quest object: Same chain. |  |
| 地の杯 | Earth Chalice |  | Quest object: Same chain. |  |
| 鉱の杯 | Ore Chalice |  | Quest object: Same chain. |  |
| 極の杯 | Ultimate Chalice |  | Quest object: Meaning provisional; do not assume polar geography. |  |
| 骨の杯 | Bone Chalice |  | Quest object: Appears under an unrelated delivery heading. |  |
| 才牙/サイガ | Saiga |  | Combat term: Fixed franchise term; manifested personal weapon. |  |
| 天力 | Divine Power |  | Energy/stat: game-original or unconfirmed spelling. Source energy for Buster abilities. |  |
| 天撃 | Divine Attack |  | Combat term: game-original or unconfirmed spelling. Technique, distinct from its energy source. |  |
| 冥力 | Dark Power |  | Energy/stat: game-original or unconfirmed spelling. Vandel energy and recovery resource. |  |
| 冥撃 | Dark Attack |  | Combat term: game-original or unconfirmed spelling. Vandel technique. |  |
| 精神冥撃 | Mental Dark Attack |  | Combat term: game-original or unconfirmed spelling. Orozon's sleep/manipulation techniques. |  |
| 冥脈 | Dark Vein |  | World term: Underground concentrations of Dark Power. |  |
| ライボルトグラスパー | Lightning Bolt Grasper |  | Saiga: game-original or unconfirmed spelling. Milfa's named weapon. |  |
| レッドヴァンソード | Red Van Sword |  | Saiga: game-original or unconfirmed spelling. Grest's named weapon; spelling uncertain. |  |
| 奥義 | Secret Technique |  | Combat term: Quest label; no particular named technique supplied. |  |
| 星 | Star |  | Rank: Vandel rank marks on the left arm. |  |
| 一ツ星/一ッ星 | One-Star |  | Rank: Initial Vandel rank. |  |
| 二ツ星/二ッ星 | Two-Star |  | Rank: Normalize orthographic variants. |  |
| 三ッ星 | Three-Star |  | Rank: Same rank system. |  |
| 四ッ星 | Four-Star |  | Rank: Same rank system. |  |
| 五ッ星 | Five-Star |  | Rank: Same rank system. |  |
| 六ツ星/六ッ星 | Six-Star |  | Rank: Harden's rank. |  |
| 七ツ星/七ッ星 | Seven-Star |  | Rank: Highest ordinary rank described here. |  |
| 八輝星 | Eight Shining Stars |  | Elite designation: game-original or unconfirmed spelling. Do not render simply "eight-star rank." |  |
| マギー | Maggy |  | Currency: game-original or unconfirmed spelling. Human currency. |  |
| 魔札 | Dark Notes |  | Currency object: game-original or unconfirmed spelling. Vandel money; denominated in Beil. |  |
| ベイル | Beil |  | Currency unit: game-original or unconfirmed spelling. Distinct from Maggy. |  |
| 二刀流 | Dual Wielding |  | Combat term: Beet admires the hero's technique. |  |
| ガブリ貝 | Snapclam |  | Monster: game-original or unconfirmed spelling. Opening and beach enemies. |  |
| ガブちゃん | Snappies |  | Monster nickname: Harden's cutesy nickname, apparently for Snapclams. |  |
| コダマンボ | Kodamanbo |  | Monster: game-original or unconfirmed spelling. Unexpected plains appearance signals increased Dark Power. |  |
| カネック | Kaneck |  | Monster: game-original or unconfirmed spelling. Eats coins. |  |
| 氷の導師 | Ice Adept |  | Monster: game-original or unconfirmed spelling. Actual identity behind "snowman" rumor. |  |
| アクアドッグ | Aqua Dog |  | Monster: game-original or unconfirmed spelling. Lake assignment. |  |
| 赤銅巨人 | Copper Giant |  | Monster: game-original or unconfirmed spelling. Five required for bridge safety. |  |
| ドローマン | Droman |  | Monster: game-original or unconfirmed spelling. Shapeshifter; fears fire. |  |
| グルメアント | Gourmet Ant |  | Monster: game-original or unconfirmed spelling. Eating function; distinct from builders. |  |
| ビルドアント | Build Ant |  | Monster: game-original or unconfirmed spelling. Builds castle/mining facilities. |  |
| 夢魔 | Nightmare |  | Monster: game-original or unconfirmed spelling. Harden's reward; do not assume a specific gendered demon. |  |
| ホバーフィッシュ | Hoverfish |  | Transport monster: game-original or unconfirmed spelling. Limited landing points. |  |
| 大怪蝶 | Giant Butterfly |  | Transport monster: game-original or unconfirmed spelling. Faster, more expensive transport. |  |
| アイアンライノス | Iron Rhino |  | Monster: game-original or unconfirmed spelling. Garonute's first dropped reward. |  |
| 火山の翼竜 | Volcanic Pterosaur |  | Monster: game-original or unconfirmed spelling. Garonute's later reward. |  |
| 突然変異 | Mutation |  | Monster term: Noa distinguishes mutation from going feral. |  |
| 薬草 | Medicinal Herb |  | Item: Ordinary healing item; distinct from flowers. |  |
| 体力丸 | Vitality Pill |  | Item: Keep consistent with Zena's named gift. |  |
| 天力丸 | Divine Pill |  | Item: Proposed short name tied to Divine Power. |  |
| 治療薬 | Healing Medicine |  | Item: Exact effect not specified here. |  |
| 万能薬 | Panacea |  | Item: Generic all-purpose remedy name. |  |
| 解毒剤 | Antidote |  | Item: Poison remedy. |  |
| しびれ取り | Paralysis Remedy |  | Item: Status remedy. |  |
| 気付け剤 | Smelling Salts |  | Item: Do not infer revival mechanics solely from name. |  |
| 栄養剤 | Nutrient Tonic |  | Item: Exact effect unspecified. |  |
| ハーブティー | Herbal Tea |  | Item: Consumable. |  |
| ホットジェル | Hot Gel |  | Item: Keep distinct from Cool Gel. |  |
| クールジェル | Cool Gel |  | Item: Consumable. |  |
| 里のおばばの秘薬 | Granny's Elixir |  | Item: Gift from the Appraiser and loot item. |  |
| おじぃの妙薬 | Grandpa's Remedy |  | Item: Separate from Granny's Elixir. |  |
| イモリの黒焼き | Charred Newt |  | Item: Traditional-medicine imagery. |  |
| イモリの干物 | Dried Newt |  | Item: Separate item. |  |
| トラキラの葉 | Torakira Leaf |  | Item: Plant name romanized; no effect inferred. |  |
| バグ | Bug |  | Item: Vandel consumable family, not a software defect here. |  |
| ベターバグ | Better Bug |  | Item: Preserve tier distinction pending item data. |  |
| リカバーバグ/リカバリーバグ | Recovery Bug |  | Item: Likely naming variant; normalize provisionally. |  |
| マックスバグ | Max Bug |  | Item: Same family. |  |
| ワーム | Worm |  | Item: Vandel consumable family. |  |
| ベターワーム | Better Worm |  | Item: Same family. |  |
| リカバーワーム | Recovery Worm |  | Item: Same family. |  |
| マックスワーム | Max Worm |  | Item: Same family. |  |
| スコルピオ | Scorpio |  | Item: Vandel consumable family. |  |
| ライズスコルピオ | Rise Scorpio |  | Item: Preserve label without guessing effect. |  |
| リターンスコルピオ | Return Scorpio |  | Item: Same family. |  |
| マックススコルピオ | Max Scorpio |  | Item: Same family. |  |
| ポイズンビー | Poison Bee |  | Item: Named insect item; exact use not explained here. |  |
| コンフューズビー | Confusion Bee |  | Item: Same family. |  |
| パラライズビー | Paralysis Bee |  | Item: Same family. |  |
| アイスビー | Ice Bee |  | Item: Same family. |  |
| ファイアビー | Fire Bee |  | Item: Same family. |  |
| マスターカタナ | Master Katana |  | Equipment: Preserve distinction from other swords. |  |
| マスターグレイブ | Master Glaive |  | Equipment: グレイブ interpreted as weapon "glaive." |  |
| マスタークロー | Master Claw |  | Equipment: Loot label. |  |
| マスターサークル | Master Circle |  | Equipment: Do not assume "chakram" without item evidence. |  |
| マスターナイフ | Master Knife |  | Equipment: Loot label. |  |
| マスターブレイド | Master Blade |  | Equipment: Separate from Master Sword. |  |
| マスターボウ | Master Bow |  | Equipment: Loot label. |  |
| マスターソード | Master Sword |  | Equipment: Loot label. |  |
| マスターハンマー | Master Hammer |  | Equipment: Loot label. |  |
| マスターボール | Master Ball |  | Equipment: Literal equipment label; no unrelated franchise implication. |  |
| マスタースピア | Master Spear |  | Equipment: Loot label. |  |
| マスターアックス | Master Axe |  | Equipment: Loot label. |  |
| マスターシールド | Master Shield |  | Equipment: Loot label. |  |
| アトスシールド | Atos Shield |  | Equipment: Proper-name spelling provisional. |  |
| マスターバンダナ | Master Bandanna |  | Equipment: Distinct from narrative keepsake. |  |
| マスターカフス | Master Cuffs |  | Equipment: Loot label. |  |
| マスターバングル | Master Bangle |  | Equipment: Loot label. |  |
| マスターグローブ | Master Gloves |  | Equipment: Natural English plural. |  |
| マスターマント | Master Cape |  | Equipment: Loot label. |  |
| マスタージャケット | Master Jacket |  | Equipment: Loot label. |  |
| マスターシャツ | Master Shirt |  | Equipment: Loot label. |  |
| 飛行機 | Airplane |  | Transport: Gantry's aircraft. |  |

## Guidance (not binding: common words with a usual rendering)

- 冒険王ビィト -> Beet the Vandel Buster (Series). Established English title.
- 冒険王ビィト ヴァンデルVSバスターズ -> Beet the Vandel Buster: Vandel vs. Busters (Game title). Proposed English game title using the established series title.
- ベカトルテ近海最強の魔人 -> Strongest Vandel in the Bekatorte Seas (Boast/title). Several rivals claim this; do not treat each claim as objective fact.
- 地底湖の門/なぞの門 -> Underground Lake Gate / Mysterious Gate (Place/object). Discovery descriptions; no unique proper name supplied.
- ブロードバスター/ＢＢ -> Broad Buster / BB (Rank/profession). Milfa's special designation; dialogue says minimum level 40.
- 民兵/民兵Ａ～Ｅ -> Militia / Militia A-E (Role). Civilian defenders.
- 父親/母親 -> Father / Mother (Role). "Dad/Mom" in the hero's direct address as appropriate.
- おじさん/おにいさん -> Man / Young Man (Role). Generic village labels, not established relatives.
- 老婆/里のおばば -> Old Woman / Village Granny (Role). Avoid assuming all references identify the same NPC without evidence.
- 地脈の扉 -> Earthvein Gate (Travel system). Portal to Vandel House; distinguish 地脈 from 冥脈.
- 双子の女神 -> Twin Goddesses (Religious term). The paired goddesses/statues.
- 封印のリング/リング -> Sealing Ring / Ring (Sacred object/system). Silver when restored; gold when broken.
- 銀の台座 -> Silver Pedestal (Object). Supports field rings.
- カギ１/２/３/４/５ -> Key 1 / 2 / 3 / 4 / 5 (Key items). Five aircraft-chain keys; retain numbering.
- 紋章 -> Emblem (Story term). Matching design reveals the killer.
- 金/黄金/銀/砂金 -> Gold / Gold / Silver / Gold Dust (Materials). Preserve Harden's gold-versus-silver obsession.
- 鉱石 -> Ore (Quest item). Do not replace every occurrence with finished steel.
- 薬花 -> Medicinal Flower (Quest item). Distinct from 薬草.
- 才牙の真髄 -> Essence of Saiga (Quest/concept). Avoid inventing an ability name from the heading.
- 属性 -> Element (System). Five elements on each side.
- 火/水/風/雷/光/魔 -> Fire / Water / Wind / Lightning / Light / Dark (Elements). Busters use Light; Vandels use Dark as fifth element.
- ブランディング -> Branding (System/lore). Enables Buster power use.
- 網膜鑑定 -> Retinal Appraisal (System/lore). Verification preceding rewards/advancement.
- 報奨金/報酬 -> Bounty / Reward (System). Distinguish specific bounties from general rewards.
- 昇格値 -> Advancement Points (System). Keep separate from currency and level.
- レベル -> Level (System). Buster progression.
- 二つ名 -> Epithet (Naming system). Player chooses one; separate from personal name.
- 魔札本位制 -> Dark-Note Standard (Economic joke). Ganeer's money-is-everything rhetoric.
- 利子/借金/返済 -> Interest / Debt / Repayment (System/event). Moneylender branch vocabulary.
- 契約金 -> Hiring Fee (Recruitment system). Goran/Shiba charge 10,000 Maggy each.
- 体力 -> HP (Stat). "Health" in natural dialogue.
- 熟練度/武器の熟練度 -> Proficiency / Weapon Proficiency (System). Weapon practice enables Saiga development.
- 装備/武器/防具 -> Equip / Weapon / Armor (System). Possession alone does not equip an item.
- 大剣/片手剣 -> Greatsword / One-Handed Sword (Weapon classes). Distinct categories in generic recruits.
- 槍/斧/銃 -> Spear / Axe / Gun (Weapon classes). Match recruitment and tutorial text.
- 格闘/投剣 -> Unarmed / Throwing Blade (Weapon classes). Proposed compact class labels.
- 仲間 -> Ally (Recruitment system). "Recruit" as a verb; party member in context.
- 配下/部下 -> Minion / Subordinate (Vandel system). Do not imply friendship.
- 軍団 -> Army (Vandel system). Up to five members per described formation.
- 軍団の派遣 -> Dispatch Army (Vandel system). Autonomous attacks on other fronts.
- リーダー -> Leader (Party system). Vandel or promoted lieutenant monster.
- 腹心モンスター -> Lieutenant Monster (Vandel system). Promoted monster granted human speech; may lead monsters, not Vandels.
- 腹心モンスター化 -> Promote to Lieutenant (Vandel system). Service/action label.
- モンスター取り込み/モンスター取込 -> Monster Absorption (Vandel system). Can raise or lower stats and grant Dark Attacks.
- 頭/胴/右腕/左腕/右足/左足 -> Head / Torso / Right Arm / Left Arm / Right Leg / Left Leg (Absorption slots). Preserve all six distinctions.
- 石像トラップ -> Statue Trap (Trap system). Seven types stated; destroyed when defeated.
- 肖像/肖像のトラップ -> Effigy / Effigy Trap (Trap/lore). Reproduction, not original resurrected character.
- ワナ/トラップ -> Trap (System). Same generic concept.
- 定期収入 -> Regular Income (Vandel system). Shagie's payments vary with achievements.
- モンスター/魔物 -> Monster (Creature class). Usually ordinary creatures distinct from Vandels.
- 雪男 -> Yeti (Rumored monster). Misidentification, not a separate confirmed species here.
- ヌシ -> Lake Guardian (Rumored creature). Descriptive title, not established species name.
- レアモンスター -> Rare Monster (System). Several hints; species often left unnamed.
- 船/小型ボート -> Ship / Small Boat (Transport). Distinguish opening vessel from evacuation boat.
- 着岸ポイント/着陸ポイント -> Docking Point / Landing Point (Travel system). Keep aquatic and aerial wording appropriate.
- 里の門 -> Village Gate (Object/speaker). Sentient defender; dialogue is not merely a sign.
- 山門 -> Mountain Gate (Object). Quest heading; no need to imply a temple.
- バリケード -> Barricade (Obstacle). Distinct from living gate.
- 倒れた木/氷柱/壁 -> Fallen Tree / Ice Pillar / Wall (Obstacles). Saiga can destroy specified versions.
- スイッチ -> Switch (Field object). Bridge mechanism.
- 宝箱 -> Treasure Chest (Field object). Includes empty/inventory-full states.
- 薬水の噴水 -> Healing Fountain (Recovery object). Restores HP and Divine Power.
- 冥力が噴出している -> Dark Power Wells Up (Recovery prompt). Restores HP and Dark Power; not a confirmed named location.
- 抜け道 -> Shortcut (Travel system). Routes revealed on restored rings.
- ワールドマップ -> World Map (UI). Ring symbols appear here.
- 持ち物 -> Inventory (UI). "Inventory full" for capacity warning.
- 依頼/クエスト -> Request / Quest (System). Natural dialogue may use "job."
- 依頼者/依頼品 -> Requester / Requested Item (System). Distinguish person and required object.
- 採集/採掘/討伐 -> Gather / Mine / Defeat (Quest actions). "Hunt" works in recurring quest titles.
- 依頼の終了報告 -> Report Completion (Quest action). Required before rewards.
- クエストクリア -> Quest Complete (UI/debug). Also sound-test label.
- クエストをあきらめる -> Abandon Quest (UI). Cancellation action.
- セーブ/ゲームデータ -> Save / Game Data (UI). Saving and completion messages.
- 移動/移動を中止 -> Travel / Cancel Travel (UI). Repeated map prompts.
- 回復 -> Restore (System). "Recovered" or "restored" according to sentence.
- 勝利/負け -> Victory / Defeat (UI/debug). Sound/event test labels also use these.
- レベルアップ -> Level Up (UI/debug). Advancement message.
- アイテムゲット -> Item Acquired (UI/debug). Test label.
- エンディング/おわり -> Ending / The End (UI/event). Use "End" where it is a menu action rather than ending card.
- ファイナルバトル -> Final Battle (Quest/event). Buster climax label.
- 下克上 -> Overthrow the Overlord (Quest/event). Vandel rebellion against Harden.
- ジャンプゲームワールド -> Jump Game World (Event). Demo announcement; preserve historical context.
- ニンテンドーＤＳ -> Nintendo DS (Platform). Official product name.
- テストメッセージ/テストメッセー字/テストメッセー時/テストメッセー自 -> Test Message (Debug). Deliberate-looking homophone variants in test strings; not story speech.
- アニメ -> Animation (Debug). Numbered animation tests, not anime episodes.
- フラグ/オン/オフ/TRUE/FALSE -> Flag / On / Off / TRUE / FALSE (Debug). Preserve numerical identifiers and Boolean meaning.
- 汎用 -> Generic (Debug). Portrait categories combine weapon and element.
- マップ -> Map (Debug/UI). Preserve numeric map IDs.
- セレクト/選択肢 -> Selection / Option (Debug/UI). Numbered test selections.
- Ｂボタン/BACK -> B Button / Back (Input/UI). Distinct button versus menu command.
- エラー -> Error (Debug). Preserve error numbers.
- ファンファーレ -> Fanfare (Debug/audio). Sound-test category.

## Decisions from earlier batches
- (none yet)
