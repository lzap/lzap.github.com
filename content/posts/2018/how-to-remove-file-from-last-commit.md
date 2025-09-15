---
type: "post"
aliases:
- /2018/02/how-to-remove-file-from-last-commit.html
date: "2018-02-01T00:00:00Z"
tags:
- linux
- git
title: How to remove file from last commit
---

Happens all the time to me. When I mis-commit a_file.txt the easiest way to
revert the change from the last commit can be tricky:

    git reset --soft HEAD^
    git reset HEAD a_file.txt
    git commit

But I figured out better way today:

    git checkout HEAD^ a_file.txt
    git commit -a --amend

That's exactly one command saved plus I don't need to dig the commit message. I
know it is possible to reference it via `ORIG_HEAD` but I never use that and I
don't remember.

Done!

