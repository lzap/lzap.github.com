---
type: "post"
aliases:
- /2019/02/linux-as-nat-server-in-easy-steps.html
date: "2019-02-18T00:00:00Z"
tags:
- linux
- fedora
title: Linux as NAT server in two easy steps
---

There are many articles explaining how to do NAT and masquerading with Linux
using iptables or other quite low-level tools. This is all not necessary these
days, NetworkManager and firewalld can do the dirty work for us! If you have
RHEL7, CentOS7 or any modern Fedora or pretty much anything which is more
recent, it's super easy.

In my scenario I want to NAT traffic from an internal network 192.168.199.0/24
to external (virtual NAT actually) network 192.168.122.0/24. My host has two
NICs eth0 and eth1 connected to these networks in this order. Kernel has
forwarding turned off (the default setting for Red Hats):

    # sysctl -a | grep ip_forward
    net.ipv4.ip_forward = 0

It's really easy! Both my interfaces are in the public zone:

    # firewall-cmd --get-active-zone
    public
      interfaces: eth1 eth0

All I need to is to move them into pre-defined zones internal and external.

    # nmcli c mod eth0 connection.zone internal
    # nmcli c mod eth1 connection.zone external

You can stop reading now, Linux has been configured as NAT with masquarade now
with the stwo simple commands. Anyway, let's do some analysis. Look, firewalld
noticed I want to do NAT and enabled IP forwarding in the kernel for me.

    # sysctl -a | grep ip_forward
    net.ipv4.ip_forward = 1

Masquerade is already enabled on the pre-defined zone called external, again no
need to do anything here. Look:

    # firewall-cmd --zone=external --query-masquerade
    yes

The external pre-defined zone is quite strict similarly to public zone, only
ssh service is allowed. In my case I wanted to allow HTTP(s) traffic as well:

    # firewall-cmd --zone=external --add-service=http
    success
    # firewall-cmd --zone=external --add-service=http --permanent
    success

It's worth noting that internal pre-defined zone is also quite strict.
Remember, 70 per-cent of all security attacks come from the inside! Since I am
performing just some testing in isolated environment, I can afford to open it
up completely as I plan to run some extra services like DHCP, DNS and TFTP on
that server.

    # firewall-cmd --list-all --zone=internal
    internal (active)
      target: default
      icmp-block-inversion: no
      interfaces: eth0
      sources:
      services: ssh mdns samba-client dhcpv6-client
      ports:
      protocols:
      masquerade: no
      forward-ports:
      source-ports:
      icmp-blocks:
      rich rules:

So I gave it the accept target policy. Do not try at home, this is dangerous!

    # firewall-cmd --permanent --zone=internal --set-target=ACCEPT
    success
    # systemctl restart firewalld

Have fun!

