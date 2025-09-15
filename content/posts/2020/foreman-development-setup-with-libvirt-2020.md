---
type: "post"
aliases:
- /2020/09/foreman-development-setup-with-libvirt-2020.html
date: "2020-09-22T00:00:00Z"
tags:
- linux
- fedora
title: Foreman development setup with libvirt 2020
---

Thanks to [dnsmasq DHCP Foreman](https://github.com/theforeman/smart_proxy_dhcp_dnsmasq) plugin, development setup for provisioning can be little bit easier. After git checkout of Foreman core, Smart Proxy and Smart Proxy DHCP Dnsmasq plugin, perform creation of initial directory structure:

    # DEVELOPER=lzap
    # mkdir /var/lib/libvirt/dnsmasq/foreman-default
    # chown $DEVELOPER:dnsmasq /var/lib/libvirt/dnsmasq/foreman-default
    # touch /var/lib/dnsmasq/foreman-default.leases
    # chown $DEVELOPER:dnsmasq /var/lib/dnsmasq/foreman-default.leases
    # mkdir /var/lib/dnsmasq/tftp
    # chown $DEVELOPER:dnsmasq /var/lib/dnsmasq/tftp/
    # setfacl -m u:$DEVELOPER:r-- /var/lib/libvirt/dnsmasq/default.conf

Copy PXELinux files, this will work also for Grub2 or iPXE:

    # cp /usr/share/syslinux/*.{bin,c32,0} /var/lib/dnsmasq/tftp

Finally, change libvirt "default" network configuration in the following way. The difference between the default configuration are the following elements or attributes:

* tftp
* bootp
* dnsmasq:options
* xmlns:dnsmasq

    <network xmlns:dnsmasq="http://libvirt.org/schemas/network/dnsmasq/1.0">
      <name>default</name>
      <uuid>25fd4c6e-4d9e-45a6-b448-57900c3315f2</uuid>
      <forward mode="nat">
        <nat>
          <port start="1024" end="65535"/>
        </nat>
      </forward>
      <bridge name="virbr0" zone="trusted" stp="on" delay="0"/>
      <mac address="52:54:00:dd:b0:55"/>
      <ip address="192.168.122.1" netmask="255.255.255.0">
        <tftp root="/var/lib/dnsmasq/tftp"/>
        <dhcp>
          <range start="192.168.122.2" end="192.168.122.254"/>
          <bootp file="pxelinux.0"/>
        </dhcp>
      </ip>
      <dnsmasq:options>
        <dnsmasq:option value="dhcp-optsfile=/var/lib/libvirt/dnsmasq/foreman-default/dhcpopts.conf"/>
        <dnsmasq:option value="dhcp-hostsfile=/var/lib/libvirt/dnsmasq/foreman-default/dhcphosts"/>
        <dnsmasq:option value="dhcp-leasefile=/var/lib/dnsmasq/foreman-default.leases"/>
      </dnsmasq:options>
    </network>

Restart libvirt network named "default" and you are good to go. Note in this setup I haven't configured DNS, therefore `unattended_url` must be set to something like `http://192.168.122.1:3000`.

