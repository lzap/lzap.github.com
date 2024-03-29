---
type: "post"
aliases:
- /2021/02/helper-script-for-easy-cherry-picks-with-git.html
date: "2021-02-19T00:00:00Z"
tags:
- linux
- fedora
title: Helper script for easy cherry picks with git
---

After many, many manual cherry picks, I've decided to put together a [short
script](https://github.com/lzap/bin-public/blob/master/git-xcp). It's fully
interactive and hopefully self-explanatory.

    [lzap@box foreman]$ git xcp
    Looks like you want to cherry-pick, huh?!
    Branch you want to pick INTO: 2.4-stable
    Branch you want to pick FROM: develop
    Allright, allright, here is the menu:
    bb1a931b6 Fixes #31064 - sequence helper macro
    089e232c0 Fixes #31830 - support children in SkeletonLoader component
    ed70741fa Fixes #31882 - set ENC var hostname to shortname
    6c3794cf1 Refs #31720 - Apply @ezr-ondrej suggestions from code review
    d43eba522 Refs #31720 - address comments and add links
    809e6eec5 Refs #31720 - Apply tbrisker suggestions
    0cc6abbb4 Fixes #31720 - add first draft doc
    648f72365 Fixes #31873 - Expose edit permissions in api index layout
    9ad6b1a25 Refs #30215 - mark string for translation
    24d2df594 Fixes #31855 - add ellipsis with tooltip for long setting values
    Commits separated by space or enter to give up: 0cc6abbb4 809e6eec5 d43eba522
    Hit ENTER to push, Ctrl-C to interrupt. See ya!

The script remembers the INTO and FROM selection (stores it in the `.git`
directory) and it uses `git stash` to work even when there are some uncommited
changes.
