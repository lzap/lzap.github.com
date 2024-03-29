---
type: "post"
aliases:
- /2018/02/accessing-libvirt-vms-via-telnet.html
date: "2018-02-20T00:00:00Z"
tags:
- linux
- fedora
- rhel
- libvirt
title: Accessing libvirt VMs via telnet
---

There are many "tricks" floating around how to connect to VM when you have a
networking issue and ssh is not available. The idea is to use serial console to
get shell access. Here is how to do this properly with RHEL7 host and guest.

First, create a VM with serial console configured with [remote TCP
server](https://libvirt.org/formatdomain.html#elementsCharTCP). There are
multiple options, I find TCP server in 'telnet' mode the most flexible
configuration because most scripting languages has the protocol built-in. You
can use virt-manager or virt-install to do that:

    <devices>
      <serial type="tcp">
        <source mode="connect" host="0.0.0.0" service="4555"/>
        <protocol type="telnet"/>
        <target port="0"/>
      </serial>
    </devices>

Boot the VM and then enable getty:

    $ systemctl enable serial-getty@ttyS0.service
    $ systemctl start serial-getty@ttyS0.service

That's all, access the console interactively:

    $ telnet localhost 4555

To access 'raw' console (protocol type in the XML snippet above), use netcat or
similar tool. Other options in libvirt are logfile, UDP, pseudo TTY, named
pipe, unix socket or null. You get the idea.

When creating multiple serial devices, only the first one (`ttyS0`) is allowed
for root access by default. To enable second one, do:

    $ echo ttyS1 >> /etc/securetty

That's all for today.
