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
| 封印のリング | Sealing Ring |  | Sacred object (phase 6 NEW TERM merge). Plural "Sealing Rings"; capitalised. | Seal Ring |
| エルファスト | Elfast |  | Place: town with an armor shop (item descriptions). |  |
| 網膜鑑定 | retinal appraisal |  | Buster guild system: appraisers read quest results from the eye. Lower case. |  |
| 昇格値 | Rank Points |  | Buster guild system: points toward a rank promotion. | promotion points |
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
| ノルナージの森 | Norunaji Forest |  | Place: Western region. Map labels (area.name, 96 px): short form "Norunaji Wood". |  |
| リンラーゴ山地 | Rinrago Mountains |  | Place: Do not merge with Rinnam Glacier. |  |
| リンナム氷河 | Rinnam Glacier |  | Place: Transport destination. |  |
| オーラン洞窟 | Oran Cave |  | Place: Distinct map name from mine. |  |
| オーラン坑道 | Oran Mine |  | Place: Resistance hideout, ambush and aircraft. |  |
| リーベリン湖 | Riberin Lake |  | Place: Lake containing a hideout tower. |  |
| リーベリン湖の塔 | Riberin Lake Tower |  | Place: Resistance hideout. |  |
| ビョンリン火山/ピョンリン火山 | Byonrin Volcano |  | Place: Main spelling uses ビョ; flight dialogue uses ピョ. Normalize provisionally. Map labels (area.name, 96 px): short form "Byonrin Mt.". |  |
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
| ゼナ体力丸 | Zena Vitality Pill |  | Key item: Return gift before the ordinary pill reward. |  |
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
| ライボルトグラスパー | Lightning Grasper |  | Saiga: game-original or unconfirmed spelling. Milfa's named weapon. |  |
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
| 火山の翼竜 | Lava Pterosaur |  | Monster: game-original or unconfirmed spelling. Garonute's later reward. |  |
| 突然変異 | Mutation |  | Monster term: Noa distinguishes mutation from going feral. |  |
| 薬草 | Medicinal Herb |  | Item: Ordinary healing item; distinct from flowers. |  |
| 体力丸 | Vitality Pill |  | Item: Keep consistent with Zena's named gift. |  |
| 天力丸 | Divine Pill |  | Item: Proposed short name tied to Divine Power. |  |
| 治療薬 | Healing Medicine |  | Item: Exact effect not specified here. |  |
| 万能薬 | Panacea |  | Item: Generic all-purpose remedy name. |  |
| 解毒剤 | Antidote |  | Item: Poison remedy. |  |
| しびれ取り | Paralysis Cure |  | Item: Status remedy. |  |
| 気付け剤 | Smelling Salts |  | Item: Do not infer revival mechanics solely from name. |  |
| 栄養剤 | Nutrient Tonic |  | Item: Exact effect unspecified. |  |
| ハーブティー | Herbal Tea |  | Item: Consumable. |  |
| ホットジェル | Hot Gel |  | Item: Keep distinct from Cool Gel. |  |
| クールジェル | Cool Gel |  | Item: Consumable. |  |
| 里のおばばの秘薬 | Granny's Elixir |  | Item: Gift from the Appraiser and loot item. |  |
| おじぃの妙薬 | Grandpa's Cure |  | Item: Separate from Granny's Elixir. |  |
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

## Names from the game tables

Generated by tools/glosstables.py from the translated tables (binding; change the table entry, then rerun).

| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 黄金城 | Golden Castle |  | area.name |  |
| ビョンリン遺跡 | Byonrin Ruins |  | area.name |  |
| 見習いのジャケット | Apprentice Jacket |  | armor.name |  |
| 新米のジャケット | Novice Jacket |  | armor.name |  |
| 普通のジャケット | Standard Jacket |  | armor.name |  |
| ルーキージャケット | Rookie Jacket |  | armor.name |  |
| 中級者のジャケット | Adept Jacket |  | armor.name |  |
| ベテランジャケット | Veteran Jacket |  | armor.name |  |
| 上級者のジャケット | Expert Jacket |  | armor.name |  |
| 強者のジャケット | Champion Jacket |  | armor.name |  |
| バトルジャケット | Battle Jacket |  | armor.name |  |
| コットンシャツ | Cotton Shirt |  | armor.name |  |
| リネンシャツ | Linen Shirt |  | armor.name |  |
| ウールシャツ | Wool Shirt |  | armor.name |  |
| シルクシャツ | Silk Shirt |  | armor.name |  |
| アンゴラシャツ | Angora Shirt |  | armor.name |  |
| アルパカシャツ | Alpaca Shirt |  | armor.name |  |
| レザーシャツ | Leather Shirt |  | armor.name |  |
| バスターズシャツ | Buster's Shirt |  | armor.name |  |
| バトルシャツ | Battle Shirt |  | armor.name |  |
| ウッドシールド | Wood Shield |  | armor.name |  |
| ブロンズシールド | Bronze Shield |  | armor.name |  |
| カッパーシールド | Copper Shield |  | armor.name |  |
| アイアンシールド | Iron Shield |  | armor.name |  |
| スティールシールド | Steel Shield |  | armor.name |  |
| シルバーシールド | Silver Shield |  | armor.name |  |
| レアメタルシールド | Rare Metal Shield |  | armor.name |  |
| ハイメタルシールド | High Metal Shield |  | armor.name |  |
| ブロンズバングル | Bronze Bangle |  | armor.name |  |
| カッパーバングル | Copper Bangle |  | armor.name |  |
| アイアンバングル | Iron Bangle |  | armor.name |  |
| スティールバングル | Steel Bangle |  | armor.name |  |
| シルバーバングル | Silver Bangle |  | armor.name |  |
| レアメタルバングル | Rare Metal Bangle |  | armor.name |  |
| ハイメタルバングル | High Metal Bangle |  | armor.name |  |
| Ｂメタルバングル | B-Metal Bangle |  | armor.name |  |
| バトルバングル | Battle Bangle |  | armor.name |  |
| コットンマント | Cotton Cape |  | armor.name |  |
| リネンマント | Linen Cape |  | armor.name |  |
| ウールマント | Wool Cape |  | armor.name |  |
| シルクマント | Silk Cape |  | armor.name |  |
| アンゴラマント | Angora Cape |  | armor.name |  |
| アルパカマント | Alpaca Cape |  | armor.name |  |
| レザーマント | Leather Cape |  | armor.name |  |
| バスターズマント | Buster's Cape |  | armor.name |  |
| バトルマント | Battle Cape |  | armor.name |  |
| コットンバンダナ | Cotton Bandanna |  | armor.name |  |
| リネンバンダナ | Linen Bandanna |  | armor.name |  |
| ウールバンダナ | Wool Bandanna |  | armor.name |  |
| シルクバンダナ | Silk Bandanna |  | armor.name |  |
| アンゴラバンダナ | Angora Bandanna |  | armor.name |  |
| アルパカバンダナ | Alpaca Bandanna |  | armor.name |  |
| レザーバンダナ | Leather Bandanna |  | armor.name |  |
| バスターズバンダナ | Buster's Bandanna |  | armor.name |  |
| バトルバンダナ | Battle Bandanna |  | armor.name |  |
| コットングローブ | Cotton Gloves |  | armor.name |  |
| リネングローブ | Linen Gloves |  | armor.name |  |
| ウールグローブ | Wool Gloves |  | armor.name |  |
| シルクグローブ | Silk Gloves |  | armor.name |  |
| アンゴラグローブ | Angora Gloves |  | armor.name |  |
| アルパカグローブ | Alpaca Gloves |  | armor.name |  |
| レザーグローブ | Leather Gloves |  | armor.name |  |
| バスターズグローブ | Buster's Gloves |  | armor.name |  |
| バトルグローブ | Battle Gloves |  | armor.name |  |
| クラウンシールド | Crown Shield |  | armor.name |  |
| 手紙 | Letter |  | keyitem.name |  |
| カギ１ | Key 1 |  | keyitem.name |  |
| カギ２ | Key 2 |  | keyitem.name |  |
| カギ３ | Key 3 |  | keyitem.name |  |
| カギ４ | Key 4 |  | keyitem.name |  |
| カギ５ | Key 5 |  | keyitem.name |  |
| 角を大きくする薬？ | Horn Tonic? |  | keyitem.name |  |
| 背を高くする薬？ | Height Tonic? |  | keyitem.name |  |
| 薬花 | Medicinal Flower |  | keyitem.name |  |
| 鉱石 | Ore |  | keyitem.name |  |
| ムガインの石像 | Mugain Statue |  | keyitem.name |  |
| ベンチュラの石像 | Ventura Statue |  | keyitem.name |  |
| ロズゴートの石像 | Rozgoat Statue |  | keyitem.name |  |
| フラウスキーの石像 | Frausky Statue |  | keyitem.name |  |
| グリニデの石像 | Grineed Statue |  | keyitem.name |  |
| グリニデの石像２ | Grineed Idol 2 |  | keyitem.name |  |
| ベルトーゼの石像 | Beltorze Statue |  | keyitem.name |  |
| 冥撃の火弾 | Dark Fire |  | meigeki.name |  |
| 冥撃の烈火 | Dark Blaze |  | meigeki.name |  |
| 冥撃の獄炎 | Hellfire |  | meigeki.name |  |
| 灼熱の冥獄炎 | Hell Inferno |  | meigeki.name |  |
| 冥撃の火勢 | Fire Surge |  | meigeki.name |  |
| 冥撃の炎流 | Fire Flow |  | meigeki.name |  |
| 冥撃の爆炎 | Fire Burst |  | meigeki.name |  |
| 灼熱の冥炎流 | Hell Flow |  | meigeki.name |  |
| 業火の冥撃流 | Hell Tide |  | meigeki.name |  |
| 冥撃の氷結 | Freeze |  | meigeki.name |  |
| 冥撃の氷塊 | Dark Ice |  | meigeki.name |  |
| 冥撃の氷柱 | Dark Icicle |  | meigeki.name |  |
| 零水の冥氷塊 | Zero Ice |  | meigeki.name |  |
| 冥撃の雹雨 | Dark Hail |  | meigeki.name |  |
| 冥撃の寒波 | Cold Wave |  | meigeki.name |  |
| 冥撃の氷嵐 | Ice Storm |  | meigeki.name |  |
| 極寒の凍結波 | Ice Wave |  | meigeki.name |  |
| 極寒の冥雹獄 | Hail Hell |  | meigeki.name |  |
| 冥撃の暴風 | Dark Gale |  | meigeki.name |  |
| 冥撃の烈風 | Fierce Gale |  | meigeki.name |  |
| 冥撃の乱気 | Wild Air |  | meigeki.name |  |
| 暗黒の冥乱気 | Dark Eddy |  | meigeki.name |  |
| 冥撃の斬風 | Wind Slash |  | meigeki.name |  |
| 冥撃の黒風 | Black Wind |  | meigeki.name |  |
| 冥撃の魔風 | Evil Gale |  | meigeki.name |  |
| 暗黒の冥爆風 | Dark Blast |  | meigeki.name |  |
| 冥獄の乱爆風 | Hell Blasts |  | meigeki.name |  |
| 冥獄の乱烈風 | Hell Gales |  | meigeki.name |  |
| 冥撃の電流 | Dark Spark |  | meigeki.name |  |
| 冥撃の雷弾 | Dark Bolt |  | meigeki.name |  |
| 冥撃の雷閃 | Bolt Flash |  | meigeki.name |  |
| 暗黒の冥雷波 | Dark Surge |  | meigeki.name |  |
| 冥撃の爆雷 | Bolt Burst |  | meigeki.name |  |
| 冥撃の列雷 | Bolt Chain |  | meigeki.name |  |
| 冥撃の獄雷 | Hell Bolt |  | meigeki.name |  |
| 冥撃の大獄魔 | Archfiend |  | meigeki.name |  |
| 暗黒の冥瞬雷 | Dark Flash |  | meigeki.name |  |
| 冥撃の魔波 | Evil Wave |  | meigeki.name |  |
| 冥撃の魔烈 | Evil Rend |  | meigeki.name |  |
| 冥撃の魔爆 | Evil Burst |  | meigeki.name |  |
| 暗黒の魔爆波 | Doom Tide |  | meigeki.name |  |
| 冥撃の重圧 | Crush |  | meigeki.name |  |
| 終局の大魔流 | Final Flood |  | meigeki.name |  |
| 岩石毛虫 | Rock Caterpillar |  | monster.name |  |
| 赤いじゅうたん | Red Carpet |  | monster.name |  |
| 海のガブリ貝 | Sea Snapclam |  | monster.name |  |
| 水晶の卵 | Crystal Egg |  | monster.name |  |
| ジャーマウス | Jarmouse |  | monster.name |  |
| ペンバリー | Penbary |  | monster.name |  |
| びっくり箱 | Jack-in-the-Box |  | monster.name |  |
| 貯金箱 | Piggy Bank |  | monster.name |  |
| パペットスパイダー | Puppet Spider |  | monster.name |  |
| オドオド | Odoodo |  | monster.name |  |
| 悪魔のココナッツ | Devil Coconut |  | monster.name |  |
| ヒルニア | Hirunia |  | monster.name |  |
| 鉄の貯金箱 | Iron Piggy Bank |  | monster.name |  |
| 空飛ぶクリオネ | Flying Sea Angel |  | monster.name |  |
| ラバーファイター | Rubber Fighter |  | monster.name |  |
| 青き炎 | Blue Flame |  | monster.name |  |
| ハンドゴースト | Hand Ghost |  | monster.name |  |
| 海のブロウガンナー | Sea Blowgunner |  | monster.name |  |
| つららこうもり | Icicle Bat |  | monster.name |  |
| ホワイトジャーマウス | White Jarmouse |  | monster.name |  |
| ボスカネック | Boss Kaneck |  | monster.name |  |
| 魔人の像 | Vandel Statue |  | monster.name |  |
| 沼のメガトンボ | Marsh Megafly |  | monster.name |  |
| ピンクの卵 | Pink Egg |  | monster.name |  |
| 毒のガブリ貝 | Poison Snapclam |  | monster.name |  |
| 泥トカゲ | Mud Lizard |  | monster.name |  |
| メタルジャーマウス | Metal Jarmouse |  | monster.name |  |
| サンゴガブリ貝 | Coral Snapclam |  | monster.name |  |
| 山賊バチ | Bandit Wasp |  | monster.name |  |
| 武装ペンバリー | Armed Penbary |  | monster.name |  |
| リビングコイン | Living Coin |  | monster.name |  |
| 拷問ねじ | Torture Screw |  | monster.name |  |
| 砂ふくろう | Sand Owl |  | monster.name |  |
| 導師の使い魔 | Mage's Familiar |  | monster.name |  |
| 沼の吸血鬼 | Marsh Vampire |  | monster.name |  |
| はじまりの卵 | Primal Egg |  | monster.name |  |
| 弾丸モグラ | Bullet Mole |  | monster.name |  |
| ガラガラ | Rattle |  | monster.name |  |
| ツチギンチャク分身 | Anemone Clone |  | monster.name |  |
| トドドリル | Sea Lion Drill |  | monster.name |  |
| 毒虫の化石 | Poison Bug Fossil |  | monster.name |  |
| 強力ガブリ貝 | Mighty Snapclam |  | monster.name |  |
| 百目タマムシ | Hundred-Eye Bug |  | monster.name |  |
| 黒煙ゼミ | Soot Cicada |  | monster.name |  |
| 猛毒タマムシ | Venom Jewelbug |  | monster.name |  |
| 黒煙虫 | Soot Bug |  | monster.name |  |
| 煙突カメムシ | Chimney Stinkbug |  | monster.name |  |
| 大将バチ | General Wasp |  | monster.name |  |
| バーム | Barm |  | monster.name |  |
| 毒バーム | Poison Barm |  | monster.name |  |
| メガトンボ | Megafly |  | monster.name |  |
| 巨大メガトンボ | Giant Megafly |  | monster.name |  |
| 暴れマギー | Rampaging Maggy |  | monster.name |  |
| 群がり犬 | Pack Dog |  | monster.name |  |
| 群がり子犬 | Pack Pup |  | monster.name |  |
| プロテク虫 | Shield Bug |  | monster.name |  |
| 森の愚者 | Forest Fool |  | monster.name |  |
| ハウンドソルジャー | Hound Soldier |  | monster.name |  |
| 腐薬虫 | Rotvenom Bug |  | monster.name |  |
| 火煙虫 | Fire-Smoke Bug |  | monster.name |  |
| スノーマン | Snowman |  | monster.name |  |
| 北斗狼 | Big Dipper Wolf |  | monster.name |  |
| トドドドリル | Sea Lion Drilldrill |  | monster.name |  |
| 黒いブロウガンナー | Black Blowgunner |  | monster.name |  |
| 鎧ペンバリー | Armored Penbary |  | monster.name |  |
| ジャガーム | Jagarm |  | monster.name |  |
| 水ふくろう | Water Owl |  | monster.name |  |
| 青いびっくり箱 | Blue Trick Box |  | monster.name |  |
| さまようガイコツ | Roaming Skeleton |  | monster.name |  |
| 闇の天狼 | Dark Sky Wolf |  | monster.name |  |
| ハエコマンド | Fly Commando |  | monster.name |  |
| ハウンドナイト | Hound Knight |  | monster.name |  |
| 洞穴の愚者 | Cave Fool |  | monster.name |  |
| 人喰い人魚 | Maneater Mermaid |  | monster.name |  |
| 氷結ゼミ | Frost Cicada |  | monster.name |  |
| 氷のハエコマンド | Ice Fly Commando |  | monster.name |  |
| 泥の導士 | Mud Mage |  | monster.name |  |
| 炎のジャガーム | Flame Jagarm |  | monster.name |  |
| 岩石エイ | Rock Ray |  | monster.name |  |
| 赤銅兵士 | Copper Soldier |  | monster.name |  |
| アサシンクロウ | Assassin Crow |  | monster.name |  |
| 猛毒ペンバリー | Venom Penbary |  | monster.name |  |
| 腐肉の人 | Rotflesh Man |  | monster.name |  |
| 岩石巨人 | Rock Giant |  | monster.name |  |
| 魔人の氷像 | Vandel Ice Statue |  | monster.name |  |
| 砂のブロウガンナー | Sand Blowgunner |  | monster.name |  |
| ブロウガンナー | Blowgunner |  | monster.name |  |
| ドローマスター | Dromaster |  | monster.name |  |
| 炎の人魚 | Flame Mermaid |  | monster.name |  |
| 首長エイ | Longneck Ray |  | monster.name |  |
| 七星餓狼 | 7-Star Direwolf |  | monster.name |  |
| 青炎馬 | Blueflame Horse |  | monster.name |  |
| 鉄騎貝 | Iron Knight Clam |  | monster.name |  |
| 砂トカゲ | Sand Lizard |  | monster.name |  |
| 墓場荒らし | Grave Robber |  | monster.name |  |
| 中甲虫 | Medium Beetle |  | monster.name |  |
| 化石の鉄騎貝 | Fossil Knight Clam |  | monster.name |  |
| 石の魔人像 | Rock Vandel Idol |  | monster.name |  |
| 潮の導士 | Tide Mage |  | monster.name |  |
| ナイトスナイパー | Night Sniper |  | monster.name |  |
| 蔦の導士 | Vine Mage |  | monster.name |  |
| 白亜の翼竜 | Chalk Pterosaur |  | monster.name |  |
| マグネソルジャー | Magne Soldier |  | monster.name |  |
| 血雪馬 | Bloodsnow Horse |  | monster.name |  |
| 土の導士 | Earth Mage |  | monster.name |  |
| マグマの導士 | Magma Mage |  | monster.name |  |
| 砂の導士 | Sand Mage |  | monster.name |  |
| 凍てつく炎 | Freezing Flame |  | monster.name |  |
| 骨の導士 | Bone Mage |  | monster.name |  |
| 罪人たいまつ | Sinner's Torch |  | monster.name |  |
| 氷の導士 | Ice Mage |  | monster.name |  |
| 青銅巨人 | Bronze Giant |  | monster.name |  |
| フレイムペンギン | Flame Penguin |  | monster.name |  |
| 砂のアサシンクロウ | Sand Killer Crow |  | monster.name |  |
| 氷雪巨人 | Frost Giant |  | monster.name |  |
| フリーズペンギン | Freeze Penguin |  | monster.name |  |
| 暗黒マグネナイト | Dark Magneknight |  | monster.name |  |
| 樹氷たいまつ | Rimewood Torch |  | monster.name |  |
| 大甲虫 | Giant Beetle |  | monster.name |  |
| 氷つららこうもり | Ice Icicle Bat |  | monster.name |  |
| 岩石モグラ | Rock Mole |  | monster.name |  |
| 軍艦トータス | Warship Tortoise |  | monster.name |  |
| バスターゾンビ | Buster Zombie |  | monster.name |  |
| 毒沼の翼竜 | Bog Pterosaur |  | monster.name |  |
| 大軍艦トータス | Grand Tortoise |  | monster.name |  |
| 砂陣の翼竜 | Sand Pterosaur |  | monster.name |  |
| 雪崩モグラ | Avalanche Mole |  | monster.name |  |
| 真紅の夢魔 | Crimson Nightmare |  | monster.name |  |
| ダイヤの巨人 | Diamond Giant |  | monster.name |  |
| ツチギンチャク | Earth Anemone |  | monster.name |  |
| 鋼の導士 | Steel Adept |  | monster.name |  |
| 鋼鉄モグラ | Steel Mole |  | monster.name |  |
| 死を呼ぶ夢魔 | Death Nightmare |  | monster.name |  |
| 鋼の魔人像 | Steel Vandel Idol |  | monster.name |  |
| 黒き炎 | Black Flame |  | monster.name |  |
| 黒の卵 | Black Egg |  | monster.name |  |
| 漆黒の翼竜 | Black Pterosaur |  | monster.name |  |
| ダークネスペンギン | Darkness Penguin |  | monster.name |  |
| 暗黒タマムシ | Dark Jewel Beetle |  | monster.name |  |
| ダークジャガーム | Dark Jagarm |  | monster.name |  |
| 民兵 | Militia |  | monster.name |  |
| 百烈突き | Hundred Thrusts |  | skill.name |  |
| 炎の衝撃波 | Flame Wave |  | skill.name |  |
| 貫通ランス | Piercing Lance |  | skill.name |  |
| 特攻 | Reckless Charge |  | skill.name |  |
| ゼノンウィンザード | Zenon Winzard |  | skill.name |  |
| 乱舞 | Wild Dance |  | skill.name |  |
| 兜割り | Helm Splitter |  | skill.name |  |
| スライドカッター | Slide Cutter |  | skill.name |  |
| 狙う | Aim |  | skill.name |  |
| カッター | Cutter |  | skill.name |  |
| もず落とし | Shrike Drop |  | skill.name |  |
| ラウンドカッター | Round Cutter |  | skill.name |  |
| 長距離射程モード | Long-Range Mode |  | skill.name |  |
| 全弾開放モード | Full Salvo Mode |  | skill.name |  |
| 炸裂弾 | Burst Shell |  | skill.name |  |
| ショットガン | Shotgun |  | skill.name |  |
| 鉄球変形 | Iron Ball Form |  | skill.name |  |
| カウンター | Counter |  | skill.name |  |
| アクアウォール | Aqua Wall |  | skill.name |  |
| 鉄球捕縛 | Iron Ball Snare |  | skill.name |  |
| ソニックエッジ | Sonic Edge |  | skill.name |  |
| イリュージョンエッジ | Illusion Edge |  | skill.name |  |
| ブレイブ・ブレイド | Brave Blade |  | skill.name |  |
| ダブル・スマッシャー | Double Smasher |  | skill.name |  |
| 変形 | Transform |  | skill.name |  |
| キラー・スピリット | Killer Spirit |  | skill.name |  |
| トルネード・レイブ | Tornado Rave |  | skill.name |  |
| チェイン・スレイヤー | Chain Slayer |  | skill.name |  |
| ソウル・クラッシュ | Soul Crush |  | skill.name |  |
| メタル・ウェーブ | Metal Wave |  | skill.name |  |
| メタル・エッジ | Metal Edge |  | skill.name |  |
| スピニングエッジ | Spinning Edge |  | skill.name |  |
| ギガクラッシャー | Giga Crusher |  | skill.name |  |
| クロストリガー | Cross Trigger |  | skill.name |  |
| バーストショット | Burst Shot |  | skill.name |  |
| メテオ・アロー | Meteor Arrow |  | skill.name |  |
| ジェノサイドキャノン | Genocide Cannon |  | skill.name |  |
| リンガーキャノン | Ringer Cannon |  | skill.name |  |
| アクセルライズ | Accel Rise |  | skill.name |  |
| メガティックボンバー | Megatic Bomber |  | skill.name |  |
| ユナイトカウンター | Unite Counter |  | skill.name |  |
| ブラスターショット | Blaster Shot |  | skill.name |  |
| ジークインフェルノ | Zeke Inferno |  | skill.name |  |
| グレイバーキャノン | Graver Cannon |  | skill.name |  |
| グレイバーショット | Graver Shot |  | skill.name |  |
| グレイバーアタック | Graver Attack |  | skill.name |  |
| ショートデスダッシュ | Short Death Dash |  | skill.name |  |
| ミドルデスダッシュ | Middle Death Dash |  | skill.name |  |
| ロングデスダッシュ | Long Death Dash |  | skill.name |  |
| ダークスピン | Dark Spin |  | skill.name |  |
| デススピン | Death Spin |  | skill.name |  |
| グレイブスピン | Grave Spin |  | skill.name |  |
| ダークストライク | Dark Strike |  | skill.name |  |
| デスストライク | Death Strike |  | skill.name |  |
| グレイブストライク | Grave Strike |  | skill.name |  |
| ダークラッシュ | Dark Rush |  | skill.name |  |
| デスラッシュ | Death Rush |  | skill.name |  |
| グレイブラッシュ | Grave Rush |  | skill.name |  |
| バーンディスチャージ | Burn Discharge |  | skill.name |  |
| ダークディスチャージ | Dark Discharge |  | skill.name |  |
| ウインディスチャージ | Wind Discharge |  | skill.name |  |
| ボルツディスチャージ | Volts Discharge |  | skill.name |  |
| フラッディスチャージ | Flood Discharge |  | skill.name |  |
| バーニングランス | Burning Lance |  | special.name |  |
| エクセリオンブレード | Excellion Blade |  | special.name |  |
| ボルティックアックス | Voltic Axe |  | special.name |  |
| サイクロンガンナー | Cyclone Gunner |  | special.name |  |
| サイレントグレイブ | Silent Glaive |  | special.name |  |
| クリスタルブロッカー | Crystal Blocker |  | special.name |  |
| フルムーンシャフト | Full Moon Shaft |  | special.name |  |
| ブラスターエッジ | Blaster Edge |  | special.name |  |
| プレイヤーソード | Player Sword |  | special.name |  |
| プレイヤースピア | Player Spear |  | special.name |  |
| プレイヤーアックス | Player Axe |  | special.name |  |
| プレイヤーガン | Player Gun |  | special.name |  |
| プレイヤーナックル | Player Knuckle |  | special.name |  |
| 天撃の火炎 | Divine Fire |  | tengeki.name |  |
| 天撃の火柱 | Divine Pyre |  | tengeki.name |  |
| 天撃の火掌 | Fire Palm |  | tengeki.name |  |
| 天烈の大火球 | Fire Orb |  | tengeki.name |  |
| 天撃の火流 | Fire Flow |  | tengeki.name |  |
| 天撃の業火 | Hellfire |  | tengeki.name |  |
| 天撃の爆炎 | Fire Blast |  | tengeki.name |  |
| 天撃の火針 | Fire Needle |  | tengeki.name |  |
| 天撃の陽炎 | Heat Haze |  | tengeki.name |  |
| 天撃の雹弾 | Hail Shot |  | tengeki.name |  |
| 天撃の雹柱 | Hail Pillar |  | tengeki.name |  |
| 天撃の雹錘 | Hail Maul |  | tengeki.name |  |
| 天青の氷結波 | Ice Wave |  | tengeki.name |  |
| 天撃の氷雨 | Ice Rain |  | tengeki.name |  |
| 天撃の吹雪 | Blizzard |  | tengeki.name |  |
| 天撃の雪崩 | Avalanche |  | tengeki.name |  |
| 天撃の浄水 | Pure Water |  | tengeki.name |  |
| 天撃の水衣 | Aqua Veil |  | tengeki.name |  |
| 天撃の疾風 | Gale |  | tengeki.name |  |
| 天撃の旋風 | Whirlwind |  | tengeki.name |  |
| 天撃の大嵐 | Tempest |  | tengeki.name |  |
| 天乱の大竜巻 | Tornado |  | tengeki.name |  |
| 天撃の戦陣 | War Gale |  | tengeki.name |  |
| 天撃の涼風 | Cool Wind |  | tengeki.name |  |
| 天撃の風車 | Windmill |  | tengeki.name |  |
| 天撃の山彦 | Echo |  | tengeki.name |  |
| 天撃の気流 | Air Current |  | tengeki.name |  |
| 天撃の風塵 | Dust Gale |  | tengeki.name |  |
| 天撃の稲妻 | Lightning |  | tengeki.name |  |
| 天撃の雷撃 | Volt Strike |  | tengeki.name |  |
| 天撃の雷轟 | Volt Roar |  | tengeki.name |  |
| 閃空の天雷破 | Skybolt |  | tengeki.name |  |
| 天撃の雷電 | Volt Storm |  | tengeki.name |  |
| 天撃の極雷 | Volt Surge |  | tengeki.name |  |
| 天撃の超雷 | Super Bolt |  | tengeki.name |  |
| 天撃の落雷 | Bolt Strike |  | tengeki.name |  |
| 天撃の電流 | Volt Flow |  | tengeki.name |  |
| 天撃の光弾 | Light Shot |  | tengeki.name |  |
| 天撃の閃光 | Flash |  | tengeki.name |  |
| 天撃の瞬光 | Light Flare |  | tengeki.name |  |
| 天撃の白熱 | White Heat |  | tengeki.name |  |
| 天撃の銀光 | Silver Glow |  | tengeki.name |  |
| 天撃の光陰 | Shade |  | tengeki.name |  |
| シャデリコ強化版 | Shaderiko EX |  | vandel.name |  |
| グリニデ変身後 | Grineed (Form 2) |  | vandel.name |  |
| ヴァンデル主人公炎 | Fire Vandel Hero |  | vandel.name |  |
| ヴァンデル主人公魔 | Magic Vandel |  | vandel.name |  |
| ヴァンデル主人公風 | Wind Vandel |  | vandel.name |  |
| ヴァンデル主人公雷 | Bolt Vandel Hero |  | vandel.name |  |
| ヴァンデル主人公水 | Water Vandel |  | vandel.name |  |
| 才牙光り | Saiga Glow |  | weapon.name |  |
| 詠唱光り | Chant Glow |  | weapon.name |  |
| エフェクト予備 | Spare Effect |  | weapon.name |  |
| 青銅の槍 | Bronze Spear |  | weapon.name |  |
| 銅の槍 | Copper Spear |  | weapon.name |  |
| 鉄の槍 | Iron Spear |  | weapon.name |  |
| 鋼の槍 | Steel Spear |  | weapon.name |  |
| 銀の槍 | Silver Spear |  | weapon.name |  |
| レアメタルの槍 | Rare Metal Spear |  | weapon.name |  |
| ハイメタルの槍 | High Metal Spear |  | weapon.name |  |
| Ｂメタルの槍 | B-Metal Spear |  | weapon.name |  |
| バトルスピア | Battle Spear |  | weapon.name |  |
| ブロンズグレイブ | Bronze Glaive |  | weapon.name |  |
| カッパーグレイブ | Copper Glaive |  | weapon.name |  |
| アイアングレイブ | Iron Glaive |  | weapon.name |  |
| スティールグレイブ | Steel Glaive |  | weapon.name |  |
| シルバーグレイブ | Silver Glaive |  | weapon.name |  |
| レアメタルグレイブ | Rare Metal Glaive |  | weapon.name |  |
| ハイメタルグレイブ | High Metal Glaive |  | weapon.name |  |
| Ｂメタルグレイブ | B-Metal Glaive |  | weapon.name |  |
| バトルグレイブ | Battle Glaive |  | weapon.name |  |
| 青銅の剣 | Bronze Sword |  | weapon.name |  |
| 銅の剣 | Copper Sword |  | weapon.name |  |
| 鉄の剣 | Iron Sword |  | weapon.name |  |
| 鋼の剣 | Steel Sword |  | weapon.name |  |
| レアメタルの剣 | Rare Metal Sword |  | weapon.name |  |
| ハイメタルの剣 | High Metal Sword |  | weapon.name |  |
| Ｂメタルの剣 | B-Metal Sword |  | weapon.name |  |
| バトルソード | Battle Sword |  | weapon.name |  |
| 青銅の投剣 | Bronze Knife |  | weapon.name |  |
| 銅の投剣 | Copper Knife |  | weapon.name |  |
| 鉄の投剣 | Iron Knife |  | weapon.name |  |
| 鋼の投剣 | Steel Knife |  | weapon.name |  |
| 銀の投剣 | Silver Knife |  | weapon.name |  |
| レアメタルの投剣 | Rare Metal Knife |  | weapon.name |  |
| ハイメタルの投剣 | High Metal Knife |  | weapon.name |  |
| Ｂメタルの投剣 | B-Metal Knife |  | weapon.name |  |
| バトルナイフ | Battle Knife |  | weapon.name |  |
| 青銅の大剣 | Bronze Blade |  | weapon.name |  |
| 銅の大剣 | Copper Blade |  | weapon.name |  |
| 鉄の大剣 | Iron Blade |  | weapon.name |  |
| 鋼の大剣 | Steel Blade |  | weapon.name |  |
| 銀の大剣 | Silver Blade |  | weapon.name |  |
| レアメタルの大剣 | Rare Metal Blade |  | weapon.name |  |
| ハイメタルの大剣 | High Metal Blade |  | weapon.name |  |
| Ｂメタルの大剣 | B-Metal Blade |  | weapon.name |  |
| バトルブレイド | Battle Blade |  | weapon.name |  |
| 青銅の斧 | Bronze Axe |  | weapon.name |  |
| 銅の斧 | Copper Axe |  | weapon.name |  |
| 鉄の斧 | Iron Axe |  | weapon.name |  |
| 鋼の斧 | Steel Axe |  | weapon.name |  |
| 銀の斧 | Silver Axe |  | weapon.name |  |
| レアメタルの斧 | Rare Metal Axe |  | weapon.name |  |
| ハイメタルの斧 | High Metal Axe |  | weapon.name |  |
| Ｂメタルの斧 | B-Metal Axe |  | weapon.name |  |
| バトルアックス | Battle Axe |  | weapon.name |  |
| 青銅の槌 | Bronze Hammer |  | weapon.name |  |
| 銅の槌 | Copper Hammer |  | weapon.name |  |
| 鉄の槌 | Iron Hammer |  | weapon.name |  |
| 鋼の槌 | Steel Hammer |  | weapon.name |  |
| 銀の槌 | Silver Hammer |  | weapon.name |  |
| レアメタルの槌 | Rare Metal Maul |  | weapon.name |  |
| ハイメタルの槌 | High Metal Maul |  | weapon.name |  |
| Ｂメタルの槌 | B-Metal Hammer |  | weapon.name |  |
| バトルハンマー | Battle Hammer |  | weapon.name |  |
| ブロンズボウ | Bronze Bow |  | weapon.name |  |
| カッパーボウ | Copper Bow |  | weapon.name |  |
| アイアンボウ | Iron Bow |  | weapon.name |  |
| スティールボウ | Steel Bow |  | weapon.name |  |
| シルバーボウ | Silver Bow |  | weapon.name |  |
| レアメタルボウ | Rare Metal Bow |  | weapon.name |  |
| ハイメタルボウ | High Metal Bow |  | weapon.name |  |
| Ｂメタルボウ | B-Metal Bow |  | weapon.name |  |
| バトルボウ | Battle Bow |  | weapon.name |  |
| ブロンズガン | Bronze Gun |  | weapon.name |  |
| カッパーガン | Copper Gun |  | weapon.name |  |
| アイアンガン | Iron Gun |  | weapon.name |  |
| スティールガン | Steel Gun |  | weapon.name |  |
| シルバーガン | Silver Gun |  | weapon.name |  |
| レアメタルガン | Rare Metal Gun |  | weapon.name |  |
| ハイメタルガン | High Metal Gun |  | weapon.name |  |
| Ｂメタルガン | B-Metal Gun |  | weapon.name |  |
| バトルガン | Battle Gun |  | weapon.name |  |
| ガンアームド | Gun Armed |  | weapon.name |  |
| ブロンズナックル | Bronze Knuckle |  | weapon.name |  |
| カッパーナックル | Copper Knuckle |  | weapon.name |  |
| アイアンナックル | Iron Knuckle |  | weapon.name |  |
| スティールナックル | Steel Knuckle |  | weapon.name |  |
| シルバーナックル | Silver Knuckle |  | weapon.name |  |
| レアメタルナックル | Rare Metal Fist |  | weapon.name |  |
| ハイメタルナックル | High Metal Fist |  | weapon.name |  |
| Ｂメタルナックル | B-Metal Knuckle |  | weapon.name |  |
| バトルナックル | Battle Knuckle |  | weapon.name |  |
| ブロンズクロー | Bronze Claw |  | weapon.name |  |
| カッパークロー | Copper Claw |  | weapon.name |  |
| アイアンクロー | Iron Claw |  | weapon.name |  |
| スティールクロー | Steel Claw |  | weapon.name |  |
| シルバークロー | Silver Claw |  | weapon.name |  |
| レアメタルクロー | Rare Metal Claw |  | weapon.name |  |
| ハイメタルクロー | High Metal Claw |  | weapon.name |  |
| Ｂメタルクロー | B-Metal Claw |  | weapon.name |  |
| バトルクロー | Battle Claw |  | weapon.name |  |
| ブロンズカフス | Bronze Cuffs |  | weapon.name |  |
| カッパーカフス | Copper Cuffs |  | weapon.name |  |
| アイアンカフス | Iron Cuffs |  | weapon.name |  |
| スティールカフス | Steel Cuffs |  | weapon.name |  |
| シルバーカフス | Silver Cuffs |  | weapon.name |  |
| レアメタルカフス | Rare Metal Cuffs |  | weapon.name |  |
| ハイメタルカフス | High Metal Cuffs |  | weapon.name |  |
| Ｂメタルカフス | B-Metal Cuffs |  | weapon.name |  |
| バトルカフス | Battle Cuffs |  | weapon.name |  |
| 青銅の鎖球 | Bronze Flail |  | weapon.name |  |
| 銅の鎖球 | Copper Flail |  | weapon.name |  |
| 鉄の鎖球 | Iron Flail |  | weapon.name |  |
| 鋼の鎖球 | Steel Flail |  | weapon.name |  |
| 銀の鎖球 | Silver Flail |  | weapon.name |  |
| レアメタルの鎖球 | Rare Metal Flail |  | weapon.name |  |
| ハイメタルの鎖球 | High Metal Flail |  | weapon.name |  |
| Ｂメタルの鎖球 | B-Metal Flail |  | weapon.name |  |
| バトルボール | Battle Ball |  | weapon.name |  |
| 青銅の円月輪 | Bronze Chakram |  | weapon.name |  |
| 銅の円月輪 | Copper Chakram |  | weapon.name |  |
| 鉄の円月輪 | Iron Chakram |  | weapon.name |  |
| 鋼の円月輪 | Steel Chakram |  | weapon.name |  |
| 銀の円月輪 | Silver Chakram |  | weapon.name |  |
| レアメタルの円月輪 | Rare Metal Ring |  | weapon.name |  |
| ハイメタルの円月輪 | High Metal Ring |  | weapon.name |  |
| Ｂメタルの円月輪 | B-Metal Chakram |  | weapon.name |  |
| バトルサークル | Battle Circle |  | weapon.name |  |
| 青銅の刀 | Bronze Katana |  | weapon.name |  |
| 銅の刀 | Copper Katana |  | weapon.name |  |
| 鉄の刀 | Iron Katana |  | weapon.name |  |
| 鋼の刀 | Steel Katana |  | weapon.name |  |
| 銀の刀 | Silver Katana |  | weapon.name |  |
| レアメタルの刀 | Raremetal Katana |  | weapon.name |  |
| ハイメタルの刀 | High Metal Katana |  | weapon.name |  |
| Ｂメタルの刀 | B-Metal Katana |  | weapon.name |  |
| バトルカタナ | Battle Katana |  | weapon.name |  |
| フラウスキー銃 | Frausky Gun |  | weapon.name |  |
| 主人公 | Protagonist |  | weapon.name |  |
| 片手剣 | One-Hand Sword |  | wpntype.name |  |
| 両手剣 | Two-Hand Sword |  | wpntype.name |  |
| 投剣 | Throwing Sword |  | wpntype.name |  |
| 鉄球 | Iron Ball |  | wpntype.name |  |
| 打撃 | Strike |  | wpntype.name |  |
| 円月輪 | Chakram |  | wpntype.name |  |
| ヒーローソード | Hero Sword |  | wpntype.name |  |
| ヒーロースピア | Hero Spear |  | wpntype.name |  |
| ヒーローアックス | Hero Axe |  | wpntype.name |  |
| ヒーローガン | Hero Gun |  | wpntype.name |  |
| ヒーローナックル | Hero Knuckles |  | wpntype.name |  |

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

