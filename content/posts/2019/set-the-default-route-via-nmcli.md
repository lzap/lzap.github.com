---
type: "post"
aliases:
- /2019/02/set-the-default-route-via-nmcli.html
date: "2019-02-18T00:00:00Z"
tags:
- linux
- fedora
title: Set the default route via nmcli
---

I've never researched anything about how route metric number work other than
it's probably "higher metric wins" (or the other way around?) Anyway, today I
added new interface to one of my VMs and repatched it. My goal was to change
the default route from eth0 to newly created eth1. NetworkManager has some
rules to automatically detect these, however since I am unsure how all of this
works I've decided to solve it this way.

Once the new interface named eth1 appeared, I configured it for DHCP:

    nmcli con add type ethernet con-name eth1 ifname eth1

Of course, two default gateways appeared in my routing table, both eth0 and
eth1 with metric of 100 and 101 respectively. Not what I wanted since I
repatched the VM and I wanted only eth1 to be the default one. Here comes the
trick, you can tell the NetworkManager to never create default route with this:

    nmcli c mod eth0 ipv4.never-default true
    nmcli c mod eth0 ipv6.never-default true

And that's all! All you need to do is to restart existing connection to clear
the routing table or manually remove the entry. Let's do the safe method
ensuring everything is set accordingly however watch out: the following can cut
the branch if you are doing this over SSH connection (use screen or tmux):

    nmcli c down eth0; nmcli c up eth0

Done.

    # ip r
    default via 192.168.122.1 dev eth1 proto dhcp metric 101 
    192.168.122.0/24 dev eth1 proto kernel scope link src 192.168.122.60 metric 101 
    192.168.199.0/24 dev eth0 proto kernel scope link src 192.168.199.11 metric 102 

Easy peasy with NetworkManager.
