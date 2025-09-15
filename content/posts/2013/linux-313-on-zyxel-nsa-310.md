---
type: "post"
aliases:
- /2013/12/linux-313-on-zyxel-nsa-310.html
date: "2013-12-08T00:00:00Z"
tags:
- linux
- fedora
title: Linux 3.13+ on Zyxel NSA 310
---
I have already written [an
article](/2013/03/booting-38-kernels-on-marwell-kirkwood-arm-zyxel-nsa-310.html)
about this Marwell Kirkwood device. This time, we are going to compile *Linus
tree kernel*. Yes, almost everything have been already merged. Except LEDs.

It's super easy now.

    # make mrproper
    # make kirkwood_defconfig

Creates clean and minimal setup for Kirwkood devices. I needed to make two
changes - u-Boot on my device is old and does not support DTS enabled kernels,
so I had to concatenate it. Also, for some reason the kernel was ignoring my
command line, so I burnt it into the kernel image itself.

    # grep CMDLINE .config
    CONFIG_CMDLINE="console=ttyS0,115200 root=/dev/sda3"

For your case, keep the console setting, but adjust our root to the proper
device. If you know why the kernel was not picking up my command line (I was
using 3.13 RC2), let me know under the article. If you need to change
configuration and add more drivers, it's the time now (e.g. USB WiFi sticks,
printers etc.)

    # make menuconfig

I usually write the configuration now and edit it via editor from now on which
is faster. Let's do the kernel now.

    # make && make dtbs

Or if you selected some modules, do this instead:

    # make && make dtbs && make modules && make modules_install

The final step is very important - we need to make an uImage with concatenated
device tree for our NSA 310.

    # cat arch/arm/boot/zImage arch/arm/boot/dts/kirkwood-nsa310.dtb \
        > /tmp/zImage-dtb-kirwood
    # mkimage -A arm -O linux -T kernel -C none -a 0x00008000 -e 0x00008000 \
        -n Linux-kikrwood-nsa310.dtb -d /tmp/zImage-dtb-kirwood \
        /boot/uImage-3.13.0-rc2

Note there are two files:

* arch/arm/boot/dts/kirkwood-nsa310.dtb
* arch/arm/boot/dts/kirkwood-nsa310a.dtb

Because there are more hardware versions, try out both and find which one
works best for you.

Boot the new kernel and note that *everything works*, except LEDs. Also the
power button is working, which is great. I don't need LEDs, actually I don't
like blinking LEDs at all so I am fine. If you _need_ LEDs, there are couple
of patches on the arm-list floating around - grab them.

I have created an ultra [simple script](https://github.com/lzap/fan3xxnsa)
which controls the fan. There are other ways of doing that (e.g. via
lm-sensors), but I prefer this lightweight solution (written in Go).

In my house, NSA 310 is great cheap 2 TB NAS, file server, print server,
backup server and WiFi AP ($10 Tenda USB stick - was working out-of-box).

Drop me a line in the comments bellow!

