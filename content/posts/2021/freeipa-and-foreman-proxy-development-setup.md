---
type: "post"
aliases:
- /2021/04/freeipa-and-foreman-proxy-development-setup.html
date: "2021-04-12T00:00:00Z"
tags:
- linux
- fedora
title: FreeIPA and Foreman Proxy development setup
---

I have been avoiding this for like ten years now, but today is the day when I
will setup a FreeIPA with Foreman Proxy for development and testing purposes
and here are my notes.

The goal is to deploy a libvirt VM with IPA server and Foreman Proxy intergated
with it. The domain will be `ipa.lan` and the host named `ipa.ipa.lan`. This is
NOT how you should deploy production Foreman FreeIPA integration! For that,
reading our [official
documentation](https://docs.theforeman.org/nightly/Administering_Red_Hat_Satellite/index-foreman-el.html#sect-Red_Hat_Satellite-Administering_Red_Hat_Satellite-Configuring_External_Authentication-External_Authentication_for_Provisioned_Hosts)
and using `foreman-installer` is suggested instead.

We need a VM, let's go with CentOS 8.

    virt-builder centos-8.2 --output /var/lib/libvirt/images/ipa.img --root-password password:redhat --hostname ipa.ipa.lan
    virt-install --name ipa.ipa.lan --memory 2048 --vcpus 2 --disk /var/lib/libvirt/images/ipa.img --import --os-variant rhel8.3 --update
    virsh console ipa.ipa.lan

We need a static IP for this VM:

    nmcli con modify enp1s0 \
      ip4 192.168.122.5/24 \
      gw4 192.168.122.1 \
      ipv4.dns 192.168.122.1
    nmcli con down enp1s0
    nmcli con up enp1s0

Make sure the hostname is correct:

    hostnamectl set-hostname ipa.ipa.lan

Make sure to fix hosts file, FQDN must resolve to the IP address not localhost:

    grep ipa /etc/hosts
    192.168.122.5 ipa.ipa.lan ipa

The installation is very smooth, expect just couple of questions like administrator password or the actual domain:

    dnf module enable idm:DL1
    dnf module install idm:DL1/dns
    ipa-server-install --setup-dns --auto-forwarder --auto-reverse

Ensure firewall ports are enabled:

    firewall-cmd --add-service=http --add-service=https --add-service=ldap --add-service=ldaps \
        --add-service=ntp --add-service=kerberos --add-service=dns --add-port=8000/tcp --permanent

Next up, install Foreman Proxy:

    dnf -y install https://yum.theforeman.org/releases/2.4/el8/x86_64/foreman-release.rpm
    dnf -y install foreman-proxy

Create the foreman user with minimum required permissions to manage Foreman
hosts, create and configure keytab file. When asked for `admin` password, use
the one used when installing the IPA server:

    foreman-prepare-realm admin realm-smart-proxy
    mv freeipa.keytab /etc/foreman-proxy/freeipa.keytab
    chown foreman-proxy:foreman-proxy /etc/foreman-proxy/freeipa.keytab

Configure and start the Foreman Proxy service. This is for development
purposes, so let's only use HTTP. You may also want to add some `trusted_hosts`
entries to allow access from Foreman:

    cat /etc/foreman-proxy/settings.yml
    ---
    :settings_directory: /etc/foreman-proxy/settings.d
    :http_port: 8000
    :log_level: DEBUG

Enable Realm module:

    cat /etc/foreman-proxy/settings.d/realm.yml
    ---
    :enabled: true
    :use_provider: realm_freeipa

And enable FreeIPA plugin:

    cat /etc/foreman-proxy/settings.d/realm_freeipa.yml
    ---
    :keytab_path: /etc/foreman-proxy/freeipa.keytab
    :principal: realm-smart-proxy@IPA.LAN
    :ipa_config: /etc/ipa/default.conf
    :remove_dns: true
    :verify_ca: true

And start it up:

    systemctl enable --now foreman-proxy

Realm feature should be available:

    curl http://ipa.ipa.lan:8000/features
    ["realm"]

To show a host entry in IPA via CLI:

    kinit admin
    ipa host-show rex-dzurnak.ipa.lan
      Host name: rex-dzurnak.ipa.lan
      Class: ipa-debian-10
      Password: True
      Keytab: False
      Managed by: rex-dzurnak.ipa.lan

Add the foreman proxy into Foreman and start developing or testing. Have fun!
