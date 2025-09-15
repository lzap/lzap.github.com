---
type: "post"
aliases:
- /2019/02/connecting-a-physical-host-to-libvirt-nat-network.html
date: "2019-02-19T00:00:00Z"
tags:
- linux
- fedora
title: Connecting a physical host to libvirt NAT network
---

A customer sent me an industrial server for testing, pretty interesting stuff
for trains, planes and boats. I have added a new PCIe NIC to my workstation and
I wanted to put it inside my libvirt NAT network which I use for testing
Foreman and Satellite.

![Network diagram](/assets/img/posts/2019-02-physical-server.png)

Surpringlisly it was not easy to figure out this for me, luckily Patrick
Talbert of Red Hat helped me to find a command that does exactly what I wanted:

    # nmcli con add type ethernet ifname eth1 slave-type bridge master virbr0

Assuming that `eth1` is the physical interface and `virbr0` is libvirt NAT
network bridge (named default). For different networks find the proper network
with the following command:

    # virsh domiflist <guest>

And with the 'source' network name, find the actual bridge name:

    # virsh net-info <network>

In my case my device was `enp9s0` and I named my bridge device as `virbr-ntln`.
Thanks to Patrick for helping me with this!

