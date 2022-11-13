---
type: "post"
aliases:
- /2020/01/how-to-get-rid-of-activate-web-console-in-centos-8.html
date: "2020-01-11T00:00:00Z"
tags:
- linux
- fedora
title: How to get rid of Activate web console in CentOS 8
---

I guess you've seen this already:

    $ ssh root@nas.local
    Activate the web console with: systemctl enable --now cockpit.socket

    Last login: Sat Jan 11 13:05:33 2020 from 192.168.1.137

    # _

That's why you are here, is it? Well, easy help:

    rm -f /etc/issue.d/cockpit.issue /etc/motd.d/cockpit

Problem solved. If you want it back, simply reinstall cockpit package. I am not
sure if upgrade would put them back or not tho.
