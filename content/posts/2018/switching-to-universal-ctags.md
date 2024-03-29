---
type: "post"
aliases:
- /2018/09/switching-to-universal-ctags.html
date: "2018-09-18T00:00:00Z"
tags:
- linux
- fedora
title: Switching to Universal Ctags
---

After some time spent with exuberant-ctags and ripper-tags, I am switching over
to [universal-ctags](https://ctags.io). Ruby language and other languages like
Golang is vastly improved over to exuberant-ctags and even ripper-tags.
[Here](https://github.com/lzap/bin-public/tree/master/files/git_hooks) are my
git hooks which I use for all my project checkouts. It's fast, fluent and works
across all my projects.

For navigation I stick with Vim, sometimes I use
[fzf.vim](https://github.com/junegunn/fzf.vim) plugin together with
[fzf](https://github.com/junegunn/fzf) for terminal.

For longer coding sessions, I am trying GNOME Builder which looks great and
every single release it is catching up with Submlime Text 3, except it is fully
open source and it has usable Vim emulation. I've tried Atom and VSCode but
these slow things are not for me.
