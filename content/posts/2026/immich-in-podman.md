---
title: "Running Immich in Podman"
date: 2026-04-03T19:50:00+01:00
type: "post"
tags:
- linux
- fedora
---

Immich has rapidly become the go-to solution for self-hosters looking to
replace Google Photos. It is a high-performance, self-hosted photo and video
backup application that boasts mobile apps, smooth timeline scrolling, and
robust machine-learning capabilities for facial recognition and object
detection. 

While the official documentation heavily leans on Docker Compose, deploying
Immich using **Podman Quadlets** is an excellent choice for a daemonless,
systemd-native setup. Quadlets allow you to define container workloads directly
via systemd unit files, making management, auto-updating, and logging
incredibly clean.

Here is a brief, straightforward guide to deploying the Immich stack using
Podman Quadlets. Note this is rootful setup, I prefer running my containers as
root, but I keep SELinux turned on.

We will be creating a pod and four distinct containers (database, machine
learning, Redis, and the main server). Since we are doing a system-wide
installation, all of these configuration files must be placed in
`/etc/containers/systemd/`. 

Create the following files with your preferred text editor:

**File:** `/etc/containers/systemd/immich.pod`

```ini
[Pod]
PodName=immich-stack
PublishPort=2283:2283
```

**File:** `/etc/containers/systemd/immich-db.container`

```ini
[Container]
ContainerName=immich-db
Pod=immich.pod
AutoUpdate=registry
Image=docker.io/tensorchord/pgvecto-rs:pg16-v0.2.0
Environment=POSTGRES_DB=immich POSTGRES_USER=immich POSTGRES_PASSWORD=immich_pass
Volume=immich-db:/var/lib/postgresql/data:Z
```

**File:** `/etc/containers/systemd/immich-ml.container`

```ini
[Container]
ContainerName=immich-ml
Pod=immich.pod
AutoUpdate=registry
Image=ghcr.io/immich-app/immich-machine-learning:release-openvino
Environment=TZ=Europe/Prague
Environment=MACHINE_LEARNING_CACHE_FOLDER=/cache
Environment=IMMICH_ML_DEVICE=openvino
AddDevice=/dev/dri/renderD128:/dev/dri/renderD128
Volume=immich-ml-cache:/cache:z
User=0:0
```

I host my immich on Intel NUC 13th gen with integrated Intel GPU, therefore
this configuration utilizes OpenVINO for hardware-accelerated machine learning
tasks. Ensure your hardware supports this and that `/dev/dri/renderD128` is the
correct path for your system's GPU.

**File:** `/etc/containers/systemd/immich-redis.container`

```ini
[Container]
ContainerName=immich-redis
Pod=immich.pod
Image=docker.io/library/redis:7-alpine
AutoUpdate=registry
Volume=immich-redis-data:/data:Z
```

**File:** `/etc/containers/systemd/immich-server.container`

```ini
[Unit]
Description=Immich Photo Manager
After=network-online.target immich-db.service immich-redis.service
Requires=immich-db.service immich-redis.service

[Container]
ContainerName=immich
Pod=immich.pod
AutoUpdate=registry
Image=ghcr.io/immich-app/immich-server:release
Environment=DB_HOSTNAME=immich-db DB_USERNAME=immich DB_PASSWORD=immich_pass DB_DATABASE_NAME=immich
Environment=REDIS_HOSTNAME=immich-redis
Environment=IMMICH_MACHINE_LEARNING_URL=http://immich-ml:3003
Environment=TZ=Europe/Prague
Environment=IMMICH_TRANSCODE_HW_ACCEL=vaapi
Volume=immich-server-data:/data:Z
Volume=/mnt/big/photos:/usr/src/app/upload:z
AddDevice=/dev/dri/renderD128:/dev/dri/renderD128
User=0:0
HealthCmd=curl -fs --connect-timeout 5 --max-time 10 -o /dev/null http://localhost:2283/favicon.ico
HealthInterval=10m
HealthRetries=3

[Install]
WantedBy=multi-user.target
```

Update the volume mount (`/mnt/big/photos`) to point to the actual directories
on your host where you want your photos stored.

Once your files are safely situated in `/etc/containers/systemd/`, you need to
tell systemd to generate the service files and load them. Podman's systemd
generator will automatically parse these `.container` and `.pod` files and
create standard `.service` units behind the scenes.

```bash
sudo systemctl daemon-reload
```

Quadlet units do not need to be enabled, just start it.

```bash
sudo systemctl start immich-pod
```

You can check the status of your newly created stack by inspecting the systemd service or viewing the Podman logs:

```bash
sudo systemctl status immich-server.service
sudo podman logs -f immich
```

Once the containers are running and the database has initialized, you can
access your Immich instance by navigating to `http://<your-server-ip>:2283` in
your web browser. Cheers!
