---
type: "post"
aliases:
- /2017/10/efi-with-libvirt-in-rhel7.html
date: "2017-10-03T00:00:00Z"
tags:
- linux
- fedora
- uefi
- efi
- libvirt
title: EFI with libvirt in RHEL7
---

RHEL 7 does not ship with EFI firmware by default, at least version 7.4 I just
tested with. There is easy help tho if you want to try EFI in libvirt which
does not make much any other sense than for development purposes.

We will follow steps from Fedora Wiki but changed into RHEL context. Download
firmware repository which have latest builds of EFI QEMU firmware and NVRAM
images:

    # wget -O /etc/yum.repos.d/firmware.repo http://www.kraxel.org/repos/firmware.repo

Install the package:

    # yum -y install edk2.git-ovmf-x64

There are several flavors available and honestly - I just randomly picked one
of these:

    # rpm -ql edk2.git-ovmf-x64
    /usr/share/doc/edk2.git-ovmf-x64
    /usr/share/doc/edk2.git-ovmf-x64/README
    /usr/share/edk2.git
    /usr/share/edk2.git/ovmf-x64
    /usr/share/edk2.git/ovmf-x64/OVMF-need-smm.fd
    /usr/share/edk2.git/ovmf-x64/OVMF-pure-efi.fd
    /usr/share/edk2.git/ovmf-x64/OVMF-with-csm.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_CODE-need-smm.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_CODE-with-csm.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_VARS-need-smm.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_VARS-pure-efi.fd
    /usr/share/edk2.git/ovmf-x64/OVMF_VARS-with-csm.fd

There are also builds for AARM64 platform, but I will focus on x64_64 in this
article.

Here comes the trick, QEMU in RHEL7 is not configured to search this rather
unusual EDK2 path, so let's add it to its configuration:

    # cat >>/etc/libvirt/qemu.conf <<EOQEMU
    nvram = [
    "/usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd:/usr/share/edk2.git/ovmf-x64/OVMF_VARS-pure-efi.fd"
    ]
    EOQEMU

And restart the daemon.

    systemctl restart libvirtd

Done, now you can create VMs with UEFI firmware instead of BIOS. Note this
cannot be changed once VM is created via virt-manager but you should be able
to use command line tools:

    # virsh edit my_domain
    ...
    <os>
    <type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
    <loader readonly='yes' type='pflash'>/usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd</loader>
    <nvram>/var/lib/libvirt/qemu/nvram/rhel7.4_VARS.fd</nvram>
    </os>
    ...

If you are PXE booting, I vaguely remember that libvirt driver had some
issues, it should be safer to use RTL chipset emulation. That's all for today.
