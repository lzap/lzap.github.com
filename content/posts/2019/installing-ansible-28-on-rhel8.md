---
type: "post"
aliases:
- /2019/06/installing-ansible-28-on-rhel8.html
date: "2019-06-03T00:00:00Z"
tags:
- linux
- rhel8
title: Installing Ansible Engine 2.8 on RHEL 8
---

Step one: Register and attach a subscription:

    # subscription-manager register --auto-attach
    Registering to: subscription.rhsm.redhat.com:443/subscription
    Username: xxx
    Password: ********
    The system has been registered with ID: db829ea7-e0f6-4586-bd0a-d2648681d1d2
    The registered system name is: eight.example.com

Step two: Enable Ansible Engine 2.8 repository, assuming the subscription have that available:

    # subscription-manager repos --enable ansible-2.8-for-rhel-8-x86_64-rpms
    Repository 'ansible-2.8-for-rhel-8-x86_64-rpms' is enabled for this system.

Step three: Install the thing:

    # yum -y install ansible

Step four: Profit!

    # ansible --version
    ansible 2.8.0
      config file = /etc/ansible/ansible.cfg
      configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
      ansible python module location = /usr/lib/python3.6/site-packages/ansible
      executable location = /usr/bin/ansible
      python version = 3.6.8 (default, Jan 11 2019, 02:17:16) [GCC 8.2.1 20180905 (Red Hat 8.2.1-3)]