## Graphics UI labels (binding for gfx/*.tsv; a list, not a table, so lint doesn't apply them to the script)
- Buttons and captions: 道具 Items, 隊列 Lineup, 戦術 Tactics, 特技 Skills, もどる Back, 決定 OK, 詳細 Details, 装備 Equip,
  情報 Info, 指示 Orders, パーティ指示 Party Orders, 軍団 Force, 軍団指示 Force Orders, 名前 Name, はい Yes, いいえ No,
  ステータス Status, 技 Skills, 図鑑 Book (バスター図鑑 Buster Book, モンスター図鑑 Monster Book, ヴァンデル図鑑 Vandel Book),
  取り込み Uptake, 種類 Type, 罠 Trap, セーブ Save, オプション Options, クエスト Quests, 武器 Weapons, 防具 Armor,
  貴重品 Treasure, はずす Remove, いれかえ Swap, 派遣 Dispatch, あきらめる Give Up, 完了報告 Report, はやい/ふつう/おそい
  Fast/Normal/Slow, クイックコマンド Quick Command, バトルメニュー Battle Menu, ターゲット Target, ポーズ Pause.
- 天撃 Divine Attack and 冥撃 Dark Attack go on two lines on buttons (`Divine|Attack`).
- Short forms where the frame is too small (graphics only; the script keeps the full term): クイックコマンド caption tab
  Quick Cmd. (53 px), 熟練度 tab on the equip screen Mastery (42 px), そうびアイテム strip on the hone screen Gear (8 rows,
  no descenders), 昇格値 battle-result banner Rank|Pts (split over its two sprites). (Script, not graphics: レジスタンスＡ～Ｌ speaker
  tags are Resist. A-L, since "Resistance D" is 85 px in the 80 px tag; only the narrow I fits in full.)

## Decisions from earlier batches
- (none yet)
