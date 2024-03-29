---
type: "post"
aliases:
- /2019/12/easy-libvirt-ipv6-routed-network.html
date: "2019-12-10T00:00:00Z"
tags:
- linux
- fedora
title: Easy libvirt IPv6 routed network
---

This is a tutorial on how to create a routed IPv6 libvirt network for testing.
Having a "default" NAT network, create a new one called "isolated" as isolated
network (no upstream connectivity). Then create new VM with two network cards
both in "default" and "isolated" networks. I used CentOS 8.0 but this would
work with any distribution.

First off, create new account at https://www.tunnelbroker.net and you will be
given an IPv6 network:

* Routed /64: 2001:db8:6f:443::/64
* Routed /48: 2001:db8:59ef::/48
* Server IPv6 Address: 2001:db8:6e:443::1/64
* Client IPv6 Address: 2001:db8:6e:443::2/64

Delete automatically created connections:

		nmcli c delete enp1s0
		nmcli c delete "Wired connection 1"

Create upstream IPv4 connection, in my case it's DHCP. Upstream is the
interface connected to "default" NAT network:

		nmcli con add type ethernet con-name upstream ifname enp1s0 ipv6.method ignore

For downstream (connected to "isolated" network) use the "Routed /48" subnet,
I've decided to resevre 8 bits making it /64 creating subnet with "cafe"
octets. Make sure the connection is put into "trusted" zone when using
firewalld, otherwise create rules to allow traffic from downstream hosts.

		nmcli c add con-name downstream type ethernet ifname enp2s0 ip6 2001:db8:59ef:cafe::1/64 connection.zone trusted

I haven't looked into how to create 6in4 tunnel via Network Manager, so I used
simple approach which can be found in Example Configurations on the
tunnelbroker.net site:

		# cat /etc/rc.local 
		#!/bin/bash
		nm-online
		IP=$(nmcli -t -f IP4.ADDRESS con show upstream | cut -f2 -d: | cut -f1 -d/)
		ip tunnel add he-ipv6 mode sit remote 216.66.86.122 local $IP ttl 255
		ip link set he-ipv6 up
		ip addr add 2001:db8:6e:443::2/64 dev he-ipv6
		ip route add ::/0 dev he-ipv6

		cat >/etc/resolv.conf <<EOF
		nameserver 2001:db8:20::2
		EOF

		sysctl -w net.ipv6.conf.all.forwarding=1

		touch /var/lock/subsys/local

Remember to make it executable:

		# chmod +x /etc/rc.local

Run the script to create the tunnel and override the upstream DNS server. IPv6
communication should work now:

		# ping6 ipv6.google.com

For my testing purposes, RADVD with DNS advertisment should be enough:

		yum -y install radvd

Configuration is pretty simple, make sure to modify the subnet and interface
name:

		# cat /etc/radvd.conf
		interface enp2s0
		{
						AdvSendAdvert on;
						AdvLinkMTU 1480;
						MaxRtrAdvInterval 300;
						prefix 2001:db8:59ef:cafe::/64
						{
										AdvOnLink on;
										AdvAutonomous on;
						};
						RDNSS 2001:db8:20::2 {
										AdvRDNSSLifetime 600;
						};
		};

Start the service, clients should be able to get IPv6 from the assigned subnet:

		systemctl enable --now radvd

That's all actually, boot a VM in the "isolated" network. Most distributions
will attempt to acquire an IPv6 addres and everything should work as expected.
