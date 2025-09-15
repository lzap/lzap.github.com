---
type: "post"
aliases:
- /2014/07/tunnel-into-your-libvirt-nat-network-with-socks.html
date: "2014-07-31T00:00:00Z"
tags:
- linux
- fedora
title: Tunnel into your libvirt NAT network with SOCKS
---

My development setup is based on two Fedora boxes: laptop and worstation
situated in Red Hat office. Both machines are powerful enough to run few VMs,
but to leverage hardware, I wanted to use libvirt virtual networks on both
devices. The Xeon server is more capable of running nested KVM virtual
appliances like oVirt or RHEV while laptop is good for local testing.

I have two virtual (NAT) libvirt networks called:

* zzz.lan (server)
* local.lan (laptop)

My goal was to use them seamlessly during my development. Let's focus on the
local.lan first.

Some time ago I was using libvirt bridges, but since I need to tackle with
DHCP/TFTP/DNS services (I work on The Foreman project), NAT was the only
viable option here. The configuration is pretty standard, I created new NAT
network and disabled DHCP service there because I wanted to run my own DHCP
server. You can use "default" one for this purpose.

The key thing is to setup local caching DNS server dnsmasq. In my case, I use
Google public DNS servers as main forwarders:

    laptop# cat /etc/dnsmasq.d/caching
    bind-interfaces
    listen-address=127.0.0.1
    resolv-file=/etc/resolv.dnsmasq

    laptop# cat /etc/resolv.dnsmasq
    nameserver 8.8.8.8
    nameserver 8.8.4.4

    laptop# cat /etc/resolv.conf
    nameserver 127.0.0.1
    domain redhat.com

    laptop# chattr +i /etc/resolv.conf

Having dnsmasq set correctly, now we can add special file that will add all
hosts that has been created via libvirt. This is done automatically by
libvirt.

    laptop# cat /etc/dnsmasq.d/local.lan
    addn-hosts=/var/lib/libvirt/dnsmasq/default.addnhosts

Restart (or start and enable) the service.

    laptop# systemctl enable dnsmasq
    laptop# systemctl start dnsmasq

Tip: When using VPN you can add extra configuration file so all `*.redhat.com`
queries goes to internal DNS servers (these IP addresses are not real). Also
we want to use public DNS server for the adress of the VPN hub, otherwise you
would need to use IP address for that service.

    laptop# cat /etc/dnsmasq.d/redhat.com
    server=/redhat.com/10.20.30.40
    server=/redhat.com/10.20.30.50
    server=/vpn-hub1.redhat.com/8.8.8.8

Now, everytime you create a new VM locally, you only need to refresh dnsmasq
configuration to re-load the default.addnhosts file.

    laptop# virt-install --os-variant rhel6 --vcpus 1 --ram 900 \
        --name myhost.local.lan --boot network --nodisk --noautoconsole

This is as easy as sending HUP signal (or you can do `service reload`) or
similar:

    laptop# pkill -SIGHUP dnsmasq

That's it. You can connect to your server easily:

    laptop# ssh root@myhost.local.lan

I do more. When you shutdown or restart your VM, libvirt (which uses dnsmasq
for DHCP too) can assign different IP, therefore the addnhost entry is not
valid anymore. Therefore I created a simple script that preallocates static
DHCP entry in libvirt, so restarts won't hurt anymore. The snippet is
something like:

    echo "Removing existing DHCP/DNS configuration from libvirt"
    netdump="sudo virsh net-dumpxml default"
    virsh_dhcp=$($netdump | xmllint --xpath "/network/ip/dhcp/host[@mac='$MAC']" - 2>/dev/null)
    virsh_dns=$($netdump | xmllint --xpath "/network/dns/host/hostname[text()='$FQDN']/parent::host" - 2>/dev/null)
    sudo virsh net-update default delete ip-dhcp-host --xml "$virsh_dhcp" --live --config 2>/dev/null
    sudo virsh net-update default delete dns-host --xml "$virsh_dns" --live --config 2>/dev/null

    while true; do
      AIP="192.168.100.$(( ( RANDOM % 250 )  + 2 ))"
      echo "Checking if random IP $AIP is not in use"
      $netdump | xmllint --xpath "/network/ip/dhcp/host[@ip='$AIP']" - &>/dev/null || break
    done

    echo "Deploying DHCP/DNS configuration via libvirt for $AIP"
    sudo virsh net-update default add-last ip-dhcp-host --xml "<host mac='$MAC' name='$FQDN' ip='$AIP'/>" --live --config
    sudo virsh net-update default add-last dns-host --xml "<host ip='$AIP'><hostname>$FQDN</hostname></host>"  --live --configpice,listen=0.0.0.0 -

This will remove existing entries, generates random IP address, checks if that
does not exist and create DHCP (and in addition to that DNS) entries.

Now, this was the easy part. I use the same on my server, but I want to
be able to access the zzz.lan VMs from my laptop too. For web access this
turns out to be quite easy task. For example in Chrome you only need to
created this file:

    laptop# cat ~/proxies.pac
    function FindProxyForURL(url, host) {
      if (shExpMatch(host, "*.zzz.lan*")) {
        return "SOCKS5 localhost:8890";
      } else {
        return "DIRECT";
      }
    }

Start dynamic tunnel to the libvirt hypervisor (the server):

    laptop# cat .ssh/config
    Host server
        HostName server.redhat.com
        DynamicForward 8890

    laptop# ssh -N server &>/dev/null &

And start Chrome with this configuration:

    laptop# google-chrome --proxy-pac-url=file:///home/lzap/proxies.pac

When working on The Foreman development, I also want the application to be
able to connect to various services (like oVirt or RHEV compute resources).
This turns to be possible too. The key utility is tsocks wrapper which is
available in Fedora. We can use the very same ssh dynamic tunnel for that.

    laptop# cat /etc/tsocks.conf
    local = 192.168.0.0/255.255.255.0
    server = 127.0.0.1
    server_port = 8890

The only difference in dnsmasq configuration on the server is that I want
to open it for incoming DNS requests, because my laptop needs to resolve hosts
from zzz.lan:

    server# cat /etc/dnsmasq.d/caching
    bind-interfaces
    resolv-file=/etc/resolv.dnsmasq
    interface=em1
    interface=lo
    no-dhcp-interface=em1

And of course we need to open firewall port:

    server# firewall-cmd --add-service=dns --permanent

Now on the laptop, one more change is needed. I need to direct my local
dnsmasq daemon to resolve from the server dnsmasq (assuming my server IP
address is 10.90.90.90):

    laptop# cat /etc/dnsmasq.d/zzz.lan
    server=/zzz.lan/10.90.90.90

After reloading dnsmasq, I can finally use tsocks:

    laptop# tsocks wget -O - http://ovirt34.zzz.lan

So I can start my application allowing it to connect to zzz.lan NAT network:

    laptop# tsocks foreman_application

That's it. Hope you were inspired.


