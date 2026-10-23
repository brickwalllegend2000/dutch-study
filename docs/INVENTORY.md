# Current inventory

Generated for maintenance truthfulness. Prefer these figures over historical counts in [MIGRATION.md](MIGRATION.md) or [START-HERE.md](../START-HERE.md). Orientation and diagrams: [OVERVIEW.md](OVERVIEW.md).

**As of:** 2026-10-23 (post starter-issue closure and overview handoff). Re-run the commands below after substantial imports.

## How to refresh

```bash
python - <<'PY'
import csv, json
from pathlib import Path
rows=list(csv.DictReader(open('vocabulary.csv',encoding='utf-8')))
m=json.loads(Path('sources/manifest.json').read_text(encoding='utf-8'))
occ=json.loads(Path('sources/vocabulary-occurrences.json').read_text(encoding='utf-8'))
print('vocabulary',len(rows))
print('reviewed',sum(1 for r in rows if r['review_status']=='reviewed'))
print('needs-review',sum(1 for r in rows if r['review_status']=='needs-review'))
print('manifest pages',len(m['pages']))
print('attachments',len(m['attachments']))
print('archived',sum(1 for a in m['attachments'] if a.get('status')=='archived'))
print('unavailable',sum(1 for a in m['attachments'] if a.get('status')=='unavailable'))
print('reference-only',sum(1 for a in m['attachments'] if a.get('status')=='reference-only'))
print('withheld-public',sum(1 for a in m['attachments'] if a.get('status')=='withheld-public'))
print('occurrences',len(occ))
print('grammar notes',len(list(Path('wiki/grammar').glob('*.md')))-1)
PY
python scripts/library.py validate
```

## Snapshot (2026-10-23)

| Item | Count | Notes |
| --- | --- | --- |
| Vocabulary records | 520 | Canonical: `vocabulary.csv` |
| Reviewed / needs-review | 501 / 19 | 19 remaining needs-review carry `[added]` English |
| Blank English | 0 | Every row has a gloss |
| Source occurrences | 911 | `sources/vocabulary-occurrences.json` |
| Manifest sources | 43 | Includes oral grouping + redacted agenda source |
| Attachments | 68 | 26 archived oral PNGs; 41 unavailable Notion originals (24 filenames); 1 withheld agenda PDF |
| Grammar topic notes | 14 | All marked reviewed (AI/course-snapshot) |
| Generated vocabulary views | 533 | Rebuild with `python scripts/library.py build` |
| Open GitHub Issues | 0 | Starters closed; see [TASKS.md](TASKS.md) |
| Deferred inbox | 1 | Class notes — not for canonical import yet |

## Source coverage labels

| Status | Meaning |
| --- | --- |
| archived | Local binary present; SHA-256 recorded and checked |
| reference-only | Filename known; bytes not yet retrieved (temporary import state) |
| unavailable | Confirmed not retrievable; listed in `sources/originals/UNAVAILABLE.md` |
| withheld-public | Binary intentionally omitted from the public tree (agenda credentials) |
| redacted-public | Study transcription without sensitive values |
| provisional / enriched snapshot | Readable text mixes transcription and editorial additions |

## Historical baseline

The 2026-10-23 Notion migration reported **53** pages, **768** occurrences and **412** vocabulary records. Later oral import and edits changed those totals. Keep [MIGRATION.md](MIGRATION.md) as a dated baseline, not as the live inventory.

The Practice tests Notion page in the manifest carries `truncated: true` and an unknown-block warning; do not claim that retrieval was complete for every page.
