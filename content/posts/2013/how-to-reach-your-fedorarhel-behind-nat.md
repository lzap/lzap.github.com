---
type: "post"
aliases:
- /2013/11/how-to-reach-your-fedorarhel-behind-nat.html
date: "2013-11-27T00:00:00Z"
tags:
- linux
- fedora
title: How to reach your Fedora/RHEL behind NAT
---

I am using an excellent open-source tunneling solution called PageKite for
about an year now. It's a small utility written in Python with almost zero
dependencies (okay there is one) and it enables you to reach various ports
behind NAT. More on the [PageKite.net](https://pagekite.net) which also
provides subscription-based service for those who do not want to run their own
man-in-the-middle server (which is needed for this to operate). By the way
they datacenters are spread over whole world with excellent Europe coverage.

After decent testing time, I pushed PageKite into EPEL 5 and 6 (it is already
included in Fedora repos). Installation and setup is ultra easy:

    # yum -y install pagekite

In the PageKite.net service, create your account and create new "kite". That
is basically a subdomain which will be used for your machine. Now edit this
file:

    # vim /etc/pagekite.d/10_account.rc

Set your 'kitename' (which you created recently) and 'kitesecret' token and
delete 'abort\_not\_configured' line. We want to enable SSH tunneling:

    # mv /etc/pagekite.d/80_sshd.rc.sample /etc/pagekite.d/80_sshd.rc

If you want to tunnel HTTP, do this:

    # mv /etc/pagekite.d/80_httpd.rc.sample /etc/pagekite.d/80_httpd.rc

You can tunnel any other protocol, read PageKite documentation for more. Start
the thing:

    # service pagekite start

Logs are here:

    # tail /var/log/pagekite/pagekite.log -f

It's the time to connect via your new tunnel. It is not that straightforward
as you may expect, but you need to tune your ssh client configuration a bit:

    # vim ~/.ssh/config
    ...
    Host *.pagekite.me
        CheckHostIP no
        ProxyCommand /usr/bin/corkscrew %h 443 %h %p
    ...

I am using corkscrew tool which is a TCP tunneling solution via HTTP, which
works great with PageKite. There are other options, but this one is the
easiest and the most reliable. You will need to install the corkscrew tool (I
am on Fedora):

    # yum -y install corkscrew

Work done!

    # ssh yourkite-yourname.pagekite.me

Nice, isn't it? Now, if you find out how to tunnel
[mosh](http://mosh.mit.edu/) protocol, let me know bellow.

