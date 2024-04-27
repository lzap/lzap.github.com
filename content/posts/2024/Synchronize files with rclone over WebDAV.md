---
title: "Synchronize files with rclone over WebDAV"
date: 2024-04-27T22:07:09+02:00
type: "post"
tags:
- linux
- fedora
---

We have a mix of devices at home ranging from Linux workstations, servers,
Macbooks, a Mac Mini and a Windows PC. Up until now, I was using Samba for a
home "share" folder which was also used to do backups of the Windows PC (family
photos and videos). But it was always a pain, smb protocol is somehow slow,
unreliable and painful to set up for seamless MacOS integration. In fact, it
never worked reliably for me.

I tried `rsync` from Windows to Linux file backups but it was quite slow - the
`rsync` server is running Fedora on somehow weak i3 CPU on 8th gen Intel NUC
and it looks like `rsync` cannot be configured without SSH for uploads. Problem
was that SSH encryption was holding the transfer speed back and there is no way
to set a SSH server without encryption. I tried to experiment with some ciphers
and found few which are a bit faster but just by few per-cents.

I discovered `rclone` command today, a client for manipulating and
synchronization of files on various clouds (AWS S3 and similar) including the
good old plain WebDAV protocol. Since I was running Apache2 httpd server with
`mod_dav` for access to my "share" folder from MacOS devices (works much better
than samba), it was pretty easy to reconfigure it for use with `rclone`. The
only missing configuration option was `LimitRequestBody` because some larger
video files could not be uploaded. I also enabled LAN-only access over HTTP
instead of HTTPS for even better performance:

```
<IfModule mod_dav_fs.c>
    DAVLockDB /var/lib/httpd/webdavlock.db
</IfModule>

<VirtualHost *:443>
  ServerName share.zapletalovi.com

  Alias /folder /mnt/big/folder
  <Location /folder>
      DAV On
      SSLRequireSSL
      Options Indexes
      Require valid-user
      AuthType Basic
      AuthName share
      AuthUserFile /etc/httpd/conf.d/webdav-folder.htpasswd
  </Location>
</VirtualHost>

<VirtualHost *:80>
  ServerName server.home.lan

  Alias /folder /mnt/big/folder
  <Location /folder>
      Order Deny,Allow
      Deny from all
      Allow from 192.168.42.0/24
      DAV On
      Options Indexes
      Require valid-user
      AuthType Basic
      AuthName share
      AuthUserFile /etc/httpd/conf.d/webdav-folder.htpasswd
      LimitRequestBody 99999999999
  </Location>
</VirtualHost>
```

Configuring users and password is easy enough with Apache2 httpd tools:

```
htpasswd -c webdav-share.htpasswd user1
htpasswd webdav-share.htpasswd user2
```

Synchronizing 500 GB of photos and videos takes less than a minute (assuming
all files are already synchronized):

```
rclone sync --progress c:\users\user\photo server:backups\windowspc\photo
rclone sync --progress --transfers=1 c:\users\user\video server:backups\windowspc\video
```

Compared to about 10 minutes for `robocopy` over `smb` or even slower `rsync`,
this is awesome. I have not tried HTTPS as that protocol is only enabled for
external access outside of home LAN, I assume that would be a bit slower.

Warning: `rclone` compares file size and last modification time stamp, it does
*not* calculate shasum of file contents like rsync does. For my use case, this
is sufficient.

By default, `rclone` uses four threads to do directory walking and file
comparisons which is super fast and you can even increase this via `transfers`
argument if you use SSDs. In my case, I actually did the opposite as both the
client and the server store the data on slow HDD and big video files were
hammering disk heads which had to seek constantly.

It looks like I will keep using WebDAV as my main file sharing protocol at
home. I wish Apple adds it into iOS, currently I must copy files using
third-party application. But from any other system including Linux, Windows and
MacOS it works just fine without any third-party software. And now it also made
my backups super-fast which is great.
