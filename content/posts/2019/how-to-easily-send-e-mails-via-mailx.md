---
type: "post"
aliases:
- /2019/11/how-to-easily-send-e-mails-via-mailx.html
date: "2019-11-27T00:00:00Z"
tags:
- linux
- fedora
title: How to easily send e-mails via mailx
---

So far I've been pretty fine with having postfix to relay my emails from
command line, but today I've learned that the tool I use for sending emails
from cron (`mailx`) can be easily configured to relay the mail directly. It's
super easy:

    $ cat ~/.mailrc
    set smtp-use-starttls
    set smtp=smtp://smtp.xxx.redhat.com:587
    set from=xxx@redhat.com

That's all. To test the delivery use `-v` option:

    echo "How you doin?" | mail -v -s Test xxx@redhat.com
    Resolving host smtp.xxx.redhat.com . . . done.
    Connecting to 10.4.203.49:587 . . . connected.
    220 smtp.xxx.redhat.com ESMTP Postfix
    >>> EHLO box
    250-smtp.xxx.redhat.com
    250-PIPELINING
    250-SIZE 30000000
    250-VRFY
    250-ETRN
    250-STARTTLS
    250-ENHANCEDSTATUSCODES
    250-8BITMIME
    250 DSN
    >>> STARTTLS
    220 2.0.0 Ready to start TLS
    >>> HELO box
    250 smtp.xxx.redhat.com
    >>> MAIL FROM:<xxx@redhat.com>
    250 2.1.0 Ok
    >>> RCPT TO:<xxx@redhat.com>
    250 2.1.5 Ok
    >>> DATA
    354 End data with <CR><LF>.<CR><LF>
    >>> .
    250 2.0.0 Ok: queued as 89664600CC
    >>> QUIT
    221 2.0.0 Bye

I think I can shutdown postfix on my workstation now. Served well, thank you,
but it was pretty much an overkill for my single email per day.

