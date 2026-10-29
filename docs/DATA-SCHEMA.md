# Data schema and editing rules

## Vocabulary

Canonical vocabulary lives at [`data/vocabulary.csv`](../data/vocabulary.csv). It is UTF-8, comma-delimited, with a header. Use a CSV library to edit it; quoted cells may contain commas or newlines. Canonical grammar notes live under [`data/grammar/`](../data/grammar/README.md).

| Column | Meaning |
| --- | --- |
| id | Stable `VOC-` plus 12 lowercase hexadecimal characters |
| dutch | Word or expression; preserve a complete phrase when it is the study unit |
| english | English meanings, empty when not established by a source |
| article | Article from the source, where applicable |
| word_type | Source's grammatical category |
| forms | Plurals, present-tense forms or other supplied forms |
| auxiliary | Auxiliary and source-specific usage notes |
| participle | Past participle |
| examples | Course examples and explicitly labeled added examples |
| chapters | Semicolon-separated chapter numbers 1–8; may be empty |
| categories | Semicolon-separated study categories |
| notes | Usage notes, conflicts and editorial context |
| source_ids | Semicolon-separated source IDs registered in the manifest |
| occurrence_ids | Semicolon-separated occurrence IDs in the provenance ledger |
| review_status | `needs-review` or `reviewed` |
| reviewed_on | YYYY-MM-DD when reviewed, otherwise empty |

The initial import groups exact terms after Unicode NFC normalization, whitespace normalization and case folding. It does not infer that similar phrases or antonym pairs are the same word. It does not distinguish senses automatically. ` ⟐ ` separates differing values from contributing sources; it is not a claim that those values are interchangeable. Follow the occurrence ledger to recover which value came from which source.

For a new term, `scripts.library.record_id(term)` produces an ID from the normalized term's SHA-256 hash. Keep an existing ID when correcting its spelling. For a deliberately separate sense, use `record_id(term + ' | ' + sense_label)` and record the distinction in notes. Validation rejects ID collisions. IDs do not encode chapter membership.

## Provenance ledger

`sources/vocabulary-occurrences.json` is an array. Each item includes `occurrence_id`, `record_id`, `source_id`, `locator`, `dutch` and the source's fields. Imported occurrences are evidence and remain unchanged. Append a new occurrence for new evidence or a sourced editorial correction. Preserve the original source's wording; place the corrected maintained value in the CSV.

Use stable IDs such as `OCC-` plus 16 hexadecimal characters. A locator should identify a page, sheet, table row or exercise. All occurrence IDs listed by a vocabulary record must exist in the ledger, and their sources must be in that record's source_ids.

## Source manifest

`sources/manifest.json` contains `pages` and `attachments` arrays. A page/source record requires `id`, `title`, `url`, `raw_path`, and `snapshot_path`; both local paths must exist. For new local originals, use a local path for url or document the external source URL. Use a stable ID such as `SRC-20261024-01`. Raw evidence may be a PDF, image, text file or exact retrieval payload. A snapshot is a readable Markdown transcription with page locators and uncertainty markings.

When a binary original is actually added, record `local_path`, `sha256`, and `status: archived` on its attachment entry. Keep original filenames or document any renaming. Attachment `status` values:

| Status | Meaning |
| --- | --- |
| `archived` | Local binary present; SHA-256 recorded and checked by validate |
| `reference-only` | Filename known from import; bytes not yet retrieved (temporary) |
| `unavailable` | Confirmed not retrievable with current tools/exports; see `unavailable_reason` |
| `withheld-public` | Binary intentionally omitted from the public tree |

A source URL is a reference, not a backup.

## Grammar and study notes

Grammar topics use YAML Properties: `id`, `source_ids`, `review_status`, and `reviewed_on` when reviewed. Explain scope and exceptions in the note body. Cite source snapshots using relative links.

Personal answers belong in study notes, separate from canonical rules. Study templates can reference vocabulary IDs and grammar paths. Exercises in course/exams/ retain imported course material and must keep their review status visible.

## Grammar quiz items

[`data/grammar-quiz.json`](../data/grammar-quiz.json) holds authored practice questions for the flashcard page. Each item has `id` (`GQ-NNN`), `note` (path of the grammar note it practises, or `imperfectum`), `question`, `choices`, `answer` (index), `why`, `origin` and `review_status`. `origin` is `course` (restates a rule or example from the note), `constructed` (new example, shown with †), `course-forms` (verb form from the CSV, explained with an external rule) or `external` (standard Dutch the course does not teach; hidden unless unreviewed items are included). Items are AI-drafted and stay `needs-review` until checked.
