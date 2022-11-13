---
type: "post"
aliases:
- /2020/09/creating-windows-10-bootable-usb-drive.html
date: "2020-09-22T00:00:00Z"
tags:
- linux
- fedora
title: Creating Windows 10 bootable USB drive
---

I had to update firmware for my super-ultra-wide LG monitor, however the utility only works in Windows and requires USB-C PC or laptop. I have one, but it's Fedora only. Luckily, there is a way how to install Windows 10 to USB hdd (or flash).

First of, download Windows 10 ISO from Microsoft's website. I've used MediaCreationTool.exe utility which prepared the ISO for me in about half an hour.

Next up it's this wonderful freeware tool called [Rufus](https://rufus.ie). By default it only shows USB flash drives, but after pressing Ctrl-Alt-F it also shows up USB external HDD drives. Pick a drive, browse the ISO and after the tool asks for type of installation select "Windows 10 To Go". That's all, really. Rufus will format the drive and copy necessary files.

After the initial reboot Windows 10 sets them up and allows the trial period without activation. I was able to download a firmware update tool and perform what I needed to do. Everything was a little bit too slow on my USB 3.0 SATA HDD, but it was fine for the job.

I hope that helps someone else using Linux!
