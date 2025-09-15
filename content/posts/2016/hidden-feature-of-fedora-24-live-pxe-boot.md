---
type: "post"
aliases:
- /2016/08/hidden-feature-of-fedora-24-live-pxe-boot.html
date: "2016-08-16T00:00:00Z"
tags:
- linux
- fedora
title: 'Hidden feature of Fedora 24: Live PXE boot'
---

Some time ago, I was trying to PXE-boot Fedora 20 LiveCD directly as a
squashfs filesystem from TFTP server. It was not working, because one of the
dracut modules was not included on the CD/DVD init RAM disk. I filed a bug,
some time passed and it's finally fixed.

Required steps to achieve Live Fedora from PXE:

* download Fedora 24 Live DVD (or older)
* extract `squashfs.img`
* put it on HTTP site (`/var/www/htdocs`)
* extract `vmlinuz` and `initrd.img`
* install TFTP server
* put them into TFTP folder (subfolder `boot` in my case)
* setup DHCP and PXE
* deploy PXELinux configuration (below)
* profit!

Example PXELinux configuration:

    default menu
    menu title PXE
    prompt 0
    timeout 200
    ontimeout local

    label local
      menu label ^Boot from local drive
      menu default
      localboot 0

    label fedora-live
      menu label Fedora Workstation LiveBoot
      kernel boot/fedora-live/vmlinuz
      append initrd=boot/fedora-live/initrd.img root=live:http://nas.home.lan/xxx/squashfs.img ro rd.live.image rd.luks=0 rd.md=0 rd.dm=0

Boot Fedora Live from your network, install it from your network when your
crying friends show up with their laptops upgraded to Windows 10. Do it like a
boss. End of transmission.

