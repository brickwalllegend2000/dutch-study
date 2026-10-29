# 04 Concept capture

Status: needs-triage
Type: task
Blocked by: 03

- **Why panel** on every miss: the rule in one line plus the source (grammar note path, VOC ID or quiz item). Generator adds a `concept` field per card: `{topic, rule, path}` taken from the grammar notes and quiz `why`. de/het has no rule ("learn the article with the noun"); say so instead of inventing one.
- **My note** button on any card: one-line personal trick or reminder, stored in `dutchstudy-notes-v1`, shown on the back of that card from then on, included in progress export/import.
- **Export missed cards**: copy/download a Markdown journal note listing missed cards with VOC IDs or grammar paths and my notes; matches the journal convention (personal, not course facts).
- **Mistake log**: list of most-missed cards grouped by topic with a link to the grammar note.

Done when: a miss shows a rule with a working source path; notes survive reload and export/import; exported Markdown passes the link check when saved under `journal/`.
