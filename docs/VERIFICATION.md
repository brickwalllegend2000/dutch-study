# Verification — 2026-10-23

- `python -m unittest discover -s tests -v`: 21 tests passed (unit test suite includes unlinked course page and cheat sheet tests, attachment hashes, CSV roundtrip, and bidirectional provenance).
- `python scripts/library.py validate`: 520 canonical vocabulary records validated; source IDs, occurrence coverage in both directions, relative links and generated freshness are consistent.
- `python scripts/library.py build`: 533 reading views generated.
- `git diff --check`: no whitespace errors.
- `python -m py_compile scripts/library.py scripts/import_notion.py scripts/publish_github.py`: passed.
- Obsidian JSON and GitHub YAML configuration files parse successfully.
- Pull Requests #13 (`exam-prep-and-descriptions`) and #14 (`oral-track-and-wiki-integration`) merged into `main` with 100% green GitHub Actions CI runs (`Library checks/validate`).
- Complete oral track curriculum (*Zo Gezegd 1.2 — Mondeling*, Themas 1–7) transcribed with core vocabulary, conversational frames, grammar focus, self-assessment goals, and exam review sections.
- Compact Exam Preparation guide ([`course/exams/exam-preparation.md`](../course/exams/exam-preparation.md)) and Master Descriptions cheat sheet ([`wiki/cheat-sheets/descriptions.md`](../wiki/cheat-sheets/descriptions.md)) integrated and cross-referenced.
- One independent final review completed; all reported defects were addressed. Regression tests were observed failing before the fixes and passing afterward.

The publishing script's local checks and guardrails are tested. Update: the repository was created and pushed, five starter issues were created, and GitHub Actions CI runs are verified green. Local Obsidian app behavior must be confirmed on the user's computer; configuration and internal links are checked here.

Content migration checks do not establish linguistic correctness. All imported study records retain needs-review status. Original scans are reference-only until their binary files are archived.
