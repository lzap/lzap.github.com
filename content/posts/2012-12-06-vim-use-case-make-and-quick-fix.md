---
type: "post"
aliases:
- /2012/12/vim-use-case-make-and-quick-fix.html
date: "2012-12-06T00:00:00Z"
tags:
- linux
- fedora
title: Vim use case - make and quick fix
---

I use Vim editor for more than thirteen years now. Today I realized that
things that seems natural to me are not always visible to new or even skilled
users. To learn Vim, you need to use it every single day. It's a very complex
tool and every person use Vim differently. There are many ways to do same
things.

I'd like to share short Vim tips on my blog which I think are nice and I find
them useful. It is challenging to select features I would like to blog about,
but I will try to do my best. Don't expect anything new and shinny -
everything what I write here was already written, zillion times perhaps. And
also - it's all in Vim documentation :-)

Let's get started!

I very often need to compile or check files or projects I work on. For this,
there are two nice features of Vim - makeprg and cwindow.

For example on a Ruby project, I usually set this:

    set makeprg=ruby\ -c\ %

On a Go language project, it is:

    set makeprg=go\ build

And so on - there are many build or check options out there. Find your own
one.

By default makeprg is set to "make" command, which is often the case. But
sometimes not. To initiate build (or check), just do :make command. (No bang
character - this is internal Vim command!) Shortcut for :makeprg is :mp.

Vim can parse output and work with it in the Quick Fix window. Typical
commands you use is :copen which opens quick fix window as a new buffer. Or
you can use :cnext and :cprevious (short versions are :cn and :cp) to jump on
next or previous errors. And :cclose, yeah, closes it. But one command I like
the most - :cwindow (:cw in short) which opens quickfix window if there are
errors and close it if there are not.

Let's compose this into one simple approach I use everyday. I usually bind one
key (F9 - yeah old good Borland times :-) to do everything for me:

 * save all buffers (this is really nice)
 * make in the background (build it, check it, whatever)
 * open quick fix window (if there are errors; or close it)
 * by default Vim jumps to the first error
 * if there are errors, fix and hit F9 again (window will be eventually
 closed)

This is it:

    map <F9> :wa|silent! make|cw<CR>

Make and output parsing works usually out of the box in Vim, but if you need
to tune it a bit, look for errorformat (efm) setting.

Easy, right?

