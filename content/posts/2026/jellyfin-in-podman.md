---
title: "Running Jellyfin in Podman"
date: 2026-04-03T19:55:00+01:00
type: "post"
tags:
- linux
- fedora
---

This guide covers deploying a streamlined, self-hosted audio and video
archiving setup using Podman Quadlets. The stack integrates UN/BT tools and a
web-based file management. All services are running rootful with SELinux in
enforcing mode.

Some containers are configured with host network for maximum performance of the
network stack, this only works in rootful mode.

By leveraging Quadlets, we can define our containers directly as native systemd
units, allowing for easy daemonless management and auto-updating without
relying on Docker Compose.

Since this is a system-wide deployment, create the following `.container` files in the `/etc/containers/systemd/` directory.

**File:** `/etc/containers/systemd/jellyfin.container`

```ini
[Unit]
Description=Jellyfin Media Server
After=network-online.target

[Container]
Image=docker.io/jellyfin/jellyfin:latest
ContainerName=jellyfin
AutoUpdate=registry
Network=host
User=0:0
GroupAdd=keep-groups
AddDevice=/dev/dri/renderD128:/dev/dri/renderD128

Volume=jellyfin-config:/config:Z
Volume=jellyfin-cache:/cache:Z
Volume=/mnt/big/media:/media:z

#Mount=type=tmpfs,destination=/transcodes,tmpfs-size=20G,tmpfs-mode=1777

[Install]
WantedBy=multi-user.target default.target
```

The commented `/transcodes` mount is only relevant, if your host has a lot of
memory like mine and you want to decrease SSD wear for transcoding. The path
must be set in the WebUI if you choose to use it.

**File:** `/etc/containers/systemd/nzbget.container`

```ini
[Unit]
Description=NZBGet-ng Downloader
After=network-online.target

[Container]
Image=ghcr.io/nzbgetcom/nzbget:latest
ContainerName=nzbget
AutoUpdate=registry
Network=host
User=0:0
Environment=PUID=0
Environment=PGID=0
GroupAdd=keep-groups
Environment=TZ=Europe/Prague
HealthCmd=none
Volume=nzbget-config:/config:Z
Volume=/mnt/big/media:/media:z

[Install]
WantedBy=multi-user.target default.target
```

**File:** `/etc/containers/systemd/transmission.container`

```ini
[Unit]
Description=Transmission
After=network-online.target

[Container]
ContainerName=transmission
Image=lscr.io/linuxserver/transmission:latest
User=0:0
Network=host
AutoUpdate=registry
Environment=PUID=0 PGID=0 TZ=Europe/Prague USER=lzap PASS=xxxxxx
Volume=transmission-config:/config:Z
Volume=/mnt/big/media:/media:z
Environment=TRANSMISSION_DOWNLOAD_DIR=/media/other
Environment=TRANSMISSION_INCOMPLETE_DIR_ENABLED=true
Environment=TRANSMISSION_INCOMPLETE_DIR=/media/intermediate

HealthCmd=curl -f -s -u lzap:xxxxxx http://localhost:9091/transmission/web/
HealthStartPeriod=30m
HealthInterval=2h
HealthOnFailure=restart

[Service]
Restart=on-failure
MemoryMax=1G

[Install]
WantedBy=multi-user.target default.target
```

**File:** `/etc/containers/systemd/filebrowser.container`

```ini
[Unit]
Description=FileBrowser
After=network-online.target

[Container]
Image=docker.io/filebrowser/filebrowser:latest
ContainerName=filebrowser
AutoUpdate=registry
PublishPort=8081:80
User=0:0
HealthCmd=none
Volume=filebrowser-db:/database:Z
Volume=filebrowser-cfg:/config:Z
Volume=/mnt/big/media:/srv:z

[Install]
WantedBy=multi-user.target default.target
```

With your configurations in place, tell systemd to regenerate the service
units. Because the `WantedBy` directives are already defined in the Quadlets,
we don't need to manually enable them; starting them is sufficient.

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl start jellyfin nzbget transmission filebrowser
```

You can check the operational status of your new stack via systemctl or by
checking the container logs directly.

```bash
sudo systemctl status jellyfin nzbget transmission filebrowser
```

Your archiving and streaming pipeline is now active. You can access Jellyfin on
port `8096`, FileBrowser on port `8081`, Transmission on port `9091`, and
NZBGet on port `6789` (assuming default host networking configurations).

Perhaps you want to expose Jellyfin to the internet, for that I use Apache
httpd. To get Let's Encrypt certificate, follow `acme-tiny` tutorial from this
blog. Here is a full example for Jellyfin and Transmission/NZBGet, the latter
is only accessible from the local network. Although I could access all services
directly, using HTTPS with correct certificate is easier and browser then will
not complain. It is also needed in order for BT/Magnet link association to work
properly.

```
<VirtualHost *:443>
        Protocols h2 http/1.1
        ServerName xxxx.zapletalovi.com

        SSLEngine On
        SSLCertificateFile /var/lib/acme/certs/xxxx.zapletalovi.com.crt
        SSLCertificateKeyFile /etc/pki/tls/private/xxxx.zapletalovi.com.key

        ProxyPreserveHost On
        RequestHeader set X-Forwarded-Proto "https"
        RequestHeader set X-Forwarded-Port "443"

        # JellyFin
        Redirect permanent "/jellyfin" "/jellyfin/"
        ProxyPass "/jellyfin/socket" "ws://127.0.0.1:8096/jellyfin/socket"
        ProxyPassReverse "/jellyfin/socket" "ws://127.0.0.1:8096/jellyfin/socket"
        ProxyPass "/jellyfin" "http://127.0.0.1:8096/jellyfin"
        ProxyPassReverse "/jellyfin" "http://127.0.0.1:8096/jellyfin"

        # Transmission
        Redirect /transmission /transmission/web/
        <Location /transmission>
                Require ip 192.168.0.0/16

                ProxyPass http://127.0.0.1:9091/transmission
                ProxyPassReverse http://127.0.0.1:9091/transmission
        </Location>

        # NZBGet
        RedirectMatch ^/nzbget$ /nzbget/
        <Location /nzbget>
                Require ip 192.168.0.0/16

                ProxyPass http://127.0.0.1:6789
                ProxyPassReverse http://127.0.0.1:6789
        </Location>
</VirtualHost>
```

Allright, that is all.
