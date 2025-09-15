---
type: "post"
aliases:
- /2014/09/efi-in-qemu-kvm-on-fedora-20.html
date: "2014-09-30T00:00:00Z"
tags:
- linux
- fedora
title: EFI in QEMU KVM on Fedora 20
---

Last sprint, I was working on EFI PXE booting support for Foreman. Although I
have a EFI-compatible PC in the house, I wanted a stable environment for
development and testing. Virtualized, of course.

The best option is KVM/QEMU/libvirt triple which I use for regular Foreman
development. I started googling around and spent a day modifying my
distribution package. It did not work well. And then I stumbled upon familiar
name, Laszlo Ersek from Red Hat, who helped me getting this rolling.

## QEMU with EFI

To get EFI working under QEMU, one needs 2.1.1+ version with modified BIOS.
Since I already almost destroyed configuration of the QEMU from Fedora 20 (had
to reinstall the packages), I was guided to install from sources:

    wget http://wiki.qemu-project.org/download/qemu-2.1.1.tar.bz2
    tar bla bla
    yum -y install spice-server-devel spice-protocol SDL-devel
    ./configure --target-list=x86_64-softmmu --enable-spice \
        --prefix=/opt/qemu-2.1.1 --enable-debug --disable-gtk
    make install
    chown root:root /opt/qemu-2.1.1/libexec/qemu-bridge-helper
    chmod u=rwxs,g=rx,o=rx /opt/qemu-2.1.1/libexec/qemu-bridge-helper
    echo 'allow virbr0' > /opt/qemu-2.1.1/etc/qemu/bridge.conf

Having stable version installed in a separate tree (which keeps your laptop
clean along smile on your face), one needs to download and install BIOS and
EFI firmware. This is important step - for PXE booting, latest nightly builds
are needed. Fortunately, for Fedora/Red Hat users, there is a repo out there
with latest and greatest build. Do not worry, those packages are compatible
with Fedora and won't overwrite/upgrade anything. You can install them next to
the official QEMU BIOS:

    sudo wget https://www.kraxel.org/repos/firmware.repo -O \
        /etc/yum.repos.d/kraxel-qemu-firmare.repo
    yum install edk2.git-ovmf-x64

This guy installs into /usr/share/edk2.git along with some dependencies which
are also compiled from git (SeaBIOS for legacy EFI mode, NIC drivers and so
on).

Now, the *hardest* part. Since libvirt currently lacks UEFI support, we need
to work directly with QEMU. I'd like to thank Laszlo for constructing me this
script which sets up things correctly:

    #!/bin/bash
    OVMF_BINARY=/usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd
    VARSTORE_TEMPLATE=/usr/share/edk2.git/ovmf-x64/OVMF_VARS-pure-efi.fd
    QEMU_ROOT=/opt/qemu-2.1.1

    # create fresh variable store
    cp $VARSTORE_TEMPLATE /tmp/guest-vars.fd

    # run qemu
    $QEMU_ROOT/bin/qemu-system-x86_64 \
      -M pc-i440fx-2.1 \
      -enable-kvm \
      -m 900 \
      -drive unit=0,if=pflash,format=raw,readonly,file=$OVMF_BINARY \
      -drive unit=1,if=pflash,format=raw,file=/tmp/guest-vars.fd \
      -global isa-debugcon.iobase=0x402 \
      -debugcon file:/tmp/guest.ovmf.log \
      -monitor stdio \
      -device piix3-usb-uhci -device usb-tablet \
      -netdev bridge,id=net0,br=virbr0,helper=$QEMU_ROOT/libexec/qemu-bridge-helper \
      -device virtio-net-pci,netdev=net0,romfile=,bootindex=0 \
      -device qxl-vga

You can run this script as regular user the only part requiring root access is
the networking one (bridge helper) and that has suid bit set. The VM will be
connected to the "default" libvirt virtual NAT network (virbr0) where you can
set up your PXE environment and start playing with EFI PXE booting.

## PXELinux and Foreman

In this second part of my blog entry, I want to share some news about Foreman
support. Since Foreman ships with templates set for PXELinux by default, I
wanted to keep on this path.

Apparently syslinux 5.x does not have EFI support and syslinux 6.02 did not
work for me. So I decided to compile 6.03 from sources which did not work
either. Luckily, folks on the IRC channel recommended to use 6.03-pre20
version which worked like a charm:

    https://www.kernel.org/pub/linux/utils/boot/syslinux/Testing/6.03/syslinux-6.03-pre20.tar.gz

The following files need to be extracted into tftpboot/efi64 directory:

    syslinux.efi
    chain.c32
    ldlinux.e64
    libutil.c32
    menu.c32

Also I created *relative* symlinks (TFTP runs in chroot usually) for
configuration and kernels:

    boot -> ../boot
    pxelinux.cfg -> ../pxelinux.cfg

You can do the same with 32bit arch. But that's pretty much it!

DHCP daemon configuration is straighforward and the best approach is only to
hand over EFI PXELinux to DHCP clients which reports as EFI-compatible. You
need something like (192.168.100.0 network with Foreman running on .2):

    # ... snippet ...

    option arch code 93 = unsigned integer 16;

    subnet 192.168.100.0 netmask 255.255.255.0 {
        pool {
            range 192.168.100.10 192.168.100.200;
        }

        option subnet-mask 255.255.255.0;
        option routers 192.168.100.1;

        class "pxeclients" {
            match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
            next-server 192.168.100.2;

            if option arch = 00:07 {
                filename "efi/syslinux.efi";
            } else if option arch = 00:06 {
                filename "efi32/syslinux.efi";
            } else {
                filename "pxelinux/pxelinux.0";
            }
        }
    }

Similarly you can use Grub, you need to copy EFI binary and create
configuration file. This is covered in RHEL6 ([1]) and RHEL7 ([2])
documentation.

[1]: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Installation_Guide/s1-netboot-pxe-config-efi.html
[2]: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Installation_Guide/chap-installation-server-setup.html#sect-network-boot-setup-uefi


