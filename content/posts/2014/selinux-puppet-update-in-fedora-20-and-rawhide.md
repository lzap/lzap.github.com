---
type: "post"
aliases:
- /2014/04/selinux-puppet-update-in-fedora-20-and-rawhide.html
date: "2014-04-10T00:00:00Z"
tags:
- linux
- fedora
- puppet
- foreman
title: SELinux Puppet update in Fedora 20 and Rawhide
---

We are rolling out update of Puppet to 3.4.3 in Fedora 20 and Rawhide that
adds one important change. We have found that puppet master was running
unconfined, therefore the Puppet SELinux policy was not effective in Fedoras.


The puppet package update fixes one little issue (missing runtime dependency) and
corrects startup wrappers for systemd which puts Puppet Master into
correct SELinux domain puppetmaster_t. Since this has low security impact, we
have decided to backport this change into Fedora 20 too. Another reason is
the change in selinux-policy package in Fedora 20 which allows us to backport
the changes into EPEL7.

- [Puppet Fedora 20 update](https://admin.fedoraproject.org/updates/puppet-3.4.3-3.fc20)
- [SELinux policy Fedora 20 update](https://admin.fedoraproject.org/updates/FEDORA-2014-4933/selinux-policy-3.12.1-153.fc20)

SELinux core puppet policy was refactored in paralel so we have now
puppetmaster_t and puppetagent_t domains which reflects the state much better.
Previously puppet agent was running under puppet_t confined domain, now it
runs under puppetagent_t domain. Also the agent has loosed security rules
which is great improvement too.

To update your host do the following:

    yum --enablerepo=updates-testing makecache
    yum --enablerepo=updates-testing update selinux-policy puppet puppet-server

When upgrading make sure you have the correct versions on the mirror:

- puppet 3.4.3-3.fc20 or higher
- policy 3.12.1-153.fc20 or higher

Restart puppetmaster, agent and watch for denials. Report success and failures
in my comments or in the update comments.

    grep AVC /var/log/audit/audit.log

Let's make sure we have rock solid version of Puppet hardened with SELinux in
the best quality possible in EPEL7. Thanks for help!
