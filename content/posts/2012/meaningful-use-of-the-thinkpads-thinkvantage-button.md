---
type: "post"
aliases:
- /2012/08/meaningful-use-of-the-thinkpads-thinkvantage-button.html
date: "2012-08-26T00:00:00Z"
tags:
- linux
- fedora
title: Meaningful use of the ThinkPad's ThinkVantage button
---

I find this button pretty useless and I like That Was easy button. So the use
is pretty clear. Download the sample:

    wget http://mhwalkers.freevar.com/sounds/that_was_easy.wav -O \
        ~/.cache/what_was_easy.wav

Load the sample:

    pactl upload-sample ~/.cache/that_was_easy.wav that_was_easy

This obviously works only for PulseAudio users. Always test before use!

    pactl play-sample that_was_easy

Now bind this to the ThinkVantage button. In my case (i3 tiling windows
manager) it's:

    bindsym XF86Launch1 exec /usr/bin/pactl play-sample that_was_easy

You can use xbindkeys program if your windows manager cannot handle this:

    $ cat ~/.xbindkeys
    "/usr/bin/pactl play-sample that_was_easy"
    XF86Launch1 

Have fun! :-)
