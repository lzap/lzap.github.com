---
type: "post"
aliases:
- /2021/11/fedora-silverlight-not-only-for-your-grandma.html
date: "2021-11-11T00:00:00Z"
tags:
- linux
- fedora
title: 'Fedora Silverlight: not only for your grandma'
---
Fedora Silverblue: not only for your grandma
============================================

I have migrated my grandparents to Fedora Silverblue, previously they used
CentOS. I was impressed how everything worked well and I like where Fedora is
going overall. Less pre-installed software, I am hoping for more packages to be
dropped - Evolution backend, on-line accounts, Maps and others. Overall, it
works great.

Setting up Fedora Silverblue was easy, installation smooth. Then I had to
ensure screen does not lock (they hate this):

    gsettings set org.gnome.desktop.screensaver lock-enabled false

Timezone was not right, I had to misclick during installation:

    timedatectl set-timezone Europe/Prague

I have found out that the default policy is not to automaticaly update OS
without askint, what I want is auto updating without any question because they
would never confirm it:

    grep Update /etc/rpm-ostreed.conf
    AutomaticUpdatePolicy=stage

This configuration should stage updates for automatic installation (I mean
boot). This finishes the configuration:

    rpm-ostree reload
    systemctl enable rpm-ostreed-automatic.timer --now

Now, I want to access those workstation via ssh, but my parents are stuck
behind home firewalls. I came up with a solution - reverse ssh tunelling. I
enabled ssh, generated keys and connected to my server:

    systemctl enable --now sshd
    ssh-keygen
    ssh xssh@xxx.zapletalovi.com

A new user service will be started to create the tunnel:

    mkdir -p ~/.config/systemd/user

I am forwarding both ports 22 and 5900:

    cat ~/.config/systemd/user/reverse-ssh.service
    [Unit]
    Description=Reverse SSH connection
    After=network.target
    [Service]
    Type=simple
    ExecStart=/usr/bin/ssh -g -N -T -o "ServerAliveInterval 10" -o "ExitOnForwardFailure yes" -R 40122:localhost:22 -R 40159:localhost:5900 xssh@xxx.zapletalovi.com
    Restart=always
    RestartSec=10m
    [Install]
    WantedBy=default.target

To enable the service:

    systemctl --user daemon-reload
    systemctl --user enable --now reverse-ssh

Unfortunately, I was not able to get VNC running. After I enabled Remote
Desktop in Gnome, I could not find any VNC client that would work. The best I
could achieve was a frozen screen when connected on my LAN. Maybe I will find
one later on, there are some developments in Fedora 35.

That should do it, ideal OS for elders - no reboots into dnf, no viruses, just
internet and a printer. Upgrading to major Fedora releases should be also easy
and I can do it via ssh:

    ostree remote refs fedora
    rpm-ostree rebase fedora:fedora/XX/x86_64/silverblue

To revert to the previus version, simply pick the previous boot entry and
perform `rpm-ostree rollback`. Which reminds me - Fedora 35 is out, I should
probably upgrade them now.
