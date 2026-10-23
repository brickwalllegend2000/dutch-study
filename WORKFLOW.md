# Ongoing workflow

The process lives here. GitHub Issues hold tasks and their status. The local clone holds the study content; Obsidian edits those same files.

## Daily study

1. In GitHub Desktop, fetch and pull before editing. Resolve any uncommitted changes before pulling.
2. Open README in Obsidian; choose a chapter, vocabulary list or practice task.
3. Make a study note in `study/` using the Study Session template. Keep your answers and personal mistakes here rather than changing course facts.
4. Capture uncertain facts as a GitHub correction issue. Link the relevant word ID or grammar file.
5. When finished, review changed files in GitHub Desktop, commit with a meaningful summary and push. Wait for a green Library checks run when changing canonical content.

Obsidian saves locally; saving is not a GitHub push. Fetch/pull on the next device before editing. Use one device at a time for the same note.

## New course material

1. Put the original file into `inbox/`. Create an Import material issue describing the chapter and desired outcome.
2. An agent or you creates a source record in `sources/manifest.json`, preserves the original in `sources/originals/`, and writes a readable transcription in `sources/pages/`. Use a stable source ID, filename and page/sheet locators. Follow the [data schema](docs/DATA-SCHEMA.md).
3. Check existing vocabulary and grammar before adding records. Update an existing record when the term and sense match; retain separate records for distinct senses when needed. Document any proposed split rather than silently merging senses.
4. Add source occurrences to `sources/vocabulary-occurrences.json`; update `vocabulary.csv` or the maintained grammar file. Preserve variants and label any added interpretation.
5. Run `python scripts/library.py build`, `python scripts/library.py validate`, and `python -m unittest discover -s tests -v`.
6. Submit substantial imports and corrections through a branch and pull request. Include coverage counts, source locations and unresolved questions. After review, merge and close the issue.
7. Move processed inbox material to its permanent source location. Do not remove source evidence.

## Review material

- `needs-review` means imported or changed and not yet linguistically checked.
- Set a vocabulary row to `reviewed` only after checking its meaning, forms, examples and source context; enter `reviewed_on` as YYYY-MM-DD.
- For grammar, update `review_status` in the note's Properties and add `reviewed_on` and a short review note.
- Different auxiliary verbs may express different meanings or sentence structures. Check each source occurrence before combining or generalizing them.
- Preserve a printed error in the source snapshot; correct the maintained record with an explanation and evidence.

## Work status

Use one GitHub status label per open issue: `status:backlog`, `status:in-progress`, or `status:review`. Closed issues are Done. The Project board provides an overview; label-filtered issue searches remain usable if the board is unavailable. Update board status when moving work.

## Weekly maintenance

Triage the inbox, review open corrections, verify that changes have been pushed, and check Library checks. Git history records changes. Keep a separate periodic backup of the local vault, including source originals. GitHub stores committed files, not uncommitted or ignored local state.

## Conflict recovery

If GitHub Desktop reports a conflict, open the conflicting files and compare both versions. Keep valid changes from both sides; ask an agent for help with CSV conflicts. Regenerate `views/` after resolving canonical files. Validate before committing the resolution. Do not discard changes or force-push to make a conflict disappear.
