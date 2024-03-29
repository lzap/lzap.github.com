---
type: "post"
aliases:
- /2013/03/booting-38-kernels-on-marwell-kirkwood-arm-zyxel-nsa-310.html
date: "2013-03-17T00:00:00Z"
tags:
- linux
- fedora
- arm
title: Booting 3.8+ kernels on Marwell Kirkwood ARM Zyxel NSA 310
---

Zyxel NSA 3xx are excellent and cheap NAS devices and finally support for
model NSA 310 landed in Linus tree in the 3.8 version. Good news, but this
Marwell Kirkwood-based ARM device is using DTS (Device Tree). I had no
experiences with compiling DTS kernels, until this night.

So the Device Tree, or The Flattened Device Tree, (FDT) is a data structure
for describing the hardware in a system. It is a derived from the device tree
format used by Open Firmware to encapsulate platform information and convey it
to the operating system. The operating system uses the FDT data to find and
register the devices in the system. (Taken from
http://elinux.org/Device_Trees)

Simply put, Device Tree helps us to boot various (ARM) hardware without need
of recompiling kernel for each device. The basic idea is to compile
information about the hardware (DTS is the source file, DTB is binary compiled
data structure) into the kernel and to integrate bootloader with it so it is
able to pick up the relevant DTB and continue booting the kernel.

The issue with NSA 310 is it's bootloader does not support Device Tree.
Fortunately, there is an option to tell the linux kernel to load DTB from end
address using an option and concatenating the DTB info to it.

Let's do it. First of all, get a 3.8+ kernel and see what we can do:

    # make help
    ...
    Architecture specific targets (arm):
    * zImage        - Compressed kernel image (arch/arm/boot/zImage)
      Image         - Uncompressed kernel image (arch/arm/boot/Image)
    * xipImage      - XIP kernel image, if configured (arch/arm/boot/xipImage)
      uImage        - U-Boot wrapped zImage
      bootpImage    - Combined zImage and initial RAM disk
                      (supply initrd image via make variable INITRD=<path>)
    * dtbs          - Build device tree blobs for enabled boards
      install       - Install uncompressed kernel
      zinstall      - Install compressed kernel
      uinstall      - Install U-Boot wrapped compressed kernel
                      Install using (your) ~/bin/installkernel or
                      (distribution) /sbin/installkernel or
                      install to $(INSTALL_PATH) and run lilo
    ...

There are some patches in the testing arm repositories that adds new make
targets that does the trick for you, so you can do something like:

    make dtbuImage.kirkwood-nsa310

to get DTB-enhanced kernel for uImage directly. This hasn't been merged into
the Linus tree yet. We are going to do this manually now. First of all,
configure your kernel. Make sure you have NSA 310 support and DTB loading:

    # grep "ARM_APPENDED_DTB|NSA" .config
    CONFIG_ARM_APPENDED_DTB=y
    CONFIG_MACH_NSA310_DT=y

As well as other ARM options. Then compile the kernel:

    # make zImage
    ...
    Kernel: arch/arm/boot/zImage is ready

Then we will compile our NSA 310 DTS into DTB binary representation:

    # make dtbs

The above target creates kirkwood-nsa310.dtb along with other kirkwood files
(and all of those you have enabled in your configuration). Now we need to
concatenate it into our kernel:

    # cat arch/arm/boot/zImage arch/arm/boot/dts/kirkwood-nsa310.dtb > /tmp/X
    # mv /tmp/X arch/arm/boot/zImage

We have changed zImage, but we can continue building our u-boot image because
the file is newer and GNU make will have no problems with that. So let's
create the final u-boot kernel:

    # make uImage
    ...
    Image Type:   ARM Linux Kernel Image (uncompressed)
    Data Size:    3684110 Bytes = 3597.76 kB = 3.51 MB
    Load Address: 00008000
    Entry Point:  00008000
    Image arch/arm/boot/uImage is ready

We are done, copy your kernel to the final destination:

    # cp arch/arm/boot/uImage /boot/uImage-nsa310

To boot it just do something like this in your u-boot environment:

    ide reset; ext2load ide 0:1 0x800000 /uImage-nsa310; bootm 0x800000

This depends on where you boot your device from. I will maybe create some
other articles about booting Fedora on this device. What I want to focus on is
creating my own setup on USB flash drive and F2FS.

If you googled my article, please drop me a line bellow. Take care!

