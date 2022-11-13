---
type: "post"
aliases:
- /2019/08/hidden-gem-of-fedora-lbzip2.html
date: "2019-08-23T00:00:00Z"
tags:
- linux
- fedora
title: 'Hidden gem of Fedora: lbzip2'
---

Fedora carries a nifty utility for years which is called lbzip2. What it does?
Well, an example is worth hundreds of words:

    [lzap@box tmp]$ time tar -c linux-5.2.9/ | bzip2 -5 > /dev/null

    real    1m10,480s
    user    1m10,228s
    sys     0m1,705s

    [lzap@box tmp]$ time tar -c linux-5.2.9/ | lbzip2 -5 > /dev/null

    real    0m4,155s
    user    1m3,190s
    sys     0m1,581s

This is my 8-core (16-threads) Ryzen CPU so pretty much a standard modern CPU
and the difference is obvious. With maximum compression block results are the
same:

    [lzap@box tmp]$ time tar -c linux-5.2.9/ | bzip2 -9 > /dev/null

    real    1m14,493s
    user    1m14,205s
    sys     0m1,705s

    [lzap@box tmp]$ time tar -c linux-5.2.9/ | lbzip2 -9 > /dev/null

    real    0m4,603s
    user    1m9,684s
    sys     0m1,641s

In 2014, it was proposed to replace bzip2 with lbzip2 in Fedora, but this was
not approved. The question is - is it time right now? Sure, the original bzip2
is from 1996 thus if we are not there yet can we probably implement
"alternatives" for bzip2 so users can easily switch between one or another to
see if everything else works as expected? I say yes to this half-way step and
have another period of extensive testing.

Want to comment on this? [Do it in a BZ](https://bugzilla.redhat.com/show_bug.cgi?id=1744212).

Kudos to Laszlo, Mikolaj and other contributors for this engineering
achievement. Let's see what we can do with it.
