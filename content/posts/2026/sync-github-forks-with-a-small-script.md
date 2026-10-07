---
title: "Sync GitHub forks with a small shell script"
date: 2026-10-07T12:51:13+02:00
type: "post"
tags:
- linux
- git
- github
---

Every now and then I need to bring a bunch of my GitHub forks up to date. This
is a note for my future self about the small script I use for that. GitHub
already knows which repository is the parent of each fork, and
`gh repo sync OWNER/REPO` can copy the parent's default branch to the fork.
Running that command in every repository by hand gets old, though.

I put together a small Bash script called `git-sync` to take care of the
routine part. The [complete script is in a public gist](https://gist.github.com/lzap/709a1f5b087ccbcc365920a241987572).

## What it does

When run without arguments, `git-sync` looks for Git repositories directly
under `$HOME` and one directory below that. It checks each repository's
`origin` and syncs it only when the remote points to `github.com`.

The script extracts the repository name from `origin` and passes it directly
to `gh repo sync`. The GitHub CLI uses the fork's parent as the source by
default, so there is no need to configure an `upstream` remote or set a
default repository in `gh`. Repositories without a GitHub `origin` are
silently skipped.

If you pass one or more directories, it processes just those directories
instead of scanning `$HOME`:

```bash
git-sync ~/src/foreman
git-sync ~/src/foreman ~/src/smart-proxy
```

The directory can be a Git repository itself or a directory inside one. The
script finds the repository root before checking its remotes.

## Requirements

You need Bash, Git, and the [GitHub CLI](https://cli.github.com/) installed and
available in `PATH`. Sign in with `gh auth login` using an account that can
update the forks you want to sync.

If an upstream change includes GitHub Actions workflow files, `gh` may ask for
the additional `workflow` authorization. Add it with:

```bash
gh auth refresh -s workflow
```

## Installing and running

Download the `git-sync` file from the gist into a directory on your `PATH`,
such as `~/bin`, and make it executable:

```bash
chmod +x ~/bin/git-sync
```

Then run it from anywhere:

```bash
git-sync
```

You can also pass repository directories when you only want to sync a few.
The script continues after a failed sync and exits with an error if any
repository failed.

It does not force updates. If a fork's branch has commits that are not in the
parent, `gh repo sync` reports that it cannot fast-forward the branch. Review
those commits before deciding whether to force the fork to match its parent;
forcing the sync can discard fork-only commits from that remote branch.

*Assisted by LLM model: OpenAI Codex GPT-6*
