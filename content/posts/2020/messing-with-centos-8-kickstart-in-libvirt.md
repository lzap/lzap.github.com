---
type: "post"
aliases:
- /2020/01/messing-with-centos-8-kickstart-in-libvirt.html
date: "2020-01-23T00:00:00Z"
tags:
- linux
- fedora
title: Messing with CentOS 8 kickstart in libvirt
---

Today, I was learning some practical details about Dracut, Anaconda and
NetworkManager. In short, the conclusion is we will stick with generating ifcfg
scripts in Foreman but I just wanted to share the command which I used to
quickly provision RHEL 8.0 to test generated networking configuration.

I created a kickstart script for RHEL 8 / CentOS 8 and published it over HTTP:

    text
    network --device=enp1s0 --activate --bootproto=dhcp --noipv6 --hostname ks-test
    firewall --enabled
    url --url="http://mirror.centos.org/centos/8/BaseOS/x86_64/kickstart"
    rootpw --plaintext redhat
    keyboard --xlayouts=us --vckeymap=us
    lang en_US.UTF-8
    selinux --enforcing
    logging --level=info
    timezone US/Eastern
    reboot
    bootloader --location=mbr
    clearpart --all --initlabel
    reqpart
    part / --fstype="ext4" --size=4000
    %packages
    @core
    %end

Make sure to replace the CentOS URL with something close to you, or even your
own mirror which was my case. Then, to create a VM to play around with do:

    sudo virt-install --name ks-test \
      --vcpus 2 --ram 3500 \
      --disk path=/var/lib/libvirt/images/ks-test.qcow2,format=qcow2,size=8 \
      --os-variant rhel8.0 --graphics spice,listen=0.0.0.0 --noautoconsole \
      -l http://mirror.centos.org/centos/8/BaseOS/x86_64/kickstart \
      -x ks=http://www.example.com/kickstart.ks \
      -w network=default -w network=default -w network=default -w network=default

This one has four network cards all connected to "default" libvirt NAT network.
Note the www.example.com host is serving the kickstart I've shown above. That's
all, hope it is useful.

Now, I was messing around with various networking setups:

    network --device=enp1s0 --activate --bootproto=dhcp --noipv6 --hostname ks-test
    network --device=enp2s0 --nodefroute --noipv4 --ipv6 fd00:aaaa:bbbb:cc::1 --vlanid 13 --interfacename=avlan13
    network --device=enp3s0 --noipv4 --noipv6
    network --device=enp4s0 --noipv4 --noipv6
    network --device=bond0 --nodefroute --noipv4 --ipv6 fd00:aaaa:bbbb:cc::2 --bondslaves enp3s0,enp4s0 --bondopts=mode=active-backup,balance-rr;primary=enp3s0 --vlanid 13 --interfacename=bvlan13

I have found that it's much better to stick with generating ifcfg scripts
ourselves in %post section. Although most of the limitations were solved in
RHEL 7 and higher (VLAN, bond, team, bridge can be configured) some interfaces
(slaves specifically) are being initialized by dracut and this would need to be
workarounded. In the end, Dracut and Anaconda writes ifcfg files the same as we
do, so there is no reason to do it this way. Also, ifcfg can be theoretically
reused on other distibutions granted these were made for Red Hat configuration
backward compatibility.

In the future, if we want to move to more consistent network generation, native
NetworkManager ini files is probably way to go because `nmcli` command cannot
be used in `%post` section in kickstart (NetworkManager is not running in the
installed OS chroot). Alternatively, a man-in-middle could be used like Ansible
or Netplan.

Until next time!
