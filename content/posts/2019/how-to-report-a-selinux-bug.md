---
type: "post"
aliases:
- /2019/06/how-to-report-a-selinux-bug.html
date: "2019-06-04T00:00:00Z"
tags:
- linux
- fedora
- rhel
- selinux
title: How to report a SELinux bug
---

A friendly reminder how to report a SELinux bug. First off, find that there actually is a denial:

    # ausearch -m AVC

If there is, let's create a good report. First, install additional tools. On EL7 do:

    # yum -y install setools-console policycoreutils-python policycoreutils selinux-policy-devel

On EL8 one package was renamed:

    # yum -y install setools-console policycoreutils-devel policycoreutils selinux-policy-devel

Now, generate interfaces for audit2allow:

    # sepolgen-ifgen

As the next step I actually recommend to turn off enforcing mode although it can sometimes generate lots of unrelated noise (if domains are not right). But for you it's the easiest way to go. You can either decide to turn it off temporarily:

    # setenforce 0

Or permanently, for this I suggest only to turn it off for the particular domain (and keep the others like ssh):

    # semanage permissive -a xyz_t

Retry again and then report this in a Bugzilla / Redmine / Github issue:

    # ausearch -m AVC
    # audit2allow -aR

That's all for now. If you want only to add an extra rule and switch enforcing back, you can:

    # audit2allow -a -M myfix
    # semodule -i myfix.pp
    # setenforce 1

