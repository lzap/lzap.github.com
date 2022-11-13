---
type: "post"
aliases:
- /2022/01/fast-backups-of-fedora-with-btrbk.html
date: "2022-01-25T00:00:00Z"
tags:
- linux
- fedora
title: Fast backups of Fedora with btrbk
---

Last year, I did full reinstall of my workstation in order to change from XFS
to BTRFS file system, which is now the default in Fedora Workstation. The plans
were simple - I wanted to achieve fast backups. And one year later, I finally
got to setting it up. Here is how to do it.

Scenario is simple, a host with BTRFS filesystem, a USB drive connected and
also formatted as BTRFS for ultra-fast snapshots/backups. To follow this
tutorial, you NEED to have BTRFS on the system itself and on the USB drive,
when not sure use this command to find out:

	# mount | grep btrfs
	/dev/sda5 on / type btrfs (rw,noatime,seclabel,ssd,space_cache,subvolid=256,subvol=/root)

You can still use the USB drive for other things (regular files), but I like to
have a dedicated USB HDD just for BTRFS backups - this filesystem does not
perform the best on traditional (spinning) drives. For small workloads it will
do just fine tho.  Let's go. Install btrbk utility which is a nice backup
script based on BTRFS tools:

	# dnf -y install btrbk

The tool was updated only recently (Fedora Rawhide / 36) so if you run into any
issue, try to upgrade it to the latest version from Rawhide (it is just a
single Perl script). Let's prepare the USB drive:

	# cfdisk /dev/sdX
	# mkfs.btrfs /dev/sdX1

	# grep backup /etc/fstab
	/dev/sdX1 /mnt/backup btrfs noatime,compress=zstd:3 0 0

	# mount -a

Compression is recommended, zstd with 3 ratio performs faster than most of USB
HDD drives, it will transparently compress blocks (which are compressable).
Let's create directories for BTRFS snapshots:

	# mkdir /btrbk /mnt/backup/{root,home}

Configure btrbk. This is an example of a very simple configuration: keep
snapshots on the source drive 2 days back, keep snapshots on the USB drive
(/mnt/backup) for 3 months, on both drives create snapshots in the /btrbk
directory and when USB drive is not mounted do not proceed (ondemand). Here is
it:

	# cat /etc/btrbk/btrbk.conf
	snapshot_preserve_min      2d
	target_preserve_min        3m
	archive_preserve_min       9m
	snapshot_create ondemand
	snapshot_dir btrbk
	volume /
	  subvolume .
	  target /mnt/backup/root
	volume /home
	  subvolume .
	  target /mnt/backup/home

Since I have root and home as two separate physical drives, your configuration
for default Fedora installation might be different:

	# cat /etc/btrbk/btrbk.conf
	snapshot_preserve_min      2d
	target_preserve_min        3m
	archive_preserve_min       9m
	snapshot_create ondemand
	snapshot_dir btrbk
	volume /
	  subvolume root
	  subvolume home
	  target /mnt/backup/root

I haven't tested this, let me know @lzap on Twitter if that works or not.
Anyways, now try it as dry-run (harmless):

	# btrbk dryrun

If there are no problems, run the first backup manually:

	# btrbk run

It will take a while as all the data needs to be trasnferred. Subsequent
backups will typically take few seconds if there were no significant changes on
the volume. Now, let's create a cron job that will daily mount the drive,
perform the backup, unmount it and puts the USB drive to sleep immediately:

	# cat /etc/cron.daily/backup.sh
	#!/bin/bash
	mount /mnt/backup || true
	btrbk -q run
	sync
	umount /mnt/backup
	sdparm -C stop -r /dev/sdX

All you need to do at this point is to set the executable flag and wait:

	# chmod +x /etc/cron.daily/backup.sh

Wait! :) You probably want to know how to restore from backups. Well, I have
some good news for you, you will use just the regular copy utility:

	# cp -a /mnt/backup/root/ROOT.20220125/etc/hosts /etc/hosts

For each day or backup, btrbk creates a new subdirectory so pick the date
correctly. Data is shared across the directories, having three months of copies
back does not mean the data is in 90 copies (unless you change them every day).
Also, everything is compressed too. And blazing fast! That is the beauty of
BTRFS backups.

Have fun backing up your Fedora!
