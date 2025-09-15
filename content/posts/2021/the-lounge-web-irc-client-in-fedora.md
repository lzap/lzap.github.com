---
type: "post"
aliases:
- /2021/03/the-lounge-web-irc-client-in-fedora.html
date: "2021-03-31T00:00:00Z"
tags:
- linux
- fedora
title: The Lounge web IRC client in Fedora
---

My graphics card died and thanks to COVID and Bitcoin, it will be a long wait
until it's back. I am on Mac M1 at the moment and it looks like there are not
many good IRC clients on MacOS.

Let's run a simple web-based IRC client which can also work as a bouncer (no
need of ZNC). I randomly selected one which is called The Lounge, looks nice
and works okay for me. This one is written in NodeJS and since there is no
package in Fedora, I've decided to build it via yarn. It needs only one native
dependency I think - sqlite3 so do not expect any problems on that front:

    # dnf install nodejs yarn sqlite-devel
    # dnf groupinstall "Development Tools"
    # mkdir ~/.thelounge
    # cd ~/.thelounge
    # yarn add thelounge

If you prefer installing it into `/usr/local` then run `yarn global add
thelounge`.

Create a user service, I will be running it as a regular user:

    # cat /home/lzap/.config/systemd/user/thelounge.service
    [Unit]
    Description=The Lounge IRC client
    After=network-online.target
    [Service]
    ExecStart=/home/lzap/.thelounge/node_modules/.bin/thelounge start
    [Install]
    WantedBy=multi-user.target

Start it to create a default configuration file:

    # systemctl --user daemon-reload
    # systemctl --user enable --now thelounge

Optionally, stop the service for now and review the configuration. There are
couple of things I recommend to tune. By default the service listens on HTTP
(9090), no HTTPS is configured, it stores all logs in both sqlite3 and text
files and it is configured as "private" instance, meaning you need to login
with a username and password:

    # vim ~/.thelounge/config.js

Create new user:

    # ~/.thelounge/node_modules/.bin/thelounge add lzap

Visit http://localhost:9090 or https://localhost:9090 if you've configured SSL.
There you can create one or more IRC connections, join all channels, everything
will be written into a separate `~/.thelounge/users/user.js` configuration file
which is nice. If you disabled sqlite3 logging, everything is stored in text
files which I appreciate a lot.

If you want a simple letsencrypt tutorial for Fedora, read my prevous blog
post:

    # grep "https: {" -A5  ~/.thelounge/config.js
      https: {
        enable: true,
        key: "/etc/pki/tls/private/home.zapletalovi.com.key",
        certificate: "/var/lib/acme/certs/home.zapletalovi.com.crt",
        ca: "",
      },

No intermediate CAs are needed for letsencrypt so you can leave the field
blank. Have fun.

