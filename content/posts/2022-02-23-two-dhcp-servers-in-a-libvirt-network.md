---
type: "post"
aliases:
- /2022/02/two-dhcp-servers-in-a-libvirt-network.html
date: "2022-02-23T00:00:00Z"
tags:
- linux
- fedora
title: Two DHCP servers in a libvirt network
---

I write provisioning software that needs to integrate with DHCP servers. Libvirt is a great Linux virtual environment for development, but by default it runs its own DHCP server (dnsmasq). That is a very good feature for spawning ad-hoc VMs which get their IPs easily. But I want also to manage some VMs with my own DHCP server. How to do this?

It's possible to configure libvirt's dnsmasq to ignore pre-reserved host entries. This is how to do it:

	virsh net-destroy default
	virsh net-undefine default
	cat >/tmp/network.xml <<EOF
	<network xmlns:dnsmasq='http://libvirt.org/schemas/network/dnsmasq/1.0'>
	  <name>default</name>
	  <forward mode='nat'/>
	  <bridge name='virbr0' zone='trusted' stp='on' delay='0'/>
	  <mac address='52:54:00:c9:00:01'/>
	  <ip address='192.168.122.1' netmask='255.255.255.0'>
	    <dhcp>
	      <range start='192.168.122.2' end='192.168.122.254'/>
	      <host mac='52:54:00:c9:00:10' ip='192.168.122.10'/>
	      <host mac='52:54:00:c9:00:11' ip='192.168.122.11'/>
	      <host mac='52:54:00:c9:00:12' ip='192.168.122.12'/>
	      <host mac='52:54:00:c9:00:13' ip='192.168.122.13'/>
	      <host mac='52:54:00:c9:00:14' ip='192.168.122.14'/>
	      <host mac='52:54:00:c9:00:15' ip='192.168.122.15'/>
	      <host mac='52:54:00:c9:00:16' ip='192.168.122.16'/>
	      <host mac='52:54:00:c9:00:17' ip='192.168.122.17'/>
	      <host mac='52:54:00:c9:00:18' ip='192.168.122.18'/>
	      <host mac='52:54:00:c9:00:19' ip='192.168.122.19'/>
	    </dhcp>
	  </ip>
	  <dnsmasq:options>
	    <dnsmasq:option value='dhcp-ignore=tag:!known'/>
	  </dnsmasq:options>
	</network>
	EOF
	virsh net-define /tmp/network.xml && rm -f /tmp/network.xml
	virsh net-start default
	virsh net-autostart default

I defined series of pre-allocated MAC addresses (10-19). VMs which I create with these MAC addresses will always get IP address from dnsmasq and they will be guaranteed to be the same. I use these VMs to deploy my the management software that includes DHCP server. Other VMs which do not have MAC addresses from the list are ignored by the dnsmasq therefore my own DHCP server can offer them IP addresses.

I tend to pre-allocated not only MAC addresses, but also VMs and their storage. I have two types, big and small:

	for X in s11 s13 s15 s17 s19; do lvcreate -L 8g -n $X vg_slow; done
	for X in b10 b12 b14 b16 b18; do lvcreate -L 25g -n $X vg_slow; done

Then installing them is a matter of creating images:

	virt-install -n b10.local --memory 15500 --vcpus 2 --os-variant rhel8-unknown --graphics none --noautoconsole --boot bootmenu.enable=on,bios.useserial=on --serial pty --disk vol=vg_virt/b10.local --network default,mac=52:54:00:c8:00:10
	virt-builder rhel-7.9 --output /dev/vg_virt/b10.local --root-password password:redhat --hostname b10.local --ssh-inject root:file:/home/lzap/.ssh/id_rsa.pub

Something like that, I just wanted to show the dhcp-ignore trick. Cheers!
