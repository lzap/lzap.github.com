---
type: "post"
aliases:
- /2020/08/prevent-virt-manager-from-asking-password.html
date: "2020-08-21T00:00:00Z"
tags:
- linux
- fedora
title: Prevent virt-manager from asking password
---

Everytime I start virt-manager, the tool I use on an every-day basis, it asks
for the root password. Because I use LVM for my VMs, I need to use system
libvirt. Well, it's pretty easy to get rid of this. All I need to do is to add
myself to the "libvirt" group. Tested on Fedora.

Run this as the user who needs to be added. Do not run this in "root shell"
otherwise you add "root" to the group which is not a terrible thing to do,
except it will not work like you intented:

    sudo usermod -a -G libvirt $(whoami)

Done! Enjoy.
