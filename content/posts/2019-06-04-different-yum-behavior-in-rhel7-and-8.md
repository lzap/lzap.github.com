---
type: "post"
aliases:
- /2019/06/different-yum-behavior-in-rhel7-and-8.html
date: "2019-06-04T00:00:00Z"
tags:
- linux
- rhel
title: Different yum behavior in RHEL7 and 8
---

Beware, there is a change in behaviour in yum. Example

    # yum -y install vim blahblah

On RHEL7 it

* installs vim,
* informs about non-existing package blahblah,
* error code is 0.

On RHEL8 it

* errors out about non-existing package blahblah,
* vim is not installed,
* error code is 1.

This is an intentional change. As much as I hate it, I understand that it was the perfect time to do it :-)

Update your scripts, this will help:

    # yum -y install --skip-broken vim blahblah

Take care. Oh, one more thing. You can also use `yum --setopt=strict=0 install`
to get the old behavior and this is actually recommended by DNF developers,
however I can hardly imagine remembering this thing.
