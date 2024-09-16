---
title: "Unifi Controller in Fedora/CentOS/RHEL"
date: 2024-09-12T14:39:37+02:00
type: "post"
tags:
- linux
- fedora
---

This article contains instructions how to run Unifi Controller from Ubiquiti via podman from Fedora, CentOS, RHEL, clones or pretty much any Linux distribution as long as it is version 5.x or higher. I tested this on Fedora 40 running with SELinux in enforcing mode and rootless containers via quadlets.

First off, make sure there is no `unifi` application installed since the system-wide `unifi.service` could collide with a new service we are creating. Also, make sure to work as a regular user as this article expects systemd units to be created under user directory. If you want, for any reason, to run Unifi as root (which I do not recommend), put all files into `/usr/containers/systemd` instead and do not use `--user` option in all systemd commands.

We will create two containers and a pod. But before that, let's create a volume for MongoDB database:

    cat > ~/.config/containers/systemd/unifi-db.volume <<EOF
    [Volume]
    VolumeName=unifi-db
    EOF

And one for the Controller application configuration:

    cat > ~/.config/containers/systemd/unifi-app.volume <<EOF
    [Volume]
    VolumeName=unifi-app
    EOF

We need to create the volume for MongoDB in advance because it needs to be initialized first:

    podman volume create unifi-db

Start MongoDB 5.0 and keep in mind that this article was written for controller version 8.4 which required MongoDB 5.0. Different version might require different MongoDB version.

    podman run --rm -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=unifi -v unifi-db:/data/db:Z docker.io/mongo:5.0

Do not stop the container (you can also run it in the background), it will have very short life tho. We only need it to run the following command to create a user for the controller:

    podman run --rm -it --entrypoint=/usr/bin/mongosh docker.io/mongo:5.0 --authenticationDatabase admin --host unifi-db -u root -p unifi admin --eval "db.createUser({user: 'unifi', pwd: 'unifi', roles: [{role: 'dbOwner', db: 'unifi'},{role: 'dbOwner', db: 'unifi_stat'}]});"

Now the container must be stopped via `ctrl-c`, data is stored in the `unifi-db` volume. Let's create a container unit:

    cat > ~/.config/containers/systemd/unifi-db.container <<EOF
    [Container]
    ContainerName=unifi-db
    Environment=MONGO_INITDB_ROOT_USERNAME=root MONGO_INITDB_ROOT_PASSWORD=unifi
    Image=docker.io/mongo:5.0
    Pod=unifi.pod
    Volume=unifi-db.volume:/data/db:Z
    EOF

And let's create a similar container with the controller from an image maintained by LinuxServer.io since Ubiquiti does not provide any official images at this time:

    cat > ~/.config/containers/systemd/unifi-app.container <<EOF
    [Container]
    ContainerName=unifi-app
    Environment=PUID=1000 PGID=1000 TZ=Europe/Prague MONGO_USER=unifi MONGO_PASS=unifi MONGO_HOST=unifi-db MONGO_PORT=27017 MONGO_DBNAME=unifi MONGO_AUTHSOURCE=admin
    Image=lscr.io/linuxserver/unifi-network-application:latest
    Pod=unifi.pod
    Volume=unifi-app.volume:/config:Z
    [Unit]
    After=unifi-db.service
    EOF

Feel free to tune up environment variables, probably timezone is different and you can change passwords as well. MongoDB will not be exposed on the host interface so you can leave the password as is.

The final step is to create a pod, as you can see only few ports are expose. Reach out to Uniquity documentation for more ports, this is the minimum set of ports recommended:

    cat > ~/.config/containers/systemd/unifi.pod <<EOF
    [Pod]
    PodName=unifi
    PublishPort=8443:8443
    PublishPort=8080:8080
    PublishPort=3478:3478/udp
    PublishPort=10001:10001/udp
    [Install]
    WantedBy=multi-user.target default.target
    EOF

Validate podman generation, this is where it fails if you don't have podman version 5.x or higher:

    /usr/libexec/podman/quadlet -dryrun -user
    quadlet-generator[6737]: Loading source unit file /home/lzap/.config/containers/systemd/unifi-app.container
    quadlet-generator[6737]: Loading source unit file /home/lzap/.config/containers/systemd/unifi-app.volume
    quadlet-generator[6737]: Loading source unit file /home/lzap/.config/containers/systemd/unifi-db.container
    quadlet-generator[6737]: Loading source unit file /home/lzap/.config/containers/systemd/unifi-db.volume
    quadlet-generator[6737]: Loading source unit file /home/lzap/.config/containers/systemd/unifi.pod
    ---unifi-app-volume.service---
    [X-Volume]
    VolumeName=unifi-app
    [Unit]
    RequiresMountsFor=%t/containers
    [Service]
    ExecStart=/usr/bin/podman volume create --ignore unifi-app
    Type=oneshot
    RemainAfterExit=yes
    SyslogIdentifier=%N
    --- ... ---

This command may print some warnings you can ignore, but it must print all the services that will be used by systemd. It is now time to generate service files:

    systemctl --user daemon-reload

You need to run the `daemon-reload` command every time a change needs to be propagated. To check out the generated units:

    ls $XDG_RUNTIME_DIR/systemd/generator -1
    unifi-app.service
    unifi-app-volume.service
    unifi-db.service
    unifi-db-volume.service
    unifi-pod.service

Start the pod (it should be enabled by default on boot):

    systemctl --user start unifi-pod

Visit your host URL `https://podman-host:8443` and perform initial setup or restore from backup. Keep in mind that all the data are kept in your `$HOME/.local/share/containers/storage/volumes/` directory, this includes automatic backups done by the controller. I suggest to set up configuration-only backups regularly in the admin interface of the Unifi Controller UI. To find the exact location of your data:

    podman volume inspect unifi-app
    ...
    /home/lzap/.local/share/containers/storage/volumes/unifi-app/_data
    ...

On my system, I need to backup the following directory: `/home/lzap/.local/share/containers/storage/volumes/unifi-app/_data/data/backup/`. You can do the same for the MongoDB data stored in the volume named `unifi-db`, but I *think* that only statistics are stored there - nothing important for a home deployment. Tho, if you are running a public service, you may be legally obligated to store records of client data.

If this article helped, share it on your favourite social networks. Cheers!
