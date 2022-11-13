---
type: "post"
aliases:
- /2020/06/on-git-master-main-and-inclusion.html
date: "2020-06-19T00:00:00Z"
tags:
- linux
- fedora
- git
title: On git master, main and inclusion
---

All I can say is that I find some words like whiltelist, blacklist and
master/slave awful. I do realize that the context in git might not be racist,
however I am trying to be nice-by-default person. I won't comment more on the
situation as this blog is strictly non-political. So let's be technical in that
regard:

If one of your projects rename master to main and you are having hard time
checking out the mainline branch, I have a tip for you:

    $ alias gcm='git checkout master || git checkout main || git checkout gh-pages'
    $ alias gll='(git checkout master || git checkout main || git checkout gh-pages) && git pull'

If you prefer git subcommand aliases, `git cm` for example, then add this to
your git configuration:

    $ cat ~/.gitconfig
    [alias]
    # ... gazillion of my other aliases ...
    cm = !sh -c 'git checkout master || git checkout main || git checkout gh-pages'

Checking out main branch is now easy, you don't need to ever think about which
project are you working on:

    $ gcm
    error: pathspec 'master' did not match any file(s) known to git
    Switched to branch 'main'

You can ignore the error when git was unable to find "master" branch, that's
expected. I did not bother to solve this issue, you can probably redirect the
standard error if you find this annoying. Let me know on my twitter @lzap if
this helped to you, if you have a better solution or similar tip.

I have been using this for years, our project Foreman actually use a different
term for the mainline branch. We call it the "develop" branch.

Oh, by the way, Steve Job's style: it even works for github pages repositories.
