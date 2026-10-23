# Set up GitHub and Obsidian

The vault files are prepared. The vault is published at `brickwalllegend2000/dutch-study` (**public** repository as of 2026-10-23). Clone it (or open your extracted folder) in Obsidian, then follow the steps below. See [publishing](PUBLISH.md) for the status of milestones and the Project board. These desktop steps run on your computer, outside the cloud workspace.

**Orientation:** [OVERVIEW — set up information](OVERVIEW.md#set-up-information) (what you need vs do not need; cloud vs desktop). **Wiki vs vault:** [OVERVIEW — wiki versus the rest](OVERVIEW.md#wiki-versus-the-rest-of-the-vault). First open: [START-HERE.md](../START-HERE.md).

## What you are opening

| Piece | Meaning |
| --- | --- |
| Git clone root | The Obsidian vault root (must include `.obsidian/` and `wiki/`) |
| `wiki/` folder | Reference notes inside the repo — **not** GitHub Wiki |
| Sync | Git pull / push only; do not double-sync with Obsidian Sync or cloud drive folders |
| Study | Markdown + generated vocab notes — **no Python** |
| Maintenance | Python 3.11+ only to `build` / `validate` / `search` after CSV edits |

## Recommended: GitHub Desktop on Windows or macOS

1. Install [GitHub Desktop](https://desktop.github.com/) and [Obsidian](https://obsidian.md/download). Sign into GitHub Desktop with the account that owns or can access the repository.
2. In GitHub Desktop, choose **File → Clone repository → URL** and enter `https://github.com/brickwalllegend2000/dutch-study`. Choose a normal local folder such as `Documents/dutch-study`, outside folders managed by another synchronization service.
3. In Obsidian's vault switcher, choose **Open folder as vault**, then select that exact `dutch-study` folder. Keep restricted mode enabled; community plugins are not required.
4. Open [journal/my-study-view.md](../journal/my-study-view.md) (or `README.md`). Use **Ctrl+Shift+F** on Windows or **Cmd+Shift+F** on macOS to search all notes; **Ctrl/Cmd+O** opens the Quick Switcher. Course chapters live under `course/`; grammar and word lists under `wiki/` (generated vocab in `wiki/vocabulary/`).
5. Create a note in `journal/` and run **Templates: Insert template** from the command palette; choose Study Session. The Templates folder is preconfigured.
6. Return to GitHub Desktop. Review the changed note, commit it with a summary such as `study: practise chapter 2`, then click **Push origin**. Do not hand-edit `wiki/vocabulary/` in Obsidian.

On your next session, click Fetch origin and Pull origin before editing. When you use a second computer, clone the repository there and repeat the Obsidian steps. Open only one editing session at a time for the same files.

## Command-line setup, including Linux

Install Git and Obsidian. Authenticate using GitHub CLI (`gh auth login`) or your normal Git credential manager; never place a token in a remote URL or note.

```bash
gh repo clone brickwalllegend2000/dutch-study
cd dutch-study
git status
```

Open that folder as a vault in Obsidian. For normal synchronization:

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

Obsidian's core editor reads Markdown; it does not provide a native CSV spreadsheet editor. Browse `wiki/vocabulary/VOCABULARY.md` and per-word notes in Obsidian. For updates, open a GitHub correction issue and ask an agent to update the CSV, regenerate notes and open a pull request. Alternatively edit UTF-8 CSV in a CSV-capable editor, keeping the exact header and delimiter.

Python 3.11+ is needed only to regenerate and check the library. No pip packages are needed. Use `python3` on systems where `python` is not defined, or `py` on Windows.

## For agents

Provide the repository to your agent's GitHub connection, or open a local clone in its workspace. Start with: “Read AGENTS.md and WORKFLOW.md.” A URL alone does not grant write access. Local search works without a hosted search index.

## Synchronization choice

Use GitHub Desktop/Git to synchronize this vault. Avoid putting the same vault under Obsidian Sync, Dropbox, OneDrive or iCloud synchronization at the same time. Those services can race with Git and create conflicting copies. Obsidian's local file recovery is enabled; it is not a replacement for backups.

## Mobile

This initial configuration is ready for desktop use. Mobile Git access requires additional software or a separately chosen synchronization method. Do not assume the desktop GitHub workflow automatically syncs to an Obsidian mobile app.

## If GitHub rejects a push

Check that you are signed into the correct account and have repository access. The GitHub connection used by an agent can have different permissions from your desktop login. Never paste a private token into a chat or issue.
