# Story reviewer brief - Bouken-ou Beet: Vandel vs. Busters (NDS)

You read one chapter of a JP->English fan translation straight through, in story order, the way a player meets it.
Per-batch reviewers already judged single lines with +-2 lines of context; your job is what they can't see.
Read-only: no edits, no git, no subagents. Return the report as your final message; the controller saves it.

## Inputs (all inlined below this brief)
- The chapter: every shown line of one script file in file order, `>> id | speaker | JP` then `EN:`. In both columns
  ` / ` is a line break inside a box and ` // ` a new page; the English is wrapped for the box, so a sentence running
  across ` / ` is normal. `[FF00]`-style codes are runtime names/numbers inserted by the game. Read ALL of it before
  judging.
- `docs/synopsis.md` (plot, file grouping, cast and voice guide; it serves as the style reference) and `glossary.md`
  (binding spellings and rulings at the top).
- Some files are not a continuous scene (field interactions, shops, movement confirmations, quest titles, debug
  text): judge those for consistency, voice of recurring speakers and stock phrasing, not for continuity.
- The Buster and Vandel stories are separate playthroughs with opposing outcomes: never read them as one chronology.

## Judge, across the whole chapter
- Continuity: each line follows from the one before; setups, callbacks and references back are kept; who knows what
  stays coherent; nothing gives a later reveal away early.
- Voice: each character sounds like the same person all chapter and matches the cast and voice guide: speech quirks,
  register, how they address others. Name the line where a voice drifts or goes neutral.
- Emotion: anger, fear, grief and comedy beats are as strong as the Japanese; a running gag keeps its punchline.
- Accuracy only where a line breaks one of the above; single-line accuracy was reviewed already.
- Also flag: a name off by a letter from the glossary, a suffix glued onto a variable ("[FF00]th"), awkward stock
  phrases.
- The English must fit the same box: a suggested EN should be about the same length as the current one.

## Report
### Issues
#### Critical (continuity break, reveal given away, wrong speaker)
#### Important (voice drift or flattened, emotional beat lost, setup or callback dropped, joke dead)
#### Minor (deferred to the polish pass)
Each: `id - JP gist - problem - suggested EN`.
### Assessment
`ok` (no Critical/Important) | `issue` - one sentence why. Put the word ok or issue first on the line after the
heading. The controller writes this word into the chapter's verdict.
