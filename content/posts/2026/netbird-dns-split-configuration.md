---
title: "Netbird DNS Split Configuration"
date: 2026-04-08T08:16:58+02:00
type: "post"
tags:
- linux
- fedora
- macos
---

Many companies provide NetBird VPN access configured with a mandatory DNS
resolving service to ensure malware protection. While this is a solid IT
recommendation for the general workforce, it can be frustrating if you run your
own DNS blocker at home (like Pi-hole or AdGuard Home) and want to keep your
personal traffic routing through it for better performance or hostname
rewrites.

If your company’s NetBird configuration forces all DNS queries through their
resolvers, you can bypass this and configure split DNS manually. Here is how to
do it on both MacOS and Linux.

## Prerequisite: Disable NetBird DNS Management

Before applying any custom routing, you need to tell the NetBird client to stop
managing your DNS. Depending on how you run NetBird, you can disable this in
the desktop client's settings or by starting the daemon with the DNS feature
disabled.

This can be done from the command line too:

```bash
netbird up --disable-dns
```

Once NetBird is connected but no longer hijacking your system DNS, proceed to
the OS-specific steps below.

## MacOS Configuration

MacOS handles split DNS through the `/etc/resolver/` directory. By creating a
file named after the domain you want to route, you can tell MacOS exactly which
nameserver to use for that specific domain.

Open your terminal and run the following commands:

```bash
sudo mkdir -p /etc/resolver

echo "nameserver 100.100.100.100" | sudo tee /etc/resolver/example.com
echo "nameserver 100.100.100.100" | sudo tee /etc/resolver/example.corp

echo "nameserver 8.8.8.8" | sudo tee /etc/resolver/wgvpn.example.com
```

MacOS will automatically detect these files and start routing queries for
`*.example.com` and `*.example.corp` to `100.100.100.100`, while continuing to
use your local home DNS for everything else.

## Linux Configuration

On Linux systems using `systemd-resolved`, you can achieve the exact same
behavior using `resolvectl`.

First, identify your NetBird network interface. It is usually named `wt0`
(Wiretrustee) or `netbird0`. You will also need the name of your primary
internet interface (e.g., `eth0`, `wlan0`, `enp3s0`). You can find both by
running `ip a`.

Once you have your interface names, use `resolvectl` to assign the DNS servers
and routing domains. The tilde (`~`) before the domain name tells
`systemd-resolved` to use that interface *exclusively* for that domain.

```bash
sudo resolvectl dns wt0 100.100.100.100
sudo resolvectl domain wt0 ~example.com ~example.corp

sudo resolvectl domain eth0 ~wgvpn.example.com
```

Keep in mind that `resolvectl` commands apply changes at runtime. If you reboot
or restart the interface, you will need to reapply them. To make this
persistent, you can add these settings directly into your NetworkManager
configuration or create a drop-in systemd network file, but keeping them as a
quick bash script to run after connecting to the VPN is often the easiest
approach for custom workstation setups.

Example unit file that executes after `wt0` is brought up, this must be
customized to your device names:

```
[Unit]
Description=NetBird Split DNS Configuration
BindsTo=sys-subsystem-net-devices-wt0.device
After=sys-subsystem-net-devices-wt0.device

[Service]
Type=oneshot
RemainAfterExit=yes

ExecStart=/usr/bin/resolvectl dns wt0 100.100.100.100
ExecStart=/usr/bin/resolvectl domain wt0 ~example.com ~example.corp

ExecStart=/usr/bin/resolvectl domain eth0 ~wgvpn.example.com

[Install]
WantedBy=sys-subsystem-net-devices-wt0.device
```

Now you can enjoy your local malware/ad-blocking while still resolving internal
company services securely.
