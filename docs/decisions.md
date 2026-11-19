# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-11-18 | Honorifics and name order | keep (-san), drop; JP or Western order | Keep honorifics; Western name order (given name first). Owner's standing answer for one-shot runs. |
| D2 | 2026-11-18 | Romanization source for names | official art, earlier patch, Hepburn | Official English names where they exist (e.g. the anime's English release / official romanized logo art), else an earlier fan patch, else Hepburn without macrons. |
| D3 | 2026-11-18 | Credits | stay Japanese, translate | English. |
| D4 | 2026-11-18 | Abbreviations | engine work first (default), abbreviate | Engine work first (default); abbreviate only as a flagged last resort. |
| D5 | 2026-11-18 | Graphics text left in Japanese | none (default), list | None: translate all graphics text (titles, menus, banners, cards). Leave the original Japanese logo only if it has no official English version. |
| D6 | 2026-11-18 | Specs and plans | need approval, pre-approved | Pre-approved: keep going through every checkpoint without asking. |
| D7 | 2026-11-18 | Existing saves / savestates | user's saves, none | None provided; build the debug tool (phase 2) as usual. |
| D8 | 2026-11-18 | Publishing | publish, hold | Never run `gh release create` or change repo visibility; the run ends at a built and verified release zip. |
| D9 | 2026-11-19 | Element (属性) values (agent default under D4/D6, not asked) | abbreviate everywhere, move the window, short form only where a 16 px cell is fixed | Monster book: full names, value window moved under the label (engine work). Vandel status grid and 魔賓館 card icons (16 px, one kanji each in the original): flagged two-letter forms Ma/Ca/Wh/Sa/Ea/Or/Tr/Ul/Bo/Se (glossary §Graphics UI labels). |
| D10 | 2026-11-19 | Errors in the Japanese original (agent default, not asked; story pass) | translate as written, correct | Keep the original's speaker tags (rom.157C0: the father's farewell is tagged {hero} in the JP script data; changing it means editing script bytecode). Correct a plain slip inside one line's own text when the same line contradicts it (rom.1CCC4: "protect West Village's statue" right after "only East Village's statue remains" -> East). |
| D11 | 2026-11-19 | Honorific after a name variable, e.g. `{vandel}-sama` (agent default under D1, not asked; polish pass) | keep `-sama`, "Lord {vandel}", drop it | Keep `{vandel}-sama` / `{hero}-san` as in D1: 32+ lines already use it, and a mix would read as inconsistent. The polish batches' proposals that dropped or replaced it were changed back. |
| D12 | 2026-11-19 | Mild swearing (agent default, not asked; polish pass) | "Damn", "Darn" | Keep "Darn" for くそっ (all-ages Jump licence game); "Damn" proposals rejected. Laughs stay English-style ("Oho", "Hmhm"), not romanized "Ufu". |
| D13 | 2026-11-19 | Numbers inside dialogue (agent default, not asked) | leave full-width (12 px pitch, "1 0 0"), proportional | Proportional digits for the two message expansions ([FF01] appraiser, quest {count}) via engine hook `num_pc`; status and other columns keep the game's full-width right-aligned digits. |
| D14 | 2026-11-19 | Publishing v1.0 (owner asked: "prepare release and publish"; supersedes D8 for this release) | publish, hold | Publish: repo `minhnhattonthat/bouken-ou-beet-vandel-vs-busters-en` made public, description set to the real title, GitHub release `v1.0` with the verified zip. Later releases still wait for the owner's word. |
