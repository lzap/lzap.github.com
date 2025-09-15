---
type: "post"
aliases:
- /2015/09/fedora-22-libvirt-with-bridge.html
date: "2015-09-24T00:00:00Z"
tags:
- linux
- fedora
title: Fedora 22 libvirt with bridge
---

Fedora 22 comes with libvirt and NetworkManager and it is pre-configured with
"default" NAT network. That's fine, until you want to reach the NATed servers
from your LAN. By the way this works in CentOS 7 too.

Good solution is network interface bridging. It was always a pain to configure
this, but in Fedora 21 most of bugs were fixed and now it is possible to
configure everything via NetworkManager.

In this tutorial, I will show you how to configure things without GUI. The
commands below adds bridge in the system and reconfigures primary wired
connection over that bridge. Make sure you set `MAIN_CONN` variable to the
correct connection (use `nmcli c show` to find it).

I recommend to execute this in screen or tmux because connection *will* be
lost during execution! Comment out IPv4 static configuration, if that's your
case.

    yum -y install bridge-utils
    yum -y groupinstall "Virtualization Tools"
    export MAIN_CONN=enp8s0
    bash -x <<EOS
    systemctl stop libvirtd
    nmcli c delete "$MAIN_CONN"
    nmcli c delete "Wired connection 1"
    nmcli c add type bridge ifname br0 autoconnect yes con-name br0 stp off
    #nmcli c modify br0 ipv4.addresses 192.168.1.99/24 ipv4.method manual
    #nmcli c modify br0 ipv4.gateway 192.168.1.1
    #nmcli c modify br0 ipv4.dns 192.168.1.1
    nmcli c add type bridge-slave autoconnect yes con-name "$MAIN_CONN" ifname "$MAIN_CONN" master br0
    systemctl restart NetworkManager
    systemctl start libvirtd
    systemctl enable libvirtd
    echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-ipforward.conf
    sysctl -p /etc/sysctl.d/99-ipforward.conf
    EOS

Do not, I repeat, do not execute this one by one. You need to do this in one
"transaction" because connection will be lost and screen wont help you in this
case. That's why I use `bash -x HEREDOC` there.

Reboot might be needed if you encounter networking issues.

Now, when creating a VM in libvirt, make sure you select "br0" as the
interface to use bridged networking. That's all for today!

