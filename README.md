# Dutch study

Your canonical Dutch study library. This repository is also an Obsidian vault: clone it once and open that same folder in Obsidian.

## Start here

**Publication pending:** the connected GitHub account could not create the repository. You can open this folder in Obsidian now; follow [publishing instructions](docs/PUBLISH.md) to activate GitHub hosting and task tracking.

- [First-time setup](docs/SETUP.md) — GitHub Desktop, Obsidian and synchronization.
- [Daily workflow](WORKFLOW.md) — capture, process, review and save.
- [Vocabulary](views/VOCABULARY.md) · [Perfectum study list](views/PERFECTUM-STUDY-LIST.md) · [All perfectum verbs](views/PERFECTUM.md) · [Irregular verbs](views/IRREGULAR-VERBS.md) · [Needs review](views/NEEDS-REVIEW.md).
- [Grammar](grammar/README.md) · [Chapters](chapters/README.md) · [Practice projects and test](practice/README.md).
- [Study journal](study/README.md) · [Inbox](inbox/README.md).
- [Prepared project backlog](docs/TASKS.md) · [Publish to GitHub](docs/PUBLISH.md).

## What is authoritative?

| Material | Maintained location |
| --- | --- |
| Words, meanings, forms and source references | [vocabulary.csv](vocabulary.csv) |
| Grammar explanations | Markdown files in [grammar](grammar/README.md) |
| Study order and chapter navigation | [chapters](chapters/README.md) |
| Writing projects and mock exam | [practice](practice/README.md) |
| Original import evidence | [source inventory](sources/README.md) |
| Outstanding work and corrections | GitHub Issues |

Files in `views/` are generated from the CSV. Edit the CSV and regenerate; edits to generated notes will be replaced. Source snapshots preserve imported material and may contain older or conflicting versions. Use the canonical files for maintained facts and snapshots to check evidence.

Imported material is marked **needs-review**. Migration checks establish extraction and provenance, not that every Dutch sentence is correct. Original photos remain reference-only until their bytes are added to `sources/originals/`. See the [migration report](docs/MIGRATION.md).

## Use an agent

Give the agent repository access or a local checkout, then say:

> Read AGENTS.md and WORKFLOW.md. Use this repository as the canonical Dutch study library. Search the relevant files before answering, cite record IDs and file paths, and distinguish imported material from reviewed facts.

For changes:

> Process issue #NUMBER following AGENTS.md. Preserve source evidence, update canonical files, regenerate views and run validation. Open a pull request with uncertainties listed for review.

Plain text search works immediately in a checkout. GitHub web/code search availability depends on GitHub indexing and permissions; agents should fall back to reading or searching a local clone.

## Maintenance commands

Python 3.11 or later; no packages to install. Run from this folder:

```bash
python scripts/library.py search vergeten
python scripts/library.py build
python scripts/library.py validate
python -m unittest discover -s tests -v
```

On Windows, use `py` if `python` is unavailable. Reading and studying in Obsidian requires no Python installation.
