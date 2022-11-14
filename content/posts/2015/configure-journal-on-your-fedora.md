---
type: "post"
aliases:
- /2015/04/configure-journal-on-your-fedora.html
date: "2015-04-01T00:00:00Z"
tags:
- linux
- fedora
title: Configure journal on your Fedora
---

I was busy last couple of months, but I am doing fine. Recently, I noticed
that journald system logs on my laptop got bigger recently. By default systemd
eats ten per cent of the size of the file system. That is too much on my 256
MB SSD drive.

    # journalctl --disk-usage
    Journals take up 1.8G on disk.

Configuration is trivial and fully documented in the journald.conf(5) manual
page. My idea is to keep half-a-gig of logs or entries with maximum age of two
months. And I don't want to forward to syslog (klog and console) anymore to
save more space:

    # grep -v '^#' /etc/systemd/journald.conf

    [Journal]
    SystemMaxUse=500M
    MaxRetentionSec=2month
    ForwardToSyslog=no
    ForwardToKMsg=no
    ForwardToConsole=no

Time to restart journald I guess.

    # sudo systemctl restart systemd-journald.service

I had some coredumps in my log and this is a laptop so there are not that many
entries every month, so it's no surprise that disk usage is smaller.

    # journalctl --disk-usage
    Journals take up 224.0M on disk.

Time to do cleanup of syslog log files:

    # sudo rm -v /var/log/*{gz,-[0-9][0-9]*}
    removed ‘/var/log/cron-20150309’
    removed ‘/var/log/cron-20150317’
    removed ‘/var/log/cron-20150323’
    removed ‘/var/log/cron-20150330’
    removed ‘/var/log/dnf.log-20150319’
    ...

And I am not going to use syslog anymore on this laptop.

    # sudo systemctl stop rsyslog.service
    # sudo systemctl disable rsyslog.service

Let's shrink syslog files to let's say thousand of bytes.

    # sudo truncate --size 1000 /var/log/{messages,secure,maillog,cron,spooler,boot.log,dnf.log,fedup.log,firewalld,lastlog,upgrade.log,wtmp,yum.log}

I could go even further by uninstalling *rsyslog* package, but I will leave
that on my system for now. Cheers!
