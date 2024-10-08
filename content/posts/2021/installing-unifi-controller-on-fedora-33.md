---
type: "post"
aliases:
- /2021/02/installing-unifi-controller-on-fedora-33.html
date: "2021-02-21T00:00:00Z"
tags:
- linux
- fedora
title: Installing Unifi Controller on Fedora 33
---

**Update**: [New article](/posts/2024/unifi-controller-in-fedora-centos-rhel) deprecates this one, you may want to read the newer one.

Installing Unifi Controller in Fedora 33 is easy. Step one: install MongoDB from [the official site](https://www.mongodb.com/download-center/community) since it is no longer available in Fedora due to licensing reasons. Use EL8 version which appears to work fine:

	# dnf install ./mongodb-org-server-4.4.4-1.el8.x86_64.rpm

If you haven't enabled RPMFusion repository, do it:

	# dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

Install the controller:

	# dnf install unifi

For some reason, unifi has hardcoded path to java alternatives symlink which did not work on the initial start (`/usr/lib/jvm/jre-1.8.0/bin/java`), reinstalling Java did help:

	# dnf reinstall java-1.8.0-openjdk-headless

And enable the service:

	# systemctl enable --now unifi

Beware, mongo service does not need to be started, unifi service spawns it's own process:

	# systemctl disable --now mongod

You're done! Visit https://nuc.home.lan:8443 to manage your site.
