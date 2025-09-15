---
type: "post"
aliases:
- /2019/06/switching-from-i3status-to-barista.html
date: "2019-06-07T00:00:00Z"
tags:
- linux
- fedora
title: Switching from i3status to barista
---

I am a long-time i3wm user and I've been using i3status [for a while now](https://i3wm.org/docs/user-contributed/lzap-config.html). However this software is very opinionated which is not a bad thing, however after upgrade to my new UPS I wanted to put battery on my bar as well as Ryzen temperature. Upstream did not like my patch, time to move on.

There is a nice i3bar called Barista available. What's a bit strange (and I like it) is that it's written in Go and you have to compile the bar yourself. Essentially, `main.go` is your bar configuration. It's also very fast and well designed. Very much like it.

I struggled a bit in order to link alsa, netlink and sys/unix libraries however on my Fedora, here is how to do it:

    cd ~/go/src
    git clone https://github.com/soumya92/barista
    cd samples/sample-bar
    dnf -y install alsa-lib-devel "golang(golang.org/x/sys/unix)" "golang(github.com/vishvananda/netlink)"
    CGO_CFLAGS="-I/usr/include/alsa" go get -u
    CGO_CFLAGS="-I/usr/include/alsa" go build

Patch for Ryzen temperature incoming. Have fun!

