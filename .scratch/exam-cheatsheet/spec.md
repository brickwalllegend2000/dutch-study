# Exam cheat sheet → writing page

Status: needs-triage

## Goal

Bring the Notion "Spiekbriefje — Schrijven A2 (Examen)" into the library and use it to make the writing page teach the exam: the right structure, fixed phrases and checks for each text type.

## Source

Notion page `407f89e5e0fc8142b07af00a9ea445a3`, fetched 2026-10-29 through the Notion connector. Contents: structure per text type (8 rows), fixed-sentence bank (12 NL/EN pairs), sentence formulas (7), form spelling rules (5), final checklist (5). Unverified in Notion; its Dutch and English glosses are not teacher-checked, so everything stays `needs-review`.

## Decisions

- **Home:** one authored page, `course/exams/schrijven-spiekbriefje.md`, in the course layer (not `data/`, which is for vocabulary and grammar facts). Header states: imported from Notion, date, needs-review. Linked from `course/exams/README.md`, `course/README.md` and the oefenexamen page.
- **No second copy of the facts.** The generator parses the tables in that page, as it already does for the writing tasks, so the page and the practice page cannot drift. Tests fail if a table is missing or empty.
- **Text type per task** comes from a small explicit map in `flashcards.py` (task id → type), not guessed from the text. 15 tasks: exam 1 form, 2 formal note, 3–6 informal notes, 7 text about the past, 8 chat, 9 formal email; exercises 2 and 6 informal email.
- **Gap:** photo descriptions (exercises 1, 5) and short advice answers (3, 4) have no type in the cheat sheet. They keep today's checklist and get no starters. Do not invent a type for them.
- **Phone first**, then laptop; no new colours; reuse the existing chips, check rows and deck machinery.
- Nothing is mixed into course transcriptions: new text is labelled `source: Notion cheat sheet`.

## Decisions from review

1. Keep the repo's chapter links (matched by grammar topic). Notion's "Verband" links are not imported.
2. Annotated model answers (issue 06): trial on a couple of tasks first (exam 2 and 9), review with the user before extending.

## Order and verification

Issues 01 → 02 → 03 and 04 (independent after 02) → 05 (deck) → 06 (optional). Each ends with `build`, `validate`, the tests, and a scripted DOM check of the page at 390 px and at laptop width. Update CHANGELOG, OVERVIEW, HANDOFF, TASKS and CLAUDE.md in the last issue.
