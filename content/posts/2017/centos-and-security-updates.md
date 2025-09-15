---
type: "post"
aliases:
- /2017/08/centos-and-security-updates.html
date: "2017-08-01T00:00:00Z"
tags:
- linux
- fedora
- centos
- rhel
title: CentOS and security updates
---

I often see articles, blog posts or even [video
tutorials](https://serversforhackers.com/c/automatic-security-updates-centos)
on how to apply security-only errata in CentOS environments or set a cron job
to do this regularly. While it can be very useful to keep components on a
specific version and only updating those which has security fixes, it has one
drawback.

It does not work in CentOS.

The thing is that yum-plugin-security plugin which is available in CentOS
installs just fine and operates properly returning no security updates when
people test this. But the missing bit is metadata in CentOS repositories,
these are not available.

The official position of the CentOS project on the yum-plugin-security is that
the project does not test for CVE closure on updates so does not publish the
necessary metadata for the security plugin to function. If you require such
validation you are encouraged to use RHEL. End of official statement which you
can get by typing "@yumsecurity" on the #centos IRC channel.

Third party repositories might provide security related metadata, EPEL to name
one. This makes things to look like everything works just fine while it does
not. The core components (e.g. kernel, libc, ssh) are indeed not in EPEL and
you can easily get fooled that you are safe.

There are several reasonable workarounds including watching security news or
Red Hat security alerts and applying updates manually, buying Red Hat
Enterprise LInux subscription or simply applying all updates. It's not that
bad as you think, tracking security news is something that every administrator
should do anyway to install just minimum set of updates possible for mission
critical systems.

Update 2018: It looks like there is a way to import errata information into
local yum mirror, Spacewalk, Katello or Satellite 5 or 6:
http://cefs.steve-meier.de/ and this is a way to load errata into CetnOS
clients.

