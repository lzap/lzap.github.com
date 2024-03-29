---
type: "post"
aliases:
- /2014/05/track-short-lived-processes-with-auditd.html
date: "2014-05-27T00:00:00Z"
tags:
- linux
- fedora
title: Track short lived processes with auditd
---

I had a hard time to find some more information about short lived processes
when I was building Foreman SELinux policy for OpenStack Installer (Staypuft).
I wanted to see process name and all the parameters for all possible processes
spawned on my system. My plan was to write a SystemTap script, but thank to
Mirek Grepl and Steve Grubb I learned much easier trick to do that. This
assumes you have auditd daemon installed (RHEL/Fedoras are fine):

    auditctl -a exit,always -S execve

Then tail your /var/log/audit/audit.log to see messages. Warning: This can
flood your system heavily. You will see some decent content there like:

    type=CWD msg=audit(1401202071.000:14728):  cwd="/"
    type=PATH msg=audit(1401202071.000:14728): item=0 name="/usr/sbin/ps" nametype=UNKNOWN
    type=SYSCALL msg=audit(1401202071.000:14729): arch=c000003e syscall=59 success=yes exit=0 a0=7fe10bbe6369 a1=7fe10bbe7580 a2=7fff0b1d3208 a3=0 items=2 ppid=26400 pid=5161 auid=0 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=875 comm="ps" exe="/bin/ps" subj=unconfined_u:system_r:passenger_t:s0 key=(null)
    type=EXECVE msg=audit(1401202071.000:14729): argc=5 a0="ps" a1="-o" a2="pid,ppid,%cpu,rss,vsize,pgid,command" a3="-p" a4="26974,26817"

I was able to tell that mod_passenger is spawning /bin/ps every few seconds.
This is very useful when tracking down some processes with long puppet runs.
To turn the audit rule down, replace `-a` option with `-d`:

    auditctl -d exit,always -S execve

You can filter out audit logs, see auditctl manual page. For example I was
interested in processes running in passenger_t SELinux domain:

    auditctl -a exit,always -S execve -F subj_type=passenger_t

To add rules permanently, edit `/etc/audit/audit.rules` file and restart
auditd daemon.
