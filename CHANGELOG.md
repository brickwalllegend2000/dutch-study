# Changelog

Dated record of merged changes to the library, newest first. Each entry names the source branch.

## 2026-10-23 — Reorganize generated vocabulary views to views/ (`task/refactor-views-layer-split`)

- Moved `wiki/vocabulary/` → `views/vocabulary/` with `git mv` so `wiki/` contains only authored summaries and cheat sheets.
- Updated `scripts/library.py` with `VIEWS = 'views/vocabulary'` and regenerated reading views.
- Updated inbound links across `course/`, `data/grammar/`, `wiki/`, `journal/`, and orientation docs (`README.md`, `START-HERE.md`, `WORKFLOW.md`, `AGENTS.md`, `docs/OVERVIEW.md`, `docs/HANDOFF.md`).
- Validation (520 vocabulary records) and all 30 tests pass cleanly.

## 2026-10-23 — Remove Obsidian; GitHub-first library (`cursor/remove-obsidian-30a6`)

- Deleted `.obsidian/` config; repository is no longer an Obsidian vault.
- Reframes README, START-HERE, SETUP, OVERVIEW, WORKFLOW, AGENTS, HANDOFF, wiki index, and templates as GitHub-first Markdown study.
- `publish_github.py` descriptions no longer mention Obsidian. A future export vault may be added later; not present now.

## 2026-10-23 — Data architecture and information flow (`cursor/data-architecture-flow-2c41`)

- Expanded `docs/OVERVIEW.md` with entity model (ER), write/read paths, consolidation rules, and provenance audit steps. Links from handoff.

## 2026-10-23 — Overview, status, handoff; defer inbox (`cursor/overview-status-handoff-2c41`)

- Added `docs/OVERVIEW.md` (architecture mermaid diagrams, ownership, live status) and `docs/HANDOFF.md` for the next session.
- Deferred inbox class notes; updated README, START-HERE, TASKS, INVENTORY, AGENTS.
- No open GitHub Issues; suggested future work listed in TASKS/HANDOFF only.

## 2026-10-23 — Clear completed task inventory (`cursor/clear-completed-tasks-2c41`)

- Updated `docs/TASKS.md` and `.github/bootstrap.json`: no open starter issues remain; bootstrap no longer re-creates the five closed starters on publish.
- GitHub closed issues #1–#5 and #15 could not be deleted (integration lacks `delete_issue`).

## 2026-10-23 — Close remaining starter issues (`cursor/close-remaining-issues-2c41`)

- Issue #1: marked 41 Notion attachment refs (24 filenames) `unavailable` with reasons; added `sources/originals/UNAVAILABLE.md`.
- Issue #3: grammar reviews already on main via PR #19 (all 14 topic notes `reviewed`).
- Issue #4: cloud-side sync/link verification note; desktop Obsidian steps documented as optional user follow-up.
- Issue #5: first perfectum study session note with 10 verbs and auxiliary checks.

## 2026-10-23 — Vocabulary review onto post-remediation main (`task/2-vocabulary-review`, PR #17)

- Merged #17 after #18/#19: filled previously blank English meanings, resolved auxiliary variants, marked checked records reviewed (AI review notes; not teacher-certified).
- Preserved PR #18 oral-enrichment provenance notes and example/forms appends on overlapping rows.
- Regenerated vocabulary views. 19 rows remain needs-review where English is labeled `[added]`.

## 2026-10-23 — Review remediation: trust, public safety, study route (`cursor/review-trust-and-workflow-2c41`)

- Confirmed repository visibility is **public**; corrected docs that called it private.
- Removed the course agenda PDF from the tree (embedded Moodle class-code/password instructions). Added study-safe transcription `sources/pages/agenda-sept-okt-26.md`, a notice file, gitignore rules, and a manifest source/attachment record (`withheld-public`).
- Cleared the personal freeform draft from `inbox/README.md`; listed the unprocessed class-notes capture.
- Labeled the oral snapshot as an enriched reconstruction; documented pp. 90–91 clothing discrepancies against archived screenshots.
- Restored 16 blank English glosses from the irregular-verbs supplement; reconciled selected oral English/examples/forms; noted the clothing “suits” sense of *staan* without merging senses.
- Added `docs/INVENTORY.md` and dated the migration report as historical; designated [Study home](journal/my-study-view.md) as the learner entry.
- Verb study lists now show auxiliary and participle. Validation: UTF-8 JSON reads, CSV row width, unexpected generated files, grammar frontmatter, archived binary format. Search `--all` is maintained-first; `--sources` opts into snapshots; inbox is searchable. Publishing credential-helper setup is idempotent.
- Fixed editorial drift in review index, describing-things (*zitten*), T-shirt cheat-sheet link, exam-prep action-verb note, and example-2 *gaan* label.

## 2026-10-23 — Oral track curriculum and wiki integration (`oral-track-and-wiki-integration`, PR #14)

- Added `course/oral/README.md`: dedicated oral track hub with curriculum overview, speaking practice guidance, and a detailed *Schriftelijk (S)* vs. *Mondeling (M)* curriculum alignment matrix.
- Enriched all 7 oral units (`course/oral/modeling-01.md` to `modeling-07.md`) with transcribed vocabulary tables, conversational frames, grammar focus, *Dit kan ik!* checklists, speaking roleplay prompts, and Section 6: Review & Exam Connections.
- Added new canonical grammar notes: `wiki/grammar/continuous-aspect-aan-het.md` (*zijn + aan het + infinitief*) and `wiki/grammar/infinitive-clauses-om-te.md` (*om te + infinitief*).
- Cross-referenced oral modules across `wiki/cheat-sheets/` (perfectum, verb + infinitive, word order, adjectives, negation and er, descriptions) and `wiki/grammar/README.md`.
- Imported 108 new vocabulary records from *Zo Gezegd 1.2 Mondeling* (`SRC-ZG12M-20261023`) into `vocabulary.csv` (bringing total vocabulary to 520 records); regenerated all reading views in `wiki/vocabulary/`.
- Verified with 21 unit tests and full repository validation. Merged in PR #14.

