---
type: "post"
aliases:
- /2013/11/installing-win-xp78-in-rhel6-kvm.html
date: "2013-11-08T00:00:00Z"
tags:
- linux
- fedora
title: Installing Win XP/7/8 in RHEL6 KVM
---

I was trying to install Windows XP system on a RHEL6 operating system using
libvirt and I was surprised how smooth this was. Basically, it is very easy to
do via virt-manager, but I had special requirements:

 * standard RHEL6 server only (not RHEV)
 * libvirt via virt-install
 * remote installation via Spice

So the first step is to enable optional and supplementary channels for RHEL6:

    subscription-manager repos --enable rhel-6-server-optional-rpms
    subscription-manager repos --enable rhel-6-server-supplementary-rpms

Now, install virtualization packages. Easiest method is:

    yum groupinstall "Virtualization" "Virtualization Client" "Virtualization Platform" "Virtualization Tools"

In the next step, we will install VirtIO official Red Hat (signed) drivers
which will work seamlessly with Windows 7/8 installers:

    yum install virtio-win

To create a VM, issue this command. Note the second `--disk` option which
contains drivers. Also note this command configures Spice at standard port
(5900) and libvirt will listen on *all* interfaces. Password is set.

    virt-install \
        -n xp \
        -r 2800 \
        --arch i686 \
        --cdrom path_to.iso \
        --os-type windows \
        --os-variant winxp \
        --disk pool=default,size=5,bus=virtio,format=qcow2 \
        --disk path=/usr/share/virtio-win/virtio-win_x86.vfd,device=floppy \
        --graphics spice,listen=0.0.0.0,password=test123 \
        --noautoconsole

The command above creates 32bit system, if you change `--arch` option to 64
bits, also change path to `virtio-win_amd64.vfd` instead of the `x86` one.

Now it is the time to connect to the hypervisor:

    remote-viewer spice://my-server:5900

This should work with Windows XP/7/8 and maybe others (Server and stuff). But
if you are using Windows XP, you must be quick to press F6 to "Install other
drivers", then press "S" and select WinXP 32bit driver (or 64bit if you
changed the architecture and VFD file).

You can mount the Red Hat official driver ISO and install Guest Agent and few
more drivers:

    virsh domblklist xp
    virsh attach-disk xp "/usr/share/virtio-win/virtio-win.iso" hdc --type cdrom --mode readonly

BUT I recommend to head over to http://www.spice-space.org/download.html and
download spice-guest-tools-XXXX.exe installer which is much easier to use. I
tried this with Windows XP, not sure if it does support Windows 7/8 (it looks
like it should).

That's it.
