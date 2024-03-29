---
type: "post"
aliases:
- /2019/02/nice-launcher-for-i3wm-xlunch.html
date: "2019-02-08T00:00:00Z"
tags:
- linux
- fedora
- i3wm
title: 'Nice launcher for i3wm: xlunch'
---

I am [happy user](https://i3wm.org/docs/user-contributed/lzap-config.html) of
i3 for some time now. About a year ago, I changed my app launcher from dmenu to
[xlunch](http://xlunch.org/) and it's been pretty fine experience. So let me
share this with you.

There is no Fedora package for xlunch yet and I am too lazy to create one.
Volunteers! But the installation is like:

    git clone https://github.com/Tomas-M/xlunch
    cd xlunch
    sudo dnf install imlib2-devel libX11-devel
    make

I don't even bother to install it and keep this in the workspace directory, I
assume the installation would go something like:

    make install DESTDIR=/usr/local

The migration was pretty easy - in the `.i3/autostart` file I deleted
`dmenu_path` and added new line that ensures generation of entries after each
start. It takes a while because the script converts many SVG icons to raster
images, but it's no big deal for me. There is also a faster script available in
the git repo that does not generate such nice icons but I like to have the
fancy ones:

    bash /home/lzap/work/xlunch/extra/genentries -p /home/lzap/.local/share/icons > /home/lzap/.config/xlunch/entries.dsv 2>/dev/null &

And that's all, assuming you have this configuration:

    bindsym $mod+space exec /home/lzap/work/xlunch/xlunch -i /home/lzap/.config/xlunch/entries.dsv -f RobotoCondensed-Regular.ttf/10 -G

In my case that's WIN key with SPACE combination what brings the thing. Have fun.
