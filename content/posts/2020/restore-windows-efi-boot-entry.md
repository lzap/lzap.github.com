---
type: "post"
aliases:
- /2020/07/restore-windows-efi-boot-entry.html
date: "2020-07-21T00:00:00Z"
tags:
- linux
- fedora
title: Restore Windows EFI boot entry
---

I experienced a SSD failure this Monday, both my root volume and /home was
lost, I had to do a full reinstall and backup restore. Duplicity saved me once
again, I had a daily backup of my home, unfortunately it was a full Fedora 32
reinstall.

Anyway, with the data I also lost the ESP parition where I had Windows
bootloader. While Fedora Linux works fine, I am unable to boot my Windows where
I have few things for fun, mostly games and audio production software. Here is
a trick how to easily restore the Windows EFI boot entry in grub.

Download a Windows 10 installation ISO, dd it to an USB stick, boot it, press a
key and on the welcome screen press SHIFT-F10. In a command prompt, make sure
it detected Windows installation as C: and type "bcdedit C:\WINDOWS".

Reboot into Linux and rewrite grub configuration. For Fedora it's:

    grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

It should print something like "Found Windows" blah blah. You are done.
