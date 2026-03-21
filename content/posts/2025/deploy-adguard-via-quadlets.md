---
title: "Deploy AdGuard Home via Podman Quadlets"
date: 2025-09-24T11:02:47+02:00
type: "post"
tags:
- linux
- fedora
---

_Update 2026: Few changes, added host network mode which is more simple and less
confusing._

Let's install AdGuard Home via Podman Quadlets. Volumes:

    sudo podman volume create adguard-work
    sudo podman volume create adguard-conf

Everything must be done as root since AdGuard needs to bind UDP port. Volume
units:

```
cat <<EOF | sudo tee /etc/containers/systemd/adguard-work.volume > /dev/null
[Volume]
VolumeName=adguard-work
EOF
```

```
cat <<EOF | sudo tee /etc/containers/systemd/adguard-conf.volume > /dev/null
[Volume]
VolumeName=adguard-conf
EOF
```

Now the container unit:

```
cat <<EOF | sudo tee /etc/containers/systemd/adguard.container > /dev/null
[Container]
ContainerName=adguard
Image=docker.io/adguard/adguardhome:latest
Pod=adguard.pod
Volume=adguard-work.volume:/opt/adguardhome/work:Z
Volume=adguard-conf.volume:/opt/adguardhome/conf:Z
EOF
```

The pod unit. Note I use "host" network, so it is important to pay attention
for the initial configuration.

```
cat <<EOF | sudo tee /etc/containers/systemd/adguard.pod > /dev/null
[Pod]
PodName=adguard
Network=host
[Install]
WantedBy=multi-user.target default.target
EOF
```

Try if it generates fine:

    sudo /usr/libexec/podman/quadlet -dryrun

Reload units:

    sudo systemctl daemon-reload

And enable and start:

    sudo systemctl enable --now adguard-pod

Visit `https://adguard.example.com:3000` to configure it. Attention! Since
AdGuard is running in host network mode, make sure to only select relevant
interfaces during its initial setup via Web UI, do not allow listening an all
that will get you into troubles.

If you did not pay attention during initial setup, you can always edit the
configuration manually. In the `bind_hosts` section, replace `0.0.0.0` with
your public IP and `localhost` as well.

```
cat /var/lib/containers/storage/volumes/adguard-conf/_data/AdGuardHome.yaml
...
dns:
  bind_hosts:
    - 192.168.1.2
    - 127.0.0.1
  port: 53
```

If you are running systemd-resolved, you will end up with many errors in
regards to PTR records:

```
dnsproxy: exchange failed upstream=127.0.0.53:53 question=";42.1.168.192.in-addr.arpa.\tIN\t PTR" duration=2.001938493s err="exchanging with 127.0.0.53:53 over udp: read udp 127.0.0.1:53633->127.0.0.53:53: i/o timeout"
```

This is because by default, AdGuard sends PTR, SOA, NS requests to the system
resolver, which is resolved (running on 127.0.0.53) which is unable to complete
those requests. In AdGuard DNS settings, use Private DNS server and set it to
the upstream DNS. You may want to disable rDNS, or even completely turn off PTR
requests for private addresses.

Okay, this is all. A very nice DNS caching server with a great UI, statistics,
filtering abilities. A great piece of software, remember to make a donation to
AdGuard or purchase some of their subscriptions if you want to support them.
