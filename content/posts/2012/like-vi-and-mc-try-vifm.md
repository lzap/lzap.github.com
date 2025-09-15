---
type: "post"
aliases:
- /2012/08/like-vi-and-mc-try-vifm.html
date: "2012-08-01T00:00:00Z"
tags:
- linux
- fedora
title: Like vi and mc? Try vifm
---

I am vim-lover and I sometimes fire off Midnight Commander when I want to
browse some content visually. Not spending much time in it, but I find this
file commander very cool. Last weekend I bumped into [vifm][1].

Installation in Fedora is pretty straightforward, I like "q" key alias for
running it (and I have remapped this key in vifm to quit - by default it's for
macros):

    $ yum -y install vifm
    $ alias q="vifm"
    $ rpm -ql vifm
    /usr/bin/vifm
    /usr/bin/vifm-pause
    /usr/bin/vifmrc-converter
    /usr/share/man/man1/vifm.1.gz
    /usr/share/vifm/vifm-help.txt
    /usr/share/vifm/vifmrc

To move around, you use standard vi keys. Yes, "jkhl" for up, down, into and
out a directory (or to execute/open a file). Keys "G" or "gg" moves to the
first and last files. Pagination works as in vi as well as many other keys
like scrolling, window manipulation (Ctrl-W w or TAB), splits, marks (very
cool feature), searching (with highlighting integrated) and few others.

Now guess what. It's not only vi normal mode that is fully working, but also
command-line mode. Yes, you can :noh, :!, !cd, :mark, :set, :split or :wq. And
there are more (non-vi) commands available.

So how to actually work with vifm when there is no help bar with F5 for copy
and F6 for move? Well, it is vi, right? To copy a file, highlight one or more
and press "y" for yank, then go to the destination directory (in the same
window or the second one) and press "p" to paste it. To move it, pres "P". And
"yy" will work too - quick yank of the file or directory caret is pointing on.
And to yank all files in a directory, "ya" is there for you. Did I write vi
registers work too? Use them with double quote key, as usual. This is really
cool.

How to highlight? Just like in vi, using "v" or "V" as well as with "t" for
highlighting (or tagging) them one by one. You can even search with
"/" which will highlight all searches by default. To rename a file, use "cw" 
combination. There are more actions on a file starting with "c", like change
group, permissions and others. I like "cW" to change file name without
extension. Also dialog for changing permissions is awesome (vi movement keys
work there).

To explore a file (or view if you want), use "e". The internal "explorer"
imitates less and it has, of course, vi keybindings with search and other
features you would expect from a less-like tool. To open a file, use movement
key "l" just like if you want to go into a directory. But when you want to
open an executable in an associated program (e.g. bash script in editor, sorry
I mean vim), then use "i".

It's nearly impossible to list all the features, use documentation on the
[homepage][1]. Note that version in Fedora 16 and 17 has not all features
listed in the documentation. Fedora 18 will have the most recent version of
course, there are builds for F16/F17 in koji too.

[1]: http://vifm.sourceforge.net/

