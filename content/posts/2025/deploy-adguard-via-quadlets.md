---
title: "Deploy AdGuard Home via Podman Quadlets"
date: 2025-09-24T11:02:47+02:00
type: "post"
tags:
- linux
- fedora
---

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

The pod unit. Maybe comment out DHCP if you do not intend to use it:

```
cat <<EOF | sudo tee /etc/containers/systemd/adguard.pod > /dev/null
[Pod]
PodName=adguard
# Admin interface
PublishPort=3000:3000/tcp
# DNS
PublishPort=53:53/udp
PublishPort=53:53/tcp
# DHCP
PublishPort=67:67/udp
PublishPort=68:68/udp
# DNS-over-HTTP
PublishPort=80:80/tcp
# DNS-over-HTTPS
PublishPort=443:443/tcp
PublishPort=443:443/udp
# DNS-over-TLS
PublishPort=853:853/tcp
# DNS-over-QUIC
PublishPort=784:784/udp
PublishPort=853:853/udp
PublishPort=8853:8853/udp
# DNSCrypt
PublishPort=5443:5443/tcp
PublishPort=5443:5443/udp
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

You may run into existing services bound to the DNS port, typically this is
`resolved` which can be disabled with:

```
$ cat /etc/systemd/resolved.conf.d/listenall.conf
[Resolve]
DNS=127.0.0.1
DNSStubListener=no
```

If you are running `libvirtd` the `dnsmasq` could be problem, although it is
only listening on `virbrX` interfaces it will cause the adblock to fail to
launch. In that case, prefix the address you want to use to all the ports:

```
PublishPort=192.168.X.X:3000:3000/tcp
```

Visit `https://adguard.example.com:3000` to configure it.
