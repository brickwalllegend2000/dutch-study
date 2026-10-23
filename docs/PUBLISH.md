# Publish the prepared vault

## Current limitation

On 2026-10-23 the connected GitHub account was authenticated, but GitHub rejected repository creation with:

> brickwalllegend2000 does not have the correct permissions to execute CreateRepository

No GitHub repository, issues, milestones, Project board or Actions run were created by that attempt. The local vault, canonical data, workflow configuration and initial task definitions are prepared. The configuration files are not evidence that the remote services are active.

If an empty private repository is created and the agent's GitHub connection is granted access, the agent can finish publication. Alternatively use the prepared publishing script with your own authenticated GitHub CLI on your computer.

## Automated publication on your computer

1. Extract the vault ZIP to a normal local folder, outside another synchronization service. Install Git, [GitHub CLI](https://cli.github.com/), Python 3.11+ and Obsidian.
2. Open a terminal in the extracted `dutch-study` folder. Run `gh auth login` and sign into `brickwalllegend2000` through GitHub's browser flow. Your login needs permission to create or write the private repository. Do not put tokens in files or chat.
3. Run:

```bash
python scripts/publish_github.py
```

Use `py` on Windows or `python3` where appropriate. The script validates the library and runs the tests before uploading. It creates a private repository if absent, refuses a public or unrelated nonempty destination, commits and pushes the prepared content, enables Issues, creates labels, three milestones and five initial issues, and attempts a Project board. It does not force-push. It records actual links in `docs/publishing-result.json`. Rerunning resumes existing work by matching issue/milestone titles.

A successful Project setup uses GitHub's standard Todo / In Progress / Done statuses. Use the status:review issue label for review work. You can edit the Project's Status field in its settings to add Review. If the token lacks Project permissions, the script reports that limitation; issues and status labels still support the workflow. Use `--skip-project` if you prefer that simpler setup.

The script stages intended vault contents, including captured study files. Run it only from this prepared vault and review its contents before using it after your own modifications. Normal later changes should use GitHub Desktop or pull requests, not repeated bootstrap runs.

4. Check the repository's Actions tab. Library checks should complete successfully. A prepared workflow file alone does not establish a successful remote run.
5. Open this same folder as an existing vault in Obsidian. If GitHub Desktop is your preferred client, use **File → Add local repository** to add the folder that the script initialized. Follow [desktop setup](SETUP.md) for daily use.

## Manual fallback

Create an empty private `dutch-study` repository in GitHub. In GitHub Desktop, add the extracted folder as a local repository (create it there if prompted), commit the prepared files, and publish it as private under the correct account. Do not overwrite an existing unrelated repository.

Issue forms and Actions become available after pushing `.github/`. Create the labels, milestones and tasks using `.github/bootstrap.json` as the exact configuration. A Project board is optional; [the task list](TASKS.md) links to issue searches after publication.
