---
title: "Unifi Controller in Fedora/CentOS/RHEL"
date: 2024-09-12T14:39:37+02:00
type: "post"
tags:
- linux
- fedora
- podman
- unifi
---

_Update: Updated in 2026 with newer MongoDB version._

This article contains instructions how to run Unifi Controller from Ubiquiti
via podman from Fedora, CentOS, RHEL, clones or pretty much any Linux
distribution as long as it is version 5.x or higher. I tested this on Fedora
versions 40-43 running with SELinux in enforcing mode and rootless containers
via quadlets.

The article assumes this is a rootful deployment, but I also tested this on
rootless containers. I tend to use rootful containers on my home-lab Fedora
servers with SELinux turned on. If you intend to install as a regular user,
make sure to use correct paths for systemd units.

We will create two containers and a pod. But before that, let's create a volume
for MongoDB database:

```
cat <<EOF | sudo tee /etc/containers/systemd/unifi-db.volume > /dev/null
[Volume]
VolumeName=unifi-db
EOF
```

And one for the Controller application configuration:

```
cat <<EOF | sudo tee /etc/containers/systemd/unifi-app.volume > /dev/null
[Volume]
VolumeName=unifi-app
EOF
```

We need to create the volume for MongoDB in advance because it needs to be
initialized first:

    podman volume create unifi-db

Start MongoDB 7.0 and keep in mind that this article was written for controller
version 9.x which requires MongoDB 7.0. Different version might require
different MongoDB version.

    podman run --rm -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=unifi -v unifi-db:/data/db:Z --name unifi-db docker.io/mongo:7.0

Do not stop the container (you can also run it in the background), it will have
very short life tho. We only need it to run the following command to create a
user for the controller:

```
podman exec -it unifi-db mongosh -u root -p unifi --authenticationDatabase admin \
  --eval "db.getSiblingDB('admin').createUser({
    user: 'unifi',
    pwd: 'unifi',
    roles: [
      { role: 'dbOwner', db: 'unifi' },
      { role: 'dbOwner', db: 'unifi_stat' },
      { role: 'dbOwner', db: 'unifi_audit' }
    ]
  });"
```

Now the container must be stopped via `ctrl-c`, data is stored in the
`unifi-db` volume. Let's create a container unit:

```
cat <<EOF | sudo tee /etc/containers/systemd/unifi-db.container > /dev/null
[Container]
ContainerName=unifi-db
Environment=MONGO_INITDB_ROOT_USERNAME=root MONGO_INITDB_ROOT_PASSWORD=unifi
Image=docker.io/mongo:7.0
Pod=unifi.pod
Volume=unifi-db.volume:/data/db:Z
[Service]
MemoryMax=1G
Restart=on-failure
StartLimitBurst=3
[Unit]
StartLimitIntervalSec=5m
EOF
```

And let's create a similar container with the controller from an image
maintained by LinuxServer.io since Ubiquiti does not provide any official
images at this time:

```
cat <<EOF | sudo tee /etc/containers/systemd/unifi-app.container > /dev/null
[Container]
ContainerName=unifi-app
Environment=PUID=1000 PGID=1000 TZ=Europe/Prague MONGO_USER=unifi MONGO_PASS=unifi MONGO_HOST=unifi-db MONGO_PORT=27017 MONGO_DBNAME=unifi MONGO_AUTHSOURCE=admin
Image=lscr.io/linuxserver/unifi-network-application:latest
Pod=unifi.pod
Volume=unifi-app.volume:/config:Z
Environment=JVM_MAX_HEAP_SIZE=1500M
[Service]
MemoryMax=2G
Restart=on-failure
StartLimitBurst=3
[Unit]
After=unifi-db.service
StartLimitIntervalSec=5m
EOF
```

Feel free to tune up environment variables, probably timezone is different and
you can change passwords as well. MongoDB will not be exposed on the host
interface so you can leave the password as is.

The final step is to create a pod, as you can see only few ports are expose.
Reach out to Uniquity documentation for more ports, this is the minimum set of
ports recommended:

```
cat <<EOF | sudo tee /etc/containers/systemd/unifi.pod > /dev/null
[Pod]
PodName=unifi
PublishPort=8080:8080
PublishPort=8443:8443
PublishPort=3478:3478/udp
PublishPort=10001:10001/udp
[Install]
WantedBy=multi-user.target default.target
EOF
```

Validate podman generation:

```
/usr/libexec/podman/quadlet -dryrun
```

This command may print some warnings you can ignore, but it must print all the
services that will be used by systemd. It is now time to generate service
files:

    systemctl daemon-reload

Start the pod (it should be enabled by default on boot):

    systemctl --user start unifi-pod

Visit your host URL `https://podman-host:8443` and perform initial setup or
restore from backup. Keep in mind that all the data are kept in podman volumes,
this includes automatic backups done by the controller. I suggest to set up
configuration-only backups regularly in the admin interface of the Unifi
Controller UI. To find the exact location of your data:

    podman volume inspect unifi-app

Important: In Device Updates and Settings (on the Devices List, older version
has this in Settings - Advanced) make sure to set Inform Host Override to the
IP address or hostname of the container host. If you don't do this, adoption of
devices will fail because they will be informed with internal container IP
addresses which are not reachable.

If this article helped, share it on your favourite social networks. Cheers!
