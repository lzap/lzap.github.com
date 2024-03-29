---
type: "post"
aliases:
- /2022/10/the-ultimate-git-hook-to-prevent-push-accidents.html
date: "2022-10-13T00:00:00Z"
tags:
- linux
- git
title: The ultimate git hook to prevent push accidents
---

So you pushed something that you did not mean to, huh? I have a simple solution
for that, a *global git hook* that checks:

* A push is not being made into a remote named `upstream`.
* A push is made into remote URL containing your username.
* A push is not being made into branch named `main` or `master`.
* If you still want to push, you can use `--no-verify` git option to force it.
* Or create `.noverify` empty file within a git repository to disable this.
* Everything is just a single and *global* POSIX-compatible shell git hook.

Let me explain.

I name upstream repositories as `upstream`, you can do this with `git clone -o
upstream https://project.com/repo.git`. Then I almost always want to create a
fork (e.g. on github.com or internal gitlab.com) and push into such repo, which
I typically name `origin`. That is check number one.

Then most of my git repositories are hosted on github.com, gitlab.com or
similar sites where I use the very same username which also matches my OS
username, `lzap` that is. So the second check verifies there's `lzap` in an URL
like `https://github.com/lzap/gitconf`.

Finally, I almost never want to push into `main` branch, sometimes named
`master`. On many projects we also used `develop` for the main branch, that's
the check number three.

You want this? It's super-easy. Create an empty directory on your computer
(e.g. `$HOME/.githooks` and drop my
[pre-push](https://github.com/lzap/gitconf/blob/main/hooks/pre-push) shell
script. Make sure to give it *executable flag*. Finally, configure git to use
it.

	mkdir $HOME/.githooks
	curl -O $HOME/.githooks/pre-push https://raw.githubusercontent.com/lzap/gitconf/main/hooks/pre-push
	chmod +x $HOME/.githooks/pre-push
	git config core.hooksPath $HOME/.githooks

Make sure to review and edit my script, you will probably have a different
preference when it comes to branch or remote names. Beware that git only
supports executing hooks from a global directory (this case), or from git
repository (`.git/hooks`). It's always one, or the other. If you need to still
use some project-level hooks, the workaround is to create global hooks that
executes project hooks when they exist.

See it in action!

	% git push
	HOOK: Pushing to disallowed branch (main, master, etc.)!
	HOOK: Use git push --no-verify to force this operation.
	error: failed to push some refs to 'github.com:lzap/gitconf.git'

If you want to force push, it's easy help.

	% git push --no-verify

Or create `.noverify` empty file in the git repository to skip all checks all togeher for a particular repo. Make sure to put this into your global `.gitignore`!

That's all for today.
