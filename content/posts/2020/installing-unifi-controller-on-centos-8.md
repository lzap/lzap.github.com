---
type: "post"
aliases:
- /2020/01/installing-unifi-controller-on-centos-8.html
date: "2020-01-13T00:00:00Z"
tags:
- linux
- fedora
title: Installing Unifi Controller on CentOS 8
---

**Update**: [New article](/posts/2024/unifi-controller-in-fedora-centos-rhel) deprecates this one, you may want to read the newer one.

This tutorial covers installation of UniFi from RPMFusion repository on OpenJDK
with MongoDB from official community repository. It kinda works, but I've hit
few bugs here and there, therefore I'd suggest you to use "tarball"
installation with Oracle JDK instead. I plan to do new blogpost on this topic
soon - search my blog.

First, enable PowerTools CentOS repository:

    dnf install dnf-plugins-core
    yum config-manager --set-enabled PowerTools

You can enable all the official repositories as they contain pretty useful
stuff, but it's not needed:

    yum config-manager --set-enabled PowerTools --set-enabled centosplus --set-enabled extras

Then enable EPEL and very much needed RPMFusion:

    dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
    dnf -y install --nogpgcheck https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
    dnf -y install --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
    dnf -y install --nogpgcheck https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm

And you guessed it:

    dnf -y install unifi

There's also `unifi-lts` Long Term Support release available if you want to
avoid frequent updates. Due to licensing issues, MongoDB has been removed from
Fedora and CentOS8, install [MongoDB Community
edition](https://www.mongodb.com/download-center/community):

    dnf -y install https://repo.mongodb.org/yum/redhat/8/mongodb-org/4.2/x86_64/RPMS/mongodb-org-server-4.2.2-1.el8.x86_64.rpm

Enable and start the unifi service. Note the mongod service does not need to be started, unifi process starts its own instance:

    systemctl enable --now unifi

Beware, logs are in non-standard location:

    tail -f /usr/share/unifi/logs/server.log

Visit the web UI for the initial configuration: `https://nuc.home.lan:8443` and
have fun!
