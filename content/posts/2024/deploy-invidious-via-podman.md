---
title: "Deploy Invidious via Podman"
date: 2024-09-28T21:00:06+02:00
type: "post"
tags:
- linux
- fedora
---

Here is how you deploy [Invidious](https://invidious.io/) via Podman 5.x or
higher. All commands are executed as a normal user, if you want to use root
then you need to modify some paths. Root-less containers are preferred together
with SELinux in enforcing mode for maximum security.

Create a new volume for database:

    podman volume create invidious-db

Start a temporary container:

    podman run --rm -it --name invidious-init -v invidious-db:/var/lib/postgresql/data:Z -p 5432:5432 -e POSTGRES_DB=invidious -e POSTGRES_USER=kemal -e POSTGRES_PASSWORD=kemal docker.io/library/postgres:14

In another terminal, migrate the database:

    export PGPASSWORD=kemal
    for F in channels videos channel_videos users session_ids nonces annotations playlists playlist_videos; do
        curl -s https://raw.githubusercontent.com/iv-org/invidious/refs/heads/master/config/sql/$F.sql | \
            psql -h localhost -p 5432 -U kemal invidious
    done

Shutdown the temporary container, it is no longer needed. Create database volume unit:

    cat > ~/.config/containers/systemd/invidious-db.volume <<EOF
    [Volume]
    VolumeName=invidious-db
    EOF

And a database container:

    cat > ~/.config/containers/systemd/invidious-db.container <<EOF
    [Container]
    ContainerName=invidious-db
    Environment=POSTGRES_DB=invidious POSTGRES_USER=kemal POSTGRES_PASSWORD=kemal
    Image=docker.io/library/postgres:14
    HealthCmd=pg_isready -h localhost -p 5432 -U kemal -d invidious
    Notify=healthy
    Pod=invidious.pod
    Volume=invidious-db.volume:/var/lib/postgresql/data:Z
    EOF

Create a helper container:

    cat > ~/.config/containers/systemd/invidious-sig-helper.container <<EOF
    [Container]
    ContainerName=invidious-sig-helper
    Environment=RUST_LOG=info
    Image=quay.io/invidious/inv-sig-helper:latest
    Exec=--tcp 0.0.0.0:12999
    Pod=invidious.pod
    EOF

Now, generate your `VISITOR_DATA` an `PO_TOKEN` secrets, run this command and wait until it prints both values:

    podman run quay.io/invidious/youtube-trusted-session-generator

Set those secrets as temporary environmental variables, also generate a random string for HMAC secret:

    HMAC=$(openssl rand -base64 21)
    VISITOR_DATA="ABCDEF%3D%3D" # notsecret
    PO_TOKEN="MpOIfiljfsdljds-Lljfsdk-ojrdjXVs==" # notsecret

In the same terminal where you defined the environmental variables, create new environmental config file:

```
cat > ~/.config/containers/systemd/invidious.env <<EOF
INVIDIOUS_DATABASE_URL="postgres://kemal:kemal@invidious-db:5432/invidious"
#INVIDIOUS_CHECK_TABLES=true
#INVIDIOUS_DOMAIN="inv.example.com"
INVIDIOUS_SIGNATURE_SERVER="invidious-sig-helper:12999"
INVIDIOUS_VISITOR_DATA="$VISITOR_DATA"
INVIDIOUS_PO_TOKEN="$PO_TOKEN"
INVIDIOUS_HMAC_KEY="$HMAC"
EOF
```

And create an invidious container unit:

    cat > ~/.config/containers/systemd/invidious.container <<EOF
    [Container]
    ContainerName=invidious
    EnvironmentFile=%h/.config/containers/systemd/invidious.env
    Image=quay.io/invidious/invidious:latest
    Pod=invidious.pod
    [Unit]
    After=invidious-db.service
    EOF

And finally, create a pod unit. Note only port 3000 is exposed, do not expose other ports!

    cat > ~/.config/containers/systemd/invidious.pod <<EOF
    [Pod]
    PodName=invidious
    PublishPort=3000:3000
    [Install]
    WantedBy=multi-user.target default.target
    EOF

Systemd units are generated on-the-fly during `daemon-reload` command, but
before that let's check syntax with quadlet generator. Note, you need Podman
version 5.0 or higher, older versions will not work:

    /usr/libexec/podman/quadlet -dryrun -user

Reload systemd daemon. Keep in mind you need to do this command every time you
change any unit file, you can change the environmental file without reload tho.

    systemctl --user daemon-reload

And the whole application can be now started:

    systemctl --user start invidious-pod

Keep in mind that generated units cannot be enabled using `systemctl enable`,
the main pod will be enabled automatically. If you do not like this behavior,
remove the `WantedBy` line from `invidious.pod`.

Head over to your instance at `http://inv.example.com:3000` and have fun!
