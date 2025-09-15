---
type: "post"
aliases:
- /2020/01/deploy-photoprism-in-centos-80.html
date: "2020-01-12T00:00:00Z"
tags:
- linux
- fedora
title: Deploy PhotoPrism in CentOS 8
---

[PhotoPrism](https://photoprism.org/) is a great web photo library and great
fit for browsing and managing photos on a home NAS server I've recently built.
It has some unique features like tagging photo using TensorFlow, however the
most appealing features for me are slick interface, easy use and
administration, support for RAW/HEIC formats (conversion to JPEG), ability to
configure "read only" mode (my originals are never touched) and "photo stream"
approach (all photos in one huge pile with search/tagging capabilities).

This is a tutorial how to deploy this app on CenOS 8 in a root-less container
with SELinux. Before starting, it's important to plan permissions and SELinux
file labels. On my NAS system, I have a user and group called "data" with
UID/GID 1000 which is the initial regular user on CentOS (and most
distributions) after installation. I keep all my photos and files under this
user and group (Samba, NFS).

    # ls -laZ /mnt/int/data/photo/ -d
    drwxrwxr-x. 4 data data system_u:object_r:public_content_rw_t:s0 70 Jan 12 21:20 /mnt/int/data/photo/

Note the SELinux file label is set to public_content_rw_t because I want my
services (Samba, NFS, PhotoPrism) to be able to read and write data. If you
don't want PhotoPrism to write into original folder, use public_content_r_t
label. Here is how to set SELinux on a directory and all its subdirectories and
folders permanently:

    # semanage fcontext -a -t public_content_rw_t "/mnt/int(/.*)?"
    # restorecon -RvvF /mnt/int

For Samba and NFS configuration, see more details in my [previous
article](/2020/01/samba-and-nfs-shared-folder-on-centos8.html). Do not turn off
SELinux, get it right this time! Install podman first and SELinux development
files:

    # dnf install podman policycoreutils-devel

Compile a custom policy rule to read and write files and directories labelled
as public_content_rw_t:

    # mkdir selinux
    # cd selinux
    # cat >photoprism.te <<EOF
    policy_module(photoprism, 1.0)
    require {
            type container_t;
    }
    miscfiles_manage_public_files(container_t)
    userdom_manage_tmp_dirs(container_t)
    userdom_manage_tmp_files(container_t)
    EOF
    # make -f /usr/share/selinux/devel/Makefile && semodule -i photoprism.pp

No other actions need to be done, the module is now loaded permanently, there
is no service to restart as SELinux applies the new rules immediately. It will
also survive restarts. It's easy, isn't it?

Before we start, small recap. The photos I want to browse via PhotoPrism are
stored on 8th gen Intel NUC on the internal 2TB drive in directory
`/mnt/int/photos/phone` and I have a separate LVM volume on NVMe SSD for
thumbnails mounted as `/mnt/fast` where I want to store PhotoPrism thumbnails
and database. Run this command as the user that has UNIX permissions to read
(or write) photos directory and with read/write permissions to thumbnails and
database directories:

    $ podman run -d --name photoprism \
      --userns=keep-id -p 2342:2342 \
      -v /mnt/int/photo_ovl/merged/telefon:/home/photoprism/Pictures/Originals \
      -v /mnt/fast/thumbs:/home/photoprism/.cache/photoprism \
      -v /mnt/fast/photoprismdb:/home/photoprism/.local/share/photoprism/resources/database \
      photoprism/photoprism

When starting for the first time, you can omit the `-d` option to start the
container in the foreground to see log messages. To stop the container:

    $ podman stop photoprism

To start it again (use `-a` to attach to the photoprism process to see logs):

    $ podman start photoprism

Note in the run command above, I used `--userns=keep-id` argument which tells
podman to keep UID/GID. Remember when I told you my "data" user has UID/GID
1000? PhotoPrism application also runs as 1000, therefore it nicely maps to the
host OS. This is the most simple option, alternatively this argument can be
removed and podman will automatically map UID/GID according OS mapping tables.
In my case, the container process would have UID 100999. In that case, modify
UNIX permissions or/and ACLs in a way that this user (or group) can read
(and/or write) to the directories.

Alternatively, a mapping can be provided. Let's say 

    $ podman run -d ...
      --uidmap 0:100000:5000

The `--uidmap` optiom tells podman to map a range of 5000 UIDs inside the
container, starting with UID 100000 outside the container (so the range is
100000-104999) to a range starting at UID 0 inside the container (so the range
is 0-4999). This can be tricky to understand, that's why I opted-in for
`keep-id` approach.

For experimenting with UIDs and GIDs, you don't need to use PhotoPrism
container, just grab a temporary shell within Fedora, then create a user "test"
and try to access required files. Remeber SELinux is turned on, if you see
permission errors and you think you have your UNIX/ACL permissions right, check
audit.log. Note the container will be automatically removed on exit:

    $ podman run --rm -it -v /mnt/fast:/mnt fedora:31 /bin/bash
    > useradd test
    > su test
    > touch /mnt/TEST
    > exit

One trick before you proceed, if you don't want PhotoPrism to convert HEIC/RAW
files into the originals folder increasing the overall size of the originals,
use overlay fs:

    # mount -t overlay overlay -o lowerdir=/mnt/int/data/photo,upperdir=/mnt/int/photo_ovl/upper,workdir=/mnt/int/photo_ovl/work /mnt/int/photo_ovl/merged

This command creates an overlay folder `/mnt/int/photo_ovl/merged` with source
`/mnt/int/data/photo`. The other two named `work` and `upper` must be just
empty directories. Then use the `/mnt/int/photo_ovl/merged` foder for the `-v`
podman option to use it instead of the original directory. All files created by
PhotoPrism will not be stored in the original folder but in the upper overlay
which can be removed at any point.

Now, access your server via `http://nuc.home.lan:2342`, go to Settings
(password is set to "photoprism" by default) and initiate reindex process.

If you need to add more SELinux rules in case you haven't labelled files
correctly, here is how to do this. The trick is to disable dontaudit rules:

	  # semodule -BD

Then the required rule can be easily found and added to the policy:

    # sepolgen-ifgen
    # audit2allow -RaM photoprism
    # semodule -i photoprism.pp
    # semodule -B
	
Although podman comes with systemd unit generator command `podman generate
systemd`, it is required to configure headless systemd login sessions in order
to achieve management of the service via systemd. This is currently (CentOS
8.1) quite some work and I believe it is not worth the effort for sever-based
deployment.

That's all, the module is active from now on. This will persist restarts.
SELinux is easy if you know what to do. Granted those dontaudit rules can be
tricky as the denials won't appear until you temporarily diable this behavior.

I look forward to new developments of this software. I would love to see WebP
previews support to save some more space on the cache volume, Android and iOS
client apps are in development but they are not available yet on app stores (I
don't have iOS development account yet I would love to start testing it).
Browsing photos on my iPad is really exciting. I really hope the authors get
pricing model right and develop a sustainable offering for both DYI and regular
users.

