---
title: "Enable libvirt 5.6+ over TCP"
date: 2023-09-11T09:09:11+02:00
type: "post"
tags:
- linux
- fedora
---

I use libvirt quite a lot during my development and I like to use it both through local UNIX sockets and unauthenticated TCP. With the libvirt version 5.6.0 the project moved to socket activation and many tutorials on the internet are not correct on how to setup libvirt for TCP communication. This post will help.

The first thing to realize is that the options which were previously used for this have no effect anymore, this is documented in the example configuration:

    # grep listen_ /etc/libvirt/libvirtd.conf
    listen_tls = 1
    listen_tcp = 1
    listen_addr = "0.0.0.0"

It is systemd who binds sockets now and passes them to the daemon, configuration got a bit easier now. All you want to do is to stop the daemon:

    # systemctl stop libvirtd

And enable TCP or TLS (or both) socket units:

    # systemctl enable --now libvirtd-tcp.socket libvirtd-tls.socket

In the next step, configure authentication as usual, in my case I just want to allow all access which is not recommended and use this with care

    # grep auth_tcp /etc/libvirt/libvirtd.conf
    auth_tcp = "none"

All done, the daemon will be started the next time it is accessed over UNIX socket, TCP and/or TLS depending on your configuration.
