---
type: "post"
aliases:
- /2020/01/setting-a-firewalld-zone-for-libvirt-network.html
date: "2020-01-14T00:00:00Z"
tags:
- linux
- fedora
title: Setting a firewalld zone for libvirt network
---

All interfaces managed by libvirt (virbr0, virbr1 etc) are being put into
frewalld zone called "libvirt". This zone allows NAT however it's set quite
strict. Only few services are opened like ssh, http, https, dns, dhcp and icmp.
In case you want to add a new service, the command is:

    firewall-cmd --zone=libvirt --add-port=12345/tcp

Alternatively, if you don't care and use this network for some testing and you
need to access all ports of the gateway, it's possible to change the zone from
"libvirt" to "trusted". You cannot do this using firewall-cmd however as it
will not survive reboot:

    firewall-cmd --zone=trusted --change-interface=virbr0 --permanent # WILL NOT WORK

The trick here is to edit the network definition and add `zone="trusted"`
attribute:

    <network>
      <name>default</name>
      <uuid>9684cabc-0144-4293-887b-d4970c2d2232</uuid>
      <forward mode="nat">
        <nat>
          <port start="1024" end="65535"/>
        </nat>
      </forward>
      <bridge name="virbr0" zone="trusted" stp="on" delay="0"/>
      <mac address="52:54:00:5e:a1:12"/>
      <domain name="nat.lan"/>
      <ip address="192.168.122.1" netmask="255.255.255.0">
        <dhcp>
          <range start="192.168.122.2" end="192.168.122.254"/>
        </dhcp>
      </ip>
    </network>

That's all I have for today.
