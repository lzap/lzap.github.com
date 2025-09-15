---
type: "post"
aliases:
- /2022/02/easy-vm-access-with-routed-libvirt-mode.html
date: "2022-02-23T00:00:00Z"
tags:
- linux
- fedora
title: Easy VM access with routed libvirt mode
---

By default, libvirt comes with a virtual network called "default" that is
configured with NAT. That is a very sane default configuration, VMs are
accessible from the host machine directly and they can also access internet via
NAT. Many people, however, want to access VMs from outside - typically when
libvirt is used as a server hypervisor. You will find many blog posts
explaining how to setup a bridge. Configuration of bridge is complex, you need
to shut down the main connection and it is a challenge for users who only have
SSH access to the machine. Only if there was a better way...

Big news if you did not know: you don't need a bridge to access your VMs. You
can use a regular (routed) network! In this article, I will describe how it
works. Spoiler alert: it is easier than bridge!

**Routing? Isn't that difficiult?**

No, it is actually a very important concept. Every machine has a thing called a
routing table, it tells what interface it should send packets to for each
individual network the system is connected to. It also tells which system it
should send patckets for all other cases - this is called the default route.
You can print your own routing table with commans `ip route`.

If you create a libvirt network in route mode and set up the host system to
route packets it will work as a regular network. Of course, all systems that
want to communicate with VMs in the route libvirt network need to know how to
reach the network. There are two options: you can modify routing table for all
systems that are supposed to communicate with VMs, or you can do this on your
(home) router. I will show you both.

**The setup**

As I said, libvirt comes with NAT network, the configuration looks like this (all commands are as root):

	virsh net-edit default

This is how it looks like:

	<network>
	  <name>default</name>
	  <uuid>9f3e4377-3d33-42df-b34c-7880295d24ee</uuid>
	  <forward mode='nat'/>
	  <bridge name='virbr0' zone='trusted' stp='on' delay='0'/>
	  <mac address='52:54:00:7a:00:01'/>
	  <ip address='192.168.122.1' netmask='255.255.255.0'>
	    <dhcp>
	      <range start='192.168.122.2' end='192.168.122.254'/>
	    </dhcp>
	  </ip>
	</network>

You can either modify this directly, or create a new network named differently. Let's simply edit the XML configuration to change it into route mode. Let's perform two changes: change forward mode to route and pick a different subnet address (122 is comonly used so let's use 200):


	<network>
	  <name>default</name>
	  <uuid>9f3e4377-3d33-42df-b34c-7880295d24ee</uuid>
	  <forward mode='route'/>
	  <bridge name='virbr0' zone='trusted' stp='on' delay='0'/>
	  <mac address='52:54:00:7a:00:01'/>
	  <ip address='192.168.200.1' netmask='255.255.255.0'>
	    <dhcp>
	      <range start='192.168.200.2' end='192.168.200.254'/>
	    </dhcp>
	  </ip>
	</network>

That's all, libvirt daemon should have restarted the network already. It should also automatically enable routing on the system, modify firewall and routes. Let's check that:

	cat /proc/sys/net/ipv4/ip_forward

This command must return `1`. Older versions of libvirt will not take care of routing kernel setting or firewall rules, but modern (2020) version I tested with does this for you, no need to do any other commands (tested on Fedora 33). Check the route table on the hosting machine:

	ip r
	...
	192.168.200.0/24 dev virbr0 proto kernel scope link src 192.168.200.1

To enable forwarding on modern Fedora versions, a [native firewall-cmd command](https://firewalld.org/2020/04/intra-zone-forwarding) can be used now:

```
firewall-cmd --zone=internal --add-forward
```

Now, launch a VM, it should get an address from 192.168.200.0 network from libvirt's DHCP automatically. Try to ping it from the host itself, as you can see above the route entry is already there and the system knows that it can reach the VM via `virbr0`.

**Accessing VMs remotely**

Now let's try scenario number one: a remote system wants to connect to your VM. Witnout any configuration, it will not work as the host does not know how to reach the 192.168.200.0 network (has no routing entry). You can create it manually (I am assuming that 192.168.1.5 is the hosting machine - the hypervisor):

	ip route add 192.168.200.0/24 via 192.168.1.5 dev eth0

Now it should work! You can now communicate with all your VMs directly, no NAT, no firewall, no forwarding. It is a direct connection!

You perhaps do not want to modify routing tables for all your hosts. Indeed, you can modify your (home) router to advertise what is called a static route. All clients in the network will automatically add such entry. If you are using ISC DHCP (linux server), then the configuration is something like:

        option classless-static-routes 192.168.200.0 192.168.1.5;

I actually have a Mikrotik DHCP server, that is a completely different beast, the value needs to be in hex and there are online calculators to construct the correct command:

	/ip dhcp-server option
	add code=121 name=classless-static-route-option value=0x00C0A8000118C0A800C0A80001

But the idea is the same for any kind of router, search for "static routes" in the UI.

There is one problem tho, you want VMs from the 192.168.200.0 want to access internet I suppose. In that case, there is one additional change needed. The main router to the internet must be aware of this and NAT (masquerade) must be enabled for such network. If your main internet router is Linux then it is as easy as making sure the internal and external interfaces are set correctly:

	nmcli connection modify ens1 connection.zone internal
	nmcli connection modify ens2 connection.zone external

And firewall daemon will take care of NAT automatically (it is already set for internal/external zones). For home routers, search for NAT, masquerade, srcnat and simply add the 192.168.200.0 next to the main network (192.168.1.0 in my examples). That's all.

**Wait, is that all?**

Yup, it is that easy. With recent libvirt, you just flip the setting to "route" and add a route to your DHCP server. I hope this was useful, retweet this if you find this helpful and remember to tag me I am @lzap on Twitter. Cheers!

