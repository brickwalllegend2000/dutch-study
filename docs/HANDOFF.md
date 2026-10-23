# Handoff — dutch-study

**Date:** 2026-10-23 (Europe/Brussels)  
**Repo:** `brickwalllegend2000/dutch-study` (public)  
**Branch tip after this work:** see latest `main`  
**Audience:** next human or agent session

Read first: [OVERVIEW.md](OVERVIEW.md) · [AGENTS.md](../AGENTS.md) · [WORKFLOW.md](../WORKFLOW.md)

---

## Session outcome (this run family)

1. Comprehensive library review acted on (public safety, oral evidence labels, stranded glosses, validation, study home).
2. Open PRs #17–#20 merged; starter Issues #1–#5 closed.
3. Closed GitHub Issues **cannot be deleted** by this integration (`deleteIssue` FORBIDDEN).
4. Starter bootstrap cleared; [TASKS.md](TASKS.md) shows no open Issues.
5. Inbox class notes **deferred** (do not process unless asked).
6. Orientation docs expanded: this handoff + [OVERVIEW.md](OVERVIEW.md) (architecture, data flow, wiki vs course, setup).
7. **Obsidian removed** from the repository (`.obsidian/` deleted; docs are GitHub-first). A future export vault may be added later; do not restore Obsidian config unless asked.

---

## Current state

| Item | Value |
| --- | --- |
| Open GitHub Issues | **0** |
| Vocabulary | 520 (501 reviewed, 19 needs-review with `[added]` English) |
| Grammar notes | 14 reviewed (AI / course-snapshot; not teacher-certified) |
| Validate + tests | Expect green on `main` |
| Obsidian | **Removed** — study on GitHub / Markdown editors |
| Deferred | `inbox/2026-10-23-class-notes-schriftelijk.md` |

---

## Do next (recommended order)

Only if the user asks — otherwise study as-is.

1. **Layering / export vault** — optional later: `data/` + generated `vault/` for Obsidian; not active now.
2. **Process deferred inbox** — when ready: Import material Issue → source record → reconcile with CSV (learner notes contain errors; do not promote mistakes as course facts).
3. **Faithful oral re-transcription** — reconcile `sources/pages/zo-gezegd-1-2-mondeling.md` theme-by-theme against `sources/originals/mondeling-1-2/*.png`; demote unreliable `reviewed` claims.
4. **Teacher pass on 19 `[added]` glosses** — confirm or replace; then mark reviewed with a human note.
5. **Visibility / history** — consider private repo + history purge if agenda credentials in old commits matter.
6. **Delete closed Issues** — only with a GitHub admin account (UI or GraphQL `deleteIssue`).

---

## Do not

- Rerun `scripts/import_notion.py` against this library (refuses to overwrite CSV; one-time tool).
- Edit `wiki/vocabulary/` by hand — edit CSV, then `build`.
- Rewrite source snapshots to match CSV corrections.
- Re-commit agenda PDF or Moodle passwords.
- Treat `reviewed` as native-speaker certification.
- Process deferred inbox into canonical files without an explicit request.
- Re-add `.obsidian/` unless the user explicitly wants an Obsidian export again.

---

## Agent prompt (copy)

```
Read AGENTS.md, docs/OVERVIEW.md, and docs/HANDOFF.md.
Use this repository as the canonical Dutch study library on GitHub.
Search maintained files before answering; cite VOC- ids and paths.
Distinguish imported / [added] / reviewed facts.
Defer inbox/2026-10-23-class-notes-schriftelijk.md unless the user asks to process it.
Do not restore Obsidian config unless asked.
After content changes: build, validate, tests; open a PR.
```

---

## Key paths

| Path | Why |
| --- | --- |
| [docs/OVERVIEW.md](OVERVIEW.md) | Architecture, data flow, wiki vs course, setup, status |
| [docs/SETUP.md](SETUP.md) | Clone and Git sync |
| [wiki/README.md](../wiki/README.md) | Reference layer index |
| [docs/DATA-SCHEMA.md](DATA-SCHEMA.md) | Column and ID rules |
| [journal/my-study-view.md](../journal/my-study-view.md) | Learner entry |
| [vocabulary.csv](../vocabulary.csv) | Lexicon |
| [sources/pages/zo-gezegd-1-2-mondeling.md](../sources/pages/zo-gezegd-1-2-mondeling.md) | Oral evidence (enriched) |
| [inbox/README.md](../inbox/README.md) | Deferred captures |
| [docs/INVENTORY.md](INVENTORY.md) | Refresh counts |

---

## Skills / tools note

Python 3.11+ stdlib only for library scripts. No app server. No Obsidian dependency.
