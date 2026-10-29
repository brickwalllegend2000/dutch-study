# Practice page: visual and concept-capture redesign

Status: needs-triage
Target: `views/vocabulary/flashcards.html` (generated; edit `scripts/flashcards.py` and `scripts/flashcards_template.html`, then `build`)

## Goal

Make the practice page quick to use on a phone, good on a laptop, and better at helping concepts stick: clean, minimal, functional. Visuals serve learning, not decoration.

## Users and devices

One learner. Mainly phone (design at 390 px wide, one hand, thumb reach), also laptop (1280 px). Works offline as a single file.

## Design principles

1. **Card first.** On a phone the card and the answer controls fill the screen. Settings live behind one button.
2. **Few visual signals, each meaning one thing.** Neutral surface and text; one accent for actions; green/red only for right/wrong; two fixed colours for articles (*de*, *het*) and two for auxiliaries (*heeft*, *is*), used the same everywhere.
3. **Explain misses.** Every wrong answer shows *why* (the rule, a source pointer) before moving on.
4. **Capture concepts.** The learner can attach a one-line note of their own to any card and export missed cards plus notes as a journal note. Notes are personal, never course facts.
5. **Calm motion.** Only a short flip and feedback flash (at most 200 ms); respect `prefers-reduced-motion`.
6. **Accessible by default.** Text contrast at least 4.5:1 in light and dark, tap targets at least 44 px, visible focus, state never shown by colour alone (also ✓/✗ and text).

## Out of scope

Dutch audio and the "Today" session (deferred), accounts or sync, external fonts or libraries, new vocabulary or grammar facts.

## Constraints

- Still one self-contained generated HTML file; no network requests.
- Keep the `dutchstudy-srs-v1` and `dutchstudy-writing-v1` storage keys compatible; add new keys (for example `dutchstudy-notes-v1`), include them in export/import.
- Any wording the page adds about grammar must come from `data/grammar/` notes or `data/grammar-quiz.json`; label anything else.
- Extend `tests/test_flashcards.py` for every new data field the generator emits; `validate` and all tests stay green.

## Verification (each issue)

Check in a real browser at 390 px and 1280 px: no horizontal scroll, no console errors, every deck still works (typed, flip, choice), light and dark. Contrast checked with computed colours.

## Tickets (in order)

| # | Ticket | Blocked by |
| --- | --- | --- |
| 01 | Mobile-first shell: settings drawer, progress bar, sticky action bar | none |
| 02 | Card faces: typography, article/aux colours, direction label, flip | 01 |
| 03 | Answer feedback: state colours, letter diff, ✓/✗ | 02 |
| 04 | Concept capture: why panel, my-note, missed-card export, mistake log | 03 |
| 05 | Home screen with due counts; session summary with "practise missed" | 01 |
| 06 | Grammar rule cards and writing view restyle | 02 |
| 07 | Theme, contrast, accessibility, desktop layout | 01-06 |
| 08 | Mastery view and streak (optional, last) | 04 |
