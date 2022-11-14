---
type: "post"
aliases:
- /2021/01/install-rhel-83-for-free-production-use-in-kvm.html
date: "2021-01-20T00:00:00Z"
tags:
- linux
- fedora
title: Install RHEL 8.3 for free production use in a VM
---

In January 2021, Red Hat
[announced](https://www.redhat.com/en/blog/new-year-new-red-hat-enterprise-linux-programs-easier-ways-access-rhel)
that Red Hat Enterprise Linux can be used at no cost for up to 16 production
servers. In this article, I want to provide step-by-step instructions on how to
install RHEL 8.3 in a VM.

First off, [download](https://access.redhat.com/downloads) the official and
updated QCOW2 image named `rhel-8.3-x86_64-kvm.qcow2` (the name will likely
change later as RHEL moves to higher versions). Creating an account on the Red
Hat Portal is free, there is an integration with 3rd party authorization
services like GitHub, Twitter or Facebook, however for successful host
registration username and password needs to be created.

To use RHEL in a cloud environment like Amazon, Azure or OpenStack, simply
upload the image and start it. It's cloud-init ready, make sure to seed the
instance with data like usernames, passwords and/or ssh-keys. Note that root
account is locked, there is no way to log in without seeding initial
information.

To start RHEL in QEMU/KVM, libvirt or oVirt (Red Hat Virtualization), [several
steps](https://access.redhat.com/solutions/641193) must be performed: root
password should be set, cloud-init must be uninstalled and optionally user
account(s) with password or ssh key should be created.

    $ virt-customize -a rhel-8.3-x86_64-kvm.qcow2 --root-password password:redhat --uninstall cloud-init --hostname rhel8-registered
    [   0.0] Examining the guest ...
    [  11.5] Setting a random seed
    [  11.5] Setting the machine ID in /etc/machine-id
    [  11.5] Uninstalling packages: cloud-init
    [  28.7] Setting passwords
    [  45.2] Finishing off

The utility virt-customize, available in Fedora, RHEL and most other Linux
distributions, is [extremely
flexible](https://libguestfs.org/virt-customize.1.html) allowing pretty much
any change from creating users, installing packages, applying updates. We will
stick with setting up the root password and hostname for now. Note the utility
performs actions on the original image, make sure to have a copy just for case.

    $ sudo virt-install \
      --name rhel8-registered \
      --memory 2048 \
      --vcpus 2 \
      --disk /var/lib/libvirt/images/rhel-8.3-x86_64-kvm.qcow2 \
      --import \
      --os-variant rhel8.3

Once the host boots up, login and register the system. Use the same credentials
as for accessing the Red Hat Portal:

    rhel8# subscription-manager register --username lzap
    Password: **********
    The system has been registered with ID: XXXXXXXXXXXXXXXXXXXXXXXXXXX

This step can be also done via the `virt-customize` utility or automated via
Ansible. And that's it! Start installing software or updating the node:

    rhel8# dnf update; dnf install vim-enhanced

It is worth nothing that `subscription-manager` runs a deamon which
periodically checks-in and uploads installed packages and some hardware facts
about the system. You can review registered systems on the [Subscription
Portal](https://access.redhat.com/management). From there, package and errata
information can be displayed (security vulnerabilities) as well as
repositories, modules and system facts. Note that it is not possible to manage
hosts via Red Hat Portal, nodes can be unregistered tho.

Although I haven't tested this, to convert QCOW2 image to VMWare, perform the
following after the image was modified via `virt-customize`:

    # qemu-img convert -f qcow2 -O vmdk rhel-8.3-x86_64-kvm.qcow2 rhel-8.3-x86_64-kvm.vmdk

To install on a bare-metal node, download one of the installation DVDs, attach
it to the CDROM device or burn and insert physical copy (who does that in 2021
really) and follow the on-screen instructions. Use Red Hat Portal credentials
when asked to register the system.

If you plan to manage fleet of RHEL servers, check out
[Foreman](https://theforeman.org) project which is the upstream for Red Hat
Satellite management platform. Note that content management features provided
by Katello plugin will not work on zero-cost accounts, but other features like
provisioning, remote execution and configuration management will work perfectly
fine with self-supported Red Hat Enterprise Linux nodes registered directly to
Red Hat Portal.

Red Hat Enterprise Linux is a reliable and trusted Linux operating system
available free of charge for up to 16 production instances. Feel free to ask on
the [discussion forums](https://access.redhat.com/discussions). By the way, Red
Hat Portal contains ton of curated and useful stuff, documentation, articles,
howtos, discussion and video content.
