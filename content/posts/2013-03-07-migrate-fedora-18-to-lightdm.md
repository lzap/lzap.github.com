---
type: "post"
aliases:
- /2013/03/migrate-fedora-18-to-lightdm.html
date: "2013-03-07T00:00:00Z"
tags:
- linux
- fedora
title: Migrate Fedora 18 to LightDM
---

Since I am using i3 window manager for a while and I am very happy with it, I
have switched from GDM over to LightDM. Installation was easy:

    # sudo yum -y install lightdm-gtk
    # sudo systemctl disable gdm.service
    # sudo systemctl enable lightdm.service
    # sudo reboot

Done!

This should work for Fedora 17+ I guess. Tested on 18 tho.
