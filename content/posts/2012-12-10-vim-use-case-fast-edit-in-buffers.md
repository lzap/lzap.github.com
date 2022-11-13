---
type: "post"
aliases:
- /2012/12/vim-use-case-fast-edit-in-buffers.html
date: "2012-12-10T00:00:00Z"
tags:
- linux
- fedora
- vim
title: Vim use case - fast edit in buffers
---

My second topic has something do to with workflow I use everyday. I often need
to edit a file(s), commit to git (usually amending the last one), build and
install a package and test it. Often when I am trying my patch that fixes some
bug or something.

I use tabs when doing regular feature coding. Tabs are great feature of Vim
and works pretty well, but they do not play very well with many files opened.
This is where buffers comes in.

Buffers are essentially files being edited, or just piece of memory for
unsaved buffers (e.g. quick fix is also a buffer). You can work with them
effectively and they are documented in the "Editing with multiple windows and
buffers" section of the Vim documentation.

Simply put, you can open multiple files in Vim (vim file1 file2 ...) and all
files will be "magically" available as buffers. To list all buffers just use
_:ls_ command, to jump on particular buffer use :Nb where N is index of the
buffer starting from one (for instance :5b). To jump to the next or previous
buffer use _:bn_ (:bnext) and _:bp_ (:bprevious) respectively.

This is the total minimum to know about buffers. You can do much more with
them, I highly recommend to search the web and read Vim documentation. As I
use them quite often, I have mapped the following combinations for buffers:  

    map <leader>j :bnext<CR>
    map <leader>k :bprevious<CR>
    map <leader>q :b#<CR>

Leader key is very special key Vim use for user-defined combinations. Many
Vim users, including me, have leader set to comma key:

    let mapleader = ","

So the final combination I use is, yes you guess it: ,j ,k and ,q. The last
command just switches between last used weapon - I mean buffer. Good old
Counter Strike times :-)

Okay, back to buffers, here comes the tip. I often need to edit last commited
file(s) from git. You can do this with buffers and simple trick I googled the
other day. Put the following into your ~/.gitconfig

    fshow = ! sh -c 'git show --pretty="format:" --name-only $1 | grep -v "^$" | uniq | sed -e "s#^#`git rev-parse --show-toplevel`/#"' -
    edit  = ! sh -c '$EDITOR `git fshow $1`' -

Suppose you do this:

    touch fileA fileB
    git add file*; git commit -a "blah"
    touch fileX
    git add file*; git commit -a "blah"

Now, to edit latest fileX real quick, just issue

    git edit

And Vim loads the latest commited file into the first buffer. Thats the
default one, you can start editing immediately. Now, to load all three files
just do this:

    git edit HEAD^..

Use what you know about buffers to navigate them. To load all changed files
from last ten commits, do

    git edit HEAD~10..

I often edit the latest file (git edit) amending the latest commit to
overwrite my change when I test it.
