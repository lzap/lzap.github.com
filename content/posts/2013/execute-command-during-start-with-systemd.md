---
type: "post"
aliases:
- /2013/08/execute-command-during-start-with-systemd.html
date: "2013-08-30T00:00:00Z"
tags:
- linux
- fedora
title: Execute command during start with systemd
---

I have installed extra bay adapter with HDD drive in my new T430s for purposes
of storing big content (images, ISOs etc). But I don't want to keep the disc
spinning all the time (I mount it only when I need the content). It's making
noise and also eating battery.

There is no rc.local with systemd anymore (sure you can enable it) and I
wanted to execute one simple command during start. How to do that? It's easy
(one need to read man pages: systemd.unit and systemd.service):

    cat /etc/systemd/system/suspend-hdd.service
    [Unit]
    Description=Suspends extra hdd during start - /dev/sdb
    ConditionPathExists=/dev/sdb

    [Service]
    Type=oneshot
    ExecStart=/usr/sbin/hdparm -y /dev/sdb
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target

And then as easy as:

    sudo systemctl enable suspend-hdd
    sudo systemctl start suspend-hdd

If you want your own command, the template would be something like:

    [Unit]
    Description=Blah blah

    [Service]
    Type=oneshot
    ExecStart=/your/command/in/absolute/path

    [Install]
    WantedBy=multi-user.target

By default oneshot service is marked as "inactive", if you want to see it
"active", you can set RemainAfterExit to yes. This is rather cosmetic thing.

My new laptop boots amazingly fast and want to keep my startup scripts fast
and clean. Read: no bash involved :-)

