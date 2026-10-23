# Set up GitHub

The library is published at `brickwalllegend2000/dutch-study` (**public** repository as of 2026-10-23). Clone it and work in GitHub’s file browser, any Markdown editor, or an agent workspace. See [publishing](PUBLISH.md) for milestones and the Project board.

**Orientation:** [OVERVIEW — set up information](OVERVIEW.md#set-up-information). First open: [START-HERE.md](../START-HERE.md).

Obsidian is **removed for now**. Do not expect a `.obsidian/` config in this clone. A future export vault may be added later; until then GitHub is the study and maintenance surface.

## What you are opening

| Piece | Meaning |
| --- | --- |
| Git clone root | The library root (`data/`, `course/`, `wiki/`, `sources/`, …) |
| `data/` | Canonical facts — `vocabulary.csv` and `grammar/` |
| `wiki/` folder | Generated vocab views + cheat sheets inside the repo — **not** GitHub Wiki; grammar facts are under `data/grammar/` |
| Sync | Git pull / push only |
| Study | Markdown + generated vocab notes — **no Python** |
| Maintenance | Python 3.11+ only to `build` / `validate` / `search` after CSV edits |

## Recommended: GitHub Desktop on Windows or macOS

1. Install [GitHub Desktop](https://desktop.github.com/). Sign in with the account that owns or can access the repository.
2. **File → Clone repository → URL** → `https://github.com/brickwalllegend2000/dutch-study`. Choose a normal local folder such as `Documents/dutch-study`.
3. Open [journal/my-study-view.md](../journal/my-study-view.md) or `README.md` on GitHub or in your editor. Course chapters live under `course/`; grammar under `data/grammar/`; generated word lists under `views/vocabulary/`.
4. For a study log, copy [templates/Study-Session.md](../templates/Study-Session.md) into `journal/` and fill it in.
5. In GitHub Desktop, review changes, commit (e.g. `study: practise chapter 2`), then **Push origin**. Do not hand-edit `views/vocabulary/`.

On your next session, Fetch and Pull before editing. On a second computer, clone again. Prefer one editing session at a time for the same files.

## Command-line setup, including Linux

Install Git. Authenticate with GitHub CLI (`gh auth login`) or your normal Git credential manager; never place a token in a remote URL or note.

```bash
gh repo clone brickwalllegend2000/dutch-study
cd dutch-study
git status
```

Synchronization:

```bash
git pull --ff-only
# Edit and study, then inspect changes.
git status
git diff
# Stage specific intended files, commit, and push.
git add journal/
git commit -m "study: record practice session"
git push
```

If Git reports local changes before pulling, commit the intended changes first. If a pull cannot fast-forward, follow WORKFLOW's conflict guidance; do not force-push.

## Editing vocabulary

Browse `views/vocabulary/VOCABULARY.md` and per-word notes on GitHub or in an editor. For updates, open a GitHub correction issue and ask an agent to update the CSV, regenerate notes and open a pull request. Alternatively edit UTF-8 CSV in a CSV-capable editor, keeping the exact header and delimiter.

Python 3.11+ is needed only to regenerate and check the library. No pip packages are needed. Use `python3` where `python` is not defined, or `py` on Windows.

## For agents

Provide the repository to your agent's GitHub connection, or open a local clone in its workspace. Start with: “Read AGENTS.md and WORKFLOW.md.” A URL alone does not grant write access. Local search works without a hosted search index.

## If GitHub rejects a push

Check that you are signed into the correct account and have repository access. The GitHub connection used by an agent can have different permissions from your desktop login. Never paste a private token into a chat or issue.
