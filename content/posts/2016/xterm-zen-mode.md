---
type: "post"
aliases:
- /2016/10/xterm-zen-mode.html
date: "2016-10-14T00:00:00Z"
tags:
- linux
- fedora
title: XTerm Zen mode
---

I do lot of talks these days with some amount of shell live demos. Although
it is easy to configure xterm for beamer (black on white, big font,
fullscreen), I created an alias for that:

    xterm -cm -fa Monospace -fs 32 -bg white -fg black -cr red -bc \
        -bcf 200 -bcn 200 -xrm "allowColorOps false" -fullscreen \
        -e "PS1='$ ' LC_ALL=C /bin/bash --norc --noprofile"

And this is how it looks like:

![xterm-zen](/assets/img/posts/2016-10-14-xterm-zen-mode/xterm-zen.png)

I cheated, the font you see is Terminus, not Monospace. But it's not installed
by default, I highly recommend it. Check it out.

If you are reading those lines, chances are this might be useful for you. Take
care!

