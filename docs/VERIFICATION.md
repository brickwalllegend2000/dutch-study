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

Content migration checks do not establish linguistic correctness. Original scans are reference-only until their binary files are archived.

## Review pass — 2026-10-23 (issues #2 and #3)

- **Who reviewed:** an AI agent (Claude), against the source snapshots and general standard-Dutch knowledge. This is not a teacher or native-speaker review. Transcriptions were not compared with the original photos, because those binaries are not archived (issue #1).
- **Grammar (#3):** the 10 notes still marked needs-review were checked for rules, word order, auxiliary choice and regional usage; each now has a labeled review note and status reviewed. No rule text changed. All 12 imported topics are now reviewed.
- **Vocabulary (#2):** all 412 needs-review rows were read for meaning, article, forms, auxiliary, participle and examples. 393 are now reviewed. 19 stay needs-review because their English meaning was added by the AI reviewer (labeled `[added]`) and is not in the course sources.
- **Missing English meanings:** all 54 filled. 35 reuse the course's own English from a sibling entry or the writing-steps snapshot; 19 are labeled `[added]`.
- **Variants:** four auxiliary conflicts (lopen, rijden, zwemmen, vergeten) merged to hebben / zijn with an explanation; source occurrences are unchanged.
- **Corrected:** one ungrammatical source example (*met bolletjes*); the original stays in the occurrence ledger.
- **Not split:** *dragen* (wear / carry) and *lenen* (borrow / lend) are documented in the record notes as proposed splits. Near-duplicate and antonym-pair entries are cross-referenced, not merged.
- Results: `library.py build` 533 views, `library.py validate` 520 records OK, 21 tests pass.