## 2026-10-23 — Exam preparation guide and master descriptions cheat sheet (`exam-prep-and-descriptions`, PR #13)

- Added `course/exams/exam-preparation.md`: compact revision guide based on the official course agenda, featuring 5 core writing prompts (person, home/room, personal message, trip, lost object), a 4-step self-correction checklist, a grammar priority checklist, and dated exam schedule (written exam 23 Oct, oral exams 26–27 Oct, NT2 test 29 Oct).
- Added `wiki/cheat-sheets/descriptions.md`: master reference for descriptions covering personal appearance, clothing, body, materials, spatial prepositions, action vs. position verbs, and room layout blueprints.
- Added action vs. position verbs distinction to `wiki/cheat-sheets/negation-and-er.md` and updated `wiki/grammar/using-er-there-is-there-are.md`.
- Archived and symlinked the official course calendar PDF at `sources/originals/agenda-sept-okt-26.pdf` (later withheld from the public tree; see 2026-10-23 review remediation).
- Cross-linked exam preparation and descriptions guide from `README.md`, `course/README.md`, `wiki/README.md`, and relevant grammar notes. Merged in PR #13.

## 2026-10-23 — Course practice, overview and view

- Added `course/wat-doe-jij-elke-dag.md` (Chapter 2 daily-routine practice) and `course/instructies-geven.md` (Chapter 3 instructions practice). Linked from chapter guides, review sheets and course README. Cross-linked to wiki grammar (perfectum, gaan + infinitive, word order, modals).
- Added course- and wiki-sourced examples to both practice notes and expanded the comparisons section in `course/describing-things.md` (regular/irregular tables, course examples from chapters 4 and 8).
- Added `course/describing-things.md`: course-wide synthesis of describing things, adjectives, locations and instructions (chapters 3–5, 7, 8; Modeling 5).
- Added `course/view.md`: single course and wiki view for browser/GitHub. Linked from main README and course README. Includes exam preparation.
- Wiki grammar pages (perfectum, gaan + infinitive, word order, modals) link back to the practice notes. `sources/` and `vocabulary.csv` unchanged. All new material is needs-review.

## 2026-10-23 — Worked examples (`claude/project-thread-7mmc4d`)

- Added `course/examples/` with two completed model texts planned on the Notion page *Example ideas* (read through the Notion connector; not in `sources/`): *Waar ik woon* (chapters 4, 5, 3, 1: flat, rooms, house rules, wardrobe) and *Een reis naar Oostenrijk* (chapters 2, 8, 6, 7: city trip, football match, e-mails, lost bag). Each part has a task, a model text, an English meaning, the grammar it practises with links, and a table of course vocabulary records used. Words outside the course vocabulary are listed. Generated by Claude and not reviewed by a native speaker.
- `course/README.md` and the exercises index link the examples. `sources/` and `vocabulary.csv` are unchanged.

## 2026-10-23 — Review sheets and cheat sheets (`claude/project-thread-3w918c`)

- Added `course/review/` with a review sheet for each written chapter (1–8) and an index: key vocabulary copied from `vocabulary.csv` (grouped by category, linked to word pages, with auxiliary and participle for verbs), the grammar to know, a *Watch out* list derived from the course rules and writing tips, the *Dit kan ik!* goals and the course grammar that has no maintained note yet.
- Added `wiki/cheat-sheets/` with five one-page grammar summaries (perfectum, verb + infinitive, word order, adjectives and comparisons, negation and *er*) and an index. They condense `wiki/grammar/` and, in places, the preserved master grammar reference and perfectum study notes.
- Sheets add no facts; examples written for them (mostly the ✗ forms in *Watch out*) are marked † and unverified. Everything is needs-review.
- Chapter guides link their review sheet and cheat sheets; grammar notes link their cheat sheet and chapter review sheets; the course, wiki, grammar and home indexes link both. `validate` now also reports orphan cheat sheets, and `search --all` searches them. `sources/` is unchanged.

## 2026-10-23 — Chapter exercises (`claude/project-thread-35p9h9`)

- Added `course/exercises/` with one page per written chapter (1–8) and an index. Exercise wording, writing tips, adapted practice and answers come from the Notion chapter pages, read from the retrieval payloads in `sources/notion/` because the Markdown snapshots fold the Practice sections into a link label. Each page separates workbook wording from practice written for the study page and lists missing material; all content is unreviewed.
- Chapter guides link their exercises page next to the preserved chapter text, and the study-session step points to it. `course/README.md` links the exercises index. `sources/` is unchanged.

## 2026-10-23 — Search everything (`claude/project-thread-nasid3`)

- `python scripts/library.py search --all TERM` searches vocabulary plus the Markdown in `wiki/grammar/`, `course/`, `journal/` and `sources/pages/`, printing matching lines grouped by file. Plain `search` is unchanged (vocabulary only).
- Piping search output into another command (for example `head`) no longer prints a BrokenPipeError.

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
