---
type: "post"
aliases:
- /2018/09/delivering-cron-emails-to-gmail-in-rhel.html
date: "2018-09-19T00:00:00Z"
tags:
- linux
- fedora
- rhel
title: Delivering cron and logwatch emails to gmail in RHEL
---

One of my servers has no real DNS name, there is no MX record and I can hardly
confiture postfix for e-mail delivery. While relaying e-mails to another SMTP
server is an option, it's actually not needed to configure MTA in order to get
emails delivered from cron and logwatch. One can use MUA called *mailx* to do
the job.

The goal is to avoid more complex configuration of `postfix` or (jeeeez)
`sendmail`, so this is an alternative approach. I am not telling you this is
the best thing you should do. It just works for few of my Linux servers. This
will work both on RHEL6 and RHEL7 and probably even older or newer versions.
And of course CentOS as well.

Vixie cron, the default cron in RHEL, uses `sendmail` command for all emails.
This is actually part of `postfix` package, delivery is handled by the MTA
which I actually wanted to avoid. In this tutorial, we will configure vixie
cron in RHEL7 to send e-mails via mailx user agent. First of all, get `mailx`
installed:

    # yum -y install mailx

Then edit either `/etc/mail.rc` or `/root/.mailrc` as follows:

    # cat /root/.mailrc
    set name="Server1234"
    set from="username@gmail.com"
    set smtp=smtps://smtp.gmail.com
    set smtp-auth=login
    set smtp-auth-user=username@gmail.com
    set smtp-auth-password=mysecretpassword
    set ssl-verify=ignore
    set nss-config-dir=/etc/pki/nssdb

Make sure that `from` address is same as `smtp-auth-user` address, gmail
servers will insist on this. Server certificate is ignored, you may want to
install it into the NSS database. We are ready to send a test e-mail:

    # mailx -r username@gmail.com username@gmail.com
    Subject: Test

    This is a test
    .
    EOT

There will be a warning on the standard error about unkonwn certificate. I
suggest to put google server CA into the NSS database, but it's harmless and
you can keep it as is if you don't mind man-in-the-middle.

    Error in certificate: Peer's certificate issuer is not recognized.

Now, create a wrapper script that will explicitly set from and to addresses:

    # cat /usr/local/sbin/mailx-r
    #!/bin/sh
    exec mailx -r username@gmail.com username@gmail.com

Make sure the script is executable. Finally, set it via crond command line
option:

    # cat /etc/sysconfig/crond
    CRONDARGS="-m /usr/local/sbin/mailx-r"

And restart crond:

    # service crond restart

You are now receiving e-mails from cron, congratulations. The next step I
usually do is installing logwatch. Since it also uses `sendmail` we want to
disable it and run it manually from our own cron script feeding the output to
the `mailx` command:

    # yum -y install logwatch

Disable the built-in daily report because this one uses `sendmail`. While it
could be possible to change this via some configuration option, I actually like
my very own cron script.

    # cat /etc/logwatch/conf/logwatch.conf
    DailyReport = no

Now, create your own script and feed the output into mailx. For a weekly report
do something like:

    # cat /etc/cron.weekly/logwatch
    #!/bin/bash
    logwatch --print --range 'between -7 days and today' | mailx -s "Logwatch from XYZ" -r username@gmail.com username@gmail.com 2>/dev/null

For a daily report do this:

    # cat /etc/cron.daily/logwatch
    #!/bin/bash
    logwatch --print --range yesterday | mailx -s "Logwatch from XYZ" -r username@gmail.com username@gmail.com 2>/dev/null

Make sure the cron script is executable and test it first. That's all, enjoy
all the e-mails!
