---
type: "post"
aliases:
- /2016/05/hidden-gem-of-fedora-git-xcleaner.html
date: "2016-05-06T00:00:00Z"
tags:
- linux
- fedora
title: 'Hidden gem of Fedora: git xcleaner'
---

Fedora 22+ now provides new tool called git-xcleaner which helps deleting
unused topic branches using TUI (text user interface). It also offers
mechanisms for pre-selecting branches that can be safely removed.

![Main menu](https://raw.githubusercontent.com/lzap/git-xcleaner/master/screenshots/01_main_menu.png)

![Selection](https://raw.githubusercontent.com/lzap/git-xcleaner/master/screenshots/02_select.png)

Possible actions:

**Merged**

Command git branch --merged is used to find a list of branches that are marked
for deletion.

**Messages**

For each branch, tip commit message is compared against base history and if
found, the branch is marked for deletion. Whole commit message is compared and
it must fully match.

User enters base branch name (defaults to "master").

**Remote**

Delete all remote branches in remote repo which are not present locally.

User enters remote name (defaults to current username).

**Upstream**

All branches which no longer exist in origin or specific remote repository are
marked for deletion.

User enters specific remote name (defaults to current username).

**Manual**

User manually marks branches for deletion.

Go ahead and try it:

    # dnf -y install git-xcleaner
    # git xcleaner

If you mis-deleted a branch and ignored all the warnings in documentation and
on the screen, check out the homepage for instructions how to checkout your
branch back.

And one more thing. File bugs at https://github.com/lzap/git-xcleaner/issues

