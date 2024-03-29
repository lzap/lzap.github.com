---
type: "post"
aliases:
- /2018/02/hidden-gem-of-fedora-virt-builder.html
date: "2018-02-06T00:00:00Z"
tags:
- linux
- fedora
- rhel
- centos
title: 'Hidden gem of Fedora: virt-builder'
---

Or I should say hidden gem of Fedora, CentOS and RHEL. This fantastic tool is
part of package named libguestfs-tools-c and it's fast image builder. To create
Fedora 27 10GB image with root password set to "redhat":

    virt-builder fedora-27 --size=10G \
      --root-password password:redhat

To start the image use libvirt utility:

    virt-install --import --name fedora --ram 2048 \
      --disk path=fedora-27.img,format=raw --os-variant fedora27

To start Fedora 25 and immediately install Xfce desktop:

    virt-builder fedora-25 --install "@Xfce Desktop"

To build Debian Wheezy image, update it and inject your SSH key to root:

    virt-builder debian-7 --update --ssh-inject root:~/.ssh/id_rsa.pub

To create CentOS 7.4 image on LVM volume with a hostname set:

    virt-builder centos-7.4 --output /dev/vg_virt/centos \
      --root-password password:redhat --hostname centos.lan

To `___________________` (complete the sentence):

    virt-builder fedora-25 \
       --hostname client.example.com \
       --update \
       --install puppet \
       --append-line '/etc/puppet/puppet.conf:[agent]' \
       --append-line '/etc/puppet/puppet.conf:server = puppetmaster.example.com/' \
       --run-command 'systemctl enable puppet' \
       --selinux-relabel

