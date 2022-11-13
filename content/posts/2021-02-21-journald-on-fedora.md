---
type: "post"
aliases:
- /2021/02/journald-on-fedora.html
date: "2021-02-21T00:00:00Z"
tags:
- linux
- fedora
title: Remove rsyslog and use journald in Fedora
---

I am reinstalling my home server from scratch, I want to start using BTRFS
which seems like a great fit for what I am doing (NAS, backups). Installation
was smooth, no problems, however I noticed that Fedora Server 33 installed both
journald and rsyslogd and journal was configured to do persistent logging.

You know, this is weird. On Red Hat Enterprise Linux 7 and 8, journald is
configured in volatile mode and it's set to forward all logs to syslog. On
Fedora 33, it looks like both rsyslog and journald are logging
(`/var/log/messages` and `/var/log/journal` respectively). No forwarding is
going on.  This is weird, I am going to file a BZ for folks to investigate.

However, I like to only use journald these days, here is how to do it.  Stop
the journald:

	# systemctl stop systemd-journald

Configure journald, if you want use persistent logging there is actually
nothing to configure and just make sure the directory exists:

	# mkdir /var/log/journal
	# systemd-tmpfiles --create --prefix /var/log/journal

If you want to use volatile logging (only in memory), configure as follows
(feel free to modify the maximum memory I am just feeling that few megabytes is
okay):

	# cat /etc/systemd/journald.conf
	[Journal]
	Storage=volatile
	RuntimeMaxUse=5M

Optionally, delete existing logs if you plan using volatile logging:

	# journalctl --rotate
	# journalctl --vacuum-size=0

Finally, start up the service:

	# systemctl start systemd-journald

You may uninstall rsyslog too:

	# systemctl disable --now rsyslog
	# dnf remove rsyslog

Done!
