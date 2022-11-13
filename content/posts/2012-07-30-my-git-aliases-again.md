---
type: "post"
aliases:
- /2012/07/my-git-aliases-again.html
date: "2012-07-30T00:00:00Z"
tags:
- linux
- fedora
- git
title: My Git aliases again
---

After more intensive work with git I have defined my own set of aliases that
helps me to interact with git every day. Some of them are borrowed from
Google, Red Hat folks or others but most of them are my own work. Please note
this will only work with Git 1.5+.

This is an updated blog post with some bugs fixed and more commands :-)

    # vim: ts=2:et
    # ...
    [alias]
      pu = pull
      pur = pull --rebase
      cam = commit -am
      ca = commit -a
      cm = commit -m
      ci = commit
      co = checkout
      st = status
      br = branch -v
      unstage = reset HEAD --
      find = !sh -c 'git ls-tree -r --name-only HEAD | grep --color $1' -
      cleanup = !git branch --merged master | grep -v 'master$' | xargs git branch -d
      k = !gitk
      g = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
      h = !git --no-pager log origin/master..HEAD --abbrev-commit --pretty=oneline
      pom = !sh -c 'git h && echo Ready to push? ENTER && read && git push origin master' -
      pomt = !sh -c 'git h && echo Ready to push? ENTER && read && git push origin master && git push origin master --tags' -
      purm = !sh -c 'test "$#" = 1 && git h && git checkout master && git pull && git checkout \"$1\" && git rebase master && exit 0 || echo \"usage: git purm <branch>\" >&2 && exit 1' -
      rem = !sh -c 'test "$#" = 1 && git h && git checkout master && git pull && git checkout \"$1\" && git rebase master && git checkout master && git merge \"$1\" && echo Done and ready to do: git pom && exit 0 || echo \"usage: git rem <branch>\" >&2 && exit 1' -
      rpom = !git pull --rebase && git pom
      v = !gvim $*
      lt = !git describe $(git rev-list --tags --max-count=1)
      mus = !sh -c 'git checkout master && git fetch upstream && git merge upstream/master && git push origin master --tags' -
    # ...

### git pu; git pur; git ci; git ca; git co; git br

Standard shortcut set for pull, commit, checkout and branch. These are
must-haves.

### git st

Git status. What an alias! I use it a lot. Got a bash alias gg for "clear &&
git st".

### git unstage

The "missing" git command, taken from the Pro Git book.

### git k

Okay this just calls gitk if I accidentally insert a space. It happens to the
best of us ;-)

### git g

Fast log with nice color formatting. Sometimes better than the standard git log.

### git h

Fast overview of differences between master and my current branch. Time saver.

### git pom

Push into origin/master but first show me the differences in short one-line
format and allow me to confirm with a key. The same command is "pomt", but it
pushes also tags. I also have various branch combinations.

### git rem

A masterpiece. Credit goes to msuchy for the original idea which I slightly
extended. This pulls and rebases master on top of a (topic) branch, then
merges it into the master and gets ready for pushing. Workflow I use everyday.

### git find

Finds a filename in the git repository. Gives absolute location (from the git
root).

### git purm

Sometimes I need to do a "quickfix" directly in the master, then pull with
rebase and push. All in one command.

### git v

My invention here. Sqmetimes I need to open a Vim with a particular filename
but I already got filename with absolute path (from git root). No need to edit
it - this command opens Vim in the root git directory.

### git cleanup

Deletes all branches that were *safely* merged into the master. All other are
skipped (no worries).