To list available images do:

    [lzap@box ~]$ virt-builder -l
    centos-6                 x86_64     CentOS 6.6
    centos-7.0               x86_64     CentOS 7.0
    centos-7.1               x86_64     CentOS 7.1
    centos-7.2               aarch64    CentOS 7.2 (aarch64)
    centos-7.2               x86_64     CentOS 7.2
    centos-7.3               x86_64     CentOS 7.3
    centos-7.4               x86_64     CentOS 7.4
    cirros-0.3.1             x86_64     CirrOS 0.3.1
    cirros-0.3.5             x86_64     CirrOS 0.3.5
    debian-6                 x86_64     Debian 6 (Squeeze)
    debian-7                 sparc64    Debian 7 (Wheezy) (sparc64)
    debian-7                 x86_64     Debian 7 (wheezy)
    debian-8                 x86_64     Debian 8 (jessie)
    debian-9                 x86_64     Debian 9 (stretch)
    fedora-18                x86_64     Fedora® 18
    fedora-19                x86_64     Fedora® 19
    fedora-20                x86_64     Fedora® 20
    fedora-21                aarch64    Fedora® 21 Server (aarch64)
    fedora-21                armv7l     Fedora® 21 Server (armv7l)
    fedora-21                ppc64      Fedora® 21 Server (ppc64)
    fedora-21                ppc64le    Fedora® 21 Server (ppc64le)
    fedora-21                x86_64     Fedora® 21 Server
    fedora-22                aarch64    Fedora® 22 Server (aarch64)
    fedora-22                armv7l     Fedora® 22 Server (armv7l)
    fedora-22                i686       Fedora® 22 Server (i686)
    fedora-22                x86_64     Fedora® 22 Server
    fedora-23                aarch64    Fedora® 23 Server (aarch64)
    fedora-23                armv7l     Fedora® 23 Server (armv7l)
    fedora-23                i686       Fedora® 23 Server (i686)
    fedora-23                ppc64      Fedora® 23 Server (ppc64)
    fedora-23                ppc64le    Fedora® 23 Server (ppc64le)
    fedora-23                x86_64     Fedora® 23 Server
    fedora-24                aarch64    Fedora® 24 Server (aarch64)
    fedora-24                armv7l     Fedora® 24 Server (armv7l)
    fedora-24                i686       Fedora® 24 Server (i686)
    fedora-24                x86_64     Fedora® 24 Server
    fedora-25                aarch64    Fedora® 25 Server (aarch64)
    fedora-25                armv7l     Fedora® 25 Server (armv7l)
    fedora-25                i686       Fedora® 25 Server (i686)
    fedora-25                ppc64      Fedora® 25 Server (ppc64)
    fedora-25                ppc64le    Fedora® 25 Server (ppc64le)
    fedora-25                x86_64     Fedora® 25 Server
    fedora-26                aarch64    Fedora® 26 Server (aarch64)
    fedora-26                armv7l     Fedora® 26 Server (armv7l)
    fedora-26                i686       Fedora® 26 Server (i686)
    fedora-26                ppc64      Fedora® 26 Server (ppc64)
    fedora-26                ppc64le    Fedora® 26 Server (ppc64le)
    fedora-26                x86_64     Fedora® 26 Server
    fedora-27                aarch64    Fedora® 27 Server (aarch64)
    fedora-27                armv7l     Fedora® 27 Server (armv7l)
    fedora-27                i686       Fedora® 27 Server (i686)
    fedora-27                ppc64      Fedora® 27 Server (ppc64)
    fedora-27                ppc64le    Fedora® 27 Server (ppc64le)
    fedora-27                x86_64     Fedora® 27 Server
    freebsd-11.1             x86_64     FreeBSD 11.1
    scientificlinux-6        x86_64     Scientific Linux 6.5
    ubuntu-10.04             x86_64     Ubuntu 10.04 (Lucid)
    ubuntu-12.04             x86_64     Ubuntu 12.04 (Precise)
    ubuntu-14.04             x86_64     Ubuntu 14.04 (Trusty)
    ubuntu-16.04             x86_64     Ubuntu 16.04 (Xenial)
    rhel-3.9                 x86_64     Red Hat Enterprise Linux 3.9
    rhel-4.9                 x86_64     Red Hat Enterprise Linux 4.9
    rhel-5.10                x86_64     Red Hat Enterprise Linux 5.10
    rhel-5.11                x86_64     Red Hat Enterprise Linux 5.11
    rhel-5.11                i686       Red Hat Enterprise Linux 5.11 (i686)
    rhel-6.1                 x86_64     Red Hat Enterprise Linux 6.1
    rhel-6.2                 x86_64     Red Hat Enterprise Linux 6.2
    rhel-6.3                 x86_64     Red Hat Enterprise Linux 6.3
    rhel-6.4                 x86_64     Red Hat Enterprise Linux 6.4
    rhel-6.5                 x86_64     Red Hat Enterprise Linux 6.5
    rhel-6.6                 x86_64     Red Hat Enterprise Linux 6.6
    rhel-6.7                 x86_64     Red Hat Enterprise Linux 6.7
    rhel-6.8                 x86_64     Red Hat Enterprise Linux 6.8
    rhel-6.8                 i686       Red Hat Enterprise Linux 6.8 (i686)
    rhel-7.0                 x86_64     Red Hat Enterprise Linux 7.0
    rhel-7.1                 x86_64     Red Hat Enterprise Linux 7.1
    rhel-7.1                 ppc64      Red Hat Enterprise Linux 7.1 (ppc64)
    rhel-7.1                 ppc64le    Red Hat Enterprise Linux 7.1 (ppc64le)
    rhel-7.2                 x86_64     Red Hat Enterprise Linux 7.2
    rhel-7.2                 aarch64    Red Hat Enterprise Linux 7.2 for aarch64
    rhel-7.2                 ppc64le    Red Hat Enterprise Linux 7.2 (ppc64le)
    rhel-7.3                 x86_64     Red Hat Enterprise Linux 7.3
    rhel-7.3                 aarch64    Red Hat Enterprise Linux 7.3 for aarch64
    rhel-7.3                 ppc64      Red Hat Enterprise Linux 7.3 (ppc64)
    rhel-7.3                 ppc64le    Red Hat Enterprise Linux 7.3 (ppc64le)
    rhel-7.4                 x86_64     Red Hat Enterprise Linux 7.4
    rhel-7.4                 aarch64    Red Hat Enterprise Linux 7.4 for aarch64
    rhel-7.4                 ppc64      Red Hat Enterprise Linux 7.4 (ppc64)
    rhel-7.4                 ppc64le    Red Hat Enterprise Linux 7.4 (ppc64le)

Keep in mind that RHEL systems are only available to redhatters, a repository
must be configured via `/etc/virt-builder/repos.d/rhel.conf` file to have them.
Search the intranet.

This post barely scratched the surface. This utility can do more. [Much
more](http://libguestfs.org/virt-builder.1.html).

Send beer, t-shirts and flowers to [Richard W.M.
Jones](http://people.redhat.com/~rjones/) and his team of contributors and
maintainers. Thanks folks!
