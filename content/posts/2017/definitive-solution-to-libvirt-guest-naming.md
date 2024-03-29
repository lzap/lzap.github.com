---
type: "post"
aliases:
- /2017/10/definitive-solution-to-libvirt-guest-naming.html
date: "2017-10-10T00:00:00Z"
tags:
- linux
- fedora
title: Definitive solution to libvirt guest naming
---

The answer is libvirt NSS. This is Fedora 26:

    yum install libvirt-nss

And enable the NSS module with two "libvirt" keywords:

    # egrep ^host /etc/nsswitch.conf
    hosts: files libvirt libvirt_guest dns myhostname

DNS resolution just works for all my libvirt guests now. NSS will figure it
out according to dnsmasq DHCP records (hostname entry). If that's not
advertised by a guest, then it will use VM name. For FQDN you need to rename
your VM names to include domain too, e.g. vm1.home.lan.

For more [visit documentation](http://libvirt.org/nss.html).

Hurray! No more fiddling with /etc/hosts, no more dnsmasq split setups or
hacks via virsh. This is elegant solution.

Via [Kamil Páral's blog](https://kparal.wordpress.com/2017/10/06/ssh-to-your-vms-without-knowing-their-ip-address/#comment-6447).
