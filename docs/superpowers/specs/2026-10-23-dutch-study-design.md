# Dutch study canonical library

## Purpose and authorization
The user asked for planning, full setup, configuration, implementation and execution for GitHub and Obsidian after choosing a GitHub-backed canonical library. Execute in this session; the conversation establishes the design and authorization. Default destination: a new private `dutch-study` repository under the authenticated personal GitHub account.

## Design
The repository root is also an Obsidian vault. Maintain vocabulary as UTF-8 CSV with stable IDs and source references. Maintain grammar topics and chapter guides as Markdown with relative links. Generate vocabulary reading views for Obsidian; never edit those generated views independently. Preserve retrieved Notion page payloads as import evidence, alongside readable Markdown snapshots. Do not modify or delete Notion originals.

Reuse existing grammar topics and chapters. Import vocabulary from the master table and perfectum task, preserving contexts and conflicts rather than silently choosing a variant. Each consolidated entry retains all contributing source occurrences. Distinguish migration checks from linguistic review. Photos and PDFs require actual byte downloads before claiming they are archived; keep a manifest of unavailable originals.

## Workflow
README is the landing page; WORKFLOW describes repeatable steps; AGENTS defines agent rules. GitHub Issues hold tasks, labels express work status, and issue forms supply import/correction/study templates. A Project board is optional; issue search links work without one. GitHub Actions validates IDs, sources, CSV schema, internal links and generated-file freshness. No required external Python packages, API keys or Obsidian community plugins. Python 3.11+ for tooling; content is readable without Python.

## Access and synchronization
Private GitHub repo; use GitHub Desktop or git for local synchronization. Open the local clone as an existing vault. Do not configure simultaneous Obsidian Sync and Git writes for this vault. Desktop app installation/opening is outside this cloud environment; provide exact user steps. Prefer connected GitHub tools; use authenticated gh for missing repository/settings/project capabilities.

## Verification
Test parsing of Markdown and HTML tables, CSV quoting, duplicate aggregation, source preservation, ID collisions, invalid records and generated freshness. Validate the complete imported library, verify remote visibility and branch contents, and inspect Actions results. Clearly report remote restrictions and migration gaps.
