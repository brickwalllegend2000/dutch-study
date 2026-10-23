# Dutch Study Implementation Plan

> For agentic workers: execute task by task inline using executing-plans.

**Goal:** Deliver a private GitHub repository usable as an Obsidian vault and searchable by agents, populated from the supplied Dutch study workspace.

**Architecture:** Canonical CSV vocabulary and Markdown grammar; generated vocabulary notes; preserved Notion evidence and source manifest. GitHub Issues and CI support the content lifecycle.

**Tech Stack:** Git, GitHub/gh, Obsidian core plugins, Python 3.11+ standard library.

**Spec:** [Design](../specs/2026-10-23-dutch-study-design.md)

## Global constraints
- Preserve Notion originals; publish only into a private repository.
- Keep stable IDs, source provenance, and draft/review distinctions.
- Use relative Markdown links and no required community plugins.
- Python 3.11+; no external Python dependencies.

## Review focus
- HTML and Markdown table inputs must retain examples and accented characters.
- Repeated words must retain every source occurrence and conflicting values.
- Unavailable scans must be disclosed, not called archived.
- Obsidian and GitHub links must resolve to the same local files.
- Local setup and remote Actions results must be distinguished.

## Task 1: Preserve source evidence
- [x] Fetch all linked Dutch study pages, existing chapter and grammar records, and referenced study tasks without crawling unrelated task parents.
- [x] Persist exact fetched payloads, an inventory and any retrieval failures.
- [x] Check completeness/truncation and identify attachments and unavailable originals.

## Task 2: Canonical library and tools
Files: scripts/library.py, tests/test_library.py, vocabulary.csv, grammar/, chapters/, sources/, views/.
Interfaces: parse_tables(text) -> list[list[list[str]]]; consolidate(occurrences) -> list[dict]; validate(root) -> list[str]; build(root) writes generated reading views.
- [x] Write tests for table parsing, duplicate provenance, CSV roundtrip and validation rejection; run and observe missing implementation failures.
- [x] Implement importer, renderer, search and validator; run tests and complete data validation.
- [x] Generate canonical entries with IDs; link chapters and grammar to evidence.

## Task 3: Daily use and automation
Files: README.md, WORKFLOW.md, AGENTS.md, docs/SETUP.md, docs/MIGRATION.md, .obsidian/, templates/, inbox/, .github/.
- [x] Configure vault and document GitHub Desktop and command-line setup, sync and conflict handling.
- [x] Add issue forms, PR template and validation workflow; verify JSON/YAML and local links.
- [x] Add concrete remaining tasks and source inventory; mark the plan and execution ledger accurately.

## Task 4: Publish and verify
- [ ] Create private GitHub repository, push verified files, configure issues/labels and attempt Project board. Blocked by GitHub CreateRepository permission; publishing script prepared.
- [ ] Create remaining issues with acceptance criteria; record actual links. Five issue definitions are prepared locally.
- [ ] Verify remote privacy, content, commit and Actions execution. Remote steps remain pending; downloadable vault packaging is performed locally.
- [x] Report completed setup and the local steps the user must perform.
