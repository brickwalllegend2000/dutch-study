# Dutch study

Your canonical Dutch study library. This repository is also an Obsidian vault: clone it once and open that same folder in Obsidian.

## Start here

**Hosted on GitHub:** this vault now lives in the private repository `brickwalllegend2000/dutch-study`. Clone it and open the folder in Obsidian. Starter tasks and labels exist as GitHub Issues; milestones and the optional Project board are not created yet, see [publishing instructions](docs/PUBLISH.md).

- [My study view](journal/my-study-view.md) — personal dashboard (viewable on GitHub).
- [What was imported](START-HERE.md) — first-run notes and import summary.
- [First-time setup](docs/SETUP.md) — GitHub Desktop, Obsidian and synchronization.
- [Daily workflow](WORKFLOW.md) — capture, process, review and save.
- [Vocabulary](wiki/vocabulary/VOCABULARY.md) · [Perfectum study list](wiki/vocabulary/PERFECTUM-STUDY-LIST.md) · [All perfectum verbs](wiki/vocabulary/PERFECTUM.md) · [Irregular verbs](wiki/vocabulary/IRREGULAR-VERBS.md) · [Needs review](wiki/vocabulary/NEEDS-REVIEW.md).
- [Grammar](wiki/grammar/README.md) · [Chapters](course/README.md) · [Practice tests](course/exams/README.md) · [Exam preparation](course/exams/exam-preparation.md).
- [Review sheets](course/review/README.md) per chapter · [Cheat sheets](wiki/cheat-sheets/README.md) ([descriptions & room layout](wiki/cheat-sheets/descriptions.md)).
- [Study journal](journal/README.md) · [Inbox](inbox/README.md).
- [Prepared project backlog](docs/TASKS.md) · [Publish to GitHub](docs/PUBLISH.md) · [Changelog](CHANGELOG.md).

## Layout

| Folder | Purpose |
| --- | --- |
| [course](course/README.md) | The course: written chapters 1-8, oral guides in `course/oral/`, exercises in `course/exercises/`, review sheets in `course/review/`, practice tests and [exam preparation](course/exams/exam-preparation.md) in `course/exams/`. |
| [wiki](wiki/README.md) | Reference you look things up in: grammar topics, grammar cheat sheets and vocabulary lists (generated from the CSV). |
| [journal](journal/README.md) | Your own study notes. |
| [inbox](inbox/README.md) | New material waiting to be processed. |
| [sources](sources/README.md) | Preserved import evidence. Never reorganized. |

## What is authoritative?

| Material | Maintained location |
| --- | --- |
| Words, meanings, forms and source references | [vocabulary.csv](vocabulary.csv) |
| Grammar explanations | Markdown files in [wiki/grammar](wiki/grammar/README.md) |
| Study order and chapter navigation | [course](course/README.md) |
| Practice tests and mock exam | [course/exams](course/exams/README.md) |
| Original import evidence | [source inventory](sources/README.md) |
| Outstanding work and corrections | GitHub Issues |

Files in `wiki/vocabulary/` are generated from the CSV. Edit the CSV and regenerate; edits to generated notes will be replaced. Source snapshots preserve imported material and may contain older or conflicting versions. Use the canonical files for maintained facts and snapshots to check evidence.

Imported material is marked **needs-review**. Migration checks establish extraction and provenance, not that every Dutch sentence is correct. Original photos remain reference-only until their bytes are added to `sources/originals/`. See the [migration report](docs/MIGRATION.md).

## Use an agent

Agent rules are in [AGENTS.md](AGENTS.md). Give the agent repository access or a local checkout, then say:

> Read AGENTS.md and WORKFLOW.md. Use this repository as the canonical Dutch study library. Search the relevant files before answering, cite record IDs and file paths, and distinguish imported material from reviewed facts.

For changes:

> Process issue #NUMBER following AGENTS.md. Preserve source evidence, update canonical files, regenerate views and run validation. Open a pull request with uncertainties listed for review.

Plain text search works immediately in a checkout. GitHub web/code search availability depends on GitHub indexing and permissions; agents should fall back to reading or searching a local clone.

## Maintenance commands

Python 3.11 or later; no packages to install. Run from this folder:

```bash
python scripts/library.py search vergeten
python scripts/library.py search --all vergeten
python scripts/library.py build
python scripts/library.py validate
python -m unittest discover -s tests -v
```

`search` looks up words in vocabulary.csv. `search --all` also searches the grammar notes and cheat sheets, course chapters, oral guides, exams, your journal and the imported source pages, and lists each matching line under its file. Searches ignore upper and lower case.

On Windows, use `py` if `python` is unavailable. Reading and studying in Obsidian requires no Python installation.
