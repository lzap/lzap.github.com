---
type: "post"
aliases:
- /2020/01/aaaa-dns-record-in-libvirt.html
date: "2020-01-31T00:00:00Z"
tags:
- linux
- fedora
title: AAAA DNS record in libvirt
---

Hello, for some time now it's possible to create AAAA DNS records in a libvirt
virtual network. It's very similar to creating A records (or host records) and
they are meant for allocating IP addresses to hosts but since libvirt uses
dnsmasq which handles both DHCP and DNS records, you can take advantage for
this and create arbitrary records.

This is useful if you want to do PXE or UEFI HTTP Boot provisioning in an IPv6
only virtual network with full DNS working setup for example because of X.509.

To create a DHCP with A record, a `<host/>` element in `<ip/>` - `<dhcp/>`
element must be created:

    <host name="a.host.lan" mac="aa:bb:cc:dd:ee:ff" ip="10.0.0.13"/>

For AAAA, it's essentially the same except there is no MAC attribute, instead
ID (client ID) can be optionally provided but that's only useful for IP
assignment:

    <host name="gw.dhcpsix.lan" ip="fd00:bbbb:cccc:dd::1"/>

Here is an example of IPv6 DHCP virtual network with a host entry:

    <network>
      <name>dhcpsix.lan</name>
      <uuid>422ded85-a29b-428e-9cb0-a48bf6299b5c</uuid>
      <forward mode="nat"/>
      <bridge name="virbr2" stp="on" delay="0"/>
      <mac address="52:54:00:e6:57:da"/>
      <domain name="dhcpsix.lan"/>
      <ip family="ipv6" address="fd00:bbbb:cccc:dd::1" prefix="64">
        <dhcp>
          <range start="fd00:bbbb:cccc:dd::100" end="fd00:bbbb:cccc:dd::1ff"/>
          <host name="gw.dhcpsix.lan" ip="fd00:bbbb:cccc:dd::1"/>
        </dhcp>
      </ip>
    </network>

To add the `<host/>` line, just use virt-manager which recently received XML
editing capability or simply use `virsh net-edit dhcpsix.lan` to edit the
configuration. Restart the network then, not host nework but libvirt virtual
network. Again, you can use virt-manager or virsh command to do that.
