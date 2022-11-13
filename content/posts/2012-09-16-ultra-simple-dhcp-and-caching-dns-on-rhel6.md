---
type: "post"
aliases:
- /2012/09/ultra-simple-dhcp-and-caching-dns-on-rhel6.html
date: "2012-09-16T00:00:00Z"
tags:
- linux
- fedora
title: Ultra simple DHCP and caching DNS on RHEL6
---

I had to configure DHCP and DNS caching server on a small LAN today, but I
needed to change several A DNS entries for specific services that has
different IP addresses externally and internally.

It turns out it is not possible to do this easily with BIND. The only way to
do this is to create zone with all the setting and zone transfer. It looks
like overkill to me.

When I was googling this, I stumbled upon [dnsmasq][1].

It is a trivial DHCP/DNS/BOOTP/TFTP/PXE server with several nice features and
one of these is ability to change DNS records. Since it is ideal for my case,
I have decided to shut down dhcpd and named and use it. It turned out it was a
great decision.

Installation is super easy, it's part of RHEL 6 base channels.

    yum -y install dnsmasq

It's a very small package.

    # rpm -ql dnsmasq
    /etc/dbus-1/system.d/dnsmasq.conf
    /etc/dnsmasq.conf
    /etc/dnsmasq.d
    /etc/rc.d/init.d/dnsmasq
    /usr/sbin/dnsmasq
    /usr/share/doc/dnsmasq-2.48
    ...
    /usr/share/man/man8/dnsmasq.8.gz
    /var/lib/dnsmasq

That does not mean it has little features. In fact, it has this nice set of
killer features and I really love how all the services it provides are
integrated. For example one can easily bind DHCP client names and DNS records,
integration between DHCP and booting protocols is also very nice.

To see all of the features read the /etc/dnsmasq.conf file. All lines are
commented, but fully documented. You don't even need to turn on anything,
dnsmasq provides sane defaults. To get basic behavior, just start it:

    service dnsmasq start
    chkconfig dnsmasq on

It will read your /etc/resolv.conf to retrieve nameservers, it will determine
your network and start serving as DNS caching daemon and DHCP service for that
network. Please note it listens on *all* interfaces by default.

In my case, I only uncommented few options:

    # grep -v '^#' /etc/dnsmasq.conf | sed '/^$/d'
    address=/some.server.net/10.0.0.100

Yeah, I need to return different IP addresses for few DNS queries. In this
case, I want some.server.net to be resolved as 10.0.0.100. Dnsmasq is also
able to read /etc/hosts if you want that, but you need to explicitly enable
this.

    expand-hosts
    domain=lan

I want to all the DHCP clients to have "lan" extension, therefore computer
that is named "alpha" is added as "alpha.lan" in DNS. By default they are
added without any extension I guess.

    dhcp-host=jirka,10.0.0.30,infinite

I want machine which says it's named "jirka" to have this address for infinite
time. Dnsmasq is very powerful in this, you can create various rules using
dhcp-host and it is also able to read /etc/hosts to read static IP
definitions from there.

    dhcp-range=10.0.0.20,10.0.0.99,999h

This is my DHCP range, I like long lease times in this network.

    dhcp-option=42,0.0.0.0

And I have ntpd daemon that is opened for LAN requests, therefore I am giving
this (maybe odd) option so clients can synchronize time against the server
itself.

Okay, today I found this little-big-daemon is super useful. For small LANs
with few computers, it's a swiss knife for every single administrator.

[1]: http://www.thekelleys.org.uk/dnsmasq/doc.html
