---
type: "post"
aliases:
- /2020/02/linux-as-a-l2-vlan-switch.html
date: "2020-02-19T00:00:00Z"
tags:
- linux
- fedora
title: Linux as a L2 VLAN switch
---

I needed to join two segments of virtual LAN together via a linux bridge.
That's an easy task for Linux, however problem was that one segment was a VLAN
(with id of 13) and the other segment was native (VLAN 0). I struggled hard
figuring out the proper commands with NetworkManager until Beniamino Galvani of
Red Hat put me on the right track.

Assuming that enp2s0 uses tagged frames and enp1s0 doesn't, enabling VLAN
filtering can do the trick:

    nmcli connection add type bridge ifname bridge0 \
      bridge.vlan-filtering on bridge.vlan-default-pvid 13 \
      ipv4.method disabled ipv6.method ignore

    nmcli connection add type ethernet ifname enp1s0 master bridge0
    nmcli connection add type ethernet ifname enp2s0 master bridge0 bridge-port.vlans "13"

This will only work on RHEL 8.1 or newer as it relies on newest NetworkManager
VLAN filtering switches. Kudos to everyone who made this possible and Beniamino
for helping me out!

