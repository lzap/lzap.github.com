---
type: "post"
aliases:
- /2013/11/how-to-backupmigrate-entire-partitions-easily.html
date: "2013-11-14T00:00:00Z"
tags:
- linux
- fedora
title: How to backup/migrate entire partitions easily
---

I needed something to migrate my NAS drive to a bigger one and I have stumbled
upon fsarchiver - awesome tool which is in Fedora and super easy to use.

I connected my drive with existing data to my USB cradle and installed this
masterpiece:

    sudo yum -y install fsarchiver

I saved partition(s) into one archive (`fsa` extension) with ultra-fast lzo
compression (`-z 1`):

    sudo fsarchiver savefs -z 1 migration.fsa /dev/sdc1 /dev/sdc2

I swapped the drive for a brand new one and after creation of exactly the same
partition layout (not using LVM in this case) I migrated the data back:

    sudo fsarchiver restfs migration.fsa id=0,dest=/dev/sdc1 id=1,dest=/dev/sdc2

There are other options (e.g. parallel compression, splitting into smaller
archives or excluding files), all is documented in the man page. Ideal tool
for fast migrations and for full off-line backups.
