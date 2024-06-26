---
type: "post"
aliases:
- /2022/11/apache2-http-logging-into-journald-ring-buffer.html
date: "2022-11-07T00:00:00Z"
tags:
- linux
- fedora
title: Apache2 http logging into journald ring buffer
---

My webserver at home has several services including Mastodon. And I use Apache2
for web content and as a reverse web proxy, however, this system is configured
to log all hits in `/var/log/httpd`. Both disks in my server are SSD and I
do not want to let it to rotate hundreds of megabytes of access logs every
week full of bots trying to find security hole in wordpress or other
known software (which is not even running on my site).

To solve this, you can configure Apache2 httpd to log into systemd journald
which can be configured in volatile mode. This is essentially a ring buffer
that consumes some memory and never writes anything to disk keeping my SSD wear
leveling at a reasonable level. To do this simply turn journal into volatile
mode, turn off rate limiting and set amount of memory you want to dedicate for
the journal:

        [Journal]
        Storage=volatile
        RateLimitIntervalSec=0
        RateLimitBurst=0
        RuntimeMaxUse=10M

Warning: If you run any kind of public service, check with legal before you do
this. Some limitations may apply depending on where you live or the server is
located in regard to data retention.

Although Apache2 httpd 2.5+ had [dedicated
module](https://httpd.apache.org/docs/trunk/mod/mod_journald.html) for writing
to the system journal, this is not even in Fedora yet. The workaround is simple
- to use piped command which logs into the journal. In this mode, httpd spawns
a process and logs into its standard input. The program we can use ships with
systemd: `logger`:

        # cat /etc/httpd/conf/httpd.conf
        ...
        LogFormat "%h \"%r\" %>s %b" journal
        CustomLog "|/usr/bin/logger -t httpd -p local7.info" journal
        ErrorLog "|/usr/bin/logger -t httpd -p local7.info"
        ...

Do the same for `ssl.conf` file which has configuration for TLS. You can use
the "common" log format, but in that case you will see date and time twice, so
I ended up creating more simple format that looks like this:

        # journalctl -f
        Nov 07 14:13:53 nuc.home.lan httpd[225124]: 162.19.29.212 "POST /users/lukas/inbox HTTP/1.1" 401 23

That's all for today. Cheers.
