---
type: "post"
aliases:
- /2015/09/how-to-configure-nfs-firewall-in-rhel7.html
date: "2015-09-11T00:00:00Z"
tags:
- linux
- fedora
- rhel7
title: How to configure NFS firewall in RHEL7
---

If you intend to use NFSv4 protocol only, all you need to do is this:

    firewall-cmd --permanent --zone public --add-service nfs
    firewall-cmd --reload

But if you want to use NFSv3 protocol, things are more complicated.

    firewall-cmd --permanent --zone public --add-service mountd
    firewall-cmd --permanent --zone public --add-service rpc-bind
    firewall-cmd --permanent --zone public --add-service nfs
    firewall-cmd --reload
