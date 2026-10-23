# Repository overview

How this vault is structured, what is authoritative, and the live status as of **2026-10-23** (Europe/Brussels). Prefer this page for orientation; keep [INVENTORY.md](INVENTORY.md) for refreshable counts.

[Home](../README.md) · [Study home](../journal/my-study-view.md) · [Handoff](HANDOFF.md) · [Workflow](../WORKFLOW.md) · [Agents](../AGENTS.md)

---

## What this is

`dutch-study` is a **canonical Dutch study library** that doubles as an **Obsidian vault**. One clone serves GitHub, Obsidian, and agents.

| Role | Location |
| --- | --- |
| Learn | [course/](../course/README.md), [wiki/](../wiki/README.md), [journal/my-study-view.md](../journal/my-study-view.md) |
| Edit facts | [vocabulary.csv](../vocabulary.csv), [wiki/grammar/](../wiki/grammar/README.md) |
| Prove facts | [sources/](../sources/README.md) (manifest, snapshots, originals) |
| Capture later | [inbox/](../inbox/README.md) |
| Automate | [scripts/library.py](../scripts/library.py), CI *Library checks* |

The repository is **public**. Do not commit course passwords or private drafts. The agenda PDF was withheld for that reason; use the [study-safe agenda](../sources/pages/agenda-sept-okt-26.md).

---

## Architecture

```mermaid
flowchart TB
  subgraph maintain["Maintained knowledge"]
    CSV["vocabulary.csv"]
    GRAM["wiki/grammar/*.md"]
    COURSE["course/**"]
  end
  subgraph generate["Generated views"]
    WV["wiki/vocabulary/**"]
  end
  subgraph evidence["Evidence — do not rewrite to match corrections"]
    MAN["sources/manifest.json"]
    OCC["sources/vocabulary-occurrences.json"]
    SNAP["sources/pages/*.md"]
    BIN["sources/originals/**"]
  end
  subgraph personal["Personal"]
    J["journal/"]
    I["inbox/ — deferred captures"]
  end
  CSV -->|build| WV
  OCC --> CSV
  MAN --> SNAP
  MAN --> BIN
  COURSE --> GRAM
  J -.->|mistakes stay personal| COURSE
  I -.->|later import issue| evidence
```

**Ownership rule:** correct a fact in the maintained layer; keep the original wording in evidence. Summaries (review sheets, cheat sheets) must follow CSV/grammar — they add no new facts (mark constructed examples with †).

```mermaid
flowchart LR
  A["Capture in inbox/"] --> B["Source record + snapshot"]
  B --> C{"Term already in CSV?"}
  C -->|same sense| D["Update row + occurrence"]
  C -->|new sense| E["New VOC- id + notes"]
  D --> F["library.py build"]
  E --> F
  F --> G["validate + tests"]
  G --> H["PR / merge"]
```

---

## How to study (short loop)

```mermaid
flowchart TD
  H["Study home"] --> T{"Choose one"}
  T --> W["Written chapter"]
  T --> O["Oral Modeling unit"]
  T --> R["Reference lookup"]
  T --> E["Exam prep"]
  W --> X["Attempt without answer"]
  O --> X
  X --> C["Check source / model"]
  C --> L["Log in journal"]
  L --> N["One next-review action"]
```

Start at [journal/my-study-view.md](../journal/my-study-view.md). Keep personal errors in the journal; open a GitHub Issue only when a **shared** course fact is wrong.

---

## Live status (2026-10-23)

| Area | Status | Detail |
| --- | --- | --- |
| GitHub Issues | **None open** | Starters #1–#5 closed; see [TASKS.md](TASKS.md) |
| Vocabulary | **520** rows | **501** reviewed · **19** needs-review (`[added]` English) |
| Blank English | **0** | All rows have a gloss; 19 are labeled `[added]` |
| Grammar topics | **14 / 14** reviewed | AI/course-snapshot review — not teacher-certified |
| Oral screenshots | **26 archived** | Hashes checked |
| Notion originals | **41 unavailable** (24 names) | [UNAVAILABLE.md](../sources/originals/UNAVAILABLE.md) |
| Agenda PDF | **withheld-public** | [Transcription](../sources/pages/agenda-sept-okt-26.md) |
| Oral snapshot | **Enriched** | Not page-faithful everywhere; see clothing pp. 90–91 note |
| Inbox class notes | **Deferred** | [Capture](../inbox/2026-10-23-class-notes-schriftelijk.md) — process later |
| CI | Green on recent merges | `python scripts/library.py validate` + 26 unit tests |

### Vocabulary by written chapter

A record may belong to more than one chapter; do not sum these as unique totals. **191** records have no written chapter (oral-only / general).

| Ch | Records | Ch | Records |
| --- | ---: | --- | ---: |
| 1 | 62 | 5 | 65 |
| 2 | 54 | 6 | 39 |
| 3 | 7 | 7 | 30 |
| 4 | 64 | 8 | 21 |

Chapter 3’s short list is expected: it reuses verbs/phrases from other chapters.

### Trust caveats

1. **`reviewed` ≠ textbook-page proof** for oral-enriched material until a faithful re-transcription exists.
2. **Cheat sheets / review sheets** can drift; CSV and grammar notes win conflicts.
3. **Public history** may still contain the old agenda PDF; do not re-add credential-bearing binaries.
4. **AI review** of grammar/vocabulary is recorded in notes and [VERIFICATION.md](VERIFICATION.md); it is not a native-speaker or teacher sign-off.

---

## Folder map

| Path | Edit? | Purpose |
| --- | --- | --- |
| `vocabulary.csv` | Yes | Canonical lexicon |
| `wiki/grammar/` | Yes | Canonical explanations |
| `course/` | Yes | Study order, exercises, oral, exams |
| `wiki/vocabulary/` | No — regenerate | Reading views from CSV |
| `wiki/cheat-sheets/`, `course/review/` | Yes, carefully | Summaries of CSV/grammar only |
| `sources/` | Append evidence; never “fix” snapshots to match CSV | Provenance |
| `journal/` | Yes | Personal attempts |
| `inbox/` | Yes | Deferred / unprocessed captures |
| `scripts/`, `tests/` | Yes | Build, validate, search |

---

## Commands

```bash
python scripts/library.py search vergeten          # vocabulary
python scripts/library.py search --all vergeten    # course, grammar, journal, inbox
python scripts/library.py search --sources term    # also source snapshots
python scripts/library.py build
python scripts/library.py validate
python -m unittest discover -s tests -v
```

On Windows use `py` if needed. Obsidian study needs no Python.

---

## Related docs

| Doc | Use when |
| --- | --- |
| [HANDOFF.md](HANDOFF.md) | Starting a new agent or human session |
| [INVENTORY.md](INVENTORY.md) | Refreshing counts |
| [DATA-SCHEMA.md](DATA-SCHEMA.md) | Adding vocabulary or sources |
| [MIGRATION.md](MIGRATION.md) | Historical Notion import baseline only |
| [VERIFICATION.md](VERIFICATION.md) | What automated checks do and do not prove |
| [SETUP.md](SETUP.md) | Desktop Obsidian + Git |
| [AGENTS.md](../AGENTS.md) | Rules for automated edits |
