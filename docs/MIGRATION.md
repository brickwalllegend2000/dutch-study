# Migration report — 2026-10-23

## Imported

- 53 Notion pages preserved as exact fetched JSON payloads and readable Markdown snapshots.
- All eight chapter records and all 12 grammar-topic records from the existing grammar database.
- 302 occurrences from the chapter-organized master vocabulary table.
- All 80 entries from the perfectum study task, plus all 68 entries from the irregular-verbs reference.
- Chapter vocabulary tables containing English meanings, master-table meaning supplements and separable-verb supplements.
- 768 source occurrences consolidated into 412 exact-term vocabulary records.
- Combined writing projects, their nine exercise pages, and the mock exam.

## Consolidation decisions

Exact normalized terms are grouped; all source occurrences are preserved. Different values are separated by ` ⟐ ` in the CSV and generated notes. No automatic linguistic adjudication or sense splitting was performed. Near-duplicate phrases and antonym pairs remain separate until review. This prioritizes evidence preservation; the review queue includes records needing editorial cleanup.

The maintained chapter guides link to generated vocabulary and the existing grammar topics. Original chapter exercises remain accessible through preserved readable snapshots. The imported master grammar reference remains a source snapshot; the 12 maintained grammar-topic notes are authoritative going forward.

## Coverage and limitations

The traversal covered the Dutch study root, linked chapters, references, writing projects and exercise pages, and relevant maintenance tasks. It did not crawl unrelated To Do List parents or copy database-view configurations. The 12 grammar records were enumerated through their data source with has_more=false. Fetched page responses contain closing content blocks; no response reported truncation or unknown blocks. This is retrieval coverage, not independent proof of transcription accuracy or completeness of the original course.

41 attachment references mention 24 distinct original filenames, including the four perfectum photos. No original binary files were downloaded: fetched image references use Notion file-block URIs, and the attachment tool only downloads integration-created text attachments. Images in Obsidian therefore remain source references until the originals are supplied or exported. Their transcribed text is available where present in Notion.

The four perfectum images were previously transcribed in the source task. This import preserves that transcription and its source claims; it did not visually recheck the photos. Generated mock-exam listening text is not an imported audio recording.

All imported vocabulary and grammar remain needs-review. No claim is made that source wording, translations, regional usage, auxiliary choices or grammar examples have been independently verified.

## Acceptance checks

Automated checks cover source references, ID uniqueness, CSV schema, occurrence references, local links, and generated-file freshness. Tests cover parser behavior, preservation of variants, stable IDs and CSV quoting. Remote verification of the Actions run is still pending. Inspect the GitHub Actions Library checks run.

## Remaining work

1. Archive the 24 referenced original filenames and record local paths and hashes.
2. Review vocabulary variants, article differences and distinct word senses.
3. Check grammar and examples against course sources, then mark reviewed items.
4. Open the local clone in Obsidian and complete a first study session.

Notion pages were not edited or deleted. GitHub is the maintained location for subsequent changes; use Notion as historical evidence until migration review is complete.
