# Changelog

Dated record of merged changes to the library, newest first. Each entry names the source branch.

## 2026-10-23 — Internal links and chapter homepages (`claude/project-thread-bb64in`)

- Chapter guides 1–8 now list the course's own grammar points from the table of contents (as the oral guides already did) above the maintained grammar notes, and add the missing notes: perfectum (chapters 1, 3, 4, 5, 6, 8) and modal verbs (chapter 2, *kunnen + infinitief*). Chapters 1–6 gain their *Dit kan ik!* can-do goals; chapters 7–8 say none were imported.
- Previous/next navigation and a Chapters link on every chapter and oral guide; links to the journal, study-session template and practice tests.
- Each grammar topic links back to the chapters and oral guides that use it, and the grammar index lists them. Generated chapter vocabulary pages link back to their chapter guide.
- `course/README.md` lists the practice tests; README links START-HERE, AGENTS and the changelog.
- `python scripts/library.py validate` now also fails when a page in `course/` or `wiki/grammar/` has no inbound link.

## 2026-10-23 — Course and wiki layout (`claude/project-thread-c3lipk`)

- Moved `chapters/` to `course/` (oral guides in `course/oral/`), `practice/` to `course/exams/`, `grammar/` and `views/` to `wiki/grammar/` and `wiki/vocabulary/`, and `study/` to `journal/`, with `git mv` so history follows. Added `wiki/README.md` and a layout table in the README.
- `scripts/library.py` now generates views into `wiki/vocabulary/`; relative links across the repo were rewritten (including link targets inside `sources/pages/` snapshots; snapshot text is otherwise unchanged). `scripts/import_notion.py` is a frozen one-time utility and still names the old paths.
- `vocabulary.csv`, word IDs and `sources/` paths are unchanged. Chapters remain one file each.

## 2026-10-23 — Remove combined projects (`remove-combined-projects`)

- Removed the user-authored Combined projects page, Projects A–C and exercises A1–C3 from `practice/` (13 pages), together with their 13 source snapshots in `sources/pages/` and payloads in `sources/notion/` (39 files), because they are not reference sources.
- Removed their entries from `sources/manifest.json`, `sources/README.md` and `practice/README.md`; replaced the link in the "Dutch study" source snapshot with a "page removed" note so no link dangles.
- Updated wording that described the removed projects: README practice link and table row, and the import summary and counts in `START-HERE.md` (41 source snapshots, 24 unretrieved image filenames).

## 2026-10-23 — Practice tests page (`add-practice-tests`)

- Added `practice/practice-tests.md` (extra exercises, CVO writing test, Schrijven A2 material) and linked it from `practice/README.md`.
- Added source snapshot `sources/pages/401f89e5e0fc80d68f96f8ba4fa251d8.md`, its retrieval payload in `sources/notion/`, a manifest entry and three reference-only image attachments; listed them in `sources/README.md`.

## 2026-10-23 — Oral chapter guides (`add-oral-chapters`)

- Added seven oral-track (luisteren/spreken) guides, `chapters/modeling-01.md` to `chapters/modeling-07.md`, built from the Inhoudstafel Zo gezegd 1.2 source snapshot.
- Added written-track skill sections to chapters 1–8 and linked the oral guides from `chapters/README.md`.
