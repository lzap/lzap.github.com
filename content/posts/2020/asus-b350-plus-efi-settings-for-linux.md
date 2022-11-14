---
type: "post"
aliases:
- /2020/08/asus-b350-plus-efi-settings-for-linux.html
date: "2020-08-05T00:00:00Z"
tags:
- linux
- fedora
title: ASUS B350 PLUS EFI settings for Linux
---

It's been two years on my Ryzen 1700, 32GB RAM and Saphire 5600XT however after
Fedora reinstallation after (another) SSD failure I started experiencing random
hangs of the graphical subsystem (I could still ssh to my workstation). Some
people recommended turning off IOMMU, so I took the opportunity to upgrade to
latest EFI firmware and review all my settings. These are the best (and safest)
ASUS B350-PLUS changed firmware settings optimized for Linux from my own
experience.

* CPU\SVM = Enabled
* CPU\SMT = Disabled
* AMD CBS\C-State = Disabled
* AMD CBS\IOMMU = Disabled
* Boot\Fast boot = Disabled
* Boot\Boot logo = Disabled
* Boot\POST delay = 2 sec
* Boot\Wait for F1 = Disabled
* Boot\Setup mode = Advanced

This solves several issues I had in the past. Virtualization is turned off by
default, SVM enables it. Multi-threading is enabled and although this is not a
thread on AMD CPUs I like to turn this off as it caused some issues in the
past. C-State and IOMMU can be problematic for AMD GPUs and the rest is just
optimizing boot process for my LG screen as it does poweroff sometimes when
using Fastboot.

I also have
[ryzen-stabilizator](https://github.com/qrwteyrutiyoup/ryzen-stabilizator)
script during the boot to turn off few more CPU flags to prevent from random
MCE freezing. It looks like after a month of testing, I haven't experienced
freeze without this but I am sticking with it for now:

    # cat /etc/rc.d/rc.local
    #!/bin/sh
    /usr/local/bin/ryzen-stabilizator --disable-c6 --disable-boosting --disable-aslr -enable-psicworkaround

The author of this tool suggests to set Power Supply Idle Control to Typical
Current Idle, however I was not able to find this setting in my firmware.
Finally, my graphics card is constantly waking up my screen every 30 seconds,
there seem to be some problem with power with the latest drivers or firmware.
The workaround is to add `amdgpu.runpm=0` on the kernel commands line. This GPU
draws 6 watts on idle anyway with fans completely turned off.

I will update this blogpost on the fly if I encounter any other instability of
my setup in the future. Overall, I am quite happy with AMD-only hardware. Sure,
it's not as stable as Intel, but I am glad there's a competition again in the
industry.
