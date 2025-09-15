---
type: "post"
aliases:
- /2021/02/booting-s390x-libvirt-vms-over-network.html
date: "2021-02-02T00:00:00Z"
tags:
- linux
- fedora
title: Booting S390x libvirt VMs over network
---

I am exploring S390x provisioning support for Foreman and it looks like network
booting S390x virtual machines could be a good start. Foreman can be used with
or without libvirt compute resource to either run and customize an image via
SSH finish template or booting from network.

In QEMU environment, s390-ccw firmware is utilized to boot the operating system
which is not as flexible as on Intel, but thanks to the recent work of Red Hat
and IBM engineers in 2018 it offers two ways of booting from network via
DHCP/BOOTP protocols.

The older method requires kernel and init RAM disk to be [concatenated and
sligthly
modified](https://github.com/ibm-s390-tools/s390-tools/blob/master/netboot/mk-s390image).
Then it's just matter of configuring DHCP to return the filename option so the
firmware can download it via TFTP and load into the memory. This would require
calling an external script from Foreman once kernel and image are downloaded
from the installation media.

The newer method from 2018 (qemu 3.0 and newer) is radically more simple, the
firmware has a limited PXELinux configuration file parser which can recognize
both kernel and init RAM disk and download them separately performing the
required concatenation on the fly. There are several options available, the
simplest one is to return the configuration file directly in the filename DHCP
option.

Configuring dnsmasq, which is controlled by libvirt, is easy. Add `<tftp>` and
`<bootp>` elements and restart the network:

    # virsh net-edit default
    <network>
      <!-- ... -->
      <ip address="192.168.122.1" netmask="255.255.255.0">
        <tftp root="/var/lib/tftpboot"/>
        <dhcp>
          <!-- ... -->
          <bootp file="pxelinux.cfg"/>
        </dhcp>
      </ip>
    </network>

Then create a PXELinux configuration file, make sure it starts with `#
pxelinux`; a magic string preventing executing this as it was a linux kernel.

    # cat /var/lib/tftpboot/pxelinux.cfg
    # pxelinux
    default linux
    label linux
    kernel kernel.img
    initrd initrd.img
    append ip=dhcp inst.repo=http://download.xxx.com/RHEL-8.4.0/BaseOS/s390x/os

A second more flexible option is to return a directory via the DHCP filename
option, the firmware then searches `pxelinux.cfg/` subdirectory using the
PXELinux pattern: UUID, MAC address and finally `default` fallback
configuration file. In that case:

    # virsh net-edit default
    <network>
      <!-- ... -->
      <ip address="192.168.122.1" netmask="255.255.255.0">
        <tftp root="/var/lib/tftpboot"/>
        <dhcp>
          <!-- ... -->
          <bootp file="/"/>
        </dhcp>
      </ip>
    </network>

The PXELinux configuration is the same, it don't even need to have the `#
pxelinux` magic header. Keep in mind that the parser ignores most of the
statements, there will be no menu, it will automatically pick the first option.
But that's good enough to automate installations via Foreman where PXELinux is
fully supported.

To see it in action:

    # virsh start test --console
    Domain test started
    Connected to domain test
    Escape character is ^]
    done
      Using IPv4 address: 192.168.122.207
      Using TFTP server: 192.168.122.1
      Bootfile name: '/'
    Trying pxelinux.cfg files...
      Receiving data:  0 KBytes
      TFTP: Received /pxelinux.cfg/default (297 bytes)
    Loading pxelinux.cfg entry 'linux'
      Receiving data:  5000 KBytes
      TFTP: Received kernel.img (5000 KBytes)
      Receiving data:  40063 KBytes
      TFTP: Received initrd.img (40063 KBytes)
    Network loading done, starting kernel...

    [    0.114133] Linux version 4.18.0-147.el8.s390x (mockbuild@s390-016.build.eng.bos.redhat.com) (gcc version 8.3.1 20190507 (Red Hat 8.3.1-4) (GCC
    )) #1 SMP Thu Sep 26 16:13:34 UTC 2019
    [    0.114135] setup: Linux is running under KVM in 64-bit mode

And Linux on S390x is booting up from the network! I haven't tried this end to
end with Foreman yet, but it looks promising. Later, lads.

