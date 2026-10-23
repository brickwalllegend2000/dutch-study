# Dutch study

Canonical Dutch study library on GitHub. Study and maintain it here first (browser, editor, Issues, PRs). An Obsidian export vault is **not** part of this repository right now.

## Start here

**Open study home:** [journal/my-study-view.md](journal/my-study-view.md) — continue, practise writing or speaking, look things up, or log mistakes.

**Understand the library:** [docs/OVERVIEW.md](docs/OVERVIEW.md) — architecture, data flow, wiki vs course, setup, and live status.  
**Next session:** [docs/HANDOFF.md](docs/HANDOFF.md). · **Clone / Git setup:** [docs/SETUP.md](docs/SETUP.md).

**Hosted on GitHub:** `brickwalllegend2000/dutch-study` is a **public** repository. Treat anything committed here as public. Course Moodle credentials must not be stored in this tree.

### Learner links

- [Study home](journal/my-study-view.md)
- [Course and wiki view](course/view.md)
- [Vocabulary](views/vocabulary/VOCABULARY.md) · [Perfectum study list](views/vocabulary/PERFECTUM-STUDY-LIST.md) · [Needs review](views/vocabulary/NEEDS-REVIEW.md)
- [Grammar](data/grammar/README.md) · [Chapters](course/README.md) · [Oral track](course/oral/README.md)
- [Exam preparation](course/exams/exam-preparation.md) · [Practice tests](course/exams/README.md)
- [Review sheets](course/review/README.md) · [Cheat sheets](wiki/cheat-sheets/README.md)

### Maintenance links

- [Overview & status](docs/OVERVIEW.md) · [Inventory](docs/INVENTORY.md) · [Handoff](docs/HANDOFF.md)
- [Daily workflow](WORKFLOW.md) · [Setup](docs/SETUP.md) · [Tasks](docs/TASKS.md)
- [START-HERE](START-HERE.md) · [Changelog](CHANGELOG.md) · [Inbox (deferred)](inbox/README.md)

## Layout

| Folder | Purpose |
| --- | --- |
| [data](data/grammar/README.md) | **Facts** — [vocabulary.csv](data/vocabulary.csv) and [grammar notes](data/grammar/README.md) |
| [course](course/README.md) | **Authored study** — chapters 1–8, oral guides, exercises, review sheets, exams |
| [wiki](wiki/README.md) | Generated vocabulary views + authored cheat sheets (grammar facts live under `data/`) |
| [journal](journal/README.md) | Personal study notes and study home |
| [inbox](inbox/README.md) | Captures waiting or **deferred** |
| [sources](sources/README.md) | Import evidence — never reorganized to match corrections |

## What is authoritative?

| Material | Maintained location |
| --- | --- |
| Words, meanings, forms, provenance | [data/vocabulary.csv](data/vocabulary.csv) |
| Grammar explanations | [data/grammar](data/grammar/README.md) |
| Study order | [course](course/README.md) |
| Evidence | [sources](sources/README.md) |
| Outstanding work | [GitHub Issues](https://github.com/brickwalllegend2000/dutch-study/issues) (currently none open) |

`views/vocabulary/` is **generated** from the CSV. Edit `data/vocabulary.csv` and run `build`. Cheat sheets and review sheets summarize facts; they add no new ones. Source snapshots may conflict with maintained facts — keep conflicts visible.

Status snapshot: **520** vocabulary rows (**501** reviewed, **19** needs-review); **14** grammar topics reviewed; inbox class notes **deferred**. Details in [OVERVIEW.md](docs/OVERVIEW.md).

## Use an agent

Rules: [AGENTS.md](AGENTS.md). Suggested start:

> Read AGENTS.md, docs/OVERVIEW.md, and docs/HANDOFF.md. Use this repository as the canonical Dutch study library on GitHub. Search before answering, cite VOC- ids and paths, and defer the inbox class-notes capture unless asked to process it.

## Maintenance commands

Python 3.11+; no packages. From this folder:

```bash
python scripts/library.py search vergeten
python scripts/library.py search --all vergeten
python scripts/library.py search --sources vergeten
python scripts/library.py build
python scripts/library.py validate
python -m unittest discover -s tests -v
```

On Windows, use `py` if needed. Reading Markdown on GitHub needs no Python.
